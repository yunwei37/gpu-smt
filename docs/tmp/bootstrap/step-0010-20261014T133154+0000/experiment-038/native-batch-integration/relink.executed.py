from pathlib import Path
import subprocess,json,os,shutil,time,datetime,shlex
r=Path('/workspaces/repository');p=Path('/tmp/gpu-smt-native-ref-branches-20261016')
sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux');src=p/'lean4-4.27.0/src'
q=sdk.parent/'repl-kimina-native-gc-header-repair'
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-batch-integration'
d=p/'batch-frozen-v1';plain=d/'plain';private=d/'private'
plain.mkdir(parents=True,exist_ok=True);private.mkdir(exist_ok=True)
env=dict(os.environ);env['LEAN_PATH']=str(q/'.lake/build/lib/lean')
def run(tag,cmd):
 start=time.monotonic()
 with (e/(tag+'.stdout')).open('w') as out,(e/(tag+'.stderr')).open('w') as err:z=subprocess.run(cmd,cwd=p,env=env,stdout=out,stderr=err)
 (e/(tag+'.json')).write_text(json.dumps({'command':cmd,'cwd':str(p),'exit_code':z.returncode,'seconds':time.monotonic()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
 print(tag,z.returncode,(e/(tag+'.stderr')).read_text()[-2200:] if z.returncode else '',flush=True)
 if z.returncode:raise SystemExit(z.returncode)
text=(q/'.lake/build/ir/REPL/Main.c').read_text()
assert text.count('res = initialize_REPL_REPL_Main(1 /* builtin */);')==1
assert text.count('res = _lean_main(in);')==1
text=text.replace('char ** lean_setup_args(int argc, char ** argv);','extern lean_object* initialize_batch_x2dfrozen_x2dv1_NativeBranchBackend(uint8_t builtin);\nextern lean_object* gpu_smt_native_backend(lean_object*);\nchar ** lean_setup_args(int argc, char ** argv);')
text=text.replace('res = initialize_REPL_REPL_Main(1 /* builtin */);','res = initialize_batch_x2dfrozen_x2dv1_NativeBranchBackend(1 /* builtin */);').replace('res = _lean_main(in);','res = gpu_smt_native_backend(in);')
(d/'Main.setup.c').write_text(text)
run('backend-entry-compile',[str(sdk/'bin/leanc'),'-c','-O3',str(d/'Main.setup.c'),'-o',str(d/'Main.setup.o')])
trace=json.loads((q/'.lake/build/bin/repl.trace').read_text())
for target,is_private in [(private,True),(plain,False)]:
 cmd=shlex.split(trace['log'][0]['message'][3:]);cmd[cmd.index('-o')+1]=str(target/'repl')
 if is_private:
  old=str(q/'.lake/build/ir/REPL/Main.c.o.export');cmd[cmd.index(old)]=str(d/'Main.setup.o')
  cmd.insert(cmd.index('-rdynamic'),str(d/'NativeBranchBackend.o'))
  cmd[cmd.index('-lleanrt')]=str(p/'libleanrt.a')
  cmd.insert(cmd.index('-L'),'-L'+str(private))
 else:cmd[cmd.index('-lleanrt')]=str(p/'plain-runtime/libleanrt.a')
 first=cmd.index('--sysroot');last=cmd.index('-fuse-ld=lld');cmd[first:last]=['-L'+str(sdk/'lib')]
 cmd.insert(cmd.index('-lc++abi')+1,'-lunwind')
 cmd+=['-Wl,-rpath,'+str(target),'-Wl,-rpath,'+str(sdk/'lib')]
 if is_private:cmd+=['-L'+str(private),'-lgpu_smt_ref_branches']
 run(target.name+'-repl-link',cmd)
 for f in ['libleanshared.so','repl']:(e/(target.name+'-'+f+'-bytes.json')).write_text(json.dumps({'path':str(target/f),'bytes':(target/f).stat().st_size})+'\n')
(e/'frozen-paths.json').write_text(json.dumps({'root':str(d),'stock':str(plain/'repl'),'candidate':str(private/'repl'),'stock_library_path':str(plain),'candidate_library_path':str(private),'same_qgc_source':str(q),'sdk':str(sdk),'note':'immutable v1 during capture; original producer and prior runtime not replaced'},indent=2)+'\n')
print('FROZEN',d,flush=True)
