"""Build robust support-search prototype without touching active original modules."""
from pathlib import Path
import os,shutil,subprocess,json,resource
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
BASE=Path('/tmp/gpu-smt-linarith-oracle-20261017');U=BASE/'batch-oracle'
T=Path('/tmp/gpu-smt-goedel427-20261014');F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.sched_setaffinity(0,{0,1,2,3});U.mkdir(exist_ok=True);(U/'GpuArithmetic').mkdir(exist_ok=True)
for src in (BASE/'GpuArithmetic').iterdir():
 if src.is_file() and not src.name.startswith('Batch'):
  dst=U/'GpuArithmetic'/src.name
  if not dst.exists():dst.symlink_to(src.resolve())
core=BASE/'native';snap=R/'artifacts/lean-modern-native-compilation-2026-10-14/source-snapshot-20261015/external-support'
s=(snap/'src/hybrid.rs').read_text()
s=s.replace('produce_certificate_tiered(hyps, max_var)','robust_fallback(hyps, max_var)')
(core/'src/batch.rs').write_text(s+'\n'+(D/'batch-support.rs').read_text())
s=(core/'src/lib.rs').read_text()
if 'pub mod batch;' not in s:(core/'src/lib.rs').write_text(s+'\npub mod batch;\n')
s=(D/'oracle.rs').read_text().replace('hybrid::produce_certificate_hybrid','batch::produce_certificate_hint as produce_certificate_hybrid')
(core/'src/bin/arithmetic-batchd.rs').write_text(s)
s=(core/'src/bin/farkas-oracled.rs').read_text().replace('hybrid::{exact_repair, produce_certificate_hybrid}','batch::{exact_repair, produce_certificate_hybrid}')
(core/'src/bin/farkas-batchd.rs').write_text(s)
# Per-call processes remove the original serial daemon lock. Their startup/wait is charged.

native=(F/'Farkas/Native.lean').read_text().replace('namespace Farkas','namespace GpuArithmetic.BatchNative').replace('end Farkas','end GpuArithmetic.BatchNative')
native=native.replace('findBinary','Farkas.findBinary').replace('Telemetry.','Farkas.Telemetry.')
a=native.index('private def queryDaemon');b=native.index('\n/--',a)
native=native[:a]+'''private def queryDaemon (req : String) : IO String := do
  let some bin ← Farkas.findBinary | throw (IO.userError "missing native support binary")
  let out ← IO.Process.output {cmd := bin} (some (req ++ "\\n"))
  if out.exitCode != 0 then throw (IO.userError out.stderr)
  return out.stdout
'''+native[b:]
(U/'GpuArithmetic/BatchNative.lean').write_text(native)
s=(F/'Farkas/Fast.lean').read_text().replace('import Farkas.Native','import GpuArithmetic.BatchNative').replace('Farkas.Fast','GpuArithmetic.BatchFast').replace('Farkas.native','GpuArithmetic.BatchNative.native')
s=s.replace('open Lean Meta Elab Tactic','open Farkas\nopen Lean Meta Elab Tactic')
(U/'GpuArithmetic/BatchFast.lean').write_text(s)
s=(D/'Baseline.lean').read_text().replace('import Farkas.Fast','import GpuArithmetic.BatchFast').replace('GpuArithmetic.Baseline','GpuArithmetic.BatchBaseline').replace('Farkas.Fast','GpuArithmetic.BatchFast').replace('Farkas.native','GpuArithmetic.BatchNative.native')
s=s.replace('IO.getEnv "GPU_ARITHMETIC_BASELINE"','IO.getEnv "GPU_ARITHMETIC_BATCH"')
(U/'GpuArithmetic/BatchBaseline.lean').write_text(s)

# Direct and native fallback queries both wait through each child process exit.
s=(D/'Oracle.lean').read_text().replace('namespace GpuArithmetic.Oracle','namespace GpuArithmetic.BatchOracle').replace('end GpuArithmetic.Oracle','end GpuArithmetic.BatchOracle')
a=s.index('private abbrev Child');b=s.index('private def atom',a)
s=s[:a]+'''private def query (request : String) : IO String := do
  let some bin ← IO.getEnv "GPU_ARITHMETIC_ORACLE" | throw (IO.userError "missing oracle")
  let out ← IO.Process.output {cmd := bin} (some (request ++ "\\n"))
  if out.exitCode != 0 then throw (IO.userError out.stderr)
  let answer := out.stdout
  if answer.isEmpty then throw (IO.userError "oracle EOF")
  return answer

'''+s[b:]
s=s.replace('import Farkas.Native','import GpuArithmetic.BatchBaseline')
s=s.replace('if (← IO.getEnv "GPU_ARITHMETIC_ORACLE").isNone','if (← IO.getEnv "GPU_ARITHMETIC_BATCH").isNone')
(U/'GpuArithmetic/BatchOracle.lean').write_text(s)
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+':/usr/local/cargo/bin:'+env['PATH'];env['CARGO_HOME']='/usr/local/cargo';env['RUSTUP_HOME']='/usr/local/rustup'
env['LEAN_PATH']=':'.join([str(U),str(BASE),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean')for p in(T/'mathlib4/.lake/packages').iterdir()if p.is_dir()])
with (U/'build.log').open('w')as log:
 def run(cmd,cwd=U):print(cmd,flush=True);subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 run(['cargo','build','--release','--offline','--bin','arithmetic-batchd','--bin','farkas-batchd'],core)
 for n in ['arithmetic-batchd','farkas-batchd']:shutil.copy2(core/'target/release'/n,U/n)
 for name in ['BatchNative','BatchFast','BatchBaseline','BatchOracle']:
  run(['lean','-o',str(U/'GpuArithmetic'/(name+'.olean')),'-c',str(U/(name+'.c')),str(U/'GpuArithmetic'/(name+'.lean'))])
 run(['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*[str(U/(n+'.c'))for n in ['BatchNative','BatchFast','BatchBaseline','BatchOracle']],'-o',str(U/'batch-oracle.so')])
print('BUILT',U,flush=True)
