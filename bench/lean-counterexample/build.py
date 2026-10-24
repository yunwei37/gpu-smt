"""Build our exporter/parser without replacing a live observation's products."""
from pathlib import Path
import argparse,datetime,importlib.util,json,os,resource,subprocess,tarfile
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--build-out',type=Path,default=Path('/tmp/gpu-smt-counterexample-20261023'))
 p.add_argument('--record-out',type=Path,default=A)
 args=p.parse_args();B=args.build_out;out=args.record_out
 launch=json.loads((A/'full-observe-start.json').read_text())if(A/'full-observe-start.json').exists()else None
 active=launch is not None and Path('/proc',str(launch['pid'])).exists()
 if active:
  previous=json.loads((A/'full-observe/source/build.json').read_text())
  if B.resolve()==Path(previous['build']).resolve():raise RuntimeError('Preserve active observation binaries; use another build output')
 if(out/'build.json').exists():raise RuntimeError('Preserve existing build records; use a new record output')
 out.mkdir(parents=True,exist_ok=True);B.mkdir(parents=True,exist_ok=False)
 source=out/'source';source.mkdir()
 for name in ['Counterexample.lean','Prepare.lean','build.py']:
  (source/name).write_bytes((R/'bench/lean-counterexample'/name).read_bytes())
 D=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture')
 S=D/'lean-4.9.0-rc1-linux';M=D/'mathlib4';N=M/'.lake/build/lib'
 env=dict(os.environ);env['PATH']=str(S/'bin')+':'+env['PATH']
 env['LEAN_PATH']=':'.join(str(q)for q in[B,N]+[q/'.lake/build/lib'for q in(M/'.lake/packages').iterdir()if q.is_dir()])
 os.sched_setaffinity(0,{8,9,10,11})
 resource.setrlimit(resource.RLIMIT_AS,(24*1024**3,24*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 spec=importlib.util.spec_from_file_location('own_build_memory',R/'bench/lean-native/linarith-oracle/memory_budget.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 guard=module.MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,2,'repl',out)
 if active:guard.include_owned_tree(launch['pid'],launch['start_ticks'],A/'full-observe/verification')
 def stop_build_children():
  import psutil
  for child in reversed(psutil.Process(os.getpid()).children(recursive=True)):
   try:child.kill()
   except psutil.NoSuchProcess:pass
 guard.on_error=stop_build_children;guard.start();commands=[]
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  for name in ['Counterexample','Prepare']:
   (B/(name+'.lean')).write_bytes((source/(name+'.lean')).read_bytes())
   cmd=[str(S/'bin/lean'),'-o',name+'.olean','-c',name+'.c',name+'.lean']
   result=subprocess.run(cmd,cwd=B,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   (out/('build-'+name+'.log')).write_text(result.stdout)
   commands.append(dict(command=cmd,exit=result.returncode));print(name,result.returncode,result.stdout[-1500:],flush=True)
   if result.returncode:raise RuntimeError('Own Lean compilation failed')
  cmd=[str(S/'bin/leanc'),'-O3','-shared','-fPIC','-o','libCounterexample.so','Counterexample.c',
   '-L'+str(N),'-Wl,--no-as-needed','-l:libMathlib-Tactic-Linarith-1.so']
  result=subprocess.run(cmd,cwd=B,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (out/'build-native.log').write_text(result.stdout);commands.append(dict(command=cmd,exit=result.returncode))
  print('native',result.returncode,result.stdout[-1500:],flush=True)
  if result.returncode:raise RuntimeError('Own native linking failed')
 finally:
  guard.stop();(out/'memory-summary.json').write_text(json.dumps(guard.summary(),indent=2)+'\n')
  (out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 if guard.error:raise RuntimeError(guard.error)
 with tarfile.open(out/'native-products.tar.gz','w:gz')as archive:
  for item in B.iterdir():archive.add(item,arcname=item.name)
 receipt=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),started_utc=started,
  build=str(B),sdk=str(S),lean_path=env['LEAN_PATH'],library=str(N),commands=commands,
  base_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),
  working_source_status=subprocess.check_output(['git','status','--short','--','bench/lean-counterexample'],cwd=R,text=True),
  scope='Own source build only; no new verification REPL and no active binary replacement. Native runtime qualification pending.')
 (out/'build.json').write_text(json.dumps(receipt,indent=2)+'\n')
 # The active capture already froze its old receipt/paths; this selects future runs.
 (A/'build.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
