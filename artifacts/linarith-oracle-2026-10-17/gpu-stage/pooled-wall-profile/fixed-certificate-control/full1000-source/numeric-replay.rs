//! Diagnostic omission control: return actual recorded coefficient answers.
//! Lean still constructs/checks every proof; no cached verification verdicts.
use std::collections::HashMap;
use std::io::{BufRead,Write};
use std::os::fd::AsRawFd;
use serde_json::{Value,json};
#[repr(C)]struct Timespec{sec:i64,nsec:i64}
unsafe extern "C"{fn clock_gettime(which:i32,out:*mut Timespec)->i32;fn flock(fd:i32,op:i32)->i32;}
fn ns(which:i32)->u64{let mut t=Timespec{sec:0,nsec:0};assert_eq!(unsafe{clock_gettime(which,&mut t)},0);(t.sec as u64)*1_000_000_000+t.nsec as u64}
fn key(mut v:Value)->String{
 let o=v.as_object_mut().expect("numerical object");
 o.remove("call_id");o.remove("product_columns");v.to_string()
}
fn record(row:Value){
 if let Ok(path)=std::env::var("GPU_ARITHMETIC_REPLAY_LOG"){
  let mut f=std::fs::OpenOptions::new().create(true).append(true).open(path).expect("replay log");
  assert_eq!(unsafe{flock(f.as_raw_fd(),2)},0);writeln!(f,"{row}").expect("replay log write");
  assert_eq!(unsafe{flock(f.as_raw_fd(),8)},0);
 }
}
fn main(){
 let start=ns(1);let cpu=ns(3);
 let path=std::env::var("GPU_ARITHMETIC_REPLAY_DATA").expect("retained request/answer file required");
 let data=std::io::BufReader::new(std::fs::File::open(&path).expect("actual numerical data"));
 let mut cache=HashMap::new();
 for line in data.lines(){
  let r:Value=serde_json::from_str(&line.expect("data read")).expect("actual cost record");
  let k=key(r["request"].clone());let answer=json!({"cert":r["answer"]["cert"]});
  if let Some(old)=cache.insert(k,answer.clone()){assert_eq!(old,answer,"conflicting actual certificates");}
 }
 record(json!({"ty":"numerical-replay-setup","pid":std::process::id(),"start_ns":start,"end_ns":ns(1),"cpu_ns":ns(3)-cpu,"entries":cache.len(),"data":path}));
 let stdin=std::io::stdin();let mut out=std::io::stdout().lock();
 for line in stdin.lock().lines(){
  let line=line.expect("request read");let start=ns(1);let cpu=ns(3);
  let request:Value=serde_json::from_str(&line).expect("native numerical request");
  let handshake=request["hello"]==true;
  let answer=if handshake{Some(json!({"farkas_protocol":1}))}else{cache.get(&key(request.clone())).cloned()};
  let hit=answer.is_some();let answer=answer.unwrap_or_else(||json!({"cert":null,"error":"recorded_numerical_answer_missing"}));
  let wire=answer.to_string();writeln!(out,"{wire}").expect("response write");out.flush().expect("response flush");
  record(json!({"ty":"numerical-replay","pid":std::process::id(),"start_ns":start,"end_ns":ns(1),"cpu_ns":ns(3)-cpu,
   "handshake":handshake,"hit":hit,"request_bytes":line.len(),"response_bytes":wire.len(),"source":request["source"],
   "scope":"actual coefficient answer replay; old timing fields removed; Lean validation still executes"}));
 }
}
