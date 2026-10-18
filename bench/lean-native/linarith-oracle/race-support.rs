// Large-LP speculative support search. Included in the pinned hybrid module.
// Both children inherit the same affinity/address-space limit. The CPU child
// remains live until a GPU certificate passes exact repair and verification.
// No detached threads; every child is cancelled (if still live) and reaped.
use std::io::{BufRead,Write};
use std::os::fd::AsRawFd;
use std::os::unix::process::CommandExt;
use std::process::{Child,Command,Stdio};
#[repr(C)] struct PollFd { fd:i32, events:i16, revents:i16 }
unsafe extern "C" {fn poll(fds:*mut PollFd,n:usize,timeout:i32)->i32;
 fn prctl(option:i32,arg:usize,...)->i32;fn getppid()->i32;}
type Certificate=Vec<(usize,BigInt)>;
struct OwnedWorker {child:Child}
impl OwnedWorker {
 fn finish(&mut self)->serde_json::Value{
  use std::os::unix::process::ExitStatusExt;
  let was_running=matches!(self.child.try_wait(),Ok(None));
  let kill_error=if was_running{self.child.kill().err().map(|e|e.to_string())}else{None};
  match self.child.wait(){
   Ok(status)=>serde_json::json!({"pid":self.child.id(),"was_running":was_running,"exit_code":status.code(),"signal":status.signal(),"kill_error":kill_error}),
   Err(e)=>serde_json::json!({"pid":self.child.id(),"wait_error":e.to_string(),"kill_error":kill_error})
  }
 }
}
impl Drop for OwnedWorker {fn drop(&mut self){let _=self.finish();}}
fn wire(hyps:&[Hyp],max_var:usize)->String{
 let rows:Vec<_>=hyps.iter().map(|h|serde_json::json!([
  match h.ineq{Ineq::Lt=>"lt",Ineq::Le=>"le",Ineq::Eq=>"eq"},
  h.coeffs.iter().map(|(i,c)|serde_json::json!([i,c.to_string().parse::<serde_json::Number>().expect("exact integer")])).collect::<Vec<_>>()
 ])).collect();
 serde_json::json!({"maxVar":max_var,"hyps":rows}).to_string()
}
fn spawn_worker(mode:&str,request:&str)->std::io::Result<OwnedWorker>{
 let path=std::env::var("GPU_ARITHMETIC_RACE_WORKER")
  .map_err(|e|std::io::Error::other(e.to_string()))?;
 let mut cmd=Command::new(path);cmd.arg(mode).stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::inherit());
 let owner=std::process::id() as i32;
 unsafe{cmd.pre_exec(move||{
  if prctl(1,9)!=0 || getppid()!=owner{return Err(std::io::Error::other("race owner exited"))}
  Ok(())
 });}
 let mut owned=OwnedWorker{child:cmd.spawn()?};
 {let mut input=owned.child.stdin.take().unwrap();writeln!(input,"{request}")?;}
 Ok(owned)
}
fn checked_reply(line:&str,hyps:&[Hyp])->Option<Option<Certificate>>{
 use std::str::FromStr;
 let v:serde_json::Value=serde_json::from_str(line).ok()?;
 let c=v.get("cert")?;
 if c.is_null(){return Some(None)}
 let cert:Certificate=c.as_array()?.iter().map(|x|Some((
  x[0].as_u64()? as usize,BigInt::from_str(x[1].as_str()?).ok()?))).collect::<Option<_>>()?;
 if cert.iter().any(|(i,c)|*i>=hyps.len()||c<=&BigInt::zero()){return None}
 if verify_cert(hyps,&cert){Some(Some(cert))}else{None}
}
fn race_log(row:serde_json::Value){
 if let Ok(path)=std::env::var("GPU_ARITHMETIC_RACE_LOG"){
  use std::fs::OpenOptions;
  unsafe extern "C"{fn flock(fd:i32,op:i32)->i32;}
  if let Ok(mut f)=OpenOptions::new().create(true).append(true).open(path){
   if unsafe{flock(f.as_raw_fd(),2)}==0{let _=writeln!(f,"{row}");unsafe{flock(f.as_raw_fd(),8)};}
  }
 }
}
fn rows_of(hyps:&[Hyp])->usize{
 // Same row definition as build_fp_lp: include all represented atom keys.
 let atoms:std::collections::BTreeSet<_>=hyps.iter().flat_map(|h|h.coeffs.iter().map(|(i,_)|*i)).collect();
 atoms.len()+1
}
fn cpu_or_decline(hyps:&[Hyp],max_var:usize)->Option<Certificate>{
 if HINT_ONLY.with(|v|v.get()){None}else{produce_certificate_tiered(hyps,max_var)}
}
thread_local!{static HINT_ONLY:std::cell::Cell<bool>=const{std::cell::Cell::new(false)};}
pub fn produce_certificate_hint(hyps:&[Hyp],max_var:usize)->(Option<Certificate>,Route){
 HINT_ONLY.with(|v|v.set(true));let ans=produce_certificate_hybrid(hyps,max_var);
 HINT_ONLY.with(|v|v.set(false));ans
}
// GPU worker calls only this function, never the CPU fallback or coordinator.
pub fn race_gpu_hint(hyps:&[Hyp])->Option<Certificate>{
 let lp=build_fp_lp(hyps)?;
 let mut offsets=vec![0usize];let mut indices=Vec::new();let mut values=Vec::new();
 for row in lp.a.chunks(lp.ncols){
  for(j,&a)in row.iter().enumerate(){if a!=0.0{indices.push(j);values.push(a);}}
  offsets.push(indices.len());
 }
 let msg=serde_json::json!({"offsets":offsets,"indices":indices,"values":values,"rhs":lp.b,"ncols":lp.ncols});
 let mut sock=std::os::unix::net::UnixStream::connect(std::env::var("GPU_ARITHMETIC_SUPPORT_SOCKET").ok()?).ok()?;
 writeln!(sock,"{msg}").ok()?;sock.flush().ok()?;
 let mut reply=String::new();std::io::BufReader::new(sock).read_line(&mut reply).ok()?;
 let reply:serde_json::Value=serde_json::from_str(&reply).ok()?;
 let mu:Vec<f64>=reply.get("primal")?.as_array()?.iter().map(|x|x.as_f64()).collect::<Option<_>>()?;
 if mu.len()!=hyps.len()||mu.iter().any(|x|!x.is_finite()){return None}
 let mut tried=Vec::new();
 for att in 0..MAX_ATTEMPTS{
  let sup=support_for(hyps,&mu,att);
  if sup.is_empty()||tried.contains(&sup){continue}
  if let Some(cert)=exact_repair(hyps,&sup){if verify_cert(hyps,&cert){return Some(cert)}}
  tried.push(sup);
 }None
}
fn race_eligible(hyps:&[Hyp])->bool{
 std::env::var("GPU_ARITHMETIC_RACE_MIN_ROWS").ok().and_then(|s|s.parse::<usize>().ok())
  .is_some_and(|m|rows_of(hyps)>=m)
}
fn robust_fallback(hyps:&[Hyp],max_var:usize)->Option<Certificate>{
 cpu_or_decline(hyps,max_var)
}
fn race_search(hyps:&[Hyp],max_var:usize)->Option<Certificate>{
 let rows=rows_of(hyps);
 let start=std::time::Instant::now();let request=wire(hyps,max_var);
 let Ok(mut cpu)=spawn_worker("--cpu",&request)else{return crate::hybrid::produce_certificate_hybrid(hyps,max_var).0};
 let gpu=spawn_worker("--gpu",&request);
 let Ok(mut gpu)=gpu else{return crate::hybrid::produce_certificate_hybrid(hyps,max_var).0};
 let mut streams=[
  std::io::BufReader::new(cpu.child.stdout.take().unwrap()),
  std::io::BufReader::new(gpu.child.stdout.take().unwrap())
 ];
 let mut live=[true,true];let mut winner="failed";let mut answer=None;
 while live[0]||live[1]{
  let mut fds=[PollFd{fd:if live[0]{streams[0].get_ref().as_raw_fd()}else{-1},events:1,revents:0},
               PollFd{fd:if live[1]{streams[1].get_ref().as_raw_fd()}else{-1},events:1,revents:0}];
  if unsafe{poll(fds.as_mut_ptr(),2,-1)}<0{continue}
  for i in 0..2{
   if !live[i]||fds[i].revents==0{continue}
   let mut line=String::new();let result=streams[i].read_line(&mut line);
   live[i]=false;
   let result=result.ok().filter(|n|*n>0).and_then(|_|checked_reply(&line,hyps));
   if let Some(Some(cert))=result{answer=Some(cert);winner=if i==0{"cpu"}else{"gpu"};break}
   if i==0 && matches!(result,Some(None)){winner="cpu-no-certificate";break}
  }
  if winner!="failed"{break}
 }
 let decision_ns=start.elapsed().as_nanos();
 let cpu_pid=cpu.child.id();let gpu_pid=gpu.child.id();
 drop(streams);let gpu_exit=gpu.finish();let cpu_exit=cpu.finish();
 // Includes kill + wait; EOF cancels abandoned GPU jobs.
 let whole_ns=start.elapsed().as_nanos();
 race_log(serde_json::json!({"ty":"lp-race","pid":std::process::id(),"cpu_pid":cpu_pid,"gpu_pid":gpu_pid,
  "rows":rows,"cols":hyps.len(),"winner":winner,"decision_ns":decision_ns,"whole_ns":whole_ns,
  "retirement_ns":whole_ns-decision_ns,"cpu_exit":cpu_exit,"gpu_exit":gpu_exit}));
 if winner=="failed"{crate::hybrid::produce_certificate_hybrid(hyps,max_var).0}else{answer}
}
