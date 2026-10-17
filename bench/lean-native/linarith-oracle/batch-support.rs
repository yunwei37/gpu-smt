// Robust support hints extend the pinned upstream hybrid engine.
// Direct AST mode may decline without exact search; Lean then uses its strong
// fallback. Native fallback mode retains the exact tiered engine on all misses.
// Returned coefficients always pass exact repair and verify_cert, followed by
// Lean proof reconstruction. Route's historical Tiered* labels are not solver
// attribution; backend invocation/termination records provide that evidence.

thread_local! { static HINT_ONLY: std::cell::Cell<bool> = const { std::cell::Cell::new(false) }; }
pub fn produce_certificate_hint(hyps:&[Hyp],max_var:usize)->(Option<Vec<(usize,BigInt)>>,Route){
 HINT_ONLY.with(|v|v.set(true));
 let answer=produce_certificate_hybrid(hyps,max_var);
 HINT_ONLY.with(|v|v.set(false));answer
}
fn robust_fallback(hyps:&[Hyp],max_var:usize)->Option<Vec<(usize,BigInt)>>{
 let hint=(||{
  let lp=build_fp_lp(hyps)?;
  let mut offsets=vec![0usize];let mut indices=Vec::new();let mut values=Vec::new();
  for row in lp.a.chunks(lp.ncols){for(j,&a)in row.iter().enumerate(){if a!=0.0{indices.push(j);values.push(a);}}offsets.push(indices.len());}
  let msg=serde_json::json!({"offsets":offsets,"indices":indices,"values":values,"rhs":lp.b,"ncols":lp.ncols});
  use std::io::{BufRead,Write};
  let mut sock=std::os::unix::net::UnixStream::connect(std::env::var("GPU_ARITHMETIC_SUPPORT_SOCKET").ok()?).ok()?;
  writeln!(sock,"{}",msg).ok()?;sock.flush().ok()?;
  let mut response=String::new();std::io::BufReader::new(sock).read_line(&mut response).ok()?;
  let reply:serde_json::Value=serde_json::from_str(&response).ok()?;
  let mu:Vec<f64>=reply.get("primal")?.as_array()?.iter().map(|x|x.as_f64()).collect::<Option<_>>()?;
  if mu.len()!=hyps.len()||mu.iter().any(|x|!x.is_finite()){return None}
  let mut tried=Vec::new();
  for att in 0..MAX_ATTEMPTS{
   let sup=support_for(hyps,&mu,att);
   if sup.is_empty()||tried.contains(&sup){continue}
   if let Some(cert)=exact_repair(hyps,&sup){if verify_cert(hyps,&cert){return Some(cert)}}
   tried.push(sup);
  }None
 })();
 hint.or_else(||if HINT_ONLY.with(|v|v.get()){None}else{produce_certificate_tiered(hyps,max_var)})
}
