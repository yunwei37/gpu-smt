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
    fn observe_retirement(done: &Value, identity: &ProcessIdentity, x: &Execution) {
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
        let mut received_native = None;
        let mut reply_before_deadline = false;
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
                reply_before_deadline = Instant::now() <= deadline;
                received_native = Some(native);
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
                Self::observe_retirement(&done, &identity, x);
                retired = true;
                if done["retired"] != 0 {
                    return Err(format!("native child exited {}", done["retired"]));
                }
                Ok::<_, String>(())
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
                if let Ok(done) = serde_json::from_str::<Value>(&line)
                    && done["retired"].is_i64()
                {
                    Self::observe_retirement(&done, &identity, x);
                    retired = true;
                    break;
                }
            }
        }
        x.registry.unregister(&identity);
        let native = match result? {
            Some(()) if reply_before_deadline => received_native,
            None if reply_before_deadline && retired && !x.cancel.is_cancelled() => {
                // Match the fresh backend: a complete timely reply determines
                // the native verdict. Retirement remains awaited and charged,
                // even when its acknowledgement arrives after the deadline.
                received_native
            }
            _ => None,
        };
        match native {
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
    fn request_resource_preemption(&self, processes: &[ProcessIdentity]) {
        self.fresh.request_resource_preemption(processes);
    }
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
    async fn verify_resource_retry(&self, c: &Candidate, x: Execution) -> Outcome {
        let deadline = Instant::now() + Duration::from_millis(c.timeout_ms);
        {
            // Engine grants exclusive headroom only after peers retire. Hold
            // the state lock through graceful teardown so no new branch can
            // acquire this parent while its memory is being reclaimed.
            let mut state = self.state.lock().await;
            self.ready.store(false, Ordering::Release);
            if let Some(parent) = state.parent.take() {
                x.registry.note(BackendEvent {
                    stage: "prepared_evicted".into(),
                    detail: serde_json::json!({
                        "reason":"exclusive_resource_retry",
                        "parent_pid":parent.identity.pid,
                        "start_ticks":parent.identity.start_ticks
                    })
                    .to_string(),
                });
                parent.stop(false).await;
            }
        }
        // Do not recreate the import parent on the very retry meant to reclaim
        // its memory. Later ordinary requests can prepare it again.
        self.fallback(
            c,
            x,
            deadline,
            "exclusive resource retry uses fresh native state".into(),
        )
        .await
    }
    async fn shutdown(&self) {
        self.ready.store(false, Ordering::Release);
        let parent = self.state.lock().await.parent.take();
        if let Some(parent) = parent {
            parent.stop(false).await;
        }
    }
}

#[cfg(test)]
mod reply_deadline_tests {
    use super::*;
    use std::sync::{Arc, Mutex as StdMutex};
    use tokio::net::UnixListener;
    use tokio_util::sync::CancellationToken;

    #[derive(Default)]
    struct Registry(StdMutex<Vec<ProcessIdentity>>, StdMutex<Vec<u64>>);
    impl ProcessRegistry for Registry {
        fn observe_rss(&self, bytes: u64) {
            self.1.lock().unwrap().push(bytes);
        }
        fn register(&self, process: ProcessIdentity) {
            self.0.lock().unwrap().push(process);
        }
        fn unregister(&self, process: &ProcessIdentity) {
            assert!(
                process_identity(process.pid).is_none(),
                "unregister before reaping"
            );
            self.0.lock().unwrap().retain(|p| p != process);
        }
    }
    struct SocketPath(PathBuf);
    impl Drop for SocketPath {
        fn drop(&mut self) {
            let _ = std::fs::remove_file(&self.0);
        }
    }

    // A protocol/lifecycle fixture, not a Lean proof or performance benchmark.
    async fn control(
        code: &str,
        late_reply: bool,
        cancel_reply: bool,
        malformed_retirement: bool,
    ) -> (Result<Outcome, String>, Duration) {
        use std::os::unix::process::ExitStatusExt;
        let path = SocketPath(std::env::temp_dir().join(format!(
            "gpu-smt-reply-{}-{}.sock",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        )));
        let listener = UnixListener::bind(&path.0).unwrap();
        let mut child = Command::new("/bin/sleep")
            .arg("5")
            .process_group(0)
            .kill_on_drop(true)
            .spawn()
            .unwrap();
        let identity = process_identity(child.id().unwrap()).unwrap();
        let sent = Arc::new(tokio::sync::Notify::new());
        let sent_by_server = sent.clone();
        let server_identity = identity.clone();
        let server = tokio::spawn(async move {
            let (stream, _) = listener.accept().await.unwrap();
            let (read, mut write) = stream.into_split();
            let mut lines = BufReader::new(read).lines();
            let start = serde_json::json!({"started":server_identity.pid,
                "start_ticks":server_identity.start_ticks});
            write
                .write_all(format!("{start}\n").as_bytes())
                .await
                .unwrap();
            let _mask = lines.next_line().await.unwrap().unwrap();
            let command: String =
                serde_json::from_str(&lines.next_line().await.unwrap().unwrap()).unwrap();
            if late_reply {
                tokio::time::sleep(Duration::from_millis(500)).await;
            }
            let response = match command.as_str() {
                "rejected" => {
                    serde_json::json!({"env":0,"messages":[{"severity":"error","data":"fixture"}]})
                }
                "incomplete" => serde_json::json!({"env":0,"sorries":[{}]}),
                _ => serde_json::json!({"env":0,"messages":[]}),
            };
            write
                .write_all(format!("{}\n", serde_json::json!({"native":response})).as_bytes())
                .await
                .unwrap();
            sent_by_server.notify_one();
            tokio::time::sleep(Duration::from_millis(if malformed_retirement {
                1
            } else {
                500
            }))
            .await;
            let _ = child.start_kill();
            let status = child.wait().await.unwrap();
            let done = if malformed_retirement {
                serde_json::json!({"retired":"invalid"})
            } else {
                serde_json::json!({"retired":status.into_raw(),"peak_rss_bytes":12345})
            };
            write
                .write_all(format!("{done}\n").as_bytes())
                .await
                .unwrap();
        });
        let registry = Arc::new(Registry::default());
        let cancel = CancellationToken::new();
        let cancel_task = if cancel_reply {
            let token = cancel.clone();
            Some(tokio::spawn(async move {
                sent.notified().await;
                token.cancel();
            }))
        } else {
            None
        };
        let backend = PreparedRepl::new(
            NativeRepl {
                program: "/unused".into(),
                args: vec![],
                project: std::env::temp_dir(),
                environment: "protocol-fixture-not-Lean".into(),
            },
            "/unused".into(),
            "/unused".into(),
        );
        // Only the wire command changes; the fixture never changes affinity.
        let candidate = Candidate {
            id: "reply".into(),
            code: code.into(),
            task_id: None,
            timeout_ms: 250,
            reuse: false,
        };
        let started = Instant::now();
        let result = backend
            .branch(
                path.0.clone(),
                &candidate,
                &Execution {
                    cancel,
                    cpus: vec![0],
                    registry: registry.clone(),
                },
                started + Duration::from_millis(250),
            )
            .await;
        let elapsed = started.elapsed();
        server.await.unwrap();
        if let Some(task) = cancel_task {
            task.await.unwrap();
        }
        assert!(process_identity(identity.pid).is_none());
        assert!(registry.0.lock().unwrap().is_empty());
        if !malformed_retirement {
            // Synthetic protocol metadata, not a measured native memory peak.
            assert_eq!(*registry.1.lock().unwrap(), vec![12345]);
        }
        (result, elapsed)
    }

    #[tokio::test]
    async fn timely_native_reply_is_not_lost_while_waiting_for_retirement() {
        for (code, expected) in [
            ("accepted", Status::Accepted),
            ("rejected", Status::Rejected),
            ("incomplete", Status::Incomplete),
        ] {
            let (result, elapsed) = control(code, false, false, false).await;
            assert_eq!(
                result.unwrap().status,
                expected,
                "timely reply lost at retirement deadline"
            );
            assert!(
                elapsed >= Duration::from_millis(500),
                "retirement cost was hidden"
            );
        }
    }
    #[tokio::test]
    async fn late_reply_cancellation_and_malformed_retirement_are_not_accepted() {
        assert_eq!(
            control("accepted", true, false, false)
                .await
                .0
                .unwrap()
                .status,
            Status::Timeout
        );
        assert_eq!(
            control("accepted", false, true, false)
                .await
                .0
                .unwrap()
                .status,
            Status::Cancelled
        );
        assert!(control("accepted", false, false, true).await.0.is_err());
    }
}
