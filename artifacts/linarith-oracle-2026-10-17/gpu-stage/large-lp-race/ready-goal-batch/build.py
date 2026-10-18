from pathlib import Path
import os,resource,subprocess,json,datetime,shutil
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/ready-goal-batch')
B=U.parent/'two-sided-oracle';O=U.parent/'native-omega-control';T=Path('/tmp/gpu-smt-goedel427-20261014');F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
os.sched_setaffinity(0,{8,9,10,11});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
env=dict(os.environ,PATH=str(T/'lean-4.27.0-linux/bin')+':/usr/local/cargo/bin:'+os.environ['PATH'],CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup')
env['LEAN_PATH']=':'.join([str(U),str(O),str(B),str(U.parent),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean')for p in(T/'mathlib4/.lake/packages').iterdir()if p.is_dir()])
commands=[]
def run(cmd,cwd):
 p=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 commands.append({'argv':cmd,'cwd':str(cwd),'exit':p.returncode,'output':p.stdout})
 (A/'build-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':commands},indent=2)+'\n')
 print(p.returncode,p.stdout[-1800:],flush=True)
 if p.returncode:raise SystemExit(p.returncode)
run(['lean','-o',str(U/'GpuArithmetic/GoalBatchOracle.olean'),'-c',str(U/'GoalBatchOracle.c'),str(U/'GpuArithmetic/GoalBatchOracle.lean')],U)
run(['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*[str(B/(n+'.c'))for n in ['BatchNative','BatchFast','BatchBaseline','BatchOracle']],str(O/'IntegerControl.c'),str(O/'IntegerAstControl.c'),str(U/'GoalBatchOracle.c'),'-o',str(U/'batch-oracle.so')],U)
run(['cargo','build','--release','--offline','--locked','--bin','arithmetic-batchd'],U/'numeric-source')
shutil.copy2(U/'numeric-source/target/release/arithmetic-batchd',U/'arithmetic-batchd')
print('GOAL_BATCH_BUILD_COMPLETE',flush=True)
