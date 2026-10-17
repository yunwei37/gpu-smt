"""Finite-run CPU/GPU support backend. Numeric hints only; Rust/Lean verify."""
import argparse,collections,http.client,json,os,resource,socketserver,threading,time,sys,math,queue,signal
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--backend',choices=['highs','cuopt'],required=True);p.add_argument('--socket',required=True);p.add_argument('--log',required=True);p.add_argument('--host');p.add_argument('--proto-root');a=p.parse_args()
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
if a.backend=='cuopt':
 sys.path.insert(0,a.proto_root)
 import grpc,cuopt_remote_data_pb2 as data_pb,cuopt_remote_pb2 as core_pb,cuopt_remote_service_pb2 as service_pb,cuopt_remote_service_pb2_grpc as rpc
lock=threading.Lock();active=0;seq=0
if a.backend=='highs':
 import numpy as np,highspy
def request_json(conn,method,path,data=None):
 body=None if data is None else json.dumps(data,separators=(',',':'))
 conn.request(method,path,body=body,headers={'Content-Type':'application/json','Accept':'application/json','CLIENT-VERSION':'custom'})
 res=conn.getresponse();raw=res.read()
 if res.status>=400:raise RuntimeError(str(res.status)+': '+raw.decode(errors='replace'))
 return json.loads(raw)
def solve(q):
 n=q['ncols'];r=len(q['rhs'])
 if a.backend=='highs':
  t=time.monotonic_ns();lp=highspy.HighsLp();lp.num_col_=n;lp.num_row_=r
  lp.col_cost_=np.zeros(n);lp.col_lower_=np.zeros(n);lp.col_upper_=np.full(n,highspy.kHighsInf)
  lp.row_lower_=np.array(q['rhs']);lp.row_upper_=np.array(q['rhs'])
  lp.a_matrix_.format_=highspy.MatrixFormat.kRowwise;lp.a_matrix_.start_=np.array(q['offsets'],dtype=np.int32);lp.a_matrix_.index_=np.array(q['indices'],dtype=np.int32);lp.a_matrix_.value_=np.array(q['values'])
  h=highspy.Highs();h.setOptionValue('output_flag',False);h.passModel(lp);packed=time.monotonic_ns();h.run();done=time.monotonic_ns()
  state=h.modelStatusToString(h.getModelStatus());point=h.getSolution().col_value if h.getModelStatus()==highspy.HighsModelStatus.kOptimal else None
  return {'primal':point,'state':state,'engine':'HiGHS','solver_seconds':h.getRunTime(),'build_ns':packed-t,'call_ns':done-packed}
 event=threading.Event();result={};gpu_queue.put((q,event,result));event.wait();return result
def solve_gpu_batch(items):
 # Every component is always feasible: A*mu + s_plus - s_minus = b.
 # Minimize sum(s_plus+s_minus); only mu is exposed as an untrusted hint.
 values=[];indices=[];offsets=[0];rhs=[];objective=[];slices=[];base=0
 for q,event,result in items:
  n=q['ncols'];r=len(q['rhs']);slices.append((base,n))
  for row in range(r):
   for k in range(q['offsets'][row],q['offsets'][row+1]):
    indices.append(base+q['indices'][k]);values.append(q['values'][k])
   indices.extend([base+n+2*row,base+n+2*row+1]);values.extend([1.,-1.]);offsets.append(len(values))
  rhs.extend(q['rhs']);objective.extend([0.]*n+[1.]*(2*r));base+=n+2*r
 conn=grpc.insecure_channel(a.host+':5001');stub=rpc.CuOptRemoteServiceStub(conn);job=None;begin=time.monotonic_ns()
 try:
  model=data_pb.OptimizationProblem(A_values=values,A_indices=indices,A_offsets=offsets,c=objective,b=rhs,variable_lower_bounds=[0.]*base,variable_upper_bounds=[float('inf')]*base,constraint_lower_bounds=rhs,constraint_upper_bounds=rhs,row_types=b'E'*len(rhs),objective_scaling_factor=1.)
  settings=data_pb.PDLPSolverSettings(method=data_pb.PDLP,crossover=True)
  request=core_pb.SolveLPRequest(header=core_pb.RequestHeader(version=1,problem_category=data_pb.LP),problem=model,settings=settings)
  job=stub.SubmitJob(service_pb.SubmitJobRequest(lp_request=request)).job_id
  with lock:pending_gpu.add(job)
  status=stub.WaitForCompletion(service_pb.WaitRequest(job_id=job))
  response=stub.GetResult(service_pb.GetResultRequest(job_id=job));sol=response.lp_solution;point=list(sol.primal_solution)
  valid=sol.lp_termination_status==data_pb.PDLP_OPTIMAL and len(point)==base and all(math.isfinite(x)for x in point)
  common={'state':data_pb.PDLPTerminationStatus.Name(sol.lp_termination_status),'engine':sol.solved_by,'iterations':sol.nb_iterations,'message':response.error_message or sol.error_message,'rpc_status':response.status,'batch_ids':[x[0]['request_id']for x in items],'batch_size':len(items),'batch_rows':len(rhs),'batch_columns':base,'batch_nnz':len(values),'batch_solver_seconds_shared':sol.solve_time,'batch_start_ns':begin,'batch_end_ns':time.monotonic_ns(),'phase1_objective':sol.primal_objective}
  return [dict(common,primal=point[start:start+n]if valid else None)for start,n in slices]
 finally:
  if job:
   with lock:pending_gpu.discard(job)
   try:stub.DeleteResult(service_pb.DeleteRequest(job_id=job))
   except Exception:pass
  conn.close()
def gpu_dispatch():
 while True:
  items=[gpu_queue.get()]
  while True:
   try:items.append(gpu_queue.get_nowait())
   except queue.Empty:break
  try:answers=solve_gpu_batch(items)
  except Exception as e:answers=[{'primal':None,'error':type(e).__name__+': '+str(e)}for x in items]
  for (_,event,result),answer in zip(items,answers):result.update(answer);event.set()
if a.backend=='cuopt':
 gpu_queue=queue.Queue();pending_gpu=set()
 threading.Thread(target=gpu_dispatch,daemon=True).start()
def stop_proxy(signum,frame):
 if a.backend=='cuopt':
  conn=grpc.insecure_channel(a.host+':5001');stub=rpc.CuOptRemoteServiceStub(conn)
  with lock:jobs=list(pending_gpu)
  for job in jobs:
   try:stub.CancelJob(service_pb.CancelRequest(job_id=job))
   except Exception:pass
  conn.close()
 raise SystemExit(128+signum)
signal.signal(signal.SIGTERM,stop_proxy)

class Handler(socketserver.StreamRequestHandler):
 def handle(self):
  global active,seq
  start=time.monotonic_ns();cpu=time.thread_time_ns()
  with lock:active+=1;seq+=1;idx=seq;concurrent=active
  q=None
  try:
   q=json.loads(self.rfile.readline());q['request_id']=idx;reply=solve(q)
  except Exception as e:reply={'primal':None,'error':type(e).__name__+': '+str(e)}
  finish=time.monotonic_ns()
  rec={'id':idx,'backend':a.backend,'start_ns':start,'end_ns':finish,'thread_cpu_ns':time.thread_time_ns()-cpu,'active_at_arrival':concurrent,'rows':len(q['rhs'])if q else None,'cols':q['ncols']if q else None,'nnz':len(q['values'])if q else None,'reply':reply}
  with lock:
   active-=1
   with open(a.log,'a')as f:f.write(json.dumps(rec,separators=(',',':'))+'\n')
  self.wfile.write((json.dumps(reply,separators=(',',':'))+'\n').encode());self.wfile.flush()
class Server(socketserver.ThreadingUnixStreamServer):
 daemon_threads=False
if os.path.exists(a.socket):raise RuntimeError('socket already exists: '+a.socket)
with Server(a.socket,Handler)as server:
 print(json.dumps({'ready':True,'pid':os.getpid(),'backend':a.backend,'socket':a.socket,'RLIMIT_AS':resource.getrlimit(resource.RLIMIT_AS)}),flush=True)
 try:server.serve_forever()
 finally:os.unlink(a.socket)
