"""Build cancellable large-LP speculation separately from active captures."""
from pathlib import Path
import os,resource,shutil,subprocess,json,datetime
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
BASE=Path('/tmp/gpu-smt-linarith-oracle-20261017')
U=BASE/'race-oracle';U.mkdir(exist_ok=True);(U/'GpuArithmetic').mkdir(exist_ok=True)
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
snap=R/'artifacts/lean-modern-native-compilation-2026-10-14/source-snapshot-20261015/external-support'
core=U/'native'
if not core.exists():shutil.copytree(snap,core)
(core/'src/bin').mkdir(exist_ok=True)
s=(snap/'src/hybrid.rs').read_text().replace('produce_certificate_tiered(hyps, max_var)','robust_fallback(hyps, max_var)')
entry='''    if race_eligible(hyps) {
        let cert=if std::env::var_os("GPU_ARITHMETIC_RACE_CPU_ONLY").is_some(){
            crate::hybrid::produce_certificate_hybrid(hyps,max_var).0
        }else{race_search(hyps,max_var)};
        return (cert,Route::TieredDirect);
    }
'''
signature=') -> (Option<Vec<(usize, BigInt)>>, Route) {'
assert signature in s
s=s.replace(signature,signature+'\n'+entry,1)
(core/'src/race.rs').write_text(s+'\n'+(D/'race-support.rs').read_text())
(core/'src/lib.rs').write_text((snap/'src/lib.rs').read_text()+'\npub mod race;\n')
s=(D/'oracle.rs').read_text().replace('hybrid::produce_certificate_hybrid','race::produce_certificate_hint as produce_certificate_hybrid')
(core/'src/bin/arithmetic-batchd.rs').write_text(s)
s=(R/'artifacts/lean-modern-native-compilation-2026-10-14/Farkas-external-support-oracled.rs').read_text().replace('hybrid::{exact_repair, produce_certificate_hybrid}','race::{exact_repair, produce_certificate_hybrid}')
(core/'src/bin/farkas-batchd.rs').write_text(s)
shutil.copyfile(D/'race-worker.rs',core/'src/bin/farkas-race-worker.rs')
# Lean per-call modules and headers are unchanged; only numeric fallback changes.
for src in (BASE/'batch-oracle/GpuArithmetic').iterdir():
 if src.is_file():
  dst=U/'GpuArithmetic'/src.name
  if not dst.exists():dst.symlink_to(src.resolve())
for name in ['batch-oracle.so','repl-candidate-timing','cuopt-grpc']:
 dst=U/name
 if not dst.exists():dst.symlink_to((BASE/'batch-oracle'/name).resolve())
env=dict(os.environ);env['PATH']='/usr/local/cargo/bin:'+env['PATH']
env['CARGO_HOME']='/usr/local/cargo';env['RUSTUP_HOME']='/usr/local/rustup'
cmd=['cargo','build','--release','--offline','--bin','arithmetic-batchd','--bin','farkas-batchd','--bin','farkas-race-worker']
with (U/'build.log').open('w')as log:subprocess.run(cmd,cwd=core,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
for n in ['arithmetic-batchd','farkas-batchd','farkas-race-worker']:shutil.copy2(core/'target/release'/n,U/n)
(U/'build-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd,'source':str(snap),'private_build':str(core)},indent=2)+'\n')
print('BUILT',U)
