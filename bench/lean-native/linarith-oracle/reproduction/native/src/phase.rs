// gpu-smt reproduction snapshot: derived from Farkas; local oracle/race/instrumentation changes. See ../PROVENANCE.md and LICENSE.
//! Linux x86_64 diagnostic: thread CPU and monotonic phase intervals.
use std::{io::Write,os::fd::AsRawFd,sync::atomic::{AtomicU64,Ordering}};
#[repr(C)]#[derive(Default)]pub struct TimeVal{pub sec:i64,pub usec:i64}
#[repr(C)]#[derive(Default)]pub struct Usage{pub user:TimeVal,pub system:TimeVal,pub counters:[i64;14]}
#[repr(C)]struct TimeSpec{sec:i64,nsec:i64}
unsafe extern "C"{
 fn clock_gettime(clock:i32,out:*mut TimeSpec)->i32;
 fn gettid()->i32;
 fn flock(fd:i32,op:i32)->i32;
 pub fn wait4(pid:i32,status:*mut i32,options:i32,usage:*mut Usage)->i32;
}
#[cfg(not(all(target_os="linux",target_arch="x86_64")))]
compile_error!("This measured diagnostic uses the retained Linux x86_64 rusage ABI");
fn ns(clock:i32)->u128{let mut t=TimeSpec{sec:0,nsec:0};assert_eq!(unsafe{clock_gettime(clock,&mut t)},0);t.sec as u128*1_000_000_000+t.nsec as u128}
fn log(path:&str,row:serde_json::Value){
 let mut f=std::fs::OpenOptions::new().create(true).append(true).open(path).expect("phase log");
 assert_eq!(unsafe{flock(f.as_raw_fd(),2)},0);
 writeln!(f,"{row}").expect("phase append");assert_eq!(unsafe{flock(f.as_raw_fd(),8)},0);
}
static SEQ:AtomicU64=AtomicU64::new(0);
pub struct Guard{data:Option<(String,serde_json::Value)>}
impl Guard{
 pub fn new(stage:&'static str)->Self{
  let Ok(path)=std::env::var("GPU_ARITHMETIC_NUMERIC_PHASE_LOG")else{return Self{data:None}};
  let wall=ns(1);let cpu=ns(3);
  let context=crate::race::context();
  let mut row=serde_json::json!({"event":"begin","pid":std::process::id(),"tid":unsafe{gettid()},"id":SEQ.fetch_add(1,Ordering::Relaxed),
   "stage":stage,"call_id":context["call_id"],"wall_ns":wall,"thread_cpu_ns":cpu});
  if stage=="native_reference_request"{row["source"]=context["source"].clone();}
  log(&path,row.clone());Self{data:Some((path,row))}
 }
}
impl Drop for Guard{
 fn drop(&mut self){if let Some((path,mut row))=self.data.take(){
  let cpu=ns(3);let wall=ns(1);row["event"]="end".into();row["wall_ns"]=serde_json::json!(wall);row["thread_cpu_ns"]=serde_json::json!(cpu);log(&path,row);
 }}
}
pub fn cpu_ns(t:&TimeVal)->u128{t.sec as u128*1_000_000_000+t.usec as u128*1000}
