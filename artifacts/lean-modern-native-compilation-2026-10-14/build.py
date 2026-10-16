from pathlib import Path
import subprocess,os,shutil,time,json,datetime,traceback
D=Path(__file__).parent;T=Path('/tmp/gpu-smt-goedel427-20261014');SDK=T/'lean-4.27.0-linux'
env=dict(os.environ);env['PATH']=str(SDK/'bin')+os.pathsep+env['PATH']
start=time.monotonic_ns();records=[];code=1
try:
 command=[str(SDK/'bin/lake'),'-v','build','+Mathlib.Tactic.Linarith:dynlib']
 with (D/'mathlib-build.log').open('xb') as h:
  code=subprocess.run(command,cwd=T/'mathlib4',env=env,stdout=h,stderr=subprocess.STDOUT).returncode
 records.append(dict(command=command,returncode=code,cwd=str(T/'mathlib4')))
 if code:raise RuntimeError('official Mathlib dynlib build failed')
 source=T/'repl-producer-options';target=T/'repl-producer-native'
 shutil.copytree(source,target,ignore=shutil.ignore_patterns('.git','.lake'))
 p=target/'REPL/Main.lean';before=p.read_text()
 old='  initSearchPath (← Lean.findSysroot)\n  repl\n'
 new='  initSearchPath (← Lean.findSysroot)\n  if let some nativeLibrary ← IO.getEnv "LEAN_SERVER_NATIVE_DYNLIB" then\n    Lean.loadDynlib nativeLibrary\n  repl\n'
 assert before.count(old)==1
 p.write_text(before.replace(old,new))
 (D/'REPL-Main.original.lean').write_text(before);(D/'REPL-Main.native.lean').write_text(p.read_text())
 command=[str(SDK/'bin/lake'),'build','repl']
 with (D/'repl-build.log').open('xb') as h:
  code=subprocess.run(command,cwd=target,env=env,stdout=h,stderr=subprocess.STDOUT).returncode
 records.append(dict(command=command,returncode=code,cwd=str(target)))
except BaseException:
 (D/'build-error.log').write_text(traceback.format_exc());code=1
record=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),returncode=code,commands=records,elapsed_seconds=(time.monotonic_ns()-start)/1e9,affinity=sorted(os.sched_getaffinity(0)),role='Dependency build only; not performance evidence. Original proofs/producer options/old4.9 active runs untouched.')
(D/'build-terminal.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record),flush=True)
