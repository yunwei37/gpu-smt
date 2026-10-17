//! Diagnostic-only intervals. No certificate or solver decision is changed.
use std::{cell::RefCell,time::Instant,io::Write};
use serde_json::{Value,json};
#[repr(C)]struct Ts{sec:i64,nsec:i64}
unsafe extern "C"{fn clock_gettime(id:i32,t:*mut Ts)->i32;}
pub fn ns(id:i32)->u64{let mut t=Ts{sec:0,nsec:0};unsafe{clock_gettime(id,&mut t);}t.sec as u64*1_000_000_000+t.nsec as u64}
thread_local!{static EVENTS:RefCell<Vec<Value>>=const{RefCell::new(Vec::new())};}
pub fn timed<T>(stage:&str,f:impl FnOnce()->T)->T{
 let w=ns(1);let c=ns(3);let ans=f();let end=ns(1);let cpu=ns(3)-c;
 EVENTS.with(|e|e.borrow_mut().push(json!({"stage":stage,"start_ns":w,"end_ns":end,"cpu_ns":cpu})));ans
}
pub fn shape(rows:usize,cols:usize,nnz:usize,kind:&str){
 EVENTS.with(|e|e.borrow_mut().push(json!({"stage":"shape","kind":kind,"rows":rows,"cols":cols,"nnz":nnz})));
}
pub fn hyps(hyps:&[crate::types::Hyp]){
 use num_traits::Zero;
 let mut rows=std::collections::BTreeSet::new();let mut nnz=0;
 for h in hyps {for(v,c)in &h.coeffs{if !c.is_zero(){rows.insert(*v);nnz+=1;}}if h.ineq==crate::types::Ineq::Lt{nnz+=1;}}
 shape(rows.len()+1,hyps.len(),nnz,"certificate-unscaled");
}
pub fn begin(){EVENTS.with(|e|e.borrow_mut().clear());}
pub fn finish(kind:&str,request:&str,answer:&str,start:u64,cpu:u64){
 let end=ns(1);let dc=ns(3)-cpu;
 let events=EVENTS.with(|e|std::mem::take(&mut *e.borrow_mut()));
 if let Ok(path)=std::env::var("FARKAS_COST_FILE"){
  let record=json!({"kind":kind,"pid":std::process::id(),"start_ns":start,"end_ns":end,"cpu_ns":dc,"request":serde_json::from_str::<Value>(request).unwrap_or(Value::Null),"answer":serde_json::from_str::<Value>(answer).unwrap_or(Value::Null),"events":events});
  if let Ok(mut f)=std::fs::OpenOptions::new().create(true).append(true).open(path){
   let mut bytes=serde_json::to_vec(&record).unwrap();bytes.push(b'\n');f.write_all(&bytes).unwrap();
  }
 }
}

pub fn record_interval(stage:&str,start:u64,cpu:u64){
 let end=ns(1);let dc=ns(3)-cpu;
 EVENTS.with(|e|e.borrow_mut().push(json!({"stage":stage,"start_ns":start,"end_ns":end,"cpu_ns":dc})));
}
