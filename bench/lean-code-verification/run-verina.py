"""Native Verina reference-file profiles at the benchmark's pinned Lean4.18."""
from pathlib import Path
import argparse,asyncio,datetime,gzip,json,os,psutil,resource,runpy,signal,sys,time,traceback
ROOT=Path('/workspaces/repository')
ART=ROOT/'artifacts/lean-code-verification-2026-10-25'
OWNED=None
def append(path,value):
 with path.open('a')as f:f.write(json.dumps(value,ensure_ascii=False)+'\n')
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(24*1024**3,24*1024**3))
 resource.setrlimit(resource.RLIMIT_CORE,(0,0))
async def cell(mode,files,out,sdk,project,lean_path):
 out.mkdir();(out/'profiles').mkdir();(out/'logs').mkdir()
 start=time.monotonic_ns()
 W=runpy.run_path(str(ROOT/'bench/lean-native/linarith-oracle/memory_budget.py'))['MemoryWatchdog']
 guard=W(os.getpid(),48*1024**3,48*1024**3,2,sdk/'bin/lean',out)
 semaphore=asyncio.Semaphore(2);rows=[];processes={}
 env=dict(os.environ);env['LEAN_PATH']=lean_path;env['PATH']=str(sdk/'bin')+os.pathsep+env['PATH']
 loop=asyncio.get_running_loop();owner=asyncio.current_task()
 def monitor_failure():
  for p in list(processes.values()):
   if p.returncode is None:
    try:os.killpg(p.pid,signal.SIGKILL)
    except ProcessLookupError:pass
  loop.call_soon_threadsafe(owner.cancel)
 guard.on_error=monitor_failure;guard.start()
 strip=runpy.run_path(str(ROOT/'bench/lean-candidate-scheduling/analyze.py'))['strip_comments']
 async def one(path):
  async with semaphore:
   sid=path.parent.name;cmd=[str(sdk/'bin/lean'),'--json']
   profile=out/'profiles'/(sid+'.json')
   if mode=='profile':cmd+=['-Dprofiler=true','-Dtrace.profiler=true','-Dtrace.profiler.output='+str(profile),'-Dtrace.profiler.output.pp=true']
   cmd+=[str(path)]
   started=time.monotonic_ns()
   proc=await asyncio.create_subprocess_exec(*cmd,cwd=project,env=env,start_new_session=True,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
   processes[proc.pid]=proc;birth=psutil.Process(proc.pid).create_time()
   activity=out/'activity'/(str(proc.pid)+'.json')
   activity.write_text(json.dumps(dict(pid=proc.pid,birth=birth,source_id=sid,phase='body'))+'\n')
   timed=False;read=asyncio.create_task(proc.communicate())
   try:
    # Published synchronous Verina checker default; not a research deadline.
    stdout,stderr=await asyncio.wait_for(asyncio.shield(read),120)
   except asyncio.TimeoutError:
    timed=True
    try:os.killpg(proc.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    stdout,stderr=await read
   except BaseException:
    if proc.returncode is None:
     try:os.killpg(proc.pid,signal.SIGKILL)
     except ProcessLookupError:pass
    await asyncio.shield(read)
    raise
   finally:
    if proc.returncode is None:
     try:os.killpg(proc.pid,signal.SIGKILL)
     except ProcessLookupError:pass
     await proc.wait()
    processes.pop(proc.pid,None)
   elapsed=(time.monotonic_ns()-started)/1e9
   (out/'logs'/(sid+'.stdout.gz')).write_bytes(gzip.compress(stdout,mtime=0))
   (out/'logs'/(sid+'.stderr.gz')).write_bytes(gzip.compress(stderr,mtime=0))
   raw=path.read_text();admission=bool(__import__('re').search(r'\b(sorry|admit)\b',strip(raw)))
   text=(stdout+stderr).decode(errors='replace')
   notices=[]
   for notice in(out/'kills').glob('*.json'):
    value=json.loads(notice.read_text())
    if value.get('victim_pid')==proc.pid:notices.append(value)
   if timed:status='timeout'
   elif notices or any(s in text for s in ['bad_alloc','failed to allocate memory','out of memory']):status='resource_failure'
   elif proc.returncode!=0:status='lean_error'
   elif admission or 'declaration uses' in text and 'sorry' in text:status='incomplete_reference'
   else:status='native_exit0_no_explicit_admission'
   row=dict(source_id=sid,path=str(path),command=cmd,pid=proc.pid,birth=birth,exit=proc.returncode,status=status,
    source_has_explicit_admission=admission,whole_file_seconds=elapsed,profile_exists=profile.exists(),
    source_bytes=len(raw.encode()),scope='Original official reference file, nativeCLI complete import/elaboration/checking and source diagnostics; status is not a corpus theorem soundness proof.')
   rows.append(row);append(out/'results.jsonl',row)
   activity.write_text(json.dumps(dict(pid=proc.pid,birth=birth,source_id=sid,phase='closed'))+'\n')
   if profile.exists():
    data=profile.read_bytes();profile.with_name(profile.name+'.gz').write_bytes(gzip.compress(data,mtime=0));profile.unlink()
 jobs=[asyncio.create_task(one(p))for p in files]
 try:
  await asyncio.gather(*jobs)
 finally:
  for job in jobs:
   if not job.done():job.cancel()
  await asyncio.gather(*jobs,return_exceptions=True)
  for p in list(processes.values()):
   if p.returncode is None:
    try:os.killpg(p.pid,signal.SIGKILL)
    except ProcessLookupError:pass
  for p in list(processes.values()):await p.wait()
  guard.stop()
 terminal=dict(mode=mode,state='complete'if len(rows)==len(files)and not guard.error else'incomplete',
  expected=len(files),returned=len(rows),whole_lifecycle_seconds=(time.monotonic_ns()-start)/1e9,
  memory_watchdog=guard.summary(),remaining_owned_descendants=[p.pid for p in guard.owned()if p.pid!=os.getpid()],
  profile_scope='Builtin100ms component profiler and default10ms structured trace thresholds; completed trace wall intervals are not sampledCPU. Missing timed-out profiles remain censored.')
 (out/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
 return terminal
async def main(args):
 global OWNED
 runpy.run_path(str(ROOT/'bench/lean-candidate-scheduling/run.py'))['check_collection_ownership']()
 if psutil.pid_exists(275822):
  p=psutil.Process(275822)
  if abs(p.create_time()-1792894799.05)<.01 and p.status()!=psutil.STATUS_ZOMBIE:raise RuntimeError('Sole existing480capture still live')
 previous=ROOT/'artifacts/lean-failure-profile-2026-10-25/full480'
 if not(previous/'client-exit.json').exists():raise RuntimeError('Resolve existing480terminal and retirement first')
 receipt=json.loads((ART/'sdk-extraction2.json').read_text());sdk=Path(receipt['SDK']);project=Path(json.loads((ART/'sdk-preparation.json').read_text())['mathlib_source'])
 source=Path(receipt['Verina_original_project'])/'datasets/verina'
 # SDK/package environment preparation is outside proof timings and recorded.
 env=dict(os.environ);env['PATH']=str(sdk/'bin')+os.pathsep+env['PATH']
 lean_path=__import__('subprocess').check_output([str(sdk/'bin/lake'),'env','printenv','LEAN_PATH'],cwd=project,env=env,text=True).strip()
 files=sorted(source.glob('*/task.lean'));assert len(files)==189
 if args.phase=='qualification':
  files=[source/'verina_basic_1/task.lean',source/'verina_basic_2/task.lean',source/'verina_advanced_1/task.lean']
 args.out.mkdir(exist_ok=False);OWNED=args.out
 (args.out/'run-source.py').write_bytes(Path(__file__).read_bytes())
 (args.out/'environment.json').write_text(json.dumps(dict(SDK=str(sdk),mathlib=str(project),LEAN_PATH=lean_path,files=[str(f)for f in files],native_timeout_seconds=120),indent=2)+'\n')
 summaries=[]
 for mode in ['native','profile']:
  terminal=await cell(mode,files,args.out/mode,sdk,project,lean_path);summaries.append(terminal)
  if terminal['state']!='complete'or terminal['remaining_owned_descendants']:raise RuntimeError('Retain incomplete/owned-lifecycle failure before proceeding')
 (args.out/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
 print(json.dumps(summaries),flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--phase',choices=['qualification','full'],required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
 os.sched_setaffinity(0,{8,9,10,11});limits();code=0;error=None
 try:asyncio.run(main(args))
 except BaseException:
  code=1;error=traceback.format_exc();raise
 finally:
  if OWNED is not None:(OWNED/'client-exit.json').write_text(json.dumps(dict(exit=code,error=error,UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
