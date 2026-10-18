//! One cancellable LP child; no persistent service or polling thread.
use std::io::{BufRead,Write};
use farkas_core::{types::parse_request,hybrid::produce_certificate_hybrid,race::race_gpu_hint,verify::verify_cert};
fn main(){
 let gpu=std::env::args().nth(1).as_deref()==Some("--gpu");
 let mut line=String::new();std::io::BufReader::new(std::io::stdin()).read_line(&mut line).unwrap();
 if let Ok(v)=serde_json::from_str(&line){farkas_core::race::set_context(&v);}
 let Some((m,hyps))=parse_request(&line)else{println!("{{\"error\":\"request\"}}");return};
 let cert=if gpu{race_gpu_hint(&hyps)}else{produce_certificate_hybrid(&hyps,m).0};
 let cert=cert.filter(|c|verify_cert(&hyps,c)).map(|c|c.into_iter().map(|(i,w)|serde_json::json!([i,w.to_string()])).collect::<Vec<_>>());
 let mut out=std::io::stdout().lock();writeln!(out,"{}",serde_json::json!({"cert":cert})).unwrap();out.flush().unwrap();
}
