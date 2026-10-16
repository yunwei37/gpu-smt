from pathlib import Path
import subprocess,os,json
D=Path(__file__).parent;T=Path('/tmp/gpu-smt-goedel427-20261014')
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+':'+env['PATH']
os.sched_setaffinity(0,{4,5,6,7})
with (D/'repl-kimina-gc-dynamic-profile-header-repair-build.log').open('xb') as log:
 code=subprocess.call(['lake','build','repl'],cwd=T/'repl-kimina-gc-dynamic-profile-header-repair',env=env,stdout=log,stderr=subprocess.STDOUT)
(D/'profile-header-repair-build-result.json').write_text(json.dumps({'exit_code':code})+'\n')
