import json,os,subprocess,datetime
from pathlib import Path
b=Path(__file__).parent
j=json.loads((b/'commands.json').read_text())
env=dict(os.environ,LEAN_PATH=j['LEAN_PATH'],LEAN_SYSROOT='/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
env.pop('LEAN_NUM_THREADS',None)
codes=[]
with (b/'build.log').open('wb') as log:
 for cmd in j['commands']:
  p=subprocess.run(cmd,cwd=j['cwd'],env=env,stdout=log,stderr=subprocess.STDOUT);codes.append(p.returncode)
  (b/'build-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncodes':codes,'complete':len(codes)==len(j['commands'])},indent=2))
  if p.returncode:break
print(codes,flush=True)
