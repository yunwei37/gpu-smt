//! Stock Lean REPL JSON backend. Fresh processes preserve request independence.
//! Safe prepared-state/COW implementations are separate future backends, not simulated here.

#![warn(missing_docs)]
use async_trait::async_trait;
use gpu_smt_core::*;
use serde_json::{Value, json};
use std::{path::PathBuf, process::Stdio, time::Duration};
use tokio::{
    io::{AsyncBufReadExt, AsyncReadExt, AsyncWriteExt, BufReader},
    process::Command,
};

/// Native executable, arguments and immutable project environment.
#[derive(Clone, Debug)]
pub struct NativeRepl {
    /// Actual native REPL executable.
    pub program: PathBuf,
    /// Launcher arguments, if required; no shell interpolation.
    pub args: Vec<String>,
    /// Native Lean project working directory.
    pub project: PathBuf,
    /// Toolchain/dependency identity, fixed during the engine lifetime.
    pub environment: String,
}
/// Conservative classification of actual stock REPL JSON.
pub fn classify(payload: Value) -> Outcome {
    let messages = payload.get("messages");
    let sorries = payload.get("sorries");
    let malformed =
        messages.is_some_and(|m| !m.is_array()) || sorries.is_some_and(|s| !s.is_array());
    let status = if malformed {
        Status::BackendError
    } else if payload.get("message").is_some_and(Value::is_string)
        || payload.get("error").is_some_and(Value::is_string)
        || messages.and_then(Value::as_array).is_some_and(|a| {
            a.iter()
                .any(|m| m.get("severity").and_then(Value::as_str) == Some("error"))
        })
    {
        Status::Rejected
    } else if sorries
        .and_then(Value::as_array)
        .is_some_and(|a| !a.is_empty())
        || messages.and_then(Value::as_array).is_some_and(|a| {
            a.iter().any(|m| {
                m.get("data")
                    .and_then(Value::as_str)
                    .is_some_and(|s| s.contains("declaration uses 'sorry'"))
            })
        })
    {
        Status::Incomplete
    } else if payload.get("env").and_then(Value::as_u64).is_some() {
        Status::Accepted
    } else {
        Status::BackendError
    };
    Outcome {
        status,
        response: Some(payload),
        error: None,
    }
}
async fn response(stdout: tokio::process::ChildStdout) -> Result<Value, String> {
    let mut lines = BufReader::new(stdout).lines();
    let mut text = String::new();
    while let Some(line) = lines.next_line().await.map_err(|e| e.to_string())? {
        if line.trim().is_empty() {
            if !text.is_empty() {
                return serde_json::from_str(&text).map_err(|e| format!("native JSON: {e}"));
            }
        } else {
            text.push_str(&line);
            text.push('\n');
        }
    }
    if text.is_empty() {
        Err("native EOF before response".into())
    } else {
        serde_json::from_str(&text).map_err(|e| format!("native JSON: {e}"))
    }
}
async fn drain(mut stderr: tokio::process::ChildStderr) -> String {
    // Drain to avoid pipe deadlock. Retain a labelled diagnostic tail, not unbounded stderr.
    let mut tail = Vec::new();
    let mut chunk = [0u8; 4096];
    let mut truncated = false;
    while let Ok(n) = stderr.read(&mut chunk).await {
        if n == 0 {
            break;
        }
        tail.extend_from_slice(&chunk[..n]);
        if tail.len() > 65536 {
            tail.drain(..tail.len() - 65536);
            truncated = true;
        }
    }
    let text = String::from_utf8_lossy(&tail);
    if truncated {
        format!("[stderr tail truncated] {text}")
    } else {
        text.into_owned()
    }
}
fn bind(command: &mut Command, cpus: &[usize]) -> Result<(), String> {
    if cpus.is_empty() || cpus.iter().any(|c| *c >= libc::CPU_SETSIZE as usize) {
        return Err("invalid CPU assignment".into());
    }
    // SAFETY: properly sized stack-local output; this runs before fork.
    let mut limit: libc::rlimit = unsafe { std::mem::zeroed() };
    if unsafe { libc::getrlimit(libc::RLIMIT_AS, &mut limit) } != 0 {
        return Err(std::io::Error::last_os_error().to_string());
    }
    if limit.rlim_cur != libc::RLIM_INFINITY {
        return Err("new resource point requires an uncapped parent RLIMIT_AS".into());
    }
    let cpus = cpus.to_vec();
    // SAFETY: the child callback only initializes local storage and calls
    // async-signal-safe sched_setaffinity; no heap allocation or locks after fork.
    unsafe {
        command.pre_exec(move || {
            let mut set: libc::cpu_set_t = std::mem::zeroed();
            libc::CPU_ZERO(&mut set);
            for cpu in &cpus {
                libc::CPU_SET(*cpu, &mut set);
            }
            if libc::sched_setaffinity(0, std::mem::size_of_val(&set), &set) != 0 {
                return Err(std::io::Error::last_os_error());
            }
            Ok(())
        });
    }
    command.process_group(0);
    Ok(())
}
fn kill_group(identity: &ProcessIdentity) {
    // Only signal a still-owned leader with matching kernel birth identity.
    if process_identity(identity.pid).is_some_and(|x| x == *identity) {
        // SAFETY: negative PID addresses only the process group created by us.
        unsafe {
            libc::kill(-(identity.pid as i32), libc::SIGKILL);
        }
    }
}
fn process_identity(pid: u32) -> Option<ProcessIdentity> {
    let s = std::fs::read_to_string(format!("/proc/{pid}/stat")).ok()?;
    let ticks = s
        .rsplit_once(')')?
        .1
        .split_whitespace()
        .nth(19)?
        .parse()
        .ok()?;
    Some(ProcessIdentity {
        pid,
        start_ticks: ticks,
    })
}
#[async_trait]
impl VerificationBackend for NativeRepl {
    fn identity(&self) -> String {
        format!(
            "lean-repl|{:?}|{:?}|{:?}|{}",
            self.program, self.args, self.project, self.environment
        )
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        let mut command = Command::new(&self.program);
        command
            .args(&self.args)
            .current_dir(&self.project)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .kill_on_drop(true);
        if let Err(e) = bind(&mut command, &x.cpus) {
            return Outcome::operational(Status::BackendError, e);
        }
        // Deliberately no RLIMIT_AS/per-process memory cap.
        let mut child = match command.spawn() {
            Ok(c) => c,
            Err(e) => return Outcome::operational(Status::BackendError, e.to_string()),
        };
        let pid = child.id().unwrap();
        let identity = match process_identity(pid) {
            Some(p) => p,
            None => {
                let _ = child.start_kill();
                let _ = child.wait().await;
                return Outcome::operational(
                    Status::BackendError,
                    "native process exited before ownership registration",
                );
            }
        };
        x.registry.register(identity.clone());
        let mut stdin = child.stdin.take().unwrap();
        let stderr = tokio::spawn(drain(child.stderr.take().unwrap()));
        let stdout = child.stdout.take().unwrap();
        let io = async {
            let text = serde_json::to_vec(&json!({"cmd":c.code})).map_err(|e| e.to_string())?;
            stdin.write_all(&text).await.map_err(|e| e.to_string())?;
            stdin.write_all(b"\n\n").await.map_err(|e| e.to_string())?;
            stdin.flush().await.map_err(|e| e.to_string())?;
            response(stdout).await
        };
        tokio::pin!(io);
        let mut result = tokio::select! {
            r=&mut io=>match r{Ok(value)=>classify(value),Err(e)=>Outcome::operational(Status::BackendError,e)},
            _=tokio::time::sleep(Duration::from_millis(c.timeout_ms))=>
                Outcome::operational(Status::Timeout,"native request timeout"),
            _=x.cancel.cancelled()=>Outcome::operational(Status::Cancelled,"attempt cancelled"),
        };
        if let Ok(raw) = std::fs::read_to_string(format!("/proc/{pid}/stat"))
            && let Some(tail) = raw.rsplit_once(')').map(|x| x.1)
            && let Some(pages) = tail
                .split_whitespace()
                .nth(21)
                .and_then(|x| x.parse::<u64>().ok())
        {
            // SAFETY: sysconf has no pointer arguments.
            let size = unsafe { libc::sysconf(libc::_SC_PAGESIZE) };
            if size > 0 {
                x.registry.observe_rss(pages.saturating_mul(size as u64));
            }
        }
        kill_group(&identity);
        let _ = child.start_kill();
        let _ = child.wait().await;
        let error = stderr
            .await
            .unwrap_or_else(|e| format!("stderr reader: {e}"));
        x.registry.unregister(&identity);
        if result.status == Status::BackendError && !error.is_empty() {
            result = Outcome::operational(
                if error.contains("bad_alloc") || error.contains("out of memory") {
                    Status::ResourceExhausted
                } else {
                    Status::BackendError
                },
                format!("{}; {}", result.error.unwrap_or_default(), error),
            );
        }
        result
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn admissions_and_unknown_shapes_are_never_accepted() {
        assert_eq!(
            classify(json!({"env":0,"sorries":[{}]})).status,
            Status::Incomplete
        );
        assert_eq!(
            classify(json!({"env":0,"messages":[],"sorries":[{}]})).status,
            Status::Incomplete
        );
        assert_eq!(
            classify(json!({"env":0,"messages":[{"severity":"error","data":"bad"}]})).status,
            Status::Rejected
        );
        assert_eq!(classify(json!({"env":0,"messages":[{"severity":"warning","data":"declaration uses 'sorry'"}]})).status,Status::Incomplete);
        assert_eq!(classify(json!({})).status, Status::BackendError);
        assert_eq!(
            classify(json!({"env":0,"messages":"malformed"})).status,
            Status::BackendError
        );
        assert_eq!(
            classify(json!({"env":0,"messages":[]})).status,
            Status::Accepted
        );
    }
}
