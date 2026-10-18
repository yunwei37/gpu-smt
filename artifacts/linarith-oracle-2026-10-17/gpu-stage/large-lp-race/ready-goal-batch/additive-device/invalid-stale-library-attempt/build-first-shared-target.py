from pathlib import Path
import os,subprocess,resource,shutil,json,datetime
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch/additive-device'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/ready-goal-additive-device')
os.sched_setaffinity(0,{12,13,14,15});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
env=dict(os.environ,PATH='/usr/local/cargo/bin:'+os.environ['PATH'],CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup',CARGO_TARGET_DIR='/tmp/gpu-smt-linarith-oracle-20261017/ready-goal-batch/numeric-source/target')
cmd=['cargo','build','--release','--offline','--locked','--bin','arithmetic-batchd','--bin','farkas-batchd','--bin','farkas-race-worker']
p=subprocess.run(cmd,cwd=U/'native',env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(A/'build-receipt.json').write_text(json.dumps({'argv':cmd,'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'output':p.stdout},indent=2)+'\n')
print(p.stdout,flush=True)
if p.returncode:raise SystemExit(p.returncode)
for name in ['arithmetic-batchd','farkas-batchd','farkas-race-worker']:shutil.copy2(Path(env['CARGO_TARGET_DIR'])/'release'/name,U/name)
print('BUILD_COMPLETE',flush=True)
