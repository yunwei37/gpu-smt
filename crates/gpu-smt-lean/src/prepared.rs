//! Optional pinned-context import parent. OS children own all candidate commands.
//! This is not a generic safe fork of arbitrary threaded Lean/FFI state.
use super::{NativeRepl, classify, drain, kill_group, process_identity};
use async_trait::async_trait;
use gpu_smt_core::*;
use serde_json::Value;
use std::{
    path::PathBuf,
    process::Stdio,
    sync::atomic::{AtomicBool, AtomicU64, Ordering},
};
use tokio::{
    io::{AsyncBufReadExt, AsyncWriteExt, BufReader},
    net::UnixStream,
    process::{Child, ChildStdin, Command},
    sync::Mutex,
    task::JoinHandle,
    time::{Duration, Instant},
};
static NEXT: AtomicU64 = AtomicU64::new(1);
struct Parent {
    child: Child,
    input: Option<ChildStdin>,
    identity: ProcessIdentity,
    socket: PathBuf,
    directory: PathBuf,
    stdout: JoinHandle<String>,
    stderr: JoinHandle<String>,
}
impl Parent {
    async fn stop(mut self, force: bool) {
        if force {
            kill_group(&self.identity);
            let _ = self.child.start_kill();
        }
        self.input.take(); // EOF asks the native parent to reap owned children.
        let _ = self.child.wait().await;
        let _ = self.stdout.await;
        let _ = self.stderr.await;
        let _ = std::fs::remove_file(&self.socket);
        let _ = std::fs::remove_dir(&self.directory);
    }
}
#[derive(Default)]
struct State {
    parent: Option<Parent>,
    disabled: Option<String>,
}

/// Import-only COW backend for a pinned, audited Lean/REPL context.
///
/// The host prepares only the first source's parsed imports, without executing
/// candidate declarations. Mismatched imports use the unchanged fresh backend.
/// Native module initialization must be deterministic; a one-thread/FD check
/// alone does not prove arbitrary FFI suitable for process branching.
pub struct PreparedRepl {
    fresh: NativeRepl,
    host: PathBuf,
    sysroot: PathBuf,
    state: Mutex<State>,
    ready: AtomicBool,
}
impl PreparedRepl {
    /// Configure the matching compiled native host and SDK. No process starts here.
    pub fn new(fresh: NativeRepl, host: PathBuf, sysroot: PathBuf) -> Self {
        Self {
            fresh,
            host,
            sysroot,
            state: Mutex::new(State::default()),
            ready: AtomicBool::new(false),
        }
    }
    async fn socket(
        &self,
        c: &Candidate,
        x: &Execution,
        deadline: Instant,
    ) -> Result<PathBuf, Outcome> {
        let mut state = tokio::select! {
            v=self.state.lock()=>v,
            _=x.cancel.cancelled()=>return Err(Outcome::operational(Status::Cancelled,"preparation cancelled")),
            _=tokio::time::sleep_until(deadline)=>return Err(Outcome::operational(Status::Timeout,"preparation queue timeout")),
        };
        if let Some(reason) = &state.disabled {
            return Err(Outcome::operational(Status::BackendError, reason.clone()));
        }
        if let Some(parent) = state.parent.as_mut() {
            if matches!(parent.child.try_wait(), Ok(None)) {
                return Ok(parent.socket.clone());
            }
            self.ready.store(false, Ordering::Release);
            let parent = state.parent.take().unwrap();
            parent.stop(true).await;
            state.disabled = Some("prepared parent exited; use fresh backend".into());
            return Err(Outcome::operational(
                Status::BackendError,
                state.disabled.clone().unwrap(),
            ));
        }
        // Reject inherited fixed caps on the same path as the fresh backend.
        let mut command = Command::new(&self.host);
        if let Err(e) = super::bind(&mut command, &x.cpus) {
            return Err(Outcome::operational(Status::BackendError, e));
        }
        let directory = std::env::temp_dir().join(format!(
            "gpu-smt-prepared-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        if let Err(e) = std::fs::create_dir(&directory) {
            return Err(Outcome::operational(Status::BackendError, e.to_string()));
        }
        let socket = directory.join("control.sock");
        command
            .args([socket.as_os_str(), self.sysroot.as_os_str()])
            .current_dir(&self.fresh.project)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .kill_on_drop(true);
        let mut child = match command.spawn() {
            Ok(c) => c,
            Err(e) => {
                let _ = std::fs::remove_dir(&directory);
                state.disabled = Some(format!("prepared host cannot start: {e}"));
                return Err(Outcome::operational(Status::BackendError, e.to_string()));
            }
        };
        let Some(identity) = process_identity(child.id().unwrap()) else {
            let _ = child.start_kill();
            let _ = child.wait().await;
            let _ = std::fs::remove_dir(&directory);
            return Err(Outcome::operational(
                Status::BackendError,
                "prepared parent registration failed",
            ));
        };
        x.registry.register(identity.clone());
        let mut input = child.stdin.take().unwrap();
        let mut output = BufReader::new(child.stdout.take().unwrap());
        let errors = tokio::spawn(drain(child.stderr.take().unwrap()));
        let result = {
            let prepare = async {
                input
                    .write_all(serde_json::to_string(&c.code).unwrap().as_bytes())
                    .await
                    .map_err(|e| e.to_string())?;
                input.write_all(b"\n").await.map_err(|e| e.to_string())?;
                input.flush().await.map_err(|e| e.to_string())?;
                let mut line = String::new();
                output
                    .read_line(&mut line)
                    .await
                    .map_err(|e| e.to_string())?;
                let ready: Value = serde_json::from_str(&line).map_err(|e| e.to_string())?;
                if ready["ready"] != true
                    || ready["parent_pid"].as_u64() != Some(identity.pid as u64)
                    || ready["parent_threads"] != 1
                    || ready["preparations"] != 1
                    || ready["prepared_context"]["header_errors"] != false
                    || !ready["prepared_context"]["imported_modules"].is_u64()
                {
                    return Err("native preparation handshake mismatch".into());
                }
                x.registry.note(BackendEvent {
                    stage: "prepared_ready".into(),
                    detail: ready.to_string(),
                });
                Ok::<_, String>(())
            };
            tokio::pin!(prepare);
            tokio::select! {
                r=&mut prepare=>r.map_err(|e|Outcome::operational(Status::BackendError,e)),
                _=x.cancel.cancelled()=>Err(Outcome::operational(Status::Cancelled,"preparation cancelled")),
                _=tokio::time::sleep_until(deadline)=>Err(Outcome::operational(Status::Timeout,"native preparation timeout")),
            }
        };
        // The native import parent becomes backend-owned idle state after ready.
        // It remains in total RSS through the engine's complete owned-tree monitor.
        if let Err(mut result) = result {
            kill_group(&identity);
            let _ = child.start_kill();
            let _ = child.wait().await;
            let stderr = errors.await.unwrap_or_default();
            x.registry.unregister(&identity);
            let _ = std::fs::remove_file(&socket);
            let _ = std::fs::remove_dir(&directory);
            if result.status == Status::BackendError {
                result.error = Some(format!("{}; {}", result.error.unwrap_or_default(), stderr));
                state.disabled = result.error.clone();
            }
            return Err(result);
        }
        let stdout = tokio::spawn(drain(output.into_inner()));
        state.parent = Some(Parent {
            child,
            input: Some(input),
            identity: identity.clone(),
            socket: socket.clone(),
            directory,
            stdout,
            stderr: errors,
        });
        x.registry.unregister(&identity);
        self.ready.store(true, Ordering::Release);
        Ok(socket)
    }
    async fn branch(
        &self,
        path: PathBuf,
        c: &Candidate,
        x: &Execution,
        deadline: Instant,
    ) -> Result<Outcome, String> {
        let stream = tokio::select! {
            s=UnixStream::connect(path)=>s.map_err(|e|e.to_string())?,
            _=x.cancel.cancelled()=>return Ok(Outcome::operational(Status::Cancelled,"branch connection cancelled")),
            _=tokio::time::sleep_until(deadline)=>return Ok(Outcome::operational(Status::Timeout,"branch connection timeout")),
        };
        let (read, mut write) = stream.into_split();
        let mut lines = BufReader::new(read).lines();
        let start = tokio::select! {
            l=lines.next_line()=>l.map_err(|e|e.to_string())?,
            _=x.cancel.cancelled()=>{
                write.shutdown().await.map_err(|e|e.to_string())?;
                while lines.next_line().await.map_err(|e|e.to_string())?.is_some() {}
                return Ok(Outcome::operational(Status::Cancelled,"branch admission cancelled"));
            },
            _=tokio::time::sleep_until(deadline)=>{
                write.shutdown().await.map_err(|e|e.to_string())?;
                while lines.next_line().await.map_err(|e|e.to_string())?.is_some() {}
                return Ok(Outcome::operational(Status::Timeout,"branch admission timeout"));
            },
        }
        .ok_or("native parent closed branch before ownership")?;
        let started: Value = serde_json::from_str(&start).map_err(|e| e.to_string())?;
        let pid = started["started"]
            .as_u64()
            .and_then(|p| u32::try_from(p).ok())
            .ok_or("missing branch PID")?;
        let expected = ProcessIdentity {
            pid,
            start_ticks: started["start_ticks"]
                .as_u64()
                .ok_or("missing branch birth identity")?,
        };
        let identity = process_identity(pid)
            .filter(|p| p == &expected)
            .ok_or("native branch birth changed before registration")?;
        x.registry.register(identity.clone());
        let mut retired = false;
        let result = {
            let operation = async {
                let mask = x
                    .cpus
                    .iter()
                    .map(usize::to_string)
                    .collect::<Vec<_>>()
                    .join(",");
                write
                    .write_all(
                        format!("{mask}\n{}\n", serde_json::to_string(&c.code).unwrap()).as_bytes(),
                    )
                    .await
                    .map_err(|e| e.to_string())?;
                write.flush().await.map_err(|e| e.to_string())?;
                let native: Value = serde_json::from_str(
                    &lines
                        .next_line()
                        .await
                        .map_err(|e| e.to_string())?
                        .ok_or("missing native response")?,
                )
                .map_err(|e| e.to_string())?;
                let done: Value = serde_json::from_str(
                    &lines
                        .next_line()
                        .await
                        .map_err(|e| e.to_string())?
                        .ok_or("missing native retirement")?,
                )
                .map_err(|e| e.to_string())?;
                if !done["retired"].is_i64() {
                    return Err("missing native retirement status".into());
                }
                if let Some(peak) = done["peak_rss_bytes"].as_u64() {
                    x.registry.observe_rss(peak);
                    x.registry.note(BackendEvent {
                        stage: "rss_observation".into(),
                        detail: serde_json::json!({
                            "kind":"leader_kernel_high_water_rss",
                            "pid":identity.pid, "start_ticks":identity.start_ticks,
                            "bytes":peak,
                            "scope":"native parent wait4 leader ru_maxrss; excludes descendants and shared parent, not aggregate RSS"
                        }).to_string(),
                    });
                }
                retired = true;
                if done["retired"] != 0 {
                    return Err(format!("native child exited {}", done["retired"]));
                }
                Ok::<_, String>(native)
            };
            tokio::pin!(operation);
            tokio::select! {
                r=&mut operation=>r.map(Some),
                _=x.cancel.cancelled()=>Ok(None),
                _=tokio::time::sleep_until(deadline)=>Ok(None),
            }
        };
        if !retired {
            kill_group(&identity);
            let _ = write.shutdown().await;
            // Parent emits retirement only after waitpid; EOF also retires transport.
            while let Ok(Some(line)) = lines.next_line().await {
                if serde_json::from_str::<Value>(&line)
                    .ok()
                    .is_some_and(|v| v["retired"].is_i64())
                {
                    break;
                }
            }
        }
        x.registry.unregister(&identity);
        match result? {
            None => Ok(Outcome::operational(
                if x.cancel.is_cancelled() {
                    Status::Cancelled
                } else {
                    Status::Timeout
                },
                "prepared branch interrupted; child retired",
            )),
            Some(v) if v["fallback"] == true => {
                Err("parsed imports differ from prepared root".into())
            }
            Some(v) => v
                .get("native")
                .cloned()
                .map(classify)
                .ok_or_else(|| "missing native result".into()),
        }
    }
    async fn fallback(
        &self,
        c: &Candidate,
        x: Execution,
        deadline: Instant,
        reason: String,
    ) -> Outcome {
        tracing::info!(target:"gpu_smt_lean::prepared",reason=%reason,"use unchanged fresh native backend");
        x.registry.note(BackendEvent {
            stage: "fresh_fallback".into(),
            detail: reason,
        });

        if x.cancel.is_cancelled() {
            return Outcome::operational(Status::Cancelled, "attempt cancelled");
        }
        let ms = deadline
            .saturating_duration_since(Instant::now())
            .as_millis()
            .min(u64::MAX as u128) as u64;
        if ms == 0 {
            return Outcome::operational(
                Status::Timeout,
                "preparation/fallback exhausted request timeout",
            );
        }
        let mut c = c.clone();
        c.timeout_ms = ms;
        self.fresh.verify(&c, x).await
    }
}
#[async_trait]
impl VerificationBackend for PreparedRepl {
    fn identity(&self) -> String {
        format!(
            "prepared-imports|{:?}|{:?}|{}",
            self.host,
            self.sysroot,
            self.fresh.identity()
        )
    }
    fn prepared_state_ready(&self) -> bool {
        self.ready.load(Ordering::Acquire)
            && self.state.try_lock().ok().is_some_and(|s| {
                s.parent
                    .as_ref()
                    .is_some_and(|p| process_identity(p.identity.pid).as_ref() == Some(&p.identity))
            })
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        let deadline = Instant::now() + Duration::from_millis(c.timeout_ms);
        let path = match self.socket(c, &x, deadline).await {
            Ok(p) => p,
            Err(o) if o.status == Status::BackendError => {
                return self
                    .fallback(c, x, deadline, o.error.unwrap_or_default())
                    .await;
            }
            Err(o) => return o,
        };
        match self.branch(path, c, &x, deadline).await {
            Ok(o) => o,
            Err(e) => self.fallback(c, x, deadline, e).await,
        }
    }
    async fn shutdown(&self) {
        self.ready.store(false, Ordering::Release);
        let parent = self.state.lock().await.parent.take();
        if let Some(parent) = parent {
            parent.stop(false).await;
        }
    }
}
