from pathlib import Path
import os,sys,json,time,asyncio,datetime,resource,psutil
R=Path('/workspaces/repository');D=Path(__file__).parent
B=Path('/tmp/gpu-smt-kimina-header-repair-20261014')
SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
method=sys.argv[1];A=D/'preflight1'/method;A.mkdir(parents=True)
os.environ['PATH']=str(SDK/'bin')+os.pathsep+os.environ['PATH']
os.environ.update(LEAN_SERVER_LEAN_VERSION='v4.9.0-rc1',LEAN_SERVER_PROJECT_DIR=str(SDK.parent/'mathlib4'))
if method=='original':
 os.environ.pop('LEAN_SERVER_NATIVE_DYNLIB',None)
 os.environ['LEAN_SERVER_REPL_PATH']='/tmp/gpu-smt-kimina-gc49-20261015/.lake/build/bin/repl'
elif method=='compiled':
 os.environ['LEAN_SERVER_REPL_PATH']='/tmp/gpu-smt-kimina-gc49-20261015/.lake/build/bin/repl'
 native=Path('/tmp/gpu-smt-native-mathlib-20261014')
 os.environ['LEAN_SERVER_NATIVE_DYNLIB']=str(native/'.lake/build/lib/libMathlib-Tactic-Linarith-1.so')
 paths=[str(native/'.lake/build/lib')]+[str(p/'.lake/build/lib') for p in (native/'.lake/packages').iterdir() if p.is_dir()]
 os.environ['LD_LIBRARY_PATH']=os.pathsep.join(paths+([os.environ['LD_LIBRARY_PATH']] if os.environ.get('LD_LIBRARY_PATH') else []))
else:raise ValueError(method)
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
sys.path.insert(0,str(B))
from server.manager import Manager
from server.routers.check import run_checks
from server.settings import settings
from kimina_client.models import Snippet,VerifyRequestBody
def read(ds,index):
 if ds=='missing-import':return {'index':index,'header':'import GPU_SMT_Missing_Module\n','code':'import GPU_SMT_Missing_Module\nexample : True := by trivial'}
 p=R/'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs'/ds/'input.jsonl'
 with p.open() as f:
  for i,line in enumerate(f):
   if i==index:return json.loads(line)
 raise IndexError(index)
def classify(native,error):
 if error or not isinstance(native,dict):return 'operational'
 if any(m.get('severity')=='error' for m in native.get('messages') or []):return 'rejected'
 if native.get('sorries') or any(m.get('severity')=='warning' and 'sorry' in m.get('data','') for m in native.get('messages') or []):return 'incomplete'
 return 'complete'
def libraries():
 rows=[]
 for p in psutil.Process().children(recursive=True):
  try:
   paths=sorted({m.path for m in p.memory_maps(grouped=False) if 'gpu-smt-native-mathlib-20261014' in m.path})
   if paths:rows.append(dict(pid=p.pid,loaded_native_libraries=paths))
  except (psutil.NoSuchProcess,psutil.AccessDenied):pass
 return rows
async def main():
 manager=Manager();rows=[];started=time.monotonic_ns()
 observed={}
 async def observe_native_limits():
  while True:
   for child in psutil.Process().children(recursive=True):
    try:
     args=child.cmdline()
     if args and args[0]=='/tmp/gpu-smt-kimina-gc49-20261015/.lake/build/bin/repl' and child.pid not in observed:
      observed[child.pid]={'pid':child.pid,'address_space_limits_bytes':child.rlimit(resource.RLIMIT_AS),'rss_bytes_at_observation':child.memory_info().rss}
    except (psutil.NoSuchProcess,psutil.AccessDenied,ProcessLookupError):pass
   await asyncio.sleep(.05)
 observer=asyncio.create_task(observe_native_limits())
 cases=[('proofnet',0),('proofnet',257),('proofnet',2913),('minif2f',0),('missing-import',-1),('minif2f',663)]
 (A/'input.jsonl').write_text(''.join(json.dumps({'dataset':ds,**read(ds,i)},ensure_ascii=False)+'\n' for ds,i in cases))
 try:
  for ds,index in cases:
   item=read(ds,index);begin=time.monotonic_ns()
   try:
    res=(await run_checks([Snippet(id=ds+'-'+str(index),code=item['code'])],VerifyRequestBody(codes=[]).timeout,False,manager,True,None))[0]
    data=res.model_dump(mode='json');native=data.get('response');error=data.get('error')
   except Exception as e:
    data={'exception_type':type(e).__name__,'exception':str(e),'detail':getattr(e,'detail',None)};native=None;error=str(e)
   row=dict(dataset=ds,source_index=index,basic=classify(native,error),elapsed_seconds=(time.monotonic_ns()-begin)/1e9,stock_result=data,loaded_libraries=libraries())
   (A/f'{ds}-{index}.json').write_text(json.dumps(row,indent=2,ensure_ascii=False)+'\n')
   rows.append(row);print(json.dumps({k:v for k,v in row.items() if k not in ['stock_result','loaded_libraries']}),flush=True)
 finally:
  observer.cancel()
  try:await observer
  except asyncio.CancelledError:pass
  await manager.cleanup()
  closing=[t for t in asyncio.all_tasks() if t is not asyncio.current_task() and getattr(t.get_coro(),'__qualname__','')=='close_verbose']
  if closing:await asyncio.gather(*closing,return_exceptions=True)
 record=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method=method,returned=len(rows),elapsed_seconds=(time.monotonic_ns()-started)/1e9,effective_stock=dict(max_repls=settings.max_repls,max_repl_uses=settings.max_repl_uses,max_repl_mem_mib=settings.max_repl_mem,timeout=VerifyRequestBody(codes=[]).timeout),observed_native_limits=list(observed.values()),affinity=sorted(os.sched_getaffinity(0)),role='Real native stock run_checks dependency preflight, not performance; no HTTP/socket and no speed inference.')
 (A/'terminal.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record),flush=True)
if __name__=='__main__':asyncio.run(main())
