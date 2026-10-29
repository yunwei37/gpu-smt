//! Stock Lean REPL JSON and source frontend backends. Fresh processes preserve independence.
//! Optional pinned-context import preparation lives in PreparedRepl; qualification is explicit.

#![warn(missing_docs)]
mod prepared;
mod source;
use async_trait::async_trait;
use gpu_smt_core::*;
pub use prepared::PreparedRepl;
use serde_json::{Value, json};
pub use source::{ConfiguredLean, NativeLean, classify_source};
use std::{future::Future, path::PathBuf, process::Stdio, time::Duration};
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
    // Only interpreted diagnostic fields are constrained; native metadata stays
    // untouched. An unknown entry must not disappear into a cacheable verdict.
    let malformed = messages.is_some_and(|m| {
        m.as_array().is_none_or(|entries| {
            entries.iter().any(|entry| {
                !matches!(
                    entry.get("severity").and_then(Value::as_str),
                    Some("trace" | "info" | "warning" | "error")
                ) || !entry.get("data").is_some_and(Value::is_string)
            })
        })
    }) || sorries.is_some_and(|s| !s.is_array())
        || ["message", "error"]
            .iter()
            .any(|field| payload.get(field).is_some_and(|v| !v.is_string()));
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
        error: malformed.then(|| "malformed native REPL diagnostics".into()),
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
// A non-yielding decoder can finish after the timer's deadline within one
// poll. Check the completion instant as well as racing the asynchronous timer.
async fn request_io<T>(
    io: impl Future<Output = T>,
    cancelled: impl Future<Output = ()>,
    deadline: tokio::time::Instant,
) -> Result<T, Status> {
    tokio::select! {
        result = io => {
            if tokio::time::Instant::now() > deadline {
                Err(Status::Timeout)
            } else {
                Ok(result)
            }
        },
        _ = tokio::time::sleep_until(deadline) => Err(Status::Timeout),
        _ = cancelled => Err(Status::Cancelled),
    }
}

async fn drain<R: tokio::io::AsyncRead + Unpin>(mut stderr: R) -> String {
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
fn observe_current_rss(identity: &ProcessIdentity, registry: &dyn ProcessRegistry) {
    if let Ok(raw) = std::fs::read_to_string(format!("/proc/{}/stat", identity.pid))
        && let Some(tail) = raw.rsplit_once(')').map(|x| x.1)
        && tail
            .split_whitespace()
            .nth(19)
            .and_then(|s| s.parse::<u64>().ok())
            == Some(identity.start_ticks)
        && let Some(pages) = tail
            .split_whitespace()
            .nth(21)
            .and_then(|x| x.parse::<u64>().ok())
    {
        // SAFETY: sysconf has no pointer arguments.
        let size = unsafe { libc::sysconf(libc::_SC_PAGESIZE) };
        if size > 0 {
            let bytes = pages.saturating_mul(size as u64);
            registry.observe_rss(bytes);
            registry.note(BackendEvent {
                    stage: "rss_observation".into(),
                    detail: json!({
                        "kind":"leader_current_rss", "pid":identity.pid,
                        "start_ticks":identity.start_ticks, "bytes":bytes,
                        "scope":"birth-matched proc stat before retirement; not a high-water or whole-tree sample"
                    }).to_string(),
                });
        }
    }
}
#[async_trait]
impl VerificationBackend for NativeRepl {
    fn request_resource_preemption(&self, processes: &[ProcessIdentity]) {
        for identity in processes {
            kill_group(identity);
        }
    }
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
            // This backend owns one fresh process per command. EOF allows
            // upstream versions without an explicit stdout flush to exit and
            // flush their complete reply instead of waiting for a second input.
            drop(stdin);
            response(stdout).await
        };
        let deadline = tokio::time::Instant::now() + Duration::from_millis(c.timeout_ms);
        let mut result = match request_io(io, x.cancel.cancelled(), deadline).await {
            Ok(Ok(value)) => classify(value),
            Ok(Err(error)) => Outcome::operational(Status::BackendError, error),
            Err(Status::Timeout) => Outcome::operational(Status::Timeout, "native request timeout"),
            Err(status) => Outcome::operational(status, "attempt cancelled"),
        };
        observe_current_rss(&identity, x.registry.as_ref());
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
    fn malformed_diagnostic_entries_are_operational_and_not_cacheable() {
        for message in [
            json!(null),
            json!("unparsed diagnostic"),
            json!({}),
            json!({"severity": "fatal", "data": "unknown severity"}),
            json!({"severity": 1, "data": "wrong type"}),
            json!({"severity": "warning", "data": null}),
            json!({"severity": "warning"}),
        ] {
            let payload = json!({"env": 0, "messages": [message]});
            let result = classify(payload.clone());
            assert_eq!(result.status, Status::BackendError, "{payload}");
            assert!(!result.cacheable(), "{payload}");
            assert_eq!(result.response, Some(payload));
            assert!(result.error.is_some());
        }
        let mixed = json!({"env": 0, "messages": [
            {"severity": "error", "data": "earlier error"}, null
        ]});
        assert_eq!(classify(mixed).status, Status::BackendError);
        for field in ["message", "error"] {
            let mut payload = json!({"env": 0});
            payload[field] = json!(false);
            assert_eq!(classify(payload).status, Status::BackendError);
        }
        for severity in ["trace", "info", "warning", "error"] {
            let payload = json!({"env": 0, "messages": [
                {"severity": severity, "data": "native message", "pos": {"line": 1, "column": 0}}
            ]});
            let result = classify(payload.clone());
            assert_eq!(
                result.status,
                if severity == "error" {
                    Status::Rejected
                } else {
                    Status::Accepted
                }
            );
            assert_eq!(result.response, Some(payload));
        }
    }

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

#[cfg(test)]
mod native_reply_deadline_tests {
    use super::*;
    use std::{future::pending, task::Poll};
    use tokio::time::{Instant, advance};
    use tokio_util::sync::CancellationToken;

    // Advance the paused test clock inside a single IO poll. Like synchronous
    // JSON decoding, the poll completes without letting the timer run first.
    // This fixture models scheduling only; it is not Lean or a measured decode.
    async fn non_yielding_reply(value: Result<Value, String>) -> Result<Value, String> {
        let advancing = advance(Duration::from_secs(2));
        tokio::pin!(advancing);
        std::future::poll_fn(|cx| {
            let _ = advancing.as_mut().poll(cx);
            Poll::Ready(())
        })
        .await;
        value
    }

    #[tokio::test(start_paused = true)]
    async fn non_yielding_decode_cannot_accept_a_reply_after_the_original_budget() {
        let cancel = CancellationToken::new();
        let started = Instant::now();
        let io = non_yielding_reply(Ok(json!({"env": 0})));
        tokio::pin!(io);
        // Exact prior selection behavior, retained as a negative control.
        let previous = tokio::select! {
            r = &mut io => match r {
                Ok(value) => classify(value),
                Err(error) => Outcome::operational(Status::BackendError, error),
            },
            _ = tokio::time::sleep(Duration::from_secs(1)) =>
                Outcome::operational(Status::Timeout, "native request timeout"),
            _ = cancel.cancelled() =>
                Outcome::operational(Status::Cancelled, "attempt cancelled"),
        };
        assert!(Instant::now() > started + Duration::from_secs(1));
        assert_eq!(
            previous.status,
            Status::Accepted,
            "negative control did not engage"
        );

        for value in [
            Ok(json!({"env": 0})),
            Ok(json!({"env": 0, "messages": [{"severity": "error", "data": "fixture"}]})),
            Ok(json!({"env": 0, "sorries": [{}]})),
            Err("late JSON decoding error".into()),
        ] {
            let deadline = Instant::now() + Duration::from_secs(1);
            let current = request_io(non_yielding_reply(value), cancel.cancelled(), deadline).await;
            assert!(
                Instant::now() > deadline,
                "single-poll clock control did not engage"
            );
            assert!(matches!(current, Err(Status::Timeout)));
        }
    }

    #[tokio::test(start_paused = true)]
    async fn timely_json_and_operational_outcomes_retain_their_contract() {
        let cancel = CancellationToken::new();
        for (payload, expected) in [
            (json!({"env": 0}), Status::Accepted),
            (
                json!({"env": 0, "messages": [{"severity": "error", "data": "fixture"}]}),
                Status::Rejected,
            ),
            (json!({"env": 0, "sorries": [{}]}), Status::Incomplete),
        ] {
            let actual = request_io(
                async { Ok::<Value, String>(payload.clone()) },
                cancel.cancelled(),
                Instant::now() + Duration::from_secs(1),
            )
            .await;
            let actual = classify(actual.unwrap().unwrap());
            assert_eq!(actual.status, expected);
            assert_eq!(actual.response, Some(payload));
        }
        let error = request_io(
            async { Err::<Value, String>("JSON failure".into()) },
            cancel.cancelled(),
            Instant::now() + Duration::from_secs(1),
        )
        .await;
        assert_eq!(error.unwrap().unwrap_err(), "JSON failure");

        let timeout = request_io(
            pending::<Result<Value, String>>(),
            cancel.cancelled(),
            Instant::now() + Duration::from_secs(1),
        )
        .await;
        assert!(matches!(timeout, Err(Status::Timeout)));
        cancel.cancel();
        let cancelled = request_io(
            pending::<Result<Value, String>>(),
            cancel.cancelled(),
            Instant::now() + Duration::from_secs(1),
        )
        .await;
        assert!(matches!(cancelled, Err(Status::Cancelled)));
    }
}

#[cfg(test)]
mod resource_preemption_tests {
    use super::*;
    #[test]
    fn native_resource_hooks_signal_only_birth_matched_owned_groups_without_a_runtime() {
        use std::io::{BufRead, BufReader};
        use std::os::unix::process::{CommandExt, ExitStatusExt};
        use std::process::{Child, Command, Stdio};

        struct OwnedChild(Child);
        impl Drop for OwnedChild {
            fn drop(&mut self) {
                let _ = self.0.kill();
                let _ = self.0.wait();
            }
        }
        fn child() -> OwnedChild {
            let mut process = Command::new("/usr/bin/python3");
            process
                .args(["-u", "-c", "import time; print('ready'); time.sleep(60)"])
                .process_group(0)
                .stdout(Stdio::piped())
                .stderr(Stdio::null());
            let mut process = OwnedChild(process.spawn().unwrap());
            let mut ready = String::new();
            BufReader::new(process.0.stdout.take().unwrap())
                .read_line(&mut ready)
                .unwrap();
            assert_eq!(ready.trim(), "ready");
            process
        }

        let fresh = NativeRepl {
            program: "/usr/bin/python3".into(),
            args: vec![],
            project: std::env::temp_dir(),
            environment: "synchronous-owned-group-control-not-Lean".into(),
        };
        let source = super::NativeLean {
            program: "/usr/bin/python3".into(),
            project: std::env::temp_dir(),
            environment: "synchronous-source-owned-group-control-not-Lean".into(),
        };
        let providers: Vec<Box<dyn VerificationBackend>> = vec![
            Box::new(fresh.clone()),
            Box::new(super::PreparedRepl::new(
                fresh,
                "/unused-prepared-host".into(),
                "/unused-sysroot".into(),
            )),
            Box::new(source.clone()),
            Box::new(source.with_args(vec!["--unused-test-identity".into()])),
        ];
        let mut sentinel = child();
        for provider in providers {
            let mut target = child();
            let identity = gpu_smt_engine::linux::identity(target.0.id()).unwrap();
            let wrong_birth = ProcessIdentity {
                pid: identity.pid,
                start_ticks: identity.start_ticks + 1,
            };
            provider.request_resource_preemption(&[wrong_birth]);
            assert!(
                target.0.try_wait().unwrap().is_none(),
                "stale birth was signalled"
            );
            provider.request_resource_preemption(&[identity]);
            let deadline = std::time::Instant::now() + Duration::from_secs(2);
            let status = loop {
                if let Some(status) = target.0.try_wait().unwrap() {
                    break status;
                }
                assert!(
                    std::time::Instant::now() < deadline,
                    "owned group was not interrupted"
                );
                std::thread::sleep(Duration::from_millis(5));
            };
            assert_eq!(status.signal(), Some(libc::SIGKILL));
            assert!(
                sentinel.0.try_wait().unwrap().is_none(),
                "unrequested group was signalled"
            );
        }
    }
}
