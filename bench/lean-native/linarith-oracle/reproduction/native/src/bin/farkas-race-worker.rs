// gpu-smt reproduction snapshot: derived from Farkas; local oracle/race/instrumentation changes. See ../PROVENANCE.md and LICENSE.
//! One cancellable LP child; no persistent service or polling thread.
use std::io::{BufRead,Write};
use farkas_core::{types::parse_request,hybrid::produce_certificate_hybrid,race::race_gpu_hint,verify::verify_cert};
fn main(){
 let mode=std::env::args().nth(1);
 let gpu=matches!(mode.as_deref(),Some("--gpu"|"--cpu-highs"));
 if mode.as_deref()==Some("--cpu-highs"){
  let path=std::env::var("GPU_ARITHMETIC_STRONG_CPU_SOCKET").expect("prepared strong CPU numeric proxy");
  unsafe{std::env::set_var("GPU_ARITHMETIC_SUPPORT_SOCKET",path);}
 }
 let mut line=String::new();std::io::BufReader::new(std::io::stdin()).read_line(&mut line).unwrap();
 if let Ok(v)=serde_json::from_str(&line){farkas_core::race::set_context(&v);}
 let whole_phase=farkas_core::phase::Guard::new("child_request_total");
 let parse_phase=farkas_core::phase::Guard::new("child_parse");
 let Some((m,hyps))=parse_request(&line)else{println!("{{\"error\":\"request\"}}");return};
 drop(parse_phase);
 let cert=if gpu{race_gpu_hint(&hyps)}else if mode.as_deref()==Some("--cpu-exact"){farkas_core::tiered::produce_certificate_tiered(&hyps,m)}else{produce_certificate_hybrid(&hyps,m).0};
 let cert=cert.filter(|c|verify_cert(&hyps,c)).map(|c|c.into_iter().map(|(i,w)|serde_json::json!([i,w.to_string()])).collect::<Vec<_>>());
 drop(whole_phase);
 let mut out=std::io::stdout().lock();writeln!(out,"{}",serde_json::json!({"cert":cert,"infeasible_certificate":farkas_core::race::take_negative_certificate()})).unwrap();out.flush().unwrap();
}
