from pathlib import Path
import subprocess,json,shutil,time,datetime,resource
r=Path('/workspaces/repository');p=Path('/tmp/gpu-smt-native-ref-branches-20261016');src=p/'lean4-4.27.0/src'
sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux')
base=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-batch-integration'
e=base.parent/'native-owner-fastpath';v1=p/'batch-frozen-v1';v2=p/'owner-cache-v2';private=v2/'private'
private.mkdir(parents=True,exist_ok=False)
def run(tag,cmd):
 t=time.monotonic_ns();before=resource.getrusage(resource.RUSAGE_CHILDREN);utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (e/(tag+'.stdout')).open('w') as out,(e/(tag+'.stderr')).open('w') as err:z=subprocess.run(cmd,cwd=p,stdout=out,stderr=err)
 after=resource.getrusage(resource.RUSAGE_CHILDREN)
 data={'utc':utc,'command':cmd,'cwd':str(p),'exit_code':z.returncode,'wall_ns':time.monotonic_ns()-t,'compiler_cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'overlap':'finite development compiler work during frozen-v1 rep1-stock; no v1 executable or DSO mutated'}
 (e/(tag+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 print(tag,z.returncode,(e/(tag+'.stderr')).read_text()[-1800:] if z.returncode else '',flush=True)
 if z.returncode:raise SystemExit(z.returncode)
helper=json.loads((base/'helper-link.json').read_text())['command']
helper=[s.replace(str(v1/'private'),str(private)) for s in helper]
common=helper[:helper.index('-shared')]
run('helper-link',helper)
run('compact-static',common+['-c',str(src/'runtime/compact.cpp'),'-o',str(v2/'compact.cpp.o')])
run('compact-shared',common+['-c',str(src/'runtime/compact.cpp'),'-o',str(v2/'compact.cpp.shared.o')])
shutil.copyfile(p/'libleanrt.a',v2/'libleanrt.a')
run('runtime-archive',[str(sdk/'bin/llvm-ar'),'rcs',str(v2/'libleanrt.a'),str(v2/'compact.cpp.o')])
cmd=json.loads((base/'private-shared-link.json').read_text())['command']
cmd=[s.replace(str(v1/'private'),str(private)).replace(str(p/'runtime-shared/compact.cpp.o'),str(v2/'compact.cpp.shared.o')) for s in cmd]
run('private-shared-link',cmd)
cmd=json.loads((base/'private-repl-link.json').read_text())['command']
cmd=[s.replace(str(v1/'private'),str(private)).replace(str(p/'libleanrt.a'),str(v2/'libleanrt.a')) for s in cmd]
run('private-repl-link',cmd)
shutil.copyfile(r/'bench/lean-native/native-ref-branches.cpp',v2/'native-ref-branches.executed.cpp')
shutil.copyfile(src/'runtime/compact.cpp',v2/'compact.executed.cpp')
(e/'candidate-paths.json').write_text(json.dumps({'candidate':str(private/'repl'),'candidate_library_path':str(private),'stock_and_fallback':str(v1/'plain/repl'),'stock_library_path':str(v1/'plain'),'root':str(v2),'source_cpp':str(v2/'native-ref-branches.executed.cpp'),'source_compact':str(v2/'compact.executed.cpp'),'status':'built separate prospective candidate; active full matrix remains frozen v1; no performance comparison'},indent=2)+'\n')
print('BUILD_COMPLETE',str(v2),flush=True)
