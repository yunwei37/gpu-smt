from pathlib import Path
import shutil,os,subprocess,resource,json,datetime
R=Path('/workspaces/repository')
A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-cpu-gpu-portfolio'
B=Path('/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/strong-cpu-gpu-portfolio')
os.sched_setaffinity(0,{4,5,6,7});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
U.mkdir(exist_ok=False)
shutil.copytree(B/'native',U/'native',ignore=shutil.ignore_patterns('target','.git'))
s=(B/'native/src/race.rs').read_text()
start=s.index('fn race_search(hyps:&[Hyp],max_var:usize)->Option<Certificate>{')
end=s.index('// Two-sided oracle capability.',start)
replacement=r'''fn race_search(hyps:&[Hyp],max_var:usize)->Option<Certificate>{
 let rows=rows_of(hyps);let start=std::time::Instant::now();let request=wire(hyps,max_var);
 let Ok(cpu)=spawn_worker("--cpu",&request)else{return crate::hybrid::produce_certificate_hybrid(hyps,max_var).0};
 let Ok(gpu)=spawn_worker("--gpu",&request)else{return crate::hybrid::produce_certificate_hybrid(hyps,max_var).0};
 let mut workers=vec![cpu,gpu];let mut labels=vec!["cpu","gpu"];
 let mut strong_cpu_spawn_error=None;
 if std::env::var_os("GPU_ARITHMETIC_STRONG_CPU_SOCKET").is_some(){
  match spawn_worker("--cpu-highs",&request){
   Ok(worker)=>{workers.push(worker);labels.push("cpu-highs");}
   Err(error)=>strong_cpu_spawn_error=Some(error.to_string())
  }
 }
 let mut streams:Vec<_>=workers.iter_mut().map(|w|std::io::BufReader::new(w.child.stdout.take().unwrap())).collect();
 let mut live=vec![true;workers.len()];let mut winner="failed";let mut answer=None;
 while live.iter().any(|&x|x){
  let mut fds:Vec<_>=streams.iter().enumerate().map(|(i,s)|PollFd{fd:if live[i]{s.get_ref().as_raw_fd()}else{-1},events:1,revents:0}).collect();
  if unsafe{poll(fds.as_mut_ptr(),fds.len(),-1)}<0{continue}
  for i in 0..streams.len(){
   if !live[i]||fds[i].revents==0{continue}
   let mut line=String::new();let result=streams[i].read_line(&mut line);live[i]=false;
   let result=result.ok().filter(|n|*n>0).and_then(|_|checked_reply(&line,hyps));
   if let Some(Some(cert))=result{answer=Some(cert);winner=labels[i];break}
   if i!=0&&matches!(result,Some(None))&&checked_negative_reply(&line,hyps){
    winner=if labels[i]=="gpu"{"external-infeasible"}else{"cpu-highs-infeasible"};break
   }
   if i==0&&matches!(result,Some(None)){winner="cpu-no-certificate";break}
  }
  if winner!="failed"{break}
 }
 let decision_ns=start.elapsed().as_nanos();let pids:Vec<_>=workers.iter().map(|w|w.child.id()).collect();
 drop(streams);let exits:Vec<_>=workers.iter_mut().map(OwnedWorker::finish).collect();
 let whole_ns=start.elapsed().as_nanos();
 race_log(serde_json::json!({"ty":"lp-race","pid":std::process::id(),"cpu_pid":pids[0],"gpu_pid":pids[1],
  "strong_cpu_pid":pids.get(2),"strong_cpu_spawn_error":strong_cpu_spawn_error,
  "source":context()["source"],"call_id":context()["call_id"],"rows":rows,"cols":hyps.len(),
  "winner":winner,"decision_ns":decision_ns,"whole_ns":whole_ns,"retirement_ns":whole_ns-decision_ns,
  "cpu_exit":exits[0],"gpu_exit":exits[1],"strong_cpu_exit":exits.get(2)}));
 if winner=="failed"{crate::hybrid::produce_certificate_hybrid(hyps,max_var).0}else{answer}
}

'''
s=s[:start]+replacement+s[end:]
(U/'native/src/race.rs').write_text(s);(A/'race.rs').write_text(s)
worker=(B/'native/src/bin/farkas-race-worker.rs').read_text()
worker=worker.replace('let mode=std::env::args().nth(1);let gpu=mode.as_deref()==Some("--gpu");',r'''let mode=std::env::args().nth(1);
 let gpu=matches!(mode.as_deref(),Some("--gpu"|"--cpu-highs"));
 if mode.as_deref()==Some("--cpu-highs"){
  let path=std::env::var("GPU_ARITHMETIC_STRONG_CPU_SOCKET").expect("prepared strong CPU numeric proxy");
  unsafe{std::env::set_var("GPU_ARITHMETIC_SUPPORT_SOCKET",path);}
 }''')
(U/'native/src/bin/farkas-race-worker.rs').write_text(worker);(A/'race-worker.rs').write_text(worker)
# Compiled verifier modules are read-only symlinks; only private numeric bins differ.
for name in ['GpuArithmetic','batch-oracle.so','cuopt-grpc','repl-candidate-timing']:
 (U/name).symlink_to((B/name).resolve(),target_is_directory=(B/name).is_dir())
env=dict(os.environ,PATH='/usr/local/cargo/bin:'+os.environ['PATH'],CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup')
cmd=['cargo','build','--release','--offline','--locked','--bin','arithmetic-batchd','--bin','farkas-batchd','--bin','farkas-race-worker']
p=subprocess.run(cmd,cwd=U/'native',env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(A/'build.log').write_text(p.stdout)
(A/'build-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd,'exit':p.returncode,'source':str(B/'native'),'private_build':str(U/'native'),'unchanged_Lean_modules':str(B/'GpuArithmetic')},indent=2)+'\n')
print(p.stdout[-4000:],flush=True)
if p.returncode:raise SystemExit(p.returncode)
for name in ['arithmetic-batchd','farkas-batchd','farkas-race-worker']:shutil.copy2(U/'native/target/release'/name,U/name)
print('BUILD_COMPLETE',flush=True)
