"""Finite GPU LP provider. Float hints only; CPU repair and Lean remain authority."""
import argparse,ctypes,json,os,queue,resource,signal,socketserver,threading,time
p=argparse.ArgumentParser(description=__doc__);p.add_argument("--library",required=True);p.add_argument("--port",type=int,default=5001);p.add_argument("--affinity",type=int,nargs="+",default=[8,9,10,11]);a=p.parse_args()
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.sched_setaffinity(0,set(a.affinity))
lib=ctypes.CDLL(a.library);P=ctypes.c_void_p;I=ctypes.c_int;D=ctypes.c_double
lib.simplex_error.restype=ctypes.c_char_p
for name in ["simplex_live_allocations","simplex_live_bytes","simplex_peak_bytes"]:
 f=getattr(lib,name);f.argtypes=[];f.restype=ctypes.c_size_t
lib.simplex_model.argtypes=[I,I,ctypes.POINTER(I),ctypes.POINTER(I),ctypes.POINTER(D),ctypes.POINTER(D)];lib.simplex_model.restype=P
lib.simplex_launch.argtypes=[ctypes.POINTER(P),I];lib.simplex_launch.restype=P
for name in ["simplex_state","simplex_iterations","simplex_done"]:
 f=getattr(lib,name);f.argtypes=[P];f.restype=I
lib.simplex_ticks.argtypes=[P];lib.simplex_ticks.restype=ctypes.POINTER(ctypes.c_uint64)
lib.simplex_values.argtypes=[P];lib.simplex_values.restype=ctypes.POINTER(D)
lib.simplex_dual_values.argtypes=[P];lib.simplex_dual_values.restype=ctypes.POINTER(D)
for name in ["simplex_cancel","simplex_model_free","simplex_batch_free"]:
 f=getattr(lib,name);f.argtypes=[P];f.restype=None
lock=threading.Lock();log_lock=threading.Lock();pending=queue.Queue();states={};early_cancel=set();stopping=threading.Event()
def log(x):
 with log_lock:print(json.dumps(x,separators=(",",":")),flush=True)
class Handler(socketserver.StreamRequestHandler):
 def handle(self):
  try:
   q=json.loads(self.rfile.readline())
   if q.get("ping"):
    self.send({"ready":True,"pid":os.getpid(),"affinity":sorted(os.sched_getaffinity(0)),"RLIMIT_AS":resource.getrlimit(resource.RLIMIT_AS),"engine":"CUDA batched phase-I simplex","live_allocations":lib.simplex_live_allocations(),"live_device_bytes":lib.simplex_live_bytes(),"peak_device_bytes":lib.simplex_peak_bytes()});return
   if "cancel"in q:
    with lock:
     for key in q["cancel"]:
      s=states.get(key)
      if s:
       s["cancelled"]=True
       if s["handle"]:lib.simplex_cancel(s["handle"])
      else:early_cancel.add(key)
    self.send({"cancelled":q["cancel"]});return
   items=q["requests"];answers=queue.Queue()
   with lock:
    for request in items:
     key=request["key"]
     if key in states:raise ValueError("duplicate live request key")
     s={"q":request,"handle":None,"cancelled":key in early_cancel,"answers":answers,"sent":False}
     early_cancel.discard(key);states[key]=s
    for request in items:pending.put(states[request["key"]])
   left=len(items);retired=set()
   # Each numeric result is streamed before siblings finish. Every actual
   # launch retirement is also streamed,so proxy shutdown owes no live kernel.
   while left or len(retired)<len(items):
    answer=answers.get();self.send(answer)
    if answer.get("event")=="retired":retired.update(answer["keys"])
    else:left-=1
  except (BrokenPipeError,ConnectionResetError):pass
  except Exception as e:
   try:self.send({"error":type(e).__name__+": "+str(e)})
   except OSError:pass
 def send(self,x):self.wfile.write((json.dumps(x,separators=(",",":"))+"\n").encode());self.wfile.flush()
class Server(socketserver.ThreadingTCPServer):
 allow_reuse_address=True;daemon_threads=False
server=Server(("0.0.0.0",a.port),Handler)
thread=threading.Thread(target=server.serve_forever,daemon=False);thread.start()
def stop(signum,frame):stopping.set()
signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
log({"event":"ready","affinity":sorted(os.sched_getaffinity(0)),"RLIMIT_AS":resource.getrlimit(resource.RLIMIT_AS)})
def finish(s,result):
 if not s["sent"]:
  s["sent"]=True;s["answers"].put(dict(result,key=s["q"]["key"]))
def retire(items,batch):
 if batch:lib.simplex_batch_free(batch)
 destinations={}
 to_free=[]
 with lock:
  for s in items:
   if s["handle"]:to_free.append(s["handle"]);s["handle"]=None
   states.pop(s["q"]["key"],None)
   key=id(s["answers"]);destinations.setdefault(key,(s["answers"],[]))[1].append(s["q"]["key"])
 for handle in to_free:lib.simplex_model_free(handle)
 for out,keys in destinations.values():out.put({"event":"retired","keys":keys,"monotonic_ns":time.monotonic_ns()})
group_threads=[]
def own_group(items):
 handles=[];live=[];batch=None;begin=time.monotonic_ns()
 try:
  for s in items:
   q=s["q"];start=time.monotonic_ns()
   if s["cancelled"]or stopping.is_set():finish(s,{"primal":None,"state":"cancelled_before_build"});continue
   m=len(q["rhs"]);n=q["ncols"]
   offsets=(I*len(q["offsets"]))(*q["offsets"]);indices=(I*len(q["indices"]))(*q["indices"])
   values=(D*len(q["values"]))(*q["values"]);rhs=(D*m)(*q["rhs"])
   h=lib.simplex_model(m,n,offsets,indices,values,rhs)
   if not h:finish(s,{"primal":None,"state":"build_failed","error":lib.simplex_error().decode()});continue
   with lock:
    s["handle"]=h
    if s["cancelled"]or stopping.is_set():lib.simplex_cancel(h)
   s["build_ns"]=time.monotonic_ns()-start;handles.append(h);live.append(s)
  batch=lib.simplex_launch((P*len(handles))(*handles),len(handles))if handles else None
  if handles and not batch:
   for s in live:finish(s,{"primal":None,"state":"launch_failed","error":lib.simplex_error().decode()})
  log({"event":"launch","batch_id":begin,"batch_size":len(handles),"keys":[s["q"]["key"]for s in live],"call_ids":[s["q"].get("call_id")for s in live],"distinct_sources":len(set(s["q"].get("source")for s in live)),"model_build_ns":sum(s["build_ns"]for s in live)})
  if batch:
   kernel_complete_seen=False
   while True:
    if stopping.is_set():
     for s in live:lib.simplex_cancel(s["handle"])
    for s in live:
     if s["sent"]:continue
     state=lib.simplex_state(s["handle"])
     if state:
      values=lib.simplex_values(s["handle"])if state==1 else None;q=s["q"]
      reply={"primal":[values[i]for i in range(q["ncols"])]if state==1 and values else None,
       "state":{1:"phase_I_feasible",2:"phase_I_no_hint",3:"cancelled",4:"numerical_no_hint"}.get(state,str(state)),
       "iterations":lib.simplex_iterations(s["handle"]),"engine":"CUDA batched phase-I simplex",
       "batch_id":begin,"batch_size":len(handles),"build_ns":s["build_ns"],"monotonic_ns":time.monotonic_ns()}
      if state==2 and q.get("want_dual"):
       dual=lib.simplex_dual_values(s["handle"]);reply["dual_ray"]=[dual[i]for i in range(len(q["rhs"]))]if dual else None
      ticks=lib.simplex_ticks(s["handle"])
      if ticks:reply["device_globaltimer_interval"]=[ticks[0],ticks[1]]
      finish(s,reply);log(dict(reply,key=q["key"],primal=None))
    done=lib.simplex_done(batch)
    if done:
     if done<0:
      for s in live:finish(s,{"primal":None,"state":"kernel_failed","error":lib.simplex_error().decode()})
     if done>0 and not kernel_complete_seen:
      kernel_complete_seen=True
      continue  # One final model scan after completion became observable.
     break
    time.sleep(.0005)
  for s in items:
   if not s["sent"]:finish(s,{"primal":None,"state":"no_hint"})
  retire(items,batch);log({"event":"batch_retired","batch_id":begin,"monotonic_ns":time.monotonic_ns()})
 except Exception as e:
  for s in items:finish(s,{"primal":None,"state":"provider_error","error":repr(e)})
  for s in live:lib.simplex_cancel(s["handle"])
  retire(items,batch)
try:
 while not stopping.is_set()or not pending.empty():
  try:first=pending.get(timeout=.01)
  except queue.Empty:continue
  items=[first]
  while True:
   try:items.append(pending.get_nowait())
   except queue.Empty:break
  worker=threading.Thread(target=own_group,args=(items,),daemon=False)
  group_threads.append(worker);worker.start()
 for worker in group_threads:worker.join()
 log({"event":"provider_retired","live_models":len(states),"live_allocations":lib.simplex_live_allocations(),"live_device_bytes":lib.simplex_live_bytes(),"peak_device_bytes":lib.simplex_peak_bytes()})
finally:server.shutdown();server.server_close();thread.join()
