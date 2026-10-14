from pathlib import Path
import json,subprocess,datetime
b=Path(__file__).resolve().parent
commands=json.loads((b/'build-command.json').read_text())['commands']
codes=[]
with (b/'build.log').open('x')as log:
 for cmd in commands:
  codes.append(subprocess.run(cmd,cwd='/workspaces/repository',stdout=log,stderr=subprocess.STDOUT).returncode)
  if codes[-1]:break
(b/'build-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':commands,'returncodes':codes,'build_complete':codes==[0,0]},indent=2)+'\n')
raise SystemExit(codes[-1])
