from pathlib import Path
import subprocess,json,os,shutil,time,datetime,shlex
r=Path('/workspaces/repository');p=Path('/tmp/gpu-smt-native-ref-branches-20261016')
sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux')
q=Path('/tmp/gpu-smt-goedel427-20261014/repl-producer-native')
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038'
shutil.copyfile(sdk/'lib/lean/libleanrt.a',p/'libleanrt.a')
env=dict(os.environ);env['LEAN_PATH']=str(q/'.lake/build/lib/lean')
def run(tag,cmd):
 start=time.monotonic()
 with (e/(tag+'.stdout')).open('w') as out,(e/(tag+'.stderr')).open('w') as err:z=subprocess.run(cmd,cwd=p,env=env,stdout=out,stderr=err)
 (e/(tag+'.json')).write_text(json.dumps({'command':cmd,'cwd':str(p),'exit_code':z.returncode,'seconds':time.monotonic()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
 print(tag,z.returncode,(e/(tag+'.stderr')).read_text()[-2500:],flush=True)
 if z.returncode:raise SystemExit(z.returncode)
run('runtime-archive',[str(sdk/'bin/llvm-ar'),'rcs',str(p/'libleanrt.a'),str(p/'io.cpp.o'),str(p/'object.cpp.o')])
shutil.copyfile(r/'bench/lean-native/NativeBranchSetup.lean',p/'NativeBranchSetup.lean')
run('setup-lean-compile',[str(sdk/'bin/lean'),'-o',str(p/'NativeBranchSetup.olean'),'-c',str(p/'NativeBranchSetup.c'),str(p/'NativeBranchSetup.lean')])
run('setup-c-compile',[str(sdk/'bin/leanc'),'-c','-O3',str(p/'NativeBranchSetup.c'),'-o',str(p/'NativeBranchSetup.o')])
text=(q/'.lake/build/ir/REPL/Main.c').read_text()
assert text.count('res = initialize_REPL_REPL_Main(1 /* builtin */);')==1
assert text.count('res = _lean_main(in);')==1
text=text.replace('char ** lean_setup_args(int argc, char ** argv);','extern lean_object* initialize_NativeBranchSetup(uint8_t builtin);\nextern lean_object* gpu_smt_native_setup(lean_object*);\nchar ** lean_setup_args(int argc, char ** argv);')
text=text.replace('res = initialize_REPL_REPL_Main(1 /* builtin */);','res = initialize_NativeBranchSetup(1 /* builtin */);').replace('res = _lean_main(in);','res = gpu_smt_native_setup(in);')
(p/'Main.setup.c').write_text(text)
run('setup-entry-compile',[str(sdk/'bin/leanc'),'-c','-O3',str(p/'Main.setup.c'),'-o',str(p/'Main.setup.o')])
trace=json.loads((q/'.lake/build/bin/repl.trace').read_text())
cmd=shlex.split(trace['log'][0]['message'][3:])
cmd[cmd.index('-o')+1]=str(p/'native-branch-setup')
old=str(q/'.lake/build/ir/REPL/Main.c.o.export');cmd[cmd.index(old)]=str(p/'Main.setup.o')
cmd.insert(cmd.index('-rdynamic'),str(p/'NativeBranchSetup.o'))
cmd.insert(cmd.index('-L'),'-Wl,-rpath,'+str(p))
cmd.insert(cmd.index('-L'),'-L'+str(p))
cmd[cmd.index('-lleanrt')]=str(p/'libleanrt.a')
# Candidate runtime uses the owning Workspace glibc headers/library consistently.
# Preserve this build difference; no matched performance claim at setup stage.
first=cmd.index('--sysroot');last=cmd.index('-fuse-ld=lld')
cmd[first:last]=['-L'+str(sdk/'lib')]
cmd.insert(cmd.index('-lc++abi')+1,'-lunwind')
cmd.extend(['-L'+str(p),'-lgpu_smt_ref_branches','-Wl,-rpath,'+str(sdk/'lib')])
run('setup-executable-link',cmd)
