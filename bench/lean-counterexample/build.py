"""Build only our goal exporter/parser against existing native Lean4.9."""
from pathlib import Path
import os,subprocess,resource,json,datetime
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
B=Path('/tmp/gpu-smt-counterexample-20261023')
D=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture')
S=D/'lean-4.9.0-rc1-linux';M=D/'mathlib4';N=M/'.lake/build/lib'
B.mkdir(exist_ok=True)
env=dict(os.environ);env['PATH']=str(S/'bin')+':'+env['PATH']
env['LEAN_PATH']=':'.join(str(p)for p in [B,N]+[p/'.lake/build/lib'for p in (M/'.lake/packages').iterdir()if p.is_dir()])
os.sched_setaffinity(0,{8,9,10,11});resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
commands=[]
for name in ['Counterexample','Prepare']:
 (B/(name+'.lean')).write_bytes((R/'bench/lean-counterexample'/(name+'.lean')).read_bytes())
 cmd=[str(S/'bin/lean'),'-o',name+'.olean','-c',name+'.c',name+'.lean']
 x=subprocess.run(cmd,cwd=B,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (A/('build-'+name+'.log')).write_text(x.stdout);commands.append(dict(command=cmd,exit=x.returncode))
 print(name,x.returncode,x.stdout[-5000:],flush=True)
 if x.returncode:raise SystemExit(x.returncode)
cmd=[str(S/'bin/leanc'),'-O3','-shared','-fPIC','-o','libCounterexample.so','Counterexample.c','-L'+str(N),'-Wl,--no-as-needed','-l:libMathlib-Tactic-Linarith-1.so']
x=subprocess.run(cmd,cwd=B,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(A/'build-native.log').write_text(x.stdout);commands.append(dict(command=cmd,exit=x.returncode));print('native',x.returncode,x.stdout[-2000:],flush=True)
if x.returncode:raise SystemExit(x.returncode)
(A/'build.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),build=str(B),sdk=str(S),lean_path=env['LEAN_PATH'],library=str(N),commands=commands),indent=2)+'\n')
