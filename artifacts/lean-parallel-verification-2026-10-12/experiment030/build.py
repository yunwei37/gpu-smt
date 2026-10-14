import pathlib,subprocess,os,json,datetime
R=pathlib.Path('/workspaces/repository');D=pathlib.Path(__file__).parent
SDK=pathlib.Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux');WORK=SDK.parent/'mathlib4'
env=dict(os.environ);env['LEAN_PATH']=json.loads((R/'artifacts/lean-native-boundary-2026-10-11/experiment012/preflight2/branch-minif2f-first32/receipt.json').read_text())['environment']['LEAN_PATH']
tmp=pathlib.Path('/tmp/gpu-smt-experiment030-build');tmp.mkdir(exist_ok=True)
commands=[];codes=[]
with (D/'build/build.log').open('w') as log:
 for name in ['candidate','profile-candidate','profile-warm']:
  b=D/'build'/name
  parent=R/'artifacts/lean-service-lifecycle-2026-10-13/build1/parent.o'
  if name=='profile-candidate':
   cmd=['gcc','-std=gnu11','-O3','-Wall','-Wextra','-I'+str(SDK/'include'),'-c',str(D/'build/profile-parent.c'),'-o',str(D/'build/profile-parent.o')]
   commands.append(cmd);rc=subprocess.run(cmd,cwd=WORK,env=env,stdout=log,stderr=log).returncode;codes.append(rc)
   if rc:break
  if name.startswith('profile'):parent=D/'build/profile-parent.o'
  seq=[
   [str(SDK/'bin/lake'),'env','lean','-R',str(b),'-c',str(b/'Lean49PreparedBranches.c'),str(b/'Lean49PreparedBranches.lean')],
   [str(SDK/'bin/leanc'),'-O3','-c',str(b/'Lean49PreparedBranches.c'),'-o',str(b/'Lean49PreparedBranches.o')],
   [str(SDK/'bin/leanc'),'-O3','-rdynamic','-o',str(tmp/name),str(parent),str(b/'Lean49PreparedBranches.o'),
    '/workspaces/.agent-state/gpu-smt-deps/lean49-owned-runtime/build4/owned-object.o',
    '/workspaces/.agent-state/gpu-smt-deps/lean49-owned-runtime/build4/owned-thread.o',
    str(WORK/'.lake/packages/REPL/.lake/build/lib/libREPL.a')]]
  for cmd in seq:
   commands.append(cmd);rc=subprocess.run(cmd,cwd=WORK,env=env,stdout=log,stderr=log).returncode;codes.append(rc);log.flush()
   if rc:break
  if rc:break
(D/'build/build-terminal.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':commands,'codes':codes,'binary_directory':str(tmp),'binary_durability':'temporary regenerable build in owning Workspace; sources and complete commands retained'},indent=2)+'\n')
