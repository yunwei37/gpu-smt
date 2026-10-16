from pathlib import Path
import subprocess,json,os,time,datetime
r=Path('/workspaces/repository');e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038'
p=Path('/tmp/gpu-smt-native-ref-branches-20261016');b=Path('/tmp/gpu-smt-goedel427-20261014');sdk=b/'lean-4.27.0-linux';a=r/'artifacts/lean-modern-native-compilation-2026-10-14'
target=e/'setup3-original';target.mkdir(exist_ok=False)
env=dict(os.environ);env['PATH']=str(sdk/'bin')+os.pathsep+env['PATH'];env['LEAN_SYSROOT']=str(sdk)
env['LEAN_PATH']=json.loads((e/'setup-environment.json').read_text())['LEAN_PATH']
c=json.loads((a/'native-library.json').read_text());env['LEAN_SERVER_NATIVE_DYNLIB']=c['load_manifest'];env['LD_LIBRARY_PATH']=os.pathsep.join(c['library_paths']+[str(sdk/'lib'),str(sdk/'lib/lean')])
tick=time.monotonic()
with (target/'stdout').open('w') as out,(target/'stderr').open('w') as err:z=subprocess.run([str(b/'repl-producer-native/.lake/build/bin/repl')],cwd=b/'mathlib4',env=env,input=(e/'setup-transport.txt').read_text(),text=True,stdout=out,stderr=err,timeout=300)
(target/'terminal.json').write_text(json.dumps({'command':[str(b/'repl-producer-native/.lake/build/bin/repl')],'cwd':str(b/'mathlib4'),'exit_code':z.returncode,'seconds':time.monotonic()-tick,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'claim':'one original setup response; not a throughput result'},indent=2)+'\n')
print(z.returncode,(target/'stdout').read_text()[-3000:],(target/'stderr').read_text()[-1500:])
