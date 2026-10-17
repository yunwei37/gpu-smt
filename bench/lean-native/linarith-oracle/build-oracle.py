"""Build the direct-certificate prototype and established native arithmetic comparator.
Requires build-stages.py and the retained pinned dependencies; Workspace only.
"""
from pathlib import Path
import os, shutil, subprocess, json, datetime
R=Path('/workspaces/repository')
D=R/'bench/lean-native/linarith-oracle'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017')
B=Path('/tmp/gpu-smt-goedel427-20261014')
F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
sdk=B/'lean-4.27.0-linux'
env=dict(os.environ)
env['PATH']=str(sdk/'bin')+':/usr/local/cargo/bin:'+env['PATH']
env['CARGO_HOME']='/usr/local/cargo';env['RUSTUP_HOME']='/usr/local/rustup'
env['LEAN_PATH']=':'.join([str(U),str(F/'.lake/build/lib/lean'),str(B/'mathlib4/.lake/build/lib/lean')]+[
 str(p/'.lake/build/lib/lean') for p in (B/'mathlib4/.lake/packages').iterdir() if p.is_dir()])
records=[]
with (U/'build-oracle.log').open('w') as log:
 def run(cmd,cwd=U):
  log.write(repr(cmd)+'\n');log.flush()
  subprocess.run(cmd,cwd=cwd,env=env,check=True,stdout=log,stderr=subprocess.STDOUT)
  records.append({'command':cmd,'cwd':str(cwd)})
 (U/'Farkas427').mkdir(exist_ok=True)
 shutil.copyfile(R/'artifacts/lean-modern-native-compilation-2026-10-14/Farkas427-Products.lean',U/'Farkas427/Products.lean')
 for module,src in [('GpuArithmetic/Oracle',D/'Oracle.lean'),('GpuArithmetic/Baseline',D/'Baseline.lean')]:
  shutil.copyfile(src,U/(module+'.lean'))
 for module in ['Farkas427/Products','GpuArithmetic/Baseline','GpuArithmetic/Oracle']:
  run(['lean','-o',str(U/(module+'.olean')),'-c',str(U/(Path(module).name+'.c')),str(U/(module+'.lean'))])
 cs=[str(U/p) for p in ['Stages.c','clock.o','Products.c','Baseline.c','Oracle.c']]
 cs += [str(F/'.lake/build/ir/Farkas'/(m+'.c')) for m in ['Platform','Telemetry','Native','Fast']]
 run(['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*cs,'-o',str(U/'comparison-strong-fallback.so')])
 core=U/'native'
 if not core.exists():
  shutil.copytree(R/'artifacts/lean-modern-native-compilation-2026-10-14/source-snapshot-20261015/external-support',core)
 (core/'src/bin').mkdir(exist_ok=True)
 shutil.copyfile(D/'oracle.rs',core/'src/bin/arithmetic-oracled.rs')
 run(['cargo','build','--release','--offline','--bin','arithmetic-oracled'],core)
 shutil.copy2(core/'target/release/arithmetic-oracled',U/'arithmetic-oracled-product-sign-fixed')
(U/'build-oracle-receipt.json').write_text(json.dumps({
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':records,
 'native_export':'LEAN_EXPORTING; retain default visibility for compiled Lean entry points',
 'status':'built; real native preflight still required'},indent=2)+'\n')
