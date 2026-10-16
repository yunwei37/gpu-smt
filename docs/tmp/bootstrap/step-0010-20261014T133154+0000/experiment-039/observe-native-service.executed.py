"""Finite E039 observation of the existing Kimina app; no verifier implementation."""
from pathlib import Path
import asyncio,datetime,gzip,json,logging,os,resource,socket,sys,time
import psutil,signal
O=Path(sys.argv[1]);O.mkdir(exist_ok=True)
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
sys.path.insert(0,str(K))
from server.repl import Repl
from server.manager import Manager
from server.settings import settings
events=gzip.open(O/'native-phase-events.jsonl.gz','wt',compresslevel=1)
workers={};outputs={};errors={};stderr_tasks={}
def emit(kind,**data):
 events.write(json.dumps({'event':kind,'ns':time.monotonic_ns(),**data},ensure_ascii=False)+'\n');events.flush()
def cpu(repl):
 if repl.proc is None:return {'processes':[],'errors':[]}
 values=[];failed=[]
 try:root=psutil.Process(repl.proc.pid);procs=[root]+root.children(recursive=True)
 except psutil.Error as e:return {'processes':[],'errors':[repr(e)]}
 for p in procs:
  try:
   v=p.cpu_times();values.append({'pid':p.pid,'created':p.create_time(),'user':v.user,'system':v.system,'threads':p.num_threads()})
  except psutil.Error as e:failed.append(repr(e))
 return {'processes':values,'errors':failed}
original_start=Repl.start
original_send=Repl.send_timeout
original_prep=Manager.prep
original_cleanup=Manager.cleanup
original_close=Repl.close
async def start(self):
 t=time.monotonic_ns()
 try:await original_start(self)
 except BaseException as e:
  emit('start_error',uuid=self.uuid.hex,elapsed_ns=time.monotonic_ns()-t,error=repr(e));raise
 key=self.uuid.hex;workers[key]=self
 reader=self.proc.stdout
 stream=gzip.open(O/('native-'+key+'.stdout.gz'),'wb',compresslevel=1);outputs[key]=stream
 if reader._buffer:stream.write(bytes(reader._buffer));stream.flush()
 feed=reader.feed_data
 def tee(data):stream.write(data);stream.flush();feed(data)
 reader.feed_data=tee
 async def stderr():
  with gzip.open(O/('native-'+key+'.stderr.gz'),'wb',compresslevel=1) as dst:
   while chunk:=await self.proc.stderr.read(65536):dst.write(chunk)
 stderr_tasks[key]=asyncio.create_task(stderr())
 emit('native_started',uuid=key,pid=self.proc.pid,elapsed_ns=time.monotonic_ns()-t,cpu=cpu(self))
async def send(self,snippet,timeout,is_header=False,infotree=None):
 t=time.monotonic_ns();before=cpu(self);error=None;response=None
 try:
  response=await original_send(self,snippet,timeout,is_header,infotree);return response
 except BaseException as e:error=repr(e);raise
 finally:
  emit('native_send_terminal',uuid=self.uuid.hex,pid=self.proc.pid if self.proc else None,
       snippet_id=snippet.id,is_header=is_header,started_ns=t,elapsed_ns=time.monotonic_ns()-t,
       cpu_before=before,cpu_after=cpu(self),error=error,
       adapter_time=None if response is None else response.time)
async def prep(self,repl,snippet_id,timeout,debug):
 t=time.monotonic_ns();was_started=repl.is_running;before=cpu(repl);error=None;response=None
 try:
  response=await original_prep(self,repl,snippet_id,timeout,debug);return response
 except BaseException as e:error=repr(e);raise
 finally:
  emit('preparation_terminal',uuid=repl.uuid.hex,pid=repl.proc.pid if repl.proc else None,
       snippet_id=snippet_id,header=repl.header,reused_started=was_started,
       started_ns=t,elapsed_ns=time.monotonic_ns()-t,cpu_before=before,cpu_after=cpu(repl),
       error=error,header_response=None if response is None else response.model_dump(exclude_none=True))
async def close(self):
 t=time.monotonic_ns();before=cpu(self);error=None
 try:return await original_close(self)
 except BaseException as e:error=repr(e);raise
 finally:
  emit('native_close_terminal',uuid=self.uuid.hex,pid=self.proc.pid if self.proc else None,
       started_ns=t,elapsed_ns=time.monotonic_ns()-t,cpu_before=before,error=error,
       exit_code=self.proc.returncode if self.proc else None)
async def cleanup(self):
 t=time.monotonic_ns()
 await original_cleanup(self)
 closing=[t for t in asyncio.all_tasks() if t is not asyncio.current_task() and getattr(t.get_coro(),'__qualname__','')=='close_verbose']
 results=await asyncio.gather(*closing,return_exceptions=True) if closing else []
 emit('stock_close_tasks',errors=[repr(x) for x in results if isinstance(x,BaseException)])
 # Wait for closes already scheduled by stock cleanup/destroy, never substitute
 # a returned response for completion or install a different kill policy.
 await asyncio.gather(*(r.proc.wait() for r in workers.values() if r.proc is not None))
 await asyncio.gather(*stderr_tasks.values(),return_exceptions=True)
 emit('manager_cleanup_terminal',elapsed_ns=time.monotonic_ns()-t,
      workers=[{'uuid':k,'pid':r.proc.pid,'exit_code':r.proc.returncode} for k,r in workers.items()])
Repl.start=start;Repl.send_timeout=send;Repl.close=close;Manager.prep=prep;Manager.cleanup=cleanup
from server.main import app
from server.__main__ import InterceptHandler
import uvicorn
logging.basicConfig(handlers=[InterceptHandler()],level=0,force=True)
for name in ('uvicorn','uvicorn.error','uvicorn.access'):
 logging.getLogger(name).handlers=[];logging.getLogger(name).propagate=True
async def main():
 sock=socket.socket();sock.bind(('127.0.0.1',0));sock.listen(4096)
 host,port=sock.getsockname()
 (O/'server-ready.json').write_text(json.dumps({'pid':os.getpid(),'host':host,'port':port})+'\n')
 emit('observer_start',pid=os.getpid(),affinity=sorted(os.sched_getaffinity(0)),
      policy={'max_repls':settings.max_repls,'max_repl_uses':settings.max_repl_uses,
              'max_repl_mem_MiB':settings.max_repl_mem,'max_wait':settings.max_wait,
              'native_thread_env':{k:os.environ.get(k) for k in ['LEAN_NUM_THREADS','OMP_NUM_THREADS','CORE']}},
      project=str(settings.project_dir),repl=str(settings.repl_path),lean_version=settings.lean_version)
 server=uvicorn.Server(uvicorn.Config(app,host=host,port=port,backlog=4096,
                      use_colors=settings.environment.value!='prod',log_config=None))
 # Uvicorn retains its ordinary first-signal graceful shutdown. Its final
 # re-raise reaches this outer observer handler, allowing raw gzip/CPU flush.
 for sig in (signal.SIGINT,signal.SIGTERM):signal.signal(sig,lambda signum,frame:None)
 await server.serve(sockets=[sock])
try:asyncio.run(main())
finally:
 ru=resource.getrusage(resource.RUSAGE_CHILDREN);own=resource.getrusage(resource.RUSAGE_SELF)
 emit('observer_terminal',reported_waited_child_cpu={'user':ru.ru_utime,'system':ru.ru_stime},
      cpu_coverage_note='StockgroupSIGKILL may prevent lake from reaping native descendants; use retained process identity snapshots for observed nativeCPU, never treat this rusage as exhaustive nativeCPU.',
      observer_cpu={'user':own.ru_utime,'system':own.ru_stime},
      workers=[{'uuid':k,'pid':r.proc.pid,'exit_code':r.proc.returncode} for k,r in workers.items()])
 for stream in outputs.values():stream.close()
 events.close()
