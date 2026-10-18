from pathlib import Path
import os,resource,subprocess,json,datetime
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-omega-control';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/native-omega-control');B=Path('/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle');T=Path('/tmp/gpu-smt-goedel427-20261014');F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
(U/'GpuArithmetic').mkdir(parents=True,exist_ok=True)
for name in ['IntegerControl','IntegerAstControl']:
 target=U/'GpuArithmetic'/(name+'.lean')
 if not target.exists():target.write_bytes((A/(name+'.lean')).read_bytes())
 else:assert target.read_bytes()==(A/(name+'.lean')).read_bytes(),'private source differs'
for dep in(B/'GpuArithmetic').glob('*'):
 if dep.suffix in ['.olean','.ilean']:
  dest=U/'GpuArithmetic'/dep.name
  if not dest.exists():dest.symlink_to(dep)
for name in ['arithmetic-batchd','farkas-batchd','farkas-race-worker','native']:
 target=U/name
 if not target.exists():target.symlink_to(B/name,target_is_directory=(B/name).is_dir())
os.sched_setaffinity(0,{4,5,6,7});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
env=dict(os.environ,PATH=str(T/'lean-4.27.0-linux/bin')+':'+os.environ['PATH'])
env['LEAN_PATH']=':'.join([str(U),str(B),str(U.parent),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean')for p in(T/'mathlib4/.lake/packages').iterdir()if p.is_dir()])
commands=[]
for name in ['IntegerControl','IntegerAstControl']:
 cmd=['lean','-o',str(U/'GpuArithmetic'/(name+'.olean')),'-c',str(U/(name+'.c')),str(U/'GpuArithmetic'/(name+'.lean'))]
 q=subprocess.run(cmd,cwd=U,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);commands.append({'argv':cmd,'exit':q.returncode,'output':q.stdout});print(name,q.returncode,q.stdout,flush=True)
 if q.returncode:break
if all(x['exit']==0 for x in commands):
 cmd=['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*[str(B/(n+'.c'))for n in ['BatchNative','BatchFast','BatchBaseline','BatchOracle']],str(U/'IntegerControl.c'),str(U/'IntegerAstControl.c'),'-o',str(U/'batch-oracle.so')]
 q=subprocess.run(cmd,cwd=U,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);commands.append({'argv':cmd,'exit':q.returncode,'output':q.stdout});print('LINK',q.returncode,q.stdout[-1000:],flush=True)
(A/'build-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':commands,'source_scope':'unchanged retained four Batch generatedC files plus two new official-omega control modules'},indent=2)+'\n')
assert len(commands)==3 and all(x['exit']==0 for x in commands)
print('COMPILED_SHARED', (U/'batch-oracle.so').stat().st_size,flush=True)
