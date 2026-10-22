from pathlib import Path
import os,resource,importlib.util,subprocess,json,datetime,shutil
R=Path('/workspaces/repository');O=R/'artifacts/linarith-oracle-2026-10-17/native-stage-profile-20261022'
B=R/'bench/lean-native/linarith-oracle/reproduction/native'
out=Path('/tmp/gpu-smt-native-reference-profile-20261022-v4');out.mkdir(exist_ok=False)
logs=O/'reference-build-v4';logs.mkdir(exist_ok=False)
os.sched_setaffinity(0,{8,9,10,11})
resource.setrlimit(resource.RLIMIT_AS,(24*1024**3,24*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
spec=importlib.util.spec_from_file_location('budget',R/'bench/lean-native/linarith-oracle/memory_budget.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
repl=Path('/tmp/gpu-smt-goedel427-20261014/repl-kimina-native-gc-header-repair/.lake/build/bin/repl')
guard=m.MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,2,repl,logs)
def stop():
 for p in guard.owned():
  if p.pid!=os.getpid():
   try:p.kill()
   except Exception:pass
guard.on_error=stop
guard.start()
env=dict(os.environ);env.update(RUSTUP_HOME='/usr/local/rustup',CARGO_HOME='/usr/local/cargo',PATH='/usr/local/cargo/bin:'+os.environ['PATH'])
cmd=['cargo','+1.98.1','build','--release','--bin','farkas-batchd','--target-dir','/tmp/gpu-smt-linarith-oracle-20261017/portable-source-build/native-target']
try:
 z=subprocess.run(cmd,cwd=B,env=env,text=True,capture_output=True)
 (logs/'cargo.log').write_text(z.stdout+z.stderr)
 record=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=cmd,returncode=z.returncode,source=str(B),output=str(out))
 (logs/'build.json').write_text(json.dumps(record,indent=2)+'\n')
 if z.returncode:raise RuntimeError((z.stdout+z.stderr)[-5000:])
 if guard.error:raise RuntimeError(guard.error)
 binary=Path(cmd[-1])/'release/farkas-batchd'
 shutil.copy2(binary,out/'farkas-batchd')
 print(json.dumps(dict(state='complete',**record)),flush=True)
finally:
 guard.stop();(logs/'memory-summary.json').write_text(json.dumps(guard.summary(),indent=2)+'\n')
