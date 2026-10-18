//! Engine "hybrid": FP64 basis identification + exact repair. Kept as the
//! measured counterfactual to the tiered engine (it LOSES on the heavy
//! tail — see the soundness note in lib.rs: FP64 evidence is a hint, never
//! an answer); not used by the daemon.
//!
//! Pipeline per instance:
//!   1. Build the certificate-space LP:
//!      one equality row per atom index present (incl. the constant atom 0),
//!      plus the normalization row  sum_{strict} mu_j = 1,  with exact
//!      per-column scaling mu_j = s_j * lambda_j, s_j = max |coeff| of hyp j,
//!      so every FP entry lies in [-1, 1] (corpus coefficients reach 607
//!      decimal digits, far beyond f64).  If any nonzero scaled coefficient
//!      is not representable as a finite nonzero f64 (overflow/underflow/
//!      conversion failure), the instance routes directly to 'tiered'.
//!   2. Solve with a small in-crate dense FP64 phase-1 simplex under Bland's
//!      rule (artificial basis; smallest-index entering among columns with
//!      negative reduced cost; min-ratio exit with smallest-basic-index
//!      tie-break).  No external LP dependency.
//!   3. Take the FP support (largest coordinates first), exact-re-solve the
//!      equality system restricted to the support with tiered-rational
//!      Gauss-Jordan elimination in the *unscaled* lambda space, pinning free
//!      columns to 0; check nonnegativity (strictness is forced by the
//!      normalization row and re-checked by the exact verifier).  On failure
//!      grow the support to the next-largest FP coordinates — max 3 support
//!      attempts — then FALL BACK to the exact 'tiered' engine.
//!
//! SOUNDNESS: a certificate is only returned after it passes the exact
//! BigRational verifier (`verify::verify_cert`); a "no certificate" answer is
//! *never* produced from FP64 information — an FP infeasibility signal is
//! only a hint, and every non-FP-certified path runs the exact tiered engine
//! for the actual answer.

use crate::rat::{self, TRat};
use crate::tiered::produce_certificate_tiered;
use crate::types::{Hyp, Ineq};
use crate::verify::verify_cert;
use num_bigint::BigInt;
use num_integer::Integer;
use num_rational::BigRational;
use num_traits::{One, Signed, ToPrimitive, Zero};
use std::collections::HashMap;

/// How the hybrid engine answered one instance (for honest reporting).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Route {
    /// Certificate found via FP support + exact repair (attempt 1..=3).
    Fp { attempts: u32 },
    /// Scaled LP not representable in finite nonzero f64 (or no strict hyp):
    /// routed directly to the exact tiered engine.
    TieredDirect,
    /// FP found a point but all support attempts failed exact repair; the
    /// exact tiered engine produced the answer.
    TieredRepairFail { attempts: u32 },
    /// FP phase-1 reported infeasible — treated as a hint only; the exact
    /// tiered engine produced the answer.
    TieredFpInfeasible,
    /// FP simplex hit the iteration cap / numeric trouble; exact tiered
    /// engine produced the answer.
    TieredFpStalled,
}

impl Route {
    /// Test-support predicate (exercised by the fallback soundness tests).
    #[cfg_attr(not(test), allow(dead_code))]
    pub fn is_fallback(&self) -> bool {
        matches!(
            self,
            Route::TieredRepairFail { .. } | Route::TieredFpStalled
        )
    }
}

const MAX_ATTEMPTS: usize = 3;
const EPS_COST: f64 = 1e-9; // entering-variable reduced-cost threshold
const EPS_PIV: f64 = 1e-11; // pivot-element threshold in the ratio test
const TOL_INFEAS: f64 = 1e-7; // phase-1 residual above this = infeasible hint
/// Relative support thresholds (vs the largest FP coordinate); one entry per
/// attempt.  0.0 = every strictly positive coordinate (last resort).
const SUPPORT_TAUS: [f64; MAX_ATTEMPTS] = [1e-6, 1e-9, 0.0];

// ---------------------------------------------------------------------------
// Step 1: exact column scaling -> dense FP LP
// ---------------------------------------------------------------------------

struct FpLp {
    /// rows = one per atom present + 1 normalization row
    nrows: usize,
    ncols: usize,
    /// row-major nrows x ncols constraint matrix (dense; entries in [-1,1])
    a: Vec<f64>,
    /// rhs: all zeros except the normalization row = 1
    b: Vec<f64>,
}

/// Exact BigInt-ratio -> f64.  Returns None unless the result is finite and
/// faithfully nonzero (a nonzero exact value that underflows to 0.0 loses the
/// constraint structure, so we refuse it and route to tiered).
fn exact_ratio_to_f64(num: &BigInt, den: &BigInt) -> Option<f64> {
    debug_assert!(den.is_positive());
    if num.is_zero() {
        return Some(0.0);
    }
    // Fast path: both fit i64 with exact f64 division for small magnitudes.
    if let (Some(n), Some(d)) = (num.to_i64(), den.to_i64())
        && n.unsigned_abs() <= (1 << 53)
        && d.unsigned_abs() <= (1 << 53)
    {
        return Some(n as f64 / d as f64);
    }
    let v = BigRational::new(num.clone(), den.clone()).to_f64()?;
    if v.is_finite() && v != 0.0 {
        Some(v)
    } else {
        None
    }
}

/// Build the column-scaled certificate-space LP.  Returns None if there is no
/// strict hypothesis (no certificate can exist — but the caller still routes
/// through the exact engine) or if some scaled coefficient is not
/// representable.
fn build_fp_lp(hyps: &[Hyp]) -> Option<FpLp> {
 let _phase=crate::phase::Guard::new("lp_float_pack");
    let n = hyps.len();
    let strict: Vec<usize> = (0..n).filter(|&j| hyps[j].ineq == Ineq::Lt).collect();
    if strict.is_empty() {
        return None;
    }
    // s_j = max |coeff| of hyp j (>= 1)
    let scales: Vec<BigInt> = hyps
        .iter()
        .map(|h| {
            h.coeffs
                .iter()
                .map(|(_, a)| a.abs())
                .max()
                .filter(|m| !m.is_zero())
                .unwrap_or_else(BigInt::one)
        })
        .collect();
    let mut atoms: Vec<usize> = hyps
        .iter()
        .flat_map(|h| h.coeffs.iter().map(|(v, _)| *v))
        .collect();
    atoms.sort_unstable();
    atoms.dedup();
    let arow: HashMap<usize, usize> = atoms.iter().enumerate().map(|(r, &a)| (a, r)).collect();
    let nrows = atoms.len() + 1;
    let mut a = vec![0.0f64; nrows * n];
    for (j, h) in hyps.iter().enumerate() {
        for (var, c) in &h.coeffs {
            if c.is_zero() {
                continue;
            }
            let v = exact_ratio_to_f64(c, &scales[j])?;
            a[arow[var] * n + j] += v;
        }
    }
    let norm = atoms.len();
    for &j in &strict {
        a[norm * n + j] = 1.0;
    }
    let mut b = vec![0.0f64; nrows];
    b[norm] = 1.0;
    Some(FpLp {
        nrows,
        ncols: n,
        a,
        b,
    })
}

// ---------------------------------------------------------------------------
// Step 2: dense FP64 phase-1 simplex, Bland's rule
// ---------------------------------------------------------------------------

enum FpResult {
    /// Feasible point mu >= 0 in scaled space.
    Feasible(Vec<f64>),
    /// Phase-1 optimum leaves artificial residual: infeasibility *hint*.
    Infeasible,
    /// Iteration cap or numeric breakdown: no usable FP information.
    Stalled,
}

fn solve_fp(lp: &FpLp) -> FpResult {
 let _phase=crate::phase::Guard::new("lp_float_solve");
    let (r, n) = (lp.nrows, lp.ncols);
    let width = n + r + 1; // structural | artificial | rhs
    let mut t = vec![0.0f64; r * width];
    let mut basis: Vec<usize> = (n..n + r).collect();
    for i in 0..r {
        for j in 0..n {
            t[i * width + j] = lp.a[i * n + j];
        }
        t[i * width + n + i] = 1.0;
        t[i * width + width - 1] = lp.b[i]; // b >= 0 by construction
    }
    // Phase-1 objective: minimize sum of artificials.  Canonical reduced-cost
    // row: z[j] = -(sum_i T[i][j]) over structural columns.
    let mut z = vec![0.0f64; width];
    for j in 0..n {
        let mut s = 0.0;
        for i in 0..r {
            s += t[i * width + j];
        }
        z[j] = -s;
    }
    // Iteration cap: Bland's rule terminates in exact arithmetic; in FP a cap
    // guards against tolerance-induced stalls.  Hitting it is a counted
    // fallback, never an answer.
    let cap = 2000 + 10 * (n + r);
    let mut scratch = vec![0.0f64; width];
    for _ in 0..cap {
        // Bland entering: smallest structural index with negative reduced
        // cost (artificials are never allowed to re-enter).
        let Some(enter) = (0..n).find(|&j| z[j] < -EPS_COST) else {
            // Optimal: measure the artificial residual.
            let mut infeas = 0.0f64;
            for i in 0..r {
                if basis[i] >= n {
                    infeas += t[i * width + width - 1].abs();
                }
            }
            if infeas > TOL_INFEAS {
                return FpResult::Infeasible;
            }
            let mut mu = vec![0.0f64; n];
            for i in 0..r {
                if basis[i] < n {
                    mu[basis[i]] = t[i * width + width - 1].max(0.0);
                }
            }
            return FpResult::Feasible(mu);
        };
        // Bland exiting: min ratio, ties by smallest basic index.
        let mut exit: Option<(f64, usize, usize)> = None; // (ratio, basis idx, row)
        for i in 0..r {
            let piv = t[i * width + enter];
            if piv > EPS_PIV {
                let ratio = t[i * width + width - 1] / piv;
                let better = match exit {
                    None => true,
                    Some((br, bb, _)) => {
                        ratio < br - 1e-12 || ((ratio - br).abs() <= 1e-12 && basis[i] < bb)
                    }
                };
                if better {
                    exit = Some((ratio, basis[i], i));
                }
            }
        }
        let Some((_, _, prow)) = exit else {
            // Phase-1 objective is bounded below by 0, so "unbounded" here
            // can only be numeric breakdown.
            return FpResult::Stalled;
        };
        // Pivot.
        let pv = t[prow * width + enter];
        scratch.copy_from_slice(&t[prow * width..(prow + 1) * width]);
        for v in scratch.iter_mut() {
            *v /= pv;
        }
        t[prow * width..(prow + 1) * width].copy_from_slice(&scratch);
        for i in 0..r {
            if i == prow {
                continue;
            }
            let f = t[i * width + enter];
            if f != 0.0 {
                for j in 0..width {
                    t[i * width + j] -= f * scratch[j];
                }
            }
        }
        let f = z[enter];
        if f != 0.0 {
            for j in 0..width {
                z[j] -= f * scratch[j];
            }
        }
        basis[prow] = enter;
    }
    FpResult::Stalled
}

// ---------------------------------------------------------------------------
// Step 3: support identification + exact tiered-rational repair
// ---------------------------------------------------------------------------

/// Exact Gauss-Jordan (tiered rationals) on the equality system restricted to
/// `support` columns in *unscaled* lambda space; free columns pinned to 0.
/// `support` must be ordered by descending FP magnitude so that the
/// large-magnitude (likely true-support) columns become basic and the
/// small/noise columns stay free at 0.  Returns a certificate candidate iff
/// the restricted system is consistent with a nonnegative solution; a
/// tampered or wrong support yields an inconsistent system or negative
/// coordinates and is rejected (None).
pub fn exact_repair(hyps: &[Hyp], support: &[usize]) -> Option<Vec<(usize, BigInt)>> {
 let _phase=crate::phase::Guard::new("exact_repair");
    let m = support.len();
    let strict_cols: Vec<usize> = (0..m)
        .filter(|&k| hyps[support[k]].ineq == Ineq::Lt)
        .collect();
    if strict_cols.is_empty() {
        return None;
    }
    // Rows: one per atom touched by the support + the normalization row
    // sum_{strict in support} lambda = 1.  Width m+1 (last = rhs).
    let mut atom_rows: HashMap<usize, Vec<TRat>> = HashMap::new();
    for (k, &j) in support.iter().enumerate() {
        for (var, c) in &hyps[j].coeffs {
            if c.is_zero() {
                continue;
            }
            let row = atom_rows
                .entry(*var)
                .or_insert_with(|| vec![TRat::zero(); m + 1]);
            row[k] = row[k].add(&TRat::from_bigint(c));
        }
    }
    let mut mat: Vec<Vec<TRat>> = atom_rows.into_values().collect();
    let mut norm = vec![TRat::zero(); m + 1];
    for &k in &strict_cols {
        norm[k] = TRat::one();
    }
    norm[m] = TRat::one();
    mat.push(norm);

    let nrows = mat.len();
    let mut pivots: Vec<(usize, usize)> = Vec::new();
    let mut prow = 0usize;
    for col in 0..m {
        let Some(pr) = (prow..nrows).find(|&r| !mat[r][col].is_zero()) else {
            continue;
        };
        mat.swap(prow, pr);
        let pv = mat[prow][col].clone();
        for e in mat[prow].iter_mut() {
            if !e.is_zero() {
                *e = e.div(&pv);
            }
        }
        for r2 in 0..nrows {
            if r2 == prow || mat[r2][col].is_zero() {
                continue;
            }
            let f = mat[r2][col].clone();
            // index loop on purpose: reads mat[prow] while writing mat[r2]
            #[allow(clippy::needless_range_loop)]
            for c2 in 0..=m {
                if !mat[prow][c2].is_zero() {
                    let delta = f.mul(&mat[prow][c2]);
                    mat[r2][c2] = mat[r2][c2].sub(&delta);
                }
            }
        }
        pivots.push((prow, col));
        prow += 1;
        if prow == nrows {
            break;
        }
    }
    // Inconsistent restricted system (e.g. tampered/short support) -> reject.
    if mat[prow..nrows].iter().any(|row| !row[m].is_zero()) {
        return None;
    }
    let mut sol = vec![TRat::zero(); m];
    for &(r, c) in &pivots {
        sol[c] = mat[r][m].clone();
    }
    if sol.iter().any(|v| v.is_negative()) {
        return None;
    }
    // Clear denominators; keep positive entries mapped back to hyp indices.
    let vals: Vec<BigRational> = sol.iter().map(|v| v.to_bigrational()).collect();
    let mut den = BigInt::one();
    for v in &vals {
        den = den.lcm(v.denom());
    }
    let den = BigRational::from(den);
    let mut cert: Vec<(usize, BigInt)> = Vec::new();
    for (k, v) in vals.into_iter().enumerate() {
        let scaled = v * &den;
        debug_assert!(scaled.is_integer());
        let w = scaled.to_integer();
        if w.is_positive() {
            cert.push((support[k], w));
        }
    }
    cert.sort_unstable_by_key(|&(j, _)| j);
    if cert.is_empty() { None } else { Some(cert) }
}

/// Support for attempt `att`: coordinates above SUPPORT_TAUS[att] * max(mu),
/// ordered by descending magnitude (ties by index), always containing at
/// least one strict column (the largest-mu strict one).
fn support_for(hyps: &[Hyp], mu: &[f64], att: usize) -> Vec<usize> {
    let mu_max = mu.iter().cloned().fold(0.0f64, f64::max);
    let tau = SUPPORT_TAUS[att] * mu_max;
    let mut sup: Vec<usize> = (0..mu.len())
        .filter(|&j| mu[j] > tau && mu[j] > 0.0)
        .collect();
    if !sup.iter().any(|&j| hyps[j].ineq == Ineq::Lt)
        && let Some(best) = (0..mu.len())
            .filter(|&j| hyps[j].ineq == Ineq::Lt)
            .max_by(|&a, &b| mu[a].total_cmp(&mu[b]))
    {
        sup.push(best);
    }
    sup.sort_unstable_by(|&a, &b| mu[b].total_cmp(&mu[a]).then(a.cmp(&b)));
    sup
}

// ---------------------------------------------------------------------------
// Engine entry point
// ---------------------------------------------------------------------------

pub fn produce_certificate_hybrid(
    hyps: &[Hyp],
    max_var: usize,
) -> (Option<Vec<(usize, BigInt)>>, Route) {
    let result = (|| {
        let Some(lp) = build_fp_lp(hyps) else {
            return (
                robust_fallback(hyps, max_var),
                Route::TieredDirect,
            );
        };
        match solve_fp(&lp) {
            FpResult::Feasible(mu) => {
                let mut tried: Vec<Vec<usize>> = Vec::new();
                let mut attempts = 0u32;
                for att in 0..MAX_ATTEMPTS {
                    let sup = support_for(hyps, &mu, att);
                    if sup.is_empty() || tried.contains(&sup) {
                        continue;
                    }
                    attempts += 1;
                    if let Some(cert) = exact_repair(hyps, &sup) {
                        // SOUNDNESS GATE: exact BigRational verifier.
                        if verify_cert(hyps, &cert) {
                            return (Some(cert), Route::Fp { attempts });
                        }
                    }
                    tried.push(sup);
                }
                (
                    robust_fallback(hyps, max_var),
                    Route::TieredRepairFail { attempts },
                )
            }
            // FP infeasibility is only a hint: the exact engine answers.
            FpResult::Infeasible => (
                robust_fallback(hyps, max_var),
                Route::TieredFpInfeasible,
            ),
            FpResult::Stalled => (
                robust_fallback(hyps, max_var),
                Route::TieredFpStalled,
            ),
        }
    })();
    rat::flush_tls();
    result
}

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
thread_local!{static CONTEXT:std::cell::RefCell<serde_json::Value>=const{std::cell::RefCell::new(serde_json::Value::Null)};}
pub fn set_context(v:&serde_json::Value){
 CONTEXT.with(|c|*c.borrow_mut()=serde_json::json!({"source":v.get("source"),"call_id":v.get("call_id")}));
}
pub(crate) fn context()->serde_json::Value{CONTEXT.with(|c|c.borrow().clone())}

struct OwnedWorker {child:Child,retired:Option<serde_json::Value>}
impl OwnedWorker {
 fn finish(&mut self)->serde_json::Value{
  use std::os::unix::process::ExitStatusExt;
  if let Some(v)=&self.retired{return v.clone()}
  let pid=self.child.id();let mut raw=0;let mut usage=crate::phase::Usage::default();
  let wait=|options,raw:&mut i32,usage:&mut crate::phase::Usage|->std::io::Result<i32>{
   loop{let v=unsafe{crate::phase::wait4(pid as i32,raw,options,usage)};
    if v>=0{return Ok(v)}let e=std::io::Error::last_os_error();if e.kind()!=std::io::ErrorKind::Interrupted{return Err(e)}
   }
  };
  let first=wait(1,&mut raw,&mut usage);let was_running=matches!(first,Ok(0));
  let kill_error=if was_running{self.child.kill().err().map(|e|e.to_string())}else{None};
  let result=if was_running{wait(0,&mut raw,&mut usage)}else{first};
  let value=match result{
   Ok(v)if v==pid as i32=>{
    let status=std::process::ExitStatus::from_raw(raw);
    serde_json::json!({"pid":pid,"was_running":was_running,"exit_code":status.code(),"signal":status.signal(),"kill_error":kill_error,
     "wait4_user_cpu_ns":crate::phase::cpu_ns(&usage.user),"wait4_system_cpu_ns":crate::phase::cpu_ns(&usage.system),"wait4_maxrss_kib":usage.counters[0]})
   },
   Ok(v)=>serde_json::json!({"pid":pid,"wait_error":format!("unexpected wait4 PID {v}"),"kill_error":kill_error}),
   Err(e)=>serde_json::json!({"pid":pid,"wait_error":e.to_string(),"kill_error":kill_error})
  };
  self.retired=Some(value.clone());value
 }
}
impl Drop for OwnedWorker {fn drop(&mut self){let _=self.finish();}}
fn wire(hyps:&[Hyp],max_var:usize)->String{
 let rows:Vec<_>=hyps.iter().map(|h|serde_json::json!([
  match h.ineq{Ineq::Lt=>"lt",Ineq::Le=>"le",Ineq::Eq=>"eq"},
  h.coeffs.iter().map(|(i,c)|serde_json::json!([i,c.to_string().parse::<serde_json::Number>().expect("exact integer")])).collect::<Vec<_>>()
 ])).collect();
 serde_json::json!({"maxVar":max_var,"hyps":rows,"source":context()["source"],"call_id":context()["call_id"]}).to_string()
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
 let mut owned=OwnedWorker{child:cmd.spawn()?,retired:None};
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
 let _phase=crate::phase::Guard::new("external_hint_total");
 let lp=build_fp_lp(hyps)?;
 let mut offsets=vec![0usize];let mut indices=Vec::new();let mut values=Vec::new();
 for row in lp.a.chunks(lp.ncols){
  for(j,&a)in row.iter().enumerate(){if a!=0.0{indices.push(j);values.push(a);}}
  offsets.push(indices.len());
 }
 let msg=serde_json::json!({"offsets":offsets,"indices":indices,"values":values,"rhs":lp.b,"ncols":lp.ncols,"source":context()["source"],"call_id":context()["call_id"]});
 let transport=crate::phase::Guard::new("external_transport");
 let mut sock=std::os::unix::net::UnixStream::connect(std::env::var("GPU_ARITHMETIC_SUPPORT_SOCKET").ok()?).ok()?;
 writeln!(sock,"{msg}").ok()?;sock.flush().ok()?;
 let mut reply=String::new();std::io::BufReader::new(sock).read_line(&mut reply).ok()?;
 drop(transport);
 let reply:serde_json::Value=serde_json::from_str(&reply).ok()?;
 if let Some(values)=reply.get("dual_ray").and_then(|v|v.as_array()).and_then(|xs|xs.iter().map(|x|x.as_f64()).collect::<Option<Vec<_>>>()){
  if let Some(ray)=repair_negative_ray(hyps,&values){
   NEGATIVE_CERTIFICATE.with(|c|*c.borrow_mut()=Some(ray));return None;
  }
 }
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
 if race_eligible(hyps){
  if std::env::var_os("GPU_ARITHMETIC_RACE_CPU_ONLY").is_some(){
   produce_certificate_tiered(hyps,max_var)
  }else{race_search(hyps,max_var)}
 }else{cpu_or_decline(hyps,max_var)}
}
fn race_search(hyps:&[Hyp],max_var:usize)->Option<Certificate>{
 let _phase=crate::phase::Guard::new("race_total");
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

// Two-sided oracle capability. A negative search answer needs an exact dual
// certificate for the same scaled LP,never a floating solver status.
thread_local!{static NEGATIVE_CERTIFICATE:std::cell::RefCell<Option<Vec<BigRational>>>=const{std::cell::RefCell::new(None)};}
pub fn take_negative_certificate()->Option<Vec<String>>{
 NEGATIVE_CERTIFICATE.with(|c|c.borrow_mut().take().map(|v|v.into_iter().map(|x|x.to_string()).collect()))
}
fn verify_negative_certificate(hyps:&[Hyp],ray:&[BigRational])->bool{
 let _phase=crate::phase::Guard::new("exact_negative_verify");
 let mut atoms:Vec<usize>=hyps.iter().flat_map(|h|h.coeffs.iter().map(|(i,_)|*i)).collect();
 atoms.sort_unstable();atoms.dedup();
 if ray.len()!=atoms.len()+1||!ray[atoms.len()].is_negative(){return false}
 let row:HashMap<usize,usize>=atoms.iter().enumerate().map(|(i,v)|(*v,i)).collect();
 for h in hyps{
  let scale=h.coeffs.iter().map(|(_,c)|c.abs()).max().filter(|x|!x.is_zero()).unwrap_or_else(BigInt::one);
  let mut sum=BigRational::zero();
  for(v,c)in &h.coeffs{sum+=&ray[row[v]]*BigRational::from_integer(c.clone());}
  if h.ineq==Ineq::Lt{sum+=&ray[atoms.len()]*BigRational::from_integer(scale);}
  if sum.is_negative(){return false}
 }
 true
}
fn repair_negative_ray(hyps:&[Hyp],values:&[f64])->Option<Vec<BigRational>>{
 let _phase=crate::phase::Guard::new("exact_negative_repair");
 let norm=*values.last()?;
 if norm==0.||!norm.is_finite()||values.iter().any(|x|!x.is_finite()){return None}
 let mut ray=values.iter().map(|x|{
  approximate_ray_coordinate(-x/norm)
 }).collect::<Option<Vec<_>>>()?;
 *ray.last_mut()?=-BigRational::one();
 if verify_negative_certificate(hyps,&ray){Some(ray)}else{None}
}
fn checked_negative_reply(line:&str,hyps:&[Hyp])->bool{
 use std::str::FromStr;
 let Ok(v)=serde_json::from_str::<serde_json::Value>(line)else{return false};
 let Some(xs)=v.get("infeasible_certificate").and_then(|v|v.as_array())else{return false};
 let ray=xs.iter().map(|x|BigRational::from_str(x.as_str()?).ok()).collect::<Option<Vec<_>>>();
 ray.is_some_and(|ray|verify_negative_certificate(hyps,&ray))
}

// Solver rays contain numerical noise. Reconstruct a nearby simple rational;
// every resulting coefficient is subsequently checked with original BigInts.
fn approximate_ray_coordinate(x:f64)->Option<BigRational>{
 if !x.is_finite(){return None}
 let sign=if x<0.{-1}else{1};let target=x.abs();let mut z=target;
 let(mut p0,mut p1,mut q0,mut q1)=(0i64,1i64,1i64,0i64);
 loop{
  let whole=z.floor();if whole>=i64::MAX as f64{return None}
  let a=whole as i64;
  let p=a.checked_mul(p1)?.checked_add(p0)?;
  let q=a.checked_mul(q1)?.checked_add(q0)?;
  if q==0{return None}
  let remainder=z-whole;
  if (p as f64/q as f64-target).abs()<=1e-9*(1.+target)||remainder==0.{
   return Some(BigRational::new(BigInt::from(p)*BigInt::from(sign),BigInt::from(q)))
  }
  p0=p1;p1=p;q0=q1;q1=q;z=1./remainder;
 }
}
