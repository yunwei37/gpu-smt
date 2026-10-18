"""Build cancellable large-LP speculation separately from active captures."""
from pathlib import Path
import os,resource,shutil,subprocess,json,datetime,argparse
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
BASE=Path('/tmp/gpu-smt-linarith-oracle-20261017')
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,default=BASE/'race-oracle-pooled')
parser.add_argument('--fp-first',action='store_true',help='Let CPU FP/repair complete before racing only exact-fallback LPs')
args=parser.parse_args()
U=args.out;U.mkdir(exist_ok=True);(U/'GpuArithmetic').mkdir(exist_ok=True)
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
if not args.fp_first:s=s.replace(signature,signature+'\n'+entry,1)
support=(D/'race-support.rs').read_text()
if args.fp_first:
 old='fn robust_fallback(hyps:&[Hyp],max_var:usize)->Option<Certificate>{\n cpu_or_decline(hyps,max_var)\n}'
 new='''fn robust_fallback(hyps:&[Hyp],max_var:usize)->Option<Certificate>{
 if race_eligible(hyps){
  if std::env::var_os("GPU_ARITHMETIC_RACE_CPU_ONLY").is_some(){
   produce_certificate_tiered(hyps,max_var)
  }else{race_search(hyps,max_var)}
 }else{cpu_or_decline(hyps,max_var)}
}'''
 assert old in support
 support=support.replace(old,new,1).replace('spawn_worker("--cpu",&request)','spawn_worker("--cpu-exact",&request)',1)
(core/'src/race.rs').write_text(s+'\n'+support)
(core/'src/lib.rs').write_text((snap/'src/lib.rs').read_text()+'\npub mod race;\n')
s=(D/'oracle.rs').read_text().replace('hybrid::produce_certificate_hybrid','race::produce_certificate_hint as produce_certificate_hybrid')
s=s.replace('fn solve(v:Value)->Result<Value,String>{','fn solve(v:Value)->Result<Value,String>{\n farkas_core::race::set_context(&v);')
(core/'src/bin/arithmetic-batchd.rs').write_text(s)
s=(R/'artifacts/lean-modern-native-compilation-2026-10-14/Farkas-external-support-oracled.rs').read_text().replace('hybrid::{exact_repair, produce_certificate_hybrid}','race::{exact_repair, produce_certificate_hybrid}')
s=s.replace('fn respond(line: &str) -> String {','fn respond(line: &str) -> String {\n if let Ok(v)=serde_json::from_str(line){farkas_core::race::set_context(&v);}')
(core/'src/bin/farkas-batchd.rs').write_text(s)
shutil.copyfile(D/'race-worker.rs',core/'src/bin/farkas-race-worker.rs')
# Keep the established line protocol, but borrow independent daemon handles.
# The mutex protects only the idle list; it is never held during a solve.
for src in (BASE/'batch-oracle/GpuArithmetic').iterdir():
 if src.is_file() and not src.name.startswith('Batch'):
  dst=U/'GpuArithmetic'/src.name
  if not dst.exists():dst.symlink_to(src.resolve())
for name in ['repl-candidate-timing','cuopt-grpc']:
 dst=U/name
 if not dst.exists():dst.symlink_to((BASE/'batch-oracle'/name).resolve())
for name in ['BatchNative','BatchFast','BatchBaseline','BatchOracle']:
 text=(BASE/'batch-oracle/GpuArithmetic'/(name+'.lean')).read_text()
 if name in ['BatchNative','BatchOracle']:
  native=name=='BatchNative'
  alias='DaemonProc' if native else 'Child'
  prefix='' if native else 'private abbrev Child := IO.Process.Child {stdin := .piped, stdout := .piped, stderr := .inherit}\n'
  pool=prefix+f'initialize idleDaemons : Std.Mutex (List {alias}) ← Std.Mutex.new []\n'
  pool+=f"""private def borrowDaemon : IO {alias} := do
  let cached ← idleDaemons.atomically do
    match ← get with
    | [] => pure none
    | c :: cs => set cs; pure (some c)
  if let some c := cached then return c
"""
  if native:pool+='  spawnAndHandshake\n'
  else:pool+="""
  let some bin ← IO.getEnv "GPU_ARITHMETIC_ORACLE" | throw (IO.userError "missing oracle")
  IO.Process.spawn {cmd := bin, stdin := .piped, stdout := .piped, stderr := .inherit}
"""
  query='queryDaemon' if native else 'query'
  pool+=f"""
private def {query} (request : String) : IO String := do
  let child ← borrowDaemon
  try
    child.stdin.putStr (request ++ "\\n")
    child.stdin.flush
    let answer ← child.stdout.getLine
    if answer.isEmpty then throw (IO.userError "oracle EOF")
    idleDaemons.atomically (modify (child :: ·))
    return answer
  catch e =>
    try child.kill catch _ => pure ()
    try discard child.wait catch _ => pure ()
    throw e
"""
  begin=text.index('private def '+query)
  end=text.index('\n/--',begin) if native else text.index('private def atom',begin)
  text=text[:begin]+pool+'\n'+text[end:]
 if name=='BatchNative':
  text=text.replace('    let req := requestLine hyps maxVar',"""    let base := requestLine hyps maxVar
    let callId ← IO.monoNanosNow
    let req := "{\\"source\\":" ++ Farkas.Telemetry.jstrEsc (← getFileMap).source ++ ",\\"call_id\\":" ++ toString callId ++ "," ++ (base.drop 1).toString""")
 if name=='BatchOracle':
  text=text.replace('    let answer ← query request',"""    let request := "{\\"source\\":" ++ Farkas.Telemetry.jstrEsc (← getFileMap).source ++ ",\\"call_id\\":" ++ toString exported ++ "," ++ (request.drop 1).toString
    let answer ← query request""")
 (U/'GpuArithmetic'/(name+'.lean')).write_text(text)
env=dict(os.environ);env['PATH']='/usr/local/cargo/bin:'+env['PATH']
env['CARGO_HOME']='/usr/local/cargo';env['RUSTUP_HOME']='/usr/local/rustup'
cmd=['cargo','build','--release','--offline','--bin','arithmetic-batchd','--bin','farkas-batchd','--bin','farkas-race-worker']
with (U/'build.log').open('w')as log:subprocess.run(cmd,cwd=core,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
for n in ['arithmetic-batchd','farkas-batchd','farkas-race-worker']:shutil.copy2(core/'target/release'/n,U/n)
T=Path('/tmp/gpu-smt-goedel427-20261014')
F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
env['PATH']=str(T/'lean-4.27.0-linux/bin')+':'+env['PATH']
env['LEAN_PATH']=':'.join([str(U),str(BASE),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean')for p in(T/'mathlib4/.lake/packages').iterdir()if p.is_dir()])
with (U/'build-lean.log').open('w')as log:
 for name in ['BatchNative','BatchFast','BatchBaseline','BatchOracle']:
  subprocess.run(['lean','-o',str(U/'GpuArithmetic'/(name+'.olean')),'-c',str(U/(name+'.c')),str(U/'GpuArithmetic'/(name+'.lean'))],cwd=U,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run(['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*[str(U/(n+'.c'))for n in ['BatchNative','BatchFast','BatchBaseline','BatchOracle']],'-o',str(U/'batch-oracle.so')],cwd=U,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
(U/'build-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd,'source':str(snap),'private_build':str(core),'FP_first':args.fp_first,'boundary':'original FP-first/exact-fallback dispatch'if args.fp_first else'eligible LP race before all search'},indent=2)+'\n')
print('BUILT',U)
