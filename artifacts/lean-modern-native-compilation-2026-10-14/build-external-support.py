from pathlib import Path
import os,subprocess,json
D=Path(__file__).parent
env=dict(os.environ);env['RUSTUP_HOME']='/usr/local/rustup';env['CARGO_HOME']='/usr/local/cargo'
env['PATH']='/usr/local/cargo/bin:'+env['PATH']
os.sched_setaffinity(0,{4,5,6,7})
with (D/'external-support-build.log').open('xb') as log:
 code=subprocess.call(['cargo','+1.98.1','build','--release','--bin','farkas-oracled'],cwd='/tmp/gpu-smt-farkas-external-support-20261014',env=env,stdout=log,stderr=subprocess.STDOUT)
(D/'external-support-build-result.json').write_text(json.dumps({'exit_code':code})+'\n')
