from pathlib import Path
import subprocess,json,time,datetime,resource,shutil
r=Path('/workspaces/repository');p=Path('/tmp/gpu-smt-native-ref-branches-20261016');sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux')
base=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-batch-integration'
e=base.parent/'native-local-access';v1=p/'batch-frozen-v1';v2=p/'owner-cache-v2';v3=p/'local-access-v3';private=v3/'private'
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
private.mkdir(parents=True,exist_ok=False)
shutil.copyfile(r/'bench/lean-native/native-ref-branches.cpp',v3/'native-ref-branches.executed.cpp')
def run(tag,cmd):
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic_ns();before=resource.getrusage(resource.RUSAGE_CHILDREN)
 with (e/(tag+'.stdout')).open('w') as out,(e/(tag+'.stderr')).open('w') as err:z=subprocess.run(cmd,cwd=p,stdout=out,stderr=err)
 after=resource.getrusage(resource.RUSAGE_CHILDREN)
 data={'utc':utc,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':str(p),'exit_code':z.returncode,'wall_ns':time.monotonic_ns()-t,'compiler_cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'overlap':'finite development compile/link during active frozen-v1 capture; preserve this competing CPU load with interpretation; no frozen v1/v2 artifact changed'}
 (e/(tag+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 print(tag,z.returncode,(e/(tag+'.stderr')).read_text()[-1800:] if z.returncode else '',flush=True)
 if z.returncode:raise SystemExit(z.returncode)
cmd=json.loads((base/'helper-link.json').read_text())['command']
cmd=[s.replace(str(v1/'private'),str(private)).replace(str(r/'bench/lean-native/native-ref-branches.cpp'),str(v3/'native-ref-branches.executed.cpp')) for s in cmd]
run('helper-link',cmd)
cmd=json.loads((base/'private-shared-link.json').read_text())['command']
cmd=[s.replace(str(v1/'private'),str(private)).replace(str(p/'runtime-shared/compact.cpp.o'),str(v2/'compact.cpp.shared.o')) for s in cmd]
run('private-shared-link',cmd)
cmd=json.loads((base/'private-repl-link.json').read_text())['command']
cmd=[s.replace(str(v1/'private'),str(private)).replace(str(p/'libleanrt.a'),str(v2/'libleanrt.a')) for s in cmd]
run('private-repl-link',cmd)
assert (v3/'native-ref-branches.executed.cpp').read_bytes()==(r/'bench/lean-native/native-ref-branches.cpp').read_bytes()
(e/'candidate-paths.json').write_text(json.dumps({'candidate':str(private/'repl'),'candidate_library_path':str(private),'stock_and_fallback':str(v1/'plain/repl'),'stock_library_path':str(v1/'plain'),'root':str(v3),'source_cpp':str(v3/'native-ref-branches.executed.cpp'),'static_runtime_archive':str(v2/'libleanrt.a'),'shared_compact_object':str(v2/'compact.cpp.shared.o'),'status':'built separate prospective candidate; active full matrix remains frozen v1; no performance comparison'},indent=2)+'\n')
print('BUILD_COMPLETE',str(v3),flush=True)
