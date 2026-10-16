from pathlib import Path
import shutil,subprocess,os,json
D=Path(__file__).parent;T=Path('/tmp/gpu-smt-goedel427-20261014')
U=Path('/tmp/gpu-smt-farkas-fast427-20261014');U.mkdir(exist_ok=True)
math=U/'mathlib4';pkg=U/'farkas427'
# Private full dependency copy; no lake build/update/cache hook touches any active Mathlib.
if not math.exists():shutil.copytree(T/'mathlib4',math,ignore=shutil.ignore_patterns('.git'))
if not pkg.exists():shutil.copytree(T/'farkas427',pkg,ignore=shutil.ignore_patterns('.git'))
upstream=Path('/workspaces/.agent-state/gpu-smt-deps/lean49-arithmetic/build3/upstream/lean/Farkas/Fast.lean')
(pkg/'Farkas/Fast.lean').write_bytes(upstream.read_bytes())
p=pkg/'Farkas/Instrument.lean';s=p.read_text()
s=s.replace('import Farkas.Native','import Farkas.Native\nimport Farkas.Fast',1)
s=s.replace('private def run (onlyOn : Bool)', 'private def run (nlin onlyOn : Bool)',1)
marker='  try\n    commitIfNoEx do liftMetaFinishingTactic'
assert marker in s
s=s.replace(marker,'''  if (← IO.getEnv "FARKAS_USE_FAST") == some "1" then
    if (← Farkas.Fast.tryFast nlin onlyOn args native id) then
      emit [("call",toString id),("source",Farkas.Telemetry.jstrEsc source),("route","\\"fast\\"")]
      return
    saved.restore
  try
    commitIfNoEx do liftMetaFinishingTactic''',1)
s=s.replace('run o.isSome args.toList cfg','run false o.isSome args.toList cfg',1)
pos=s.rfind('run o.isSome args.toList cfg')
assert pos>=0;s=s[:pos]+s[pos:].replace('run o.isSome args.toList cfg','run true o.isSome args.toList cfg',1)
p.write_text(s);(D/'Farkas427-Fast-Instrument.lean').write_text(s)
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+':'+env['PATH']
os.sched_setaffinity(0,{16,17,18,19})
with (D/'farkas-fast427-build.log').open('xb') as log:
 code=subprocess.call(['lake','build','Farkas.Fast','Farkas.Instrument'],cwd=pkg,env=env,stdout=log,stderr=subprocess.STDOUT)
(D/'farkas-fast427-build-result.json').write_text(json.dumps({'exit_code':code,'private_dependency_root':str(U)})+'\n')
