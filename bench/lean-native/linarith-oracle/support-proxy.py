"""Finite-run numeric support backend; every hint still passes exact repair/Lean."""
import argparse,json,os,resource,socket,socketserver,threading,time,sys,math,queue,signal,select
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--min-batch',type=int,default=1,help='Ready requests required before GPU launch; racing CPU owners can cancel while a partial batch waits.');p.add_argument('--backend',choices=['highs','cuopt'],required=True)
p.add_argument('--socket',required=True);p.add_argument('--log',required=True)
p.add_argument('--host');p.add_argument('--proto-root');a=p.parse_args()
if a.min_batch<1:p.error('--min-batch must be positive')
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
if a.backend=='cuopt':
 sys.path.insert(0,a.proto_root)
 import grpc,cuopt_remote_data_pb2 as data_pb,cuopt_remote_pb2 as core_pb,cuopt_remote_service_pb2 as service_pb,cuopt_remote_service_pb2_grpc as rpc
else:
 import numpy as np,highspy
lock=threading.Lock();active=0;seq=0
def append_record(path,record):
 with lock:
  with open(path,'a')as f:f.write(json.dumps(record,separators=(',',':'))+'\n')
class GPUCall:
 def __init__(self,q):
  self.q=q;self.result={};self.cancelled=threading.Event()
  self.fd=os.eventfd(0,os.EFD_CLOEXEC|os.EFD_NONBLOCK)
 def deliver(self,answer):
  with lock:
   self.result.update(answer)
   if self.fd is not None:os.eventfd_write(self.fd,1)
 def close(self):
  with lock:
   if self.fd is not None:os.close(self.fd);self.fd=None
def cancel_abandoned():
 # Cancel a joint solve only when no original client still owns its result.
 with lock:jobs=[j for j,items in pending_gpu.items()if all(x.cancelled.is_set()for x in items)]
 for job in jobs:
  channel=grpc.insecure_channel(a.host+':5001')
  try:
   reply=rpc.CuOptRemoteServiceStub(channel).CancelJob(service_pb.CancelRequest(job_id=job))
   append_record(a.log+'.batches',{'event':'cancel_no_live_clients','job_id':job,'monotonic_ns':time.monotonic_ns(),'reply':str(reply)})
  except Exception as e:append_record(a.log+'.batches',{'event':'cancel_error','job_id':job,'error':str(e)})
  finally:channel.close()
def solve_highs(q):
 n=q['ncols'];r=len(q['rhs']);t=time.monotonic_ns()
 lp=highspy.HighsLp();lp.num_col_=n;lp.num_row_=r
 lp.col_cost_=np.zeros(n);lp.col_lower_=np.zeros(n);lp.col_upper_=np.full(n,highspy.kHighsInf)
 lp.row_lower_=np.array(q['rhs']);lp.row_upper_=np.array(q['rhs'])
 lp.a_matrix_.format_=highspy.MatrixFormat.kRowwise
 lp.a_matrix_.start_=np.array(q['offsets'],dtype=np.int32)
 lp.a_matrix_.index_=np.array(q['indices'],dtype=np.int32);lp.a_matrix_.value_=np.array(q['values'])
 h=highspy.Highs();h.setOptionValue('output_flag',False);h.passModel(lp)
 packed=time.monotonic_ns();h.run();done=time.monotonic_ns()
 state=h.modelStatusToString(h.getModelStatus())
 point=h.getSolution().col_value if h.getModelStatus()==highspy.HighsModelStatus.kOptimal else None
 return {'primal':point,'state':state,'engine':'HiGHS','solver_seconds':h.getRunTime(),'build_ns':packed-t,'call_ns':done-packed}
def solve_gpu_batch(items):
 # Phase I keeps no-certificate systems feasible. Keep the measured PDLP+
 # crossover mechanism, with corrected client lifetime and header composition.
 values=[];indices=[];offsets=[0];rhs=[];slices=[];objective=[];base=0
 for item in items:
  q=item.q;n=q['ncols'];r=len(q['rhs']);slices.append((base,n))
  for row in range(r):
   for k in range(q['offsets'][row],q['offsets'][row+1]):
    indices.append(base+q['indices'][k]);values.append(q['values'][k])
   indices.extend([base+n+2*row,base+n+2*row+1]);values.extend([1.,-1.])
   offsets.append(len(values))
  rhs.extend(q['rhs']);objective.extend([0.]*n+[1.]*(2*r));base+=n+2*r
 channel=grpc.insecure_channel(a.host+':5001');stub=rpc.CuOptRemoteServiceStub(channel)
 job=None;begin=time.monotonic_ns()
 try:
  model=data_pb.OptimizationProblem(A_values=values,A_indices=indices,A_offsets=offsets,c=objective,b=rhs,variable_lower_bounds=[0.]*base,variable_upper_bounds=[float('inf')]*base,constraint_lower_bounds=rhs,constraint_upper_bounds=rhs,row_types=b'E'*len(rhs),objective_scaling_factor=1.)
  settings=data_pb.PDLPSolverSettings(method=data_pb.PDLP,crossover=True)
  request=core_pb.SolveLPRequest(header=core_pb.RequestHeader(version=1,problem_category=data_pb.LP),problem=model,settings=settings)
  job=stub.SubmitJob(service_pb.SubmitJobRequest(lp_request=request)).job_id
  with lock:pending_gpu[job]=items
  append_record(a.log+'.batches',{'event':'submit','job_id':job,'start_ns':begin,'batch_ids':[x.q['request_id']for x in items],'rows':len(rhs),'cols':base,'nnz':len(values),'formulation':'phase_I_artificial_slack','settings':{'method':'PDLP','crossover':True,'first_primal_feasible':False}})
  cancel_abandoned()
  status=stub.WaitForCompletion(service_pb.WaitRequest(job_id=job))
  response=stub.GetResult(service_pb.GetResultRequest(job_id=job));sol=response.lp_solution
  point=list(sol.primal_solution)
  # Termination status is not proof authority. Any finite hint must still pass
  # unchanged exact repair/verification and Lean checking, otherwise fallback.
  usable=len(point)==base and all(math.isfinite(x)for x in point)
  common={'job_id':job,'state':data_pb.PDLPTerminationStatus.Name(sol.lp_termination_status),'engine':sol.solved_by,'generic_iterations':sol.nb_iterations,'message':response.error_message or sol.error_message,'rpc_status':response.status,'batch_ids':[x.q['request_id']for x in items],'batch_size':len(items),'batch_rows':len(rhs),'batch_columns':base,'batch_nnz':len(values),'batch_solver_seconds_shared':sol.solve_time,'batch_start_ns':begin,'batch_end_ns':time.monotonic_ns(),'phase1_objective':sol.primal_objective}
  append_record(a.log+'.batches',dict(common,event='result'))
  return [dict(common,primal=point[start:start+n]if usable else None)for start,n in slices]
 finally:
  if job:
   with lock:pending_gpu.pop(job,None)
   try:stub.DeleteResult(service_pb.DeleteRequest(job_id=job))
   except Exception:pass
  channel.close()
def gpu_dispatch():
 items=[]
 while not stopping.is_set():
  item=gpu_queue.get()  # Arrival or cancellation wakeup; no polling/timer.
  if stopping.is_set():break
  if item is not None:items.append(item)
  while True:
   try:
    item=gpu_queue.get_nowait()
    if item is not None:items.append(item)
   except queue.Empty:break
  items=[x for x in items if not x.cancelled.is_set()]
  if len(items)<a.min_batch:continue
  ready=time.monotonic_ns()
  append_record(a.log+'.batches',{'event':'batch_ready','monotonic_ns':ready,
    'batch_size':len(items),'minimum_ready':a.min_batch,
    'scope':'Only simultaneously live device-ready requests; CPU shadows remain active.'})
  try:answers=solve_gpu_batch(items)
  except Exception as e:answers=[{'primal':None,'error':type(e).__name__+': '+str(e)}for _ in items]
  for item,answer in zip(items,answers):item.deliver(answer)
  items=[]
if a.backend=='cuopt':
 gpu_queue=queue.Queue();pending_gpu={};stopping=threading.Event()
 dispatcher=threading.Thread(target=gpu_dispatch,daemon=False);dispatcher.start()
def stop_proxy(signum,frame):
 if a.backend=='cuopt':
  with lock:
   for items in pending_gpu.values():
    for item in items:item.cancelled.set()
  stopping.set();gpu_queue.put(None);cancel_abandoned()
  dispatcher.join() # WaitForCompletion + DeleteResult return before cell retirement.
  append_record(a.log+'.batches',{'event':'dispatcher_retired','monotonic_ns':time.monotonic_ns(),'pending_jobs':len(pending_gpu)})
 raise SystemExit(128+signum)
signal.signal(signal.SIGTERM,stop_proxy)
class Handler(socketserver.StreamRequestHandler):
 def handle(self):
  global active,seq
  start=time.monotonic_ns();cpu=time.thread_time_ns();item=None;q=None;gone=False
  with lock:active+=1;seq+=1;idx=seq;concurrent=active
  try:
   q=json.loads(self.rfile.readline());q['request_id']=idx
   if a.backend=='highs':reply=solve_highs(q)
   else:
    item=GPUCall(q);gpu_queue.put(item)
    while True:
     ready,_,_=select.select([item.fd,self.connection],[],[])
     if item.fd in ready:
      os.eventfd_read(item.fd);reply=item.result;break
     if self.connection in ready:
      # One request/response per native child. EOF means its candidate expired.
      gone=True;item.cancelled.set();gpu_queue.put(None);cancel_abandoned()
      reply={'primal':None,'state':'client_disconnected'};break
  except Exception as e:reply={'primal':None,'error':type(e).__name__+': '+str(e)}
  finally:
   if item:item.close()
  finish=time.monotonic_ns()
  record={'id':idx,'backend':a.backend,'start_ns':start,'end_ns':finish,'thread_cpu_ns':time.thread_time_ns()-cpu,'active_at_arrival':concurrent,'rows':len(q['rhs'])if q else None,'cols':q['ncols']if q else None,'nnz':len(q['values'])if q else None,'input':q,'reply':reply}
  with lock:active-=1
  append_record(a.log,record)
  if not gone:
   try:self.wfile.write((json.dumps(reply,separators=(',',':'))+'\n').encode());self.wfile.flush()
   except (BrokenPipeError,ConnectionResetError):pass
class Server(socketserver.ThreadingUnixStreamServer):
 daemon_threads=False
if os.path.exists(a.socket):raise RuntimeError('socket already exists: '+a.socket)
with Server(a.socket,Handler)as server:
 print(json.dumps({'ready':True,'pid':os.getpid(),'backend':a.backend,'socket':a.socket,'RLIMIT_AS':resource.getrlimit(resource.RLIMIT_AS)}),flush=True)
 try:server.serve_forever()
 finally:os.unlink(a.socket)
