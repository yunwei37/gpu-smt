"""Complete all-call oracle cost attribution; separate diagnostic binaries/modules.
The original primary binaries and active Lean 4.9 prefix process are untouched.
"""
from pathlib import Path
import os,shutil,subprocess,json,datetime,argparse
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
BASE=Path('/tmp/gpu-smt-linarith-oracle-20261017')
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,default=BASE)
U=parser.parse_args().out;U.mkdir(parents=True,exist_ok=True);(U/'GpuArithmetic').mkdir(exist_ok=True)
# Lean resolves a namespace in its first package root; reuse base module files.
for src in (BASE/'GpuArithmetic').iterdir():
 if src.is_file() and not src.name.startswith('Cost'):
  dst=U/'GpuArithmetic'/src.name
  if not dst.exists():dst.symlink_to(src.resolve())
T=Path('/tmp/gpu-smt-goedel427-20261014')
F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
core=BASE/'native'; snap=R/'artifacts/lean-modern-native-compilation-2026-10-14/source-snapshot-20261015/external-support'
# Reuse the existing build tree, generate from retained immutable original inputs.
for name in ['lib.rs','hybrid.rs']:
 s=(snap/'src'/name).read_text()
 if name=='lib.rs':s+='\npub mod cost;\n'
 else:
  for old,new in [
   ('build_fp_lp(hyps) else','crate::cost::timed("lp_build", || build_fp_lp(hyps)) else'),
   ('match solve_fp(&lp) {','match crate::cost::timed("fp_solve", || solve_fp(&lp)) {'),
   ('exact_repair(hyps, &sup)','crate::cost::timed("exact_repair", || exact_repair(hyps, &sup))'),
   ('verify_cert(hyps, &cert)','crate::cost::timed("exact_verify", || verify_cert(hyps, &cert))'),
   ('produce_certificate_tiered(hyps, max_var)','crate::cost::timed("exact_lp", || produce_certificate_tiered(hyps, max_var))')]:
   assert old in s,old;s=s.replace(old,new)
  s=s.replace('    Some(FpLp {','    crate::cost::shape(nrows,n,a.iter().filter(|v| **v != 0.0).count(),"fp-scaled");\n    Some(FpLp {',1)
 (core/'src'/name).write_text(s)
shutil.copyfile(D/'cost.rs',core/'src/cost.rs')
# Direct AST oracle: intervals emitted even for cert:null, parse failure or panic.
s=(D/'oracle.rs').read_text()
s=s.replace('fn main(){','fn main(){\n if farkas_core::cost::supervise("direct"){return;}')
s=s.replace(' for line in stdin.lock().lines(){',' let mut lines=stdin.lock().lines();\n loop {let Some(line)=farkas_core::cost::read_line(&mut lines) else{break};')
s=' }\n farkas_core::cost::process_end("direct");\n }'.join(s.rsplit(' }}',1))
s=s.replace(' let start=Instant::now();',' let start=Instant::now();let linear_start=farkas_core::cost::ns(1);let linear_cpu=farkas_core::cost::ns(3);')
s=s.replace(' let linear_ns=start.elapsed().as_nanos();',' let linear_ns=start.elapsed().as_nanos();farkas_core::cost::record_interval("linear",linear_start,linear_cpu);')
s=s.replace('let mut pool=facts.clone();','let mut pool=facts.clone();\n let product_start=farkas_core::cost::ns(1);let product_cpu=farkas_core::cost::ns(3);')
s=s.replace(' let products_ns=start.elapsed().as_nanos()-linear_ns;',' let products_ns=start.elapsed().as_nanos()-linear_ns;\n farkas_core::cost::record_interval("products",product_start,product_cpu);\n let matrix_start=farkas_core::cost::ns(1);let matrix_cpu=farkas_core::cost::ns(3);')
s=s.replace(' let products_ns=start.elapsed().as_nanos()-linear_ns;',' farkas_core::cost::metadata(serde_json::json!({"stage":"products_count","products":all.len()-pool.len()-1,"pool_facts":pool.len(),"nlin":v["nlin"]}));\n let products_ns=start.elapsed().as_nanos()-linear_ns;')
s=s.replace(' let before_lp=Instant::now();',' farkas_core::cost::record_interval("matrix_pack",matrix_start,matrix_cpu);\n farkas_core::cost::hyps(&hyps);\n let before_lp=Instant::now();')
s=s.replace('verify_cert(&hyps,&c)','farkas_core::cost::timed("exact_verify",||verify_cert(&hyps,&c))')
s=s.replace('serde_json::from_str(&line).map_err','farkas_core::cost::timed("request_parse",||serde_json::from_str(&line)).map_err')
s=s.replace(' let answer=std::panic::catch_unwind', ' farkas_core::cost::begin();let wall=farkas_core::cost::ns(1);let cpu=farkas_core::cost::ns(3);\n let answer=std::panic::catch_unwind')
s=s.replace(' writeln!(out,"{}",v).unwrap();out.flush().unwrap();',' let answer=farkas_core::cost::timed("response_pack",||v.to_string());\n farkas_core::cost::timed("response_write",||{writeln!(out,"{}",answer).unwrap();out.flush().unwrap();});\n farkas_core::cost::finish("direct",&line,&answer,wall,cpu);')
s=s.replace(' farkas_core::cost::hyps(&hyps);',' farkas_core::cost::metadata(serde_json::json!({"stage":"product_columns","columns":origins.iter().map(|(origin,_)|origin[0]=="mul").collect::<Vec<_>>() }));\n farkas_core::cost::hyps(&hyps);')
(core/'src/bin/arithmetic-costd.rs').write_text(s)
# Strong native fallback service, same algorithms/protocol; all calls captured.
s=(R/'artifacts/lean-modern-native-compilation-2026-10-14/Farkas-external-support-oracled.rs').read_text()
s=s.replace('fn main() {','fn main() {\n    if farkas_core::cost::supervise("fallback"){return;}')
s=s.replace('    for line in stdin.lock().lines() {','    let mut lines=stdin.lock().lines();\n    loop { let Some(line)=farkas_core::cost::read_line(&mut lines) else{break};')
s=s.replace('    }\n}\n\n#[cfg(test)]','    }\n    farkas_core::cost::process_end("fallback");\n}\n\n#[cfg(test)]',1)
s=s.replace('serde_json::from_str::<serde_json::Value>(line)','farkas_core::cost::timed("request_parse",||serde_json::from_str::<serde_json::Value>(line))')
s=s.replace('match answer {','farkas_core::cost::timed("response_pack",||match answer {',1)
s=s.replace('            None => "{\\"cert\\":null}".to_string(),\n            }','            None => "{\\"cert\\":null}".to_string(),\n            })',1)
s=s.replace('match parse_request(line) {','match farkas_core::cost::timed("request_parse",||parse_request(line)) {')
s=s.replace('            let request = serde_json', '            farkas_core::cost::hyps(&hyps);\n            let request = serde_json')
s=s.replace('exact_repair(&hyps,xs)','farkas_core::cost::timed("exact_repair",||exact_repair(&hyps,xs))')
s=s.replace('verify_cert(&hyps,c)','farkas_core::cost::timed("exact_verify",||verify_cert(&hyps,c))')
s=s.replace('verify_cert(&hyps, &cert)','farkas_core::cost::timed("exact_verify",||verify_cert(&hyps, &cert))')
s=s.replace('produce_certificate_tiered(&hyps,max_var)','farkas_core::cost::timed("exact_lp",||produce_certificate_tiered(&hyps,max_var))')
s=s.replace('        let answer = std::panic::catch_unwind','        farkas_core::cost::begin();let wall=farkas_core::cost::ns(1);let cpu=farkas_core::cost::ns(3);\n        let answer = std::panic::catch_unwind')
s=s.replace('        writeln!(out, "{}", answer).expect("stdout write");\n        out.flush().expect("stdout flush");','        farkas_core::cost::timed("response_write",||{writeln!(out, "{}", answer).expect("stdout write");out.flush().expect("stdout flush");});\n        farkas_core::cost::finish("fallback",&line,&answer,wall,cpu);')
(core/'src/bin/farkas-costd.rs').write_text(s)
# Preserve a separate timed Mathlib implementation for all fallback stages.
s=(BASE/'GpuArithmetic/Stages.lean').read_text().replace('GpuArithmetic.Stages','GpuArithmetic.CostStages')
s=s.replace('abbrev Costs := Std.HashMap String (Nat × Nat)', '''structure Costs where
  times : Std.HashMap String (Nat × Nat) := {}
  products : Std.HashSet Expr := {}
def Costs.getD (s : Costs) (key : String) (fallback : Nat × Nat) : Nat × Nat :=
  s.times.getD key fallback
def Costs.insert (s : Costs) (key : String) (value : Nat × Nat) : Costs :=
  {s with times := s.times.insert key value}
def Costs.toList (s : Costs) : List (String × (Nat × Nat)) := s.times.toList
def registerProducts (ref : IO.Ref Costs) (proofs : List Expr) : IO Unit :=
  ref.modify fun s => {s with products := proofs.foldl (fun seen e => seen.insert e) s.products}
def productColumns (ref : IO.Ref Costs) (inputs : List Expr) : IO String := do
  let st ← ref.get
  let flags := inputs.map fun e => (e.find? fun x => st.products.contains x).isSome
  return "[" ++ ",".intercalate (flags.map fun x => if x then "true" else "false") ++ "]"
''')
s=s.replace('              oracle.produceCertificate comps max_var', '''              let flags ← productColumns cost inputs
              withOptions (fun opts => opts.setString `gpuSmtCostProductColumns flags) do
                oracle.produceCertificate comps max_var''')
s=s.replace('      m.insert name (old.1 + dc, old.2 + dw)', '''      m.insert name (old.1 + dc, old.2 + dw)
    Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\\"cost-stage\\""),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),("stage",Farkas.Telemetry.jstrEsc name),("start_ns",toString w),("end_ns",toString (w+dw)),("cpu_ns",toString dc)]''')
s=s.replace('      let certificate : Std.HashMap Nat Nat ←', '''      Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\\"cost-lp-input\\""),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),("at_ns",toString (← IO.monoNanosNow)),("maxVar",toString max_var),("hyps","[" ++ ",".intercalate (comps.map Farkas.Telemetry.compJson) ++ "]")]
      let certificate : Std.HashMap Nat Nat ←''')
s=s.replace('("maxVar",toString max_var),', '("product_columns",← productColumns cost inputs),("maxVar",toString max_var),')
(U/'GpuArithmetic/CostStages.lean').write_text(s)
s=(BASE/'Farkas427/Products.lean').read_text().replace('namespace Farkas427.Products','namespace GpuArithmetic.CostProducts').replace('end Farkas427.Products','end GpuArithmetic.CostProducts')
s=s.replace('import Farkas.Telemetry','import Farkas.Telemetry\nimport GpuArithmetic.CostStages')
s=s.replace('private def productProofs (ls','private def productProofs (cost : IO.Ref GpuArithmetic.CostStages.Costs) (ls')
s=s.replace('  compWithZero.globalize.transform products.reduceOption','''  let normalized ← compWithZero.globalize.transform products.reduceOption
  GpuArithmetic.CostStages.registerProducts cost normalized
  return normalized''')
s=s.replace('def extras : GlobalPreprocessor','def extras (cost : IO.Ref GpuArithmetic.CostStages.Costs) : GlobalPreprocessor')
s=s.replace('productProofs (new_es ++ ls)','productProofs cost (new_es ++ ls)')
s=s.replace('end GpuArithmetic.CostProducts','''def stockExtras (cost : IO.Ref GpuArithmetic.CostStages.Costs) : GlobalPreprocessor where
  description := "nonlinear arithmetic extras"
  transform ls := do
    let new_es ← nlinarithGetSquareProofs ls
    let products ← nlinarithGetProductsProofs (new_es ++ ls)
    GpuArithmetic.CostStages.registerProducts cost products
    return new_es ++ ls ++ products
end GpuArithmetic.CostProducts''')
stock_source=(T/'mathlib4/Mathlib/Tactic/Linarith/Preprocessing.lean').read_text()
start=stock_source.index('private def nlinarithGetProductsProofs')
stop=stock_source.index('/--\n`nlinarithExtras',start)
stock=stock_source[start:stop].replace('nlinarithGetProductsProofs (ls','stockProductProofs (cost : IO.Ref GpuArithmetic.CostStages.Costs) (ls').replace('Ineq','Mathlib.Ineq')
stock=stock.replace('  compWithZero.globalize.transform products.reduceOption','''  let normalized ← compWithZero.globalize.transform products.reduceOption
  GpuArithmetic.CostStages.registerProducts cost normalized
  return normalized''')
s=s.replace('def stockExtras',stock+'\ndef stockExtras')
s=s.replace('nlinarithGetSquareProofs ls','squareProofs ls')
s=s.replace('nlinarithGetProductsProofs (new_es ++ ls)','stockProductProofs cost (new_es ++ ls)')
(U/'GpuArithmetic/CostProducts.lean').write_text(s)
# Namespaced native client carries source identity and round-trip/mutex intervals.
s=(F/'Farkas/Native.lean').read_text()
s=s.replace('namespace Farkas\n','namespace GpuArithmetic.CostNative\n').replace('end Farkas','end GpuArithmetic.CostNative')
s=s.replace('Telemetry.','Farkas.Telemetry.').replace('← findBinary','← Farkas.findBinary')
s=s.replace('    let req := requestLine hyps maxVar','    let source := (← getFileMap).source\n    let start ← IO.monoNanosNow\n    let base := requestLine hyps maxVar\n    let req := "{\\"source\\":" ++ Farkas.Telemetry.jstrEsc source ++ ",\\"call_id\\":" ++ toString start ++ "," ++ (base.drop 1).toString')
s=s.replace('    match parseCert line with','    let finished ← IO.monoNanosNow\n    Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\\"cost-native-roundtrip\\""),("call_id",toString start),("source",Farkas.Telemetry.jstrEsc source),("start_ns",toString start),("end_ns",toString finished),("answer",line.trimAscii.toString)]\n    match parseCert line with')
s=s.replace('    let base := requestLine hyps maxVar','    let flags := (← getOptions).getString `gpuSmtCostProductColumns "null"\n    let base := requestLine hyps maxVar')
s=s.replace('++ (base.drop 1).toString','++ "\\\"product_columns\\\":" ++ flags ++ "," ++ (base.drop 1).toString')
(U/'GpuArithmetic/CostNative.lean').write_text(s)
s=(BASE/'GpuArithmetic/FastProfile.lean').read_text().replace('GpuArithmetic.FastProfile','GpuArithmetic.CostFast').replace('GpuArithmetic.Stages','GpuArithmetic.CostStages').replace('Farkas.native','GpuArithmetic.CostNative.native')
s=s.replace('import Farkas.Native','import GpuArithmetic.CostNative')
s=s.replace('  natTyped : Bool := false','  natTyped : Bool := false\n  productGenerated : Bool := false')
s=s.replace('intLike := a.intLike && b.intLike }','intLike := a.intLike && b.intLike, productGenerated := true }')
s=s.replace('let cert ← GpuArithmetic.CostNative.native.produceCertificate comps maxVar','''let flags := "[" ++ ",".intercalate (all.map fun h => if h.productGenerated then "true" else "false") ++ "]"
    let cert ← withOptions (fun opts => opts.setString `gpuSmtCostProductColumns flags) do
      GpuArithmetic.CostNative.native.produceCertificate comps maxVar''')
(U/'GpuArithmetic/CostFast.lean').write_text(s)
s=(BASE/'GpuArithmetic/StrongProfile.lean').read_text().replace('GpuArithmetic.StrongProfile','GpuArithmetic.CostBaseline').replace('GpuArithmetic.Stages','GpuArithmetic.CostStages').replace('GpuArithmetic.FastProfile','GpuArithmetic.CostFast').replace('GpuArithmetic.Stages','GpuArithmetic.CostStages').replace('Farkas.native','GpuArithmetic.CostNative.native')
s=s.replace('import GpuArithmetic.FastProfile','import GpuArithmetic.CostFast')
s=s.replace('import Farkas427.Products','import GpuArithmetic.CostProducts')
s=s.replace('concat Farkas427.Products.extras','concat (GpuArithmetic.CostProducts.extras cost)')
s=s.replace('concat nlinarithExtras','concat (GpuArithmetic.CostProducts.stockExtras cost)')
(U/'GpuArithmetic/CostBaseline.lean').write_text(s)
# Oracle source rewrite lives separately and logs all attempted branches.
s=(D/'Oracle.lean').read_text().replace('namespace GpuArithmetic.Oracle','namespace GpuArithmetic.CostOracle').replace('end GpuArithmetic.Oracle','end GpuArithmetic.CostOracle')
s=s.replace('import Farkas.Native','import GpuArithmetic.CostBaseline')
s=s.replace('    let answer ← query request','    let request := "{\\"source\\":" ++ Farkas.Telemetry.jstrEsc (← getFileMap).source ++ ",\\"call_id\\":" ++ toString exported ++ "," ++ (request.drop 1).toString\n    let answer ← query request\n    let answered ← IO.monoNanosNow\n    Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\\"cost-direct-roundtrip\\""),("call_id",toString exported),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),("start_ns",toString exported),("end_ns",toString answered),("answer",answer.trimAscii.toString)]')
s=s.replace('    let .ok j := Json.parse answer | throwError "invalid oracle response"\n    let .ok cj := j.getObjVal? "cert" | throwError "oracle failure"\n    let cert ← getArray cj\n    checkCertificate cfg goal carrier raw (← atoms.get) cert', '''    let checkStart ← IO.monoNanosNow
    let checkCpu ← GpuArithmetic.CostStages.threadCpuNs
    let ok ← IO.mkRef false
    try
      let .ok j := Json.parse answer | throwError "invalid oracle response"
      let .ok cj := j.getObjVal? "cert" | throwError "oracle failure"
      let cert ← getArray cj
      checkCertificate cfg goal carrier raw (← atoms.get) cert
      ok.set true
    finally
      let finish ← IO.monoNanosNow
      let cpu ← GpuArithmetic.CostStages.threadCpuNs
      Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\\"cost-direct-check\\""),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),("call_id",toString exported),("start_ns",toString checkStart),("end_ns",toString finish),("cpu_ns",toString (cpu.toNat-checkCpu.toNat)),("accepted",if (← ok.get) then "true" else "false")]''')
(U/'GpuArithmetic/CostOracle.lean').write_text(s)
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+':/usr/local/cargo/bin:'+env['PATH']
env['CARGO_HOME']='/usr/local/cargo';env['RUSTUP_HOME']='/usr/local/rustup'
env['LEAN_PATH']=':'.join([str(U),str(BASE),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean') for p in (T/'mathlib4/.lake/packages').iterdir() if p.is_dir()])
records=[]
with (U/'build-cost.log').open('w') as log:
 def run(cmd,cwd=U):
  records.append({'cmd':cmd,'cwd':str(cwd)});log.write(repr(cmd)+'\n');log.flush()
  subprocess.run(cmd,cwd=cwd,env=env,check=True,stdout=log,stderr=subprocess.STDOUT)
 run(['cargo','build','--release','--bin','arithmetic-costd','--bin','farkas-costd'],core)
 for name in ['arithmetic-costd','farkas-costd']:shutil.copy2(core/'target/release'/name,U/name)
 names=['CostStages','CostProducts','CostNative','CostFast','CostBaseline','CostOracle']
 for name in names:
  run(['lean','-o',str(U/'GpuArithmetic'/(name+'.olean')),'-c',str(U/(name+'.c')),str(U/'GpuArithmetic'/(name+'.lean'))])
 run(['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*[str(U/(n+'.c')) for n in names],'-o',str(U/'cost-profile.so')])
(U/'build-cost-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':records,'diagnostic_only':True},indent=2)+'\n')
print('BUILT cost-profile.so and both cost daemons',flush=True)
