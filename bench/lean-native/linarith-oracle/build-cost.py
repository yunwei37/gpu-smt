"""Complete all-call oracle cost attribution; separate diagnostic binaries/modules.
The original primary binaries and active Lean 4.9 prefix process are untouched.
"""
from pathlib import Path
import os,shutil,subprocess,json,datetime
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017');T=Path('/tmp/gpu-smt-goedel427-20261014')
F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
core=U/'native'; snap=R/'artifacts/lean-modern-native-compilation-2026-10-14/source-snapshot-20261015/external-support'
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
(core/'src/bin/arithmetic-costd.rs').write_text(s)
# Strong native fallback service, same algorithms/protocol; all calls captured.
s=(R/'artifacts/lean-modern-native-compilation-2026-10-14/Farkas-external-support-oracled.rs').read_text()
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
s=(U/'GpuArithmetic/Stages.lean').read_text().replace('GpuArithmetic.Stages','GpuArithmetic.CostStages')
s=s.replace('      m.insert name (old.1 + dc, old.2 + dw)', '''      m.insert name (old.1 + dc, old.2 + dw)
    Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\\"cost-stage\\""),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),("stage",Farkas.Telemetry.jstrEsc name),("start_ns",toString w),("end_ns",toString (w+dw)),("cpu_ns",toString dc)]''')
s=s.replace('      let certificate : Std.HashMap Nat Nat ←', '''      Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\\"cost-lp-input\\""),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),("at_ns",toString (← IO.monoNanosNow)),("maxVar",toString max_var),("hyps","[" ++ ",".intercalate (comps.map Farkas.Telemetry.compJson) ++ "]")]
      let certificate : Std.HashMap Nat Nat ←''')
(U/'GpuArithmetic/CostStages.lean').write_text(s)
# Namespaced native client carries source identity and round-trip/mutex intervals.
s=(F/'Farkas/Native.lean').read_text()
s=s.replace('namespace Farkas\n','namespace GpuArithmetic.CostNative\n').replace('end Farkas','end GpuArithmetic.CostNative')
s=s.replace('Telemetry.','Farkas.Telemetry.').replace('← findBinary','← Farkas.findBinary')
s=s.replace('    let req := requestLine hyps maxVar','    let source := (← getFileMap).source\n    let start ← IO.monoNanosNow\n    let base := requestLine hyps maxVar\n    let req := "{\\"source\\":" ++ Farkas.Telemetry.jstrEsc source ++ ",\\"call_id\\":" ++ toString start ++ "," ++ (base.drop 1).toString')
s=s.replace('    match parseCert line with','    let finished ← IO.monoNanosNow\n    Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\\"cost-native-roundtrip\\""),("call_id",toString start),("source",Farkas.Telemetry.jstrEsc source),("start_ns",toString start),("end_ns",toString finished),("answer",line.trimAscii.toString)]\n    match parseCert line with')
(U/'GpuArithmetic/CostNative.lean').write_text(s)
s=(U/'GpuArithmetic/FastProfile.lean').read_text().replace('GpuArithmetic.FastProfile','GpuArithmetic.CostFast').replace('GpuArithmetic.Stages','GpuArithmetic.CostStages').replace('Farkas.native','GpuArithmetic.CostNative.native')
s=s.replace('import Farkas.Native','import GpuArithmetic.CostNative')
(U/'GpuArithmetic/CostFast.lean').write_text(s)
s=(U/'GpuArithmetic/StrongProfile.lean').read_text().replace('GpuArithmetic.StrongProfile','GpuArithmetic.CostBaseline').replace('GpuArithmetic.Stages','GpuArithmetic.CostStages').replace('GpuArithmetic.FastProfile','GpuArithmetic.CostFast').replace('GpuArithmetic.Stages','GpuArithmetic.CostStages').replace('Farkas.native','GpuArithmetic.CostNative.native')
s=s.replace('import GpuArithmetic.FastProfile','import GpuArithmetic.CostFast')
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
env['LEAN_PATH']=':'.join([str(U),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean') for p in (T/'mathlib4/.lake/packages').iterdir() if p.is_dir()])
records=[]
with (U/'build-cost.log').open('w') as log:
 def run(cmd,cwd=U):
  records.append({'cmd':cmd,'cwd':str(cwd)});log.write(repr(cmd)+'\n');log.flush()
  subprocess.run(cmd,cwd=cwd,env=env,check=True,stdout=log,stderr=subprocess.STDOUT)
 run(['cargo','build','--release','--bin','arithmetic-costd','--bin','farkas-costd'],core)
 for name in ['arithmetic-costd','farkas-costd']:shutil.copy2(core/'target/release'/name,U/name)
 names=['CostStages','CostNative','CostFast','CostBaseline','CostOracle']
 for name in names:
  run(['lean','-o',str(U/'GpuArithmetic'/(name+'.olean')),'-c',str(U/(name+'.c')),str(U/'GpuArithmetic'/(name+'.lean'))])
 run(['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*[str(U/(n+'.c')) for n in names],'-o',str(U/'cost-profile.so')])
(U/'build-cost-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':records,'diagnostic_only':True},indent=2)+'\n')
print('BUILT cost-profile.so and both cost daemons',flush=True)
