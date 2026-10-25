from pathlib import Path
import os,json,subprocess,time,runpy,psutil,resource
R=Path('/workspaces/repository');O=R/'artifacts/lean-code-verification-2026-10-25';P=Path('/tmp/gpu-smt-code-verification-20261025')
M=O/'cache-prepare-memory';M.mkdir()
os.sched_setaffinity(0,{8,9,10,11})
resource.setrlimit(resource.RLIMIT_AS,(24*1024**3,24*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
W=runpy.run_path(str(R/'bench/lean-native/linarith-oracle/memory_budget.py'))['MemoryWatchdog']
w=W(os.getpid(),48*1024**3,48*1024**3,2,'/tmp/gpu-smt-failure-profiler-20261025/repl',M)
if psutil.pid_exists(275822):
 proc=psutil.Process(275822);assert abs(proc.create_time()-1792894799.05)<.01
 w.include_owned_tree(275822,int(Path('/proc/275822/stat').read_text().rsplit(')',1)[1].split()[19]),R/'artifacts/lean-failure-profile-2026-10-25/full480/profile')
env=dict(os.environ);sdk=P/'sdk/lean-4.18.0-linux';env['PATH']=str(sdk/'bin')+os.pathsep+env['PATH']
cmd=[str(sdk/'bin/lake'),'exe','cache','get'];start=time.time();w.start()
try:
 with(O/'mathlib-cache-prepare.log').open('w')as log:
  q=subprocess.Popen(cmd,cwd=P/'mathlib-source',env=env,stdout=log,stderr=subprocess.STDOUT)
  (O/'mathlib-cache-prepare-launch.json').write_text(json.dumps(dict(pid=q.pid,parent=os.getpid(),command=cmd,cwd=str(P/'mathlib-source'),utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),scope='Dependency/cache setup only, no proof workload collection; actual group remains full480.'),indent=2)+'\n')
  code=q.wait()
 (O/'mathlib-cache-prepare-exit.json').write_text(json.dumps(dict(exit=code,seconds=time.time()-start,finished_UTC=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())),indent=2)+'\n')
 print('CACHE_SETUP_EXIT',code,flush=True)
 print((O/'mathlib-cache-prepare.log').read_text()[-3500:])
finally:
 w.stop();(O/'cache-prepare-memory-summary.json').write_text(json.dumps(w.summary(),indent=2)+'\n')
