from pathlib import Path
import subprocess,os,time,json,gzip,datetime,signal,psutil
r=Path('/workspaces/repository')
sdk=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
project=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/mathlib4')
source=r/'bench/lean-failure-profile/hotspot-sites/HotspotSites.lean'
base=r/'artifacts/hotspot-mechanisms-2026-10-25/goal-effects'
base.mkdir(exist_ok=True)
number=len(list(base.glob('compile-*')))+1
out=base/('compile-'+str(number).zfill(3));out.mkdir()
build=Path('/tmp/gpu-smt-interval-continuation-20261025');build.mkdir(exist_ok=True)
os.sched_setaffinity(0,{11})
cmd=[str(sdk/'bin/lake'),'env',str(sdk/'bin/lean'),'--run',str(source),'/tmp/gpu-smt-hotspot-sites-20261025/inputs.json',str(out/'sites.json')]
env=dict(os.environ,PATH=str(sdk/'bin')+os.pathsep+os.environ['PATH'],LEAN_SYSROOT=str(sdk))
env['LEAN_PATH']='/tmp/gpu-smt-simp-all-profile-20261025'+os.pathsep+subprocess.check_output([str(sdk/'bin/lake'),'env','printenv','LEAN_PATH'],cwd=project,env=env,text=True).strip()
root=psutil.Process();old=None
try:
 q=psutil.Process(283334)
 if abs(q.create_time()-1792912973.05)<.01:old=q
except psutil.NoSuchProcess:pass
samples=[];pressure=False;errors=[];start=time.monotonic()
with(out/'compiler.log').open('wb')as f:
 p=subprocess.Popen(cmd,cwd=project,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
 try:
  while True:
   processes={}
   for owner in [root]+([old]if old else[]):
    try:
     for q in [owner]+owner.children(recursive=True):
      try:processes[(q.pid,q.create_time())]=q.memory_info().rss
      except psutil.NoSuchProcess:pass
    except psutil.NoSuchProcess:pass
   total=sum(processes.values())
   samples.append(dict(seconds=time.monotonic()-start,rss_bytes=total,owned=[dict(pid=k[0],birth=k[1],rss=v)for k,v in processes.items()]))
   if total>48*1024**3 and p.poll()is None:
    pressure=True;os.killpg(p.pid,signal.SIGKILL)
   if p.poll()is not None:break
   time.sleep(1)
 except BaseException as e:
  errors.append(repr(e))
  if p.poll()is None:os.killpg(p.pid,signal.SIGKILL)
  raise
 finally:code=p.wait()
receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=cmd,cwd=str(project),exit=code,seconds=time.monotonic()-start,samples=len(samples),combined_peak_rss_bytes=max(x['rss_bytes']for x in samples),budget_bytes=48*1024**3,pressure_aborted_only_new_compiler=pressure,monitor_errors=errors,source_compile_only=False,source_parse_only=True,native_candidate_executions=0,original_group=old.pid if old else None)
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(out/'memory-samples.jsonl.gz').write_bytes(gzip.compress(''.join(json.dumps(s)+'\n'for s in samples).encode(),mtime=0))
(out/'source.lean').write_bytes(source.read_bytes())
(out/'run-source.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(receipt),flush=True)
print((out/'compiler.log').read_text()[-6000:],flush=True)
