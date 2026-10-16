from pathlib import Path
import subprocess,os,json
D=Path(__file__).parent;T=Path('/tmp/gpu-smt-goedel427-20261014')
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+':'+env['PATH']
os.sched_setaffinity(0,{4,5,6,7})
results=[]
for name in ['repl-kimina-gc-header-repair','repl-kimina-native-gc-header-repair']:
 with (D/(name+'-build.log')).open('xb') as log:
  code=subprocess.call(['lake','build','repl'],cwd=T/name,env=env,stdout=log,stderr=subprocess.STDOUT)
 results.append({'name':name,'exit_code':code})
 if code:break
(D/'header-repair-build-results.json').write_text(json.dumps(results,indent=2)+'\n')
