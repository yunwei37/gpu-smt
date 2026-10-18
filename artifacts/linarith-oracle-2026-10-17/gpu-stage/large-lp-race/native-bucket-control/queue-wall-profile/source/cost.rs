//! Diagnostic-only intervals. No certificate or solver decision is changed.
use std::{cell::RefCell,io::Write,os::fd::AsRawFd};
unsafe extern "C"{fn flock(fd:i32,operation:i32)->i32;}
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
 SESSION_CPU.with(|x|x.set(x.get()+dc));SESSIONS.with(|x|x.set(x.get()+1));
 let before_log=ns(3);
 let record=json!({"kind":kind,"pid":std::process::id(),"start_ns":start,"end_ns":end,"cpu_ns":dc,
  "process_cpu_ns":ns(2),"request_bytes":request.len(),"response_bytes":answer.len(),
  "request":serde_json::from_str::<Value>(request).unwrap_or(Value::Null),
  "answer":serde_json::from_str::<Value>(answer).unwrap_or(Value::Null),"events":events});
 LOG_CPU.with(|x|x.set(x.get()+ns(3)-before_log));append_record(&record);
}

pub fn record_interval(stage:&str,start:u64,cpu:u64){
 let end=ns(1);let dc=ns(3)-cpu;
 EVENTS.with(|e|e.borrow_mut().push(json!({"stage":stage,"start_ns":start,"end_ns":end,"cpu_ns":dc})));
}

pub fn metadata(v:Value){EVENTS.with(|e|e.borrow_mut().push(v));}

thread_local!{
 static LOG_CPU:std::cell::Cell<u64>=const{std::cell::Cell::new(0)};
 static READ_CPU:std::cell::Cell<u64>=const{std::cell::Cell::new(0)};
 static SESSION_CPU:std::cell::Cell<u64>=const{std::cell::Cell::new(0)};
 static SESSIONS:std::cell::Cell<u64>=const{std::cell::Cell::new(0)};
}
pub fn read_line<I:Iterator<Item=std::io::Result<String>>>(lines:&mut I)->Option<std::io::Result<String>>{
 let before=ns(3);let row=lines.next();let cpu=ns(3)-before;
 READ_CPU.with(|x|x.set(x.get()+cpu));row
}
fn append_record(record:&Value){
 let before=ns(3);
 if let Ok(path)=std::env::var("FARKAS_COST_FILE"){
  let mut f=std::fs::OpenOptions::new().create(true).append(true).open(path).expect("cost log open");
  let mut bytes=serde_json::to_vec(record).unwrap();bytes.push(b'\n');
  assert_eq!(unsafe{flock(f.as_raw_fd(),2)},0,"cost log lock");
  f.write_all(&bytes).expect("cost log write");
  assert_eq!(unsafe{flock(f.as_raw_fd(),8)},0,"cost log unlock");
 }
 LOG_CPU.with(|x|x.set(x.get()+ns(3)-before));
}
pub fn process_end(kind:&str){
 append_record(&json!({"kind":"worker-eof","service_kind":kind,"pid":std::process::id(),
  "mono_ns":ns(1),"process_cpu_ns":ns(2),"session_cpu_ns":SESSION_CPU.with(|x|x.get()),
  "stdin_read_cpu_ns":READ_CPU.with(|x|x.get()),"diagnostic_write_cpu_ns":LOG_CPU.with(|x|x.get()),
  "sessions":SESSIONS.with(|x|x.get())}));
}
#[repr(C)]struct Tv{sec:i64,usec:i64}
#[repr(C)]struct Usage{user:Tv,sys:Tv,rest:[i64;14]}
unsafe extern "C"{fn wait4(pid:i32,status:*mut i32,flags:i32,usage:*mut Usage)->i32;}
/// Diagnostic executable owns and reaps its worker once; no polling or service.
pub fn supervise(kind:&str)->bool{
 if std::env::var_os("FARKAS_COST_FILE").is_none() || std::env::var_os("FARKAS_COST_WORKER").is_some(){return false}
 let exe=std::env::current_exe().expect("diagnostic executable");
 let child=std::process::Command::new(exe).args(std::env::args().skip(1))
  .env("FARKAS_COST_WORKER","1").stdin(std::process::Stdio::inherit())
  .stdout(std::process::Stdio::inherit()).stderr(std::process::Stdio::inherit()).spawn().expect("cost worker");
 let mut usage=Usage{user:Tv{sec:0,usec:0},sys:Tv{sec:0,usec:0},rest:[0;14]};
 let mut status=0;
 loop{
  let rc=unsafe{wait4(child.id() as i32,&mut status,0,&mut usage)};
  if rc>=0{break}
  if std::io::Error::last_os_error().kind()!=std::io::ErrorKind::Interrupted{panic!("cost wait4 failed")}
 }
 append_record(&json!({"kind":"process-exit","service_kind":kind,"pid":child.id(),"supervisor_pid":std::process::id(),
  "mono_ns":ns(1),"wait_status":status,"user_us":usage.user.sec*1_000_000+usage.user.usec,
  "system_us":usage.sys.sec*1_000_000+usage.sys.usec,"maxrss_kib":usage.rest[0],
  "scope":"complete waited worker CPU including protocol, diagnostics and exit; supervisor CPU excluded"}));
 let code=if status&127==0{(status>>8)&255}else{128+(status&127)};
 std::process::exit(code)
}
