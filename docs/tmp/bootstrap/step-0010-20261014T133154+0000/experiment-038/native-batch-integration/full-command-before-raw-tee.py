"""Executed finite E038 native comparison command; frozen v1, all original sources.
Not a scheduler/helper service. This file preserves the actual one-off command.
"""
from pathlib import Path
import asyncio,collections,contextlib,datetime,gzip,json,os,resource,shutil,sys,time
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d');sys.path.insert(0,str(K))
import psutil
from server.repl import Repl
from server.settings import settings
R=Path('/workspaces/repository');B=Path('/tmp/gpu-smt-goedel427-20261014');SDK=B/'lean-4.27.0-linux'
E=R/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-batch-integration'
F=Path('/tmp/gpu-smt-native-ref-branches-20261016/batch-frozen-v1')
INPUT=R/'artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl'
OUT=Path(sys.argv[1]);OUT.mkdir(exist_ok=False)
HEADER='import Mathlib\nimport Aesop\n';WIDTH=len(os.sched_getaffinity(0))
ITEMS=[json.loads(line) for line in INPUT.open()]
assert len(ITEMS)==29750 and all(x['code'].startswith(HEADER) for x in ITEMS)
assert len({x['proof_id'] for x in ITEMS})==len(ITEMS)
CONFIG=json.loads((INPUT.parent/'native-library.json').read_text())
INHERITED_AS=resource.getrlimit(resource.RLIMIT_AS)
os.environ['PATH']=str(SDK/'bin')+os.pathsep+os.environ['PATH']
os.environ['LEAN_SYSROOT']=str(SDK);os.environ['LEAN_SERVER_NATIVE_DYNLIB']=CONFIG['load_manifest']
settings.project_dir=str(B/'mathlib4')
def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def emit(stream,value):stream.write(json.dumps(value,ensure_ascii=False)+'\n')
def limits_cpu():return {k:os.environ.get(k) for k in ['LEAN_NUM_THREADS','OMP_NUM_THREADS','CORE']}
def outcome(value):
 if not isinstance(value,dict):return 'operational'
 if 'error' in value or 'message' in value:return 'native_error'
 if any(x.get('severity')=='error' for x in value.get('messages',[])):return 'rejected'
 if value.get('sorries'):return 'incomplete'
 return 'complete'
def ru():return resource.getrusage(resource.RUSAGE_SELF),resource.getrusage(resource.RUSAGE_CHILDREN)
ORDERS=[['stock','private','off'],['private','off','stock'],['off','stock','private']]
dump(OUT/'launch.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source':str(INPUT),'sources':len(ITEMS),'source_bytes':INPUT.stat().st_size,'width':WIDTH,'affinity':sorted(os.sched_getaffinity(0)),'inherited_RLIMIT_AS':INHERITED_AS,'nominal_Kimina_max_repl_mem_MiB':settings.max_repl_mem,'effective_policy':'inherit Workspace AS for every native worker/replay child; not default12GiB Kimina policy','native_thread_env':limits_cpu(),'orders':ORDERS,'frozen_paths':json.loads((E/'frozen-paths.json').read_text()),'native_manifest':CONFIG,'header_timeout_seconds':60,'batch_and_normal_exit_timeout_seconds':300,'sampling_seconds':1,'collector_source':str(Path(__file__))})
with INPUT.open('rb') as source,gzip.open(OUT/'original-input.jsonl.gz','wb',compresslevel=1) as archive:shutil.copyfileobj(source,archive)
async def cell(rep,name):
 path=OUT/('rep'+str(rep)+'-'+name);path.mkdir()
 started=time.monotonic_ns();ru0=ru();counts=collections.Counter();workers=0;completed=0;peak_pss=0;peak_rss=0;sample_errors=0
 events=gzip.open(path/'events.jsonl.gz','wt',compresslevel=1);rows=gzip.open(path/'responses.jsonl.gz','wt',compresslevel=1);samples=gzip.open(path/'resources.jsonl.gz','wt',compresslevel=1);raw=gzip.open(path/'stdout.gz','wb',compresslevel=1)
 repl=None;err_task=None;sampler=None
 def event(kind,**data):emit(events,{'event':kind,'ns':time.monotonic_ns(),**data});events.flush()
 async def stderr(worker,number):
  with gzip.open(path/('stderr-worker'+str(number)+'.gz'),'wb',compresslevel=1) as stream:
   while data:=await worker.proc.stderr.read(65536):stream.write(data)
 async def sample(worker,number):
  nonlocal peak_pss,peak_rss,sample_errors
  while True:
   processes=[];errors=[]
   try:
    root=psutil.Process(os.getpid());processes=[root]+root.children(recursive=True)
   except psutil.Error as exc:errors.append(repr(exc))
   values=[]
   for proc in processes:
    try:
     m=proc.memory_full_info();c=proc.cpu_times();values.append({'pid':proc.pid,'created':proc.create_time(),'rss':m.rss,'pss':m.pss,'vms':m.vms,'user':c.user,'system':c.system,'threads':proc.num_threads()})
    except psutil.Error as exc:errors.append(repr(exc))
   pss=sum(x['pss'] for x in values);rss=sum(x['rss'] for x in values)
   peak_pss=max(peak_pss,pss);peak_rss=max(peak_rss,rss);sample_errors+=len(errors)
   emit(samples,{'ns':time.monotonic_ns(),'worker':number,'collector_included':True,'pss':pss,'rss':rss,'processes':values,'errors':errors})
   samples.flush()
   if worker.proc.returncode is not None:break
   await asyncio.sleep(1)
 async def exchange(value,deadline):
  wire=(json.dumps(value,ensure_ascii=False)+'\n\n').encode()
  repl.proc.stdin.write(wire);await repl.proc.stdin.drain()
  response=await asyncio.wait_for(repl._read_response(),deadline)
  raw.write(response if isinstance(response,bytes) else response.encode());raw.write(b'\n\n');raw.flush()
  return json.loads(response)
 async def retire(normal):
  nonlocal repl,err_task,sampler
  if repl is None:return
  worker=repl;error=None;native_eof=False
  try:
   if normal:
    worker.proc.stdin.close()
    tail=asyncio.create_task(worker.proc.stdout.read())
    await asyncio.wait_for(worker.proc.wait(),300)
    remaining=await asyncio.wait_for(tail,300)
    raw.write(remaining);native_eof=True
   else:await worker.close()
  except Exception as exc:
   error=repr(exc)
   if worker.proc is not None and worker.proc.returncode is None:await worker.close()
  finally:
   if err_task is not None:await err_task
   if sampler is not None:
    sampler.cancel();await asyncio.gather(sampler,return_exceptions=True)
   for task in [worker._cpu_task,worker._mem_task]:
    if task is not None:task.cancel();await asyncio.gather(task,return_exceptions=True)
   event('worker_terminal',worker=workers,pid=worker.proc.pid if worker.proc else None,exit_code=worker.proc.returncode if worker.proc else None,normal_eof=native_eof,error=error)
   worker.error_file.close();repl=None;err_task=None;sampler=None
  if normal and (not native_eof or error or worker.proc.returncode!=0):return {'error':error,'exit_code':worker.proc.returncode}
  return None
 async def start():
  nonlocal repl,workers,err_task,sampler
  settings.repl_path=str(F/('plain' if name=='stock' else 'private')/'repl')
  lib=os.pathsep.join([str(F/('plain' if name=='stock' else 'private')),str(SDK/'lib'),str(SDK/'lib/lean')]+CONFIG['library_paths'])
  os.environ['LD_LIBRARY_PATH']=lib;os.environ['GPU_SMT_FALLBACK_REPL']=str(F/'plain/repl')
  os.environ['GPU_SMT_FALLBACK_LIBRARY_PATH']=os.pathsep.join([str(F/'plain'),str(SDK/'lib'),str(SDK/'lib/lean')]+CONFIG['library_paths'])
  if name=='off':os.environ['GPU_SMT_BRANCH_OFF']='1'
  else:os.environ.pop('GPU_SMT_BRANCH_OFF',None)
  repl=await Repl.create(header=HEADER,max_repl_uses=settings.max_repl_uses,max_repl_mem=settings.max_repl_mem)
  repl.max_memory_bytes=INHERITED_AS[0];workers+=1;t=time.monotonic_ns()
  event('worker_start',worker=workers,executable=settings.repl_path,library_path=lib,effective_RLIMIT_AS=INHERITED_AS[0])
  await repl.start();err_task=asyncio.create_task(stderr(repl,workers));sampler=asyncio.create_task(sample(repl,workers))
  header=await exchange({'cmd':HEADER},60)
  event('header',worker=workers,pid=repl.proc.pid,elapsed_ns=time.monotonic_ns()-t,response=header)
  if header.get('env')!=0:raise RuntimeError('native header did not return env0')
 try:
  for offset in range(0,len(ITEMS),WIDTH):
   batch=ITEMS[offset:offset+WIDTH];t=time.monotonic_ns();failure=None;response=None
   try:
    if repl is None:await start()
    request={'env':0,'cmds':['\n\n'+x['code'][len(HEADER):] for x in batch],'mode':'naive'}
    event('request',worker=workers,offset=offset,count=len(batch),ids=[x['proof_id'] for x in batch])
    response=await exchange(request,300)
    if not isinstance(response,list) or len(response)!=len(batch):raise RuntimeError('native response is not a complete matching array')
   except Exception as exc:
    failure=repr(exc);event('batch_operational',worker=workers,offset=offset,error=failure,partial=response)
    await retire(False)
   observed=time.monotonic_ns()
   for index,item in enumerate(batch):
    value=None if failure else response[index];state='operational' if failure else outcome(value);counts[state]+=1
    emit(rows,{'index':offset+index,'proof_id':item['proof_id'],'worker':workers,'batch_offset':offset,'admitted_ns':t,'observed_ns':observed,'batch_latency_ns':observed-t,'outcome':state,'operational_error':failure,'response':value})
   completed+=len(batch);rows.flush()
   event('batch_terminal',offset=offset,count=len(batch),completed=completed,elapsed_ns=observed-t,operational=failure is not None)
   if failure and ('Separator is not found' in failure or 'longer than limit' in failure or 'chunk exceed' in failure):
    raise RuntimeError('native frame transport limit encountered: preserve partial run and repair equally before continuing')
  finalization=await retire(True)
  if finalization is not None:raise RuntimeError('normal EOF failure: '+repr(finalization))
  status='complete'
 except BaseException:
  await retire(False);status='failed'
  raise
 finally:
  for stream in [events,rows,samples,raw]:stream.close()
  ru1=ru();cpu={}
  for label,before,after in [('collector',ru0[0],ru1[0]),('waited_children',ru0[1],ru1[1])]:cpu[label]={'user':after.ru_utime-before.ru_utime,'system':after.ru_stime-before.ru_stime}
  result={'method':name,'rep':rep,'state':locals().get('status','failed'),'expected':len(ITEMS),'attempts':completed,'counts':dict(counts),'whole_ns':time.monotonic_ns()-started,'cpu':cpu,'sampled_peak_fleet_pss_with_collector':peak_pss,'sampled_peak_fleet_rss_with_collector':peak_rss,'sampling_read_errors':sample_errors,'workers':workers,'effective_RLIMIT_AS':INHERITED_AS[0],'width':WIDTH,'normalization':'none; preserve complete parsed native JSON values','scope':'one original-order offline native-batch whole-corpus observation; grouped array latency'}
  dump(path/'terminal.json',result);print('CELL_TERMINAL',json.dumps(result),flush=True)
 return result
async def main():
 results=[]
 for rep,order in enumerate(ORDERS,1):
  for name in order:
   results.append(await cell(rep,name));dump(OUT/'completed-cells.json',results)
 dump(OUT/'terminal.json',{'state':'complete','cells':len(results),'attempts':sum(x['attempts'] for x in results),'results':results,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
try:asyncio.run(main())
except BaseException as exc:
 dump(OUT/'failed-terminal.json',{'state':'failed','exception':repr(exc),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 raise
