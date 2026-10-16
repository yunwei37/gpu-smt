"""Actual one-off native first-write-copy actual batch engagement; no performance comparison."""
from pathlib import Path
import asyncio,contextlib,datetime,gzip,json,os,resource,sys,time
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
sys.path.insert(0,str(K))
from server.repl import Repl,Snippet
from server.settings import settings
R=Path('/workspaces/repository')
B=Path('/tmp/gpu-smt-goedel427-20261014');SDK=B/'lean-4.27.0-linux'
ROOT=Path(sys.argv[1]);OUT=Path(sys.argv[2]);METHODS=sys.argv[3].split(',')
OUT.mkdir(exist_ok=False)
INPUT=R/'artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl'
ITEMS=[{'proof_id': 'read-before', 'index': 0, 'code': 'import Mathlib\nimport Aesop\ninitialize branchProbe : IO.Ref Nat ← IO.mkRef 0\nrun_cmd do\n  let value ← liftIO branchProbe.get\n  unless value == 0 do throwError "base ref changed"'}, {'proof_id': 'write-private', 'index': 1, 'code': 'import Mathlib\nimport Aesop\ninitialize branchProbe : IO.Ref Nat ← IO.mkRef 0\nrun_cmd do\n  liftIO (branchProbe.set 7)\n  let value ← liftIO branchProbe.get\n  unless value == 7 do throwError "private write missing"'}, {'proof_id': 'read-other', 'index': 2, 'code': 'import Mathlib\nimport Aesop\ninitialize branchProbe : IO.Ref Nat ← IO.mkRef 0\nrun_cmd do\n  let value ← liftIO branchProbe.get\n  unless value == 0 do throwError "base ref changed"'}]
HEADER='import Mathlib\nimport Aesop\ninitialize branchProbe : IO.Ref Nat ← IO.mkRef 0\n'
CONFIG=json.loads((INPUT.parent/'native-library.json').read_text())
INHERITED_AS=resource.getrlimit(resource.RLIMIT_AS)
os.environ['PATH']=str(SDK/'bin')+os.pathsep+os.environ['PATH']
os.environ['LEAN_SYSROOT']=str(SDK)
os.environ['LEAN_SERVER_NATIVE_DYNLIB']=CONFIG['load_manifest']
os.environ.pop('GPU_SMT_BRANCH_OFF',None)
settings.project_dir=str(B/'mathlib4')
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
with gzip.open(OUT/'original-inputs.jsonl.gz','wt') as f:
 for x in ITEMS:f.write(json.dumps(x,ensure_ascii=False)+'\n')
dump(OUT/'launch.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'root':str(ROOT),'methods':METHODS,'source':'generated control','selected_source_indices':None,'selection':'generated read/write branch validity control, not a benchmark source or performance sample','client':str(K/'server/repl.py'),'inherited_RLIMIT_AS':INHERITED_AS,'policy':'same existing benchmark Workspace AS inheritance; not deployment default memory policy','affinity':sorted(os.sched_getaffinity(0)),'native_manifest':CONFIG,'header_timeout':60,'request_timeout':300,'scope':'two-source protocol regression only, not performance or full service experiment'})
async def check(method):
 target=ROOT/method
 settings.repl_path=str(target/'repl')
 os.environ['LD_LIBRARY_PATH']=os.pathsep.join([str(target),str(SDK/'lib'),str(SDK/'lib/lean')]+CONFIG['library_paths'])
 os.environ['GPU_SMT_FALLBACK_REPL']=str(ROOT/'plain/repl')
 os.environ['GPU_SMT_FALLBACK_LIBRARY_PATH']=os.pathsep.join([str(ROOT/'plain'),str(SDK/'lib'),str(SDK/'lib/lean')]+CONFIG['library_paths'])
 p=OUT/method;p.mkdir();rows=[]
 worker=await Repl.create(header=HEADER,max_repl_uses=settings.max_repl_uses,max_repl_mem=settings.max_repl_mem)
 worker.max_memory_bytes=INHERITED_AS[0]
 before=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 raw=gzip.open(p/'stdout.gz','wb');err=gzip.open(p/'stderr.gz','wb')
 await worker.start()
 reader=worker.proc.stdout;initial=bytes(reader._buffer)
 if initial:raw.write(initial);raw.flush()
 feed=reader.feed_data
 def capture(data):raw.write(data);raw.flush();feed(data)
 reader.feed_data=capture
 async def stderr():
  while data:=await worker.proc.stderr.read(65536):err.write(data);err.flush()
 drain=asyncio.create_task(stderr())
 try:
  header=await asyncio.wait_for(worker.send(Snippet(id='original-header',code=HEADER),is_header=True),60)
  dump(p/'header.json',{'response':header[0],'client_seconds':header[1]})
  bodies=['\n\n'+item['code'][len(HEADER):] for item in ITEMS]
  command={'env':0,'cmds':bodies,'mode':'naive'}
  dump(p/'batch-command.json',command)
  worker.proc.stdin.write((json.dumps(command,ensure_ascii=False)+'\n\n').encode())
  await worker.proc.stdin.drain()
  response=json.loads(await asyncio.wait_for(worker._read_response(),300))
  assert isinstance(response,list) and len(response)==len(ITEMS)
  rows=[{'proof_id':item['proof_id'],'source_index':item['index'],'response':value}
        for item,value in zip(ITEMS,response)]
  dump(p/'responses.json',rows)
  final=await asyncio.wait_for(worker.send(Snippet(id='base-after',code='run_cmd do\n  let value ← liftIO branchProbe.get\n  unless value == 0 do throwError "base ref changed"')),300)
  dump(p/'base-after.json',{'response':final[0]})
  worker.proc.stdin.close()
  await asyncio.wait_for(worker.proc.wait(),300)
  await asyncio.wait_for(drain,300)
  terminal={'state':'complete','start_utc':utc,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':worker.proc.returncode,'normal_eof':True,'rows':rows,'whole_seconds':time.monotonic()-before,'native_executable':settings.repl_path,'library_path':os.environ['LD_LIBRARY_PATH']}
  dump(p/'terminal.json',terminal)
  return terminal
 finally:
  if worker.proc.returncode is None:
   await worker.close()
  for task in [worker._cpu_task,worker._mem_task,drain]:
   if task:
    task.cancel();await asyncio.gather(task,return_exceptions=True)
  worker.error_file.close();raw.close();err.close()
async def main():
 results={}
 for method in METHODS:results[method]=await check(method)
 dump(OUT/'terminal.json',{'state':'complete','methods':results,'scope':'native first-write-copy actual batch engagement, no performance comparison'})
try:asyncio.run(main())
except BaseException as exc:
 dump(OUT/'failed-terminal.json',{'state':'failed','error':repr(exc),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 raise
