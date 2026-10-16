from pathlib import Path
import os,shutil,subprocess,json,datetime,time
R=Path('/workspaces/repository')
D=Path(__file__).parent
S=Path('/tmp/gpu-smt-goedel427-20261014/repl-kimina-gc')
T=Path('/tmp/gpu-smt-kimina-gc49-20261015')
SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
start=time.monotonic_ns()
shutil.copytree(S,T,ignore=shutil.ignore_patterns('.git','.lake'))
(T/'lean-toolchain').write_text('leanprover/lean4:v4.9.0-rc1\n')
p=T/'REPL/Main.lean';s=p.read_text()
old='unsafe def main (_ : List String) : IO Unit := do\n  initSearchPath (← Lean.findSysroot)\n  repl\n'
new='unsafe def main (_ : List String) : IO Unit := do\n  initSearchPath (← Lean.findSysroot)\n  if let some nativeLibrary ← IO.getEnv "LEAN_SERVER_NATIVE_DYNLIB" then\n    Lean.loadDynlib nativeLibrary\n  repl\n'
assert s.count(old)==1
p.write_text(s.replace(old,new))
env=dict(os.environ);env['PATH']=str(SDK/'bin')+os.pathsep+env['PATH']
command=[str(SDK/'bin/lake'),'build','repl']
record=dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=command,cwd=str(T),
 source=str(S),sdk=str(SDK),scope='Private producer4.9 port of existing published GC source; dependency build, no benchmark result')
(D/'build1-command.json').write_text(json.dumps(record,indent=2)+'\n')
with (D/'build1.log').open('xb')as f:
 status=subprocess.run(command,cwd=T,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
record.update(returncode=status,whole_build_seconds=(time.monotonic_ns()-start)/1e9,
 finish_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(D/'build1-terminal.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
