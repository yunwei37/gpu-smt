from pathlib import Path
import os,subprocess,json,datetime
D=Path(__file__).parent
U=Path('/tmp/gpu-smt-lazy-products427-20261015/farkas427')
N=Path('/tmp/gpu-smt-stock-products427-20261015')
T=Path('/tmp/gpu-smt-goedel427-20261014')
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+os.pathsep+env['PATH']
commands=[]
cmd=['lake','build','+Farkas.ProductsOnly:dynlib']
commands.append({'cwd':str(U),'argv':cmd})
with (D/'stock-products-module-build.log').open('w') as log:
 r=subprocess.run(cmd,cwd=U,env=env,stdout=log,stderr=subprocess.STDOUT)
if r.returncode:raise SystemExit(r.returncode)
paths=[str(U/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(x/'.lake/build/lib/lean') for x in (T/'mathlib4/.lake/packages').iterdir() if x.is_dir()]
env['LEAN_PATH']=os.pathsep.join(paths+([env['LEAN_PATH']] if env.get('LEAN_PATH') else []))
cmd=['lake','build','repl'];commands.append({'cwd':str(N/'repl'),'argv':cmd,'LEAN_PATH':env['LEAN_PATH']})
with (D/'stock-products-repl-build.log').open('w') as log:
 r=subprocess.run(cmd,cwd=N/'repl',env=env,stdout=log,stderr=subprocess.STDOUT)
(D/'stock-products-build-result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':commands,'returncode':r.returncode},indent=2)+'\n')
raise SystemExit(r.returncode)
