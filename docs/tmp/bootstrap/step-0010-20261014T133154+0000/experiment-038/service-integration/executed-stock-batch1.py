from pathlib import Path
import subprocess,json,os,time,threading
r=Path('/workspaces/repository');a=r/'artifacts/lean-modern-native-compilation-2026-10-14';e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/service-integration'
p=Path('/tmp/gpu-smt-native-ref-branches-20261016');b=Path('/tmp/gpu-smt-goedel427-20261014');sdk=b/'lean-4.27.0-linux'
config=json.loads((a/'native-library.json').read_text());d=e/'stock-native-batch1';d.mkdir(exist_ok=False)
env=dict(os.environ);env['PATH']=str(sdk/'bin')+os.pathsep+env['PATH'];env['LEAN_SYSROOT']=str(sdk)
env['LEAN_PATH']=subprocess.check_output([str(sdk/'bin/lake'),'env','printenv','LEAN_PATH'],cwd=b/'mathlib4',env=env,text=True).strip()
env['LEAN_SERVER_NATIVE_DYNLIB']=config['load_manifest'];env['LD_LIBRARY_PATH']=os.pathsep.join([str(p/'plain-runtime'),str(sdk/'lib'),str(sdk/'lib/lean')]+config['library_paths'])
header='import Mathlib\nimport Aesop\n'
with (a/'input.jsonl').open() as f:items=[json.loads(next(f)) for _ in range(4)]
payload=json.dumps({'cmd':header})+'\n\n'+json.dumps({'env':0,'cmds':['\n\n'+x['code'][len(header):] for x in items],'mode':'naive'})+'\n\n'
(d/'transport.txt').write_text(payload);(d/'input.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in items))
t=time.monotonic_ns()
with (d/'stdout').open('w') as out,(d/'stderr').open('w') as err:
 z=subprocess.run([str(p/'plain-runtime/repl-kimina-gc')],cwd=b/'mathlib4',env=env,input=payload,text=True,stdout=out,stderr=err,timeout=300)
terminal={'exit_code':z.returncode,'whole_seconds':(time.monotonic_ns()-t)/1e9,'command':[str(p/'plain-runtime/repl-kimina-gc')],'cwd':str(b/'mathlib4'),'explicit_env':{k:env[k] for k in ['LEAN_SYSROOT','LEAN_PATH','LD_LIBRARY_PATH','LEAN_SERVER_NATIVE_DYNLIB']},'boundary':'one actual existing native BatchCommand mode naive; four unchanged original sources; complete prep/batch/EOF; setup observation, not full cohort or per-input emission latency'}
(d/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
frames=[json.loads(x) for x in (d/'stdout').read_text().split('\n\n') if x.strip()]
(d/'parsed-frames.json').write_text(json.dumps(frames,indent=2)+'\n')
print(json.dumps(terminal), 'frames',len(frames),'batch_rows',len(frames[-1]) if isinstance(frames[-1],list) else frames[-1])
