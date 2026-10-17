from pathlib import Path
import sys,os,json,asyncio,time,resource,psutil,datetime
k=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d');sys.path.insert(0,str(k))
from server.repl import Repl
from server.settings import settings
r=Path('/workspaces/repository');b=Path('/tmp/gpu-smt-goedel427-20261014');sdk=b/'lean-4.27.0-linux'
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-local-ref-lifetime'
d=Path('/tmp/gpu-smt-native-local-ref-lifetime-20261017/build')
locked=Path('/tmp/gpu-smt-native-write-copy-20261016/build/private')
config=json.loads((r/'artifacts/lean-modern-native-compilation-2026-10-14/native-library.json').read_text())
os.environ['PATH']=str(sdk/'bin')+os.pathsep+os.environ['PATH'];os.environ['LEAN_SYSROOT']=str(sdk)
os.environ['LEAN_SERVER_NATIVE_DYNLIB']=config['load_manifest']
header='import Mathlib\nimport Aesop\n';width=len(os.sched_getaffinity(0))
with (r/'artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl').open() as f:items=[json.loads(next(f)) for _ in range(width)]
for row in items:assert row['code'].startswith(header)
request={'env':0,'mode':'naive','cmds':['\n\n'+x['code'][len(header):] for x in items]}
(e/'preflight-original-inputs.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in items))
settings.project_dir=str(b/'mathlib4')
async def method(name,block):
 out=e/('diagnostic-block'+str(block)+'-'+name);out.mkdir(exist_ok=False)
 target=d/'plain' if name=='stock' else locked if name=='locked' else d/'private'
 settings.repl_path=str(target/'repl')
 os.environ['LD_LIBRARY_PATH']=os.pathsep.join([str(target),str(sdk/'lib'),str(sdk/'lib/lean')]+config['library_paths'])
 os.environ['GPU_SMT_FALLBACK_REPL']=str(d/'plain/repl')
 os.environ['GPU_SMT_FALLBACK_LIBRARY_PATH']=os.pathsep.join([str(d/'plain'),str(sdk/'lib'),str(sdk/'lib/lean')]+config['library_paths'])
 if name=='off':os.environ['GPU_SMT_BRANCH_OFF']='1'
 else:os.environ.pop('GPU_SMT_BRANCH_OFF',None)
 repl=await Repl.create(header=header,max_repl_uses=settings.max_repl_uses,max_repl_mem=settings.max_repl_mem)
 repl.max_memory_bytes=resource.getrlimit(resource.RLIMIT_AS)[0]
 started=time.monotonic_ns();ru0=resource.getrusage(resource.RUSAGE_CHILDREN);self0=resource.getrusage(resource.RUSAGE_SELF);samples=[];result={'method':name,'block':block,'binary':str(target/'repl'),'width':width,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'nominal_Kimina_max_repl_mem_MiB':settings.max_repl_mem,'effective_RLIMIT_AS':repl.max_memory_bytes,'original_ids':[x['proof_id'] for x in items]}
 async def stderr():
  with (out/'stderr').open('wb') as f:
   while chunk:=await repl.proc.stderr.read(65536):f.write(chunk);f.flush()
 async def sample():
  while repl.proc.returncode is None:
   procs=[]
   try:root=psutil.Process(repl.proc.pid);procs=[root]+root.children(recursive=True)
   except psutil.Error:pass
   row={'ns':time.monotonic_ns(),'rss':0,'pss':0,'processes':[]}
   for p in procs:
    try:
     mem=p.memory_full_info();cpu=p.cpu_times();row['rss']+=mem.rss;row['pss']+=mem.pss;row['processes'].append({'pid':p.pid,'rss':mem.rss,'pss':mem.pss,'cpu_user':cpu.user,'cpu_system':cpu.system})
    except psutil.Error:pass
   samples.append(row);await asyncio.sleep(1)
 async def exchange(value,timeout):
  payload=json.dumps(value,ensure_ascii=False)+'\n\n'
  repl.proc.stdin.write(payload.encode());await repl.proc.stdin.drain()
  raw=await asyncio.wait_for(repl._read_response(),timeout)
  return raw,json.loads(raw)
 errtask=None;sampler=None
 try:
  await repl.start();errtask=asyncio.create_task(stderr());sampler=asyncio.create_task(sample())
  result['pid']=repl.proc.pid
  raw,h=await exchange({'cmd':header},60);(out/'header.stdout').write_bytes(raw if isinstance(raw,bytes) else raw.encode());result['header_ns']=time.monotonic_ns()-started;result['header']=h
  t=time.monotonic_ns();raw,res=await exchange(request,300);result['batch_ns']=time.monotonic_ns()-t
  (out/'batch.stdout').write_bytes(raw if isinstance(raw,bytes) else raw.encode());result['responses']=res;result['complete_array']=isinstance(res,list) and len(res)==len(items)
  repl.proc.stdin.close();await asyncio.wait_for(repl.proc.wait(),300);result['normal_eof']=True
 except Exception as exc:
  result['exception']=repr(exc);result['normal_eof']=False
  if repl.proc is not None:await repl.close()
 finally:
  if errtask is not None:await errtask
  if sampler is not None:sampler.cancel();await asyncio.gather(sampler,return_exceptions=True)
  for task in [repl._cpu_task,repl._mem_task]:
   if task is not None:task.cancel();await asyncio.gather(task,return_exceptions=True)
  result['exit_code']=repl.proc.returncode if repl.proc else None
  self1=resource.getrusage(resource.RUSAGE_SELF);result['collector_cpu_seconds']=self1.ru_utime+self1.ru_stime-self0.ru_utime-self0.ru_stime
  result['whole_ns']=time.monotonic_ns()-started
  ru1=resource.getrusage(resource.RUSAGE_CHILDREN);result['waited_tree_cpu_user']=ru1.ru_utime-ru0.ru_utime;result['waited_tree_cpu_system']=ru1.ru_stime-ru0.ru_stime
  result['sampled_peak_pss']=max((x['pss'] for x in samples),default=0);result['sampled_peak_rss']=max((x['rss'] for x in samples),default=0)
  (out/'resources.json').write_text(json.dumps(samples,indent=2)+'\n')
  (out/'terminal.json').write_text(json.dumps(result,indent=2)+'\n')
 print(name,json.dumps({x:result.get(x) for x in ['width','whole_ns','batch_ns','normal_eof','exit_code','complete_array','exception','sampled_peak_pss','waited_tree_cpu_user','waited_tree_cpu_system']}),flush=True)
 return result
async def main():
 results=[]
 for block,order in enumerate([['stock','locked','atomic'],['atomic','locked','stock']],1):
  for name in order:results.append(await method(name,block))
 (e/'diagnostic-summary.json').write_text(json.dumps(results,indent=2)+'\n')
 print('ALL_NATIVE_OUTCOMES_EQUAL',all(x.get('complete_array') for x in results) and all(x.get('responses')==results[0].get('responses') for x in results),flush=True)
asyncio.run(main())
