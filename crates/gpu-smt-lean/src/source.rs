//! Direct stock frontend backend for code-verification source files.
use super::{bind, drain, kill_group, observe_current_rss, process_identity};
use async_trait::async_trait;
use gpu_smt_core::*;
use serde_json::{Value, json};
use std::{path::PathBuf, process::Stdio, time::Duration};
use tokio::{
    io::{AsyncReadExt, AsyncWriteExt},
    process::Command,
};

// Observe exit without reaping: the birth-matched leader must still exist
// when retiring its process group. SIGCHLD is already used by Tokio children;
// install our receiver before checking, so an exit cannot be missed.
async fn exited_unreaped(pid: u32) -> Result<(), String> {
    let mut changed = tokio::signal::unix::signal(tokio::signal::unix::SignalKind::child())
        .map_err(|error| error.to_string())?;
    loop {
        let exited = {
            // SAFETY: initialized output, our owned child PID, no pointers retained.
            let mut info: libc::siginfo_t = unsafe { std::mem::zeroed() };
            let result = unsafe {
                libc::waitid(
                    libc::P_PID,
                    pid,
                    &mut info,
                    libc::WEXITED | libc::WNOWAIT | libc::WNOHANG,
                )
            };
            if result != 0 {
                let error = std::io::Error::last_os_error();
                if error.kind() == std::io::ErrorKind::Interrupted {
                    continue;
                }
                return Err(error.to_string());
            }
            // SAFETY: waitid initialized the siginfo output above.
            unsafe { info.si_pid() != 0 }
        };
        if exited {
            return Ok(());
        }
        changed
            .recv()
            .await
            .ok_or("native exit signal stream closed")?;
    }
}

/// Stock Lean CLI using exact full source on stdin and JSON diagnostics.
///
/// This is a distinct backend from Lean REPL; the raw response envelope retains
/// CLI stdout, stderr tail and exit code. It does not compile output modules,
/// execute a main function or add trust/memory/heartbeat overrides.
#[derive(Clone, Debug)]
pub struct NativeLean {
    /// Matching native SDK's lean executable.
    pub program: PathBuf,
    /// Original project directory, with its discovered import environment.
    pub project: PathBuf,
    /// Immutable SDK/dependency/project context identity.
    pub environment: String,
}

/// Classify an actual Lean --json --stdin exit without discarding raw output.
///
/// Only successful native exit with recognized JSON diagnostics can establish
/// acceptance. A source can print arbitrary output, so unknown/non-JSON stdout
/// remains a backend fault instead of being mistaken for a checked proof.
/// A nonzero exit alone is also operational: only a recognized JSON error
/// establishes source rejection. Runtime crashes can produce no such error.
/// This is native frontend behavior, not an audit of axioms or trusted imports.
pub fn classify_source(exit_code: Option<i32>, stdout: String, stderr: String) -> Outcome {
    let parsed = stdout
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(serde_json::from_str::<Value>)
        .collect::<Result<Vec<_>, _>>();
    let mut protocol_error = None;
    let messages = match parsed {
        Ok(messages)
            if messages.iter().all(|m| {
                matches!(
                    m.get("severity").and_then(Value::as_str),
                    Some("information" | "info" | "warning" | "error")
                ) && m.get("data").is_some_and(Value::is_string)
            }) =>
        {
            messages
        }
        Ok(_) => {
            protocol_error = Some("unknown native diagnostic shape".to_string());
            vec![]
        }
        Err(e) => {
            protocol_error = Some(format!("non-JSON native stdout: {e}"));
            vec![]
        }
    };
    let status = if stderr.contains("bad_alloc") || stderr.contains("out of memory") {
        Status::ResourceExhausted
    } else if exit_code.is_none() || protocol_error.is_some() {
        Status::BackendError
    } else if messages.iter().any(|m| m["severity"] == "error") {
        Status::Rejected
    } else if exit_code != Some(0) {
        protocol_error = Some(format!(
            "native exit {} without a JSON error diagnostic",
            exit_code.unwrap()
        ));
        Status::BackendError
    } else if messages.iter().any(|m| {
        m["data"]
            .as_str()
            .is_some_and(|data| data.contains("declaration uses 'sorry'"))
    }) {
        Status::Incomplete
    } else if !stderr.is_empty() {
        Status::BackendError
    } else {
        Status::Accepted
    };
    Outcome {
        status,
        response: Some(
            json!({"exit_code":exit_code, "stdout":stdout, "stderr":stderr, "messages":messages}),
        ),
        error: protocol_error,
    }
}

impl NativeLean {
    /// Preserve declared upstream SDK arguments without changing the default
    /// struct/API. Arguments are forwarded individually, before --json --stdin,
    /// and included in backend identity so contexts cannot share cached results.
    /// Callers must qualify the same flags against their raw native invocation.
    pub fn with_args(self, args: Vec<String>) -> ConfiguredLean {
        ConfiguredLean {
            backend: self,
            args,
            source_file: None,
            stderr_dir: None,
        }
    }
    /// Check an original source file in its original project context.
    ///
    /// The file must match the submitted source bytes before each execution.
    /// Relative paths are resolved from the project; file path and argv become
    /// part of backend identity. Callers must keep the pinned project immutable,
    /// as with imported dependencies. No file is created or rewritten.
    pub fn with_source_file(self, path: PathBuf, args: Vec<String>) -> ConfiguredLean {
        ConfiguredLean {
            backend: self,
            args,
            source_file: Some(path),
            stderr_dir: None,
        }
    }
    async fn verify_args(
        &self,
        candidate: &Candidate,
        execution: Execution,
        args: &[String],
        source_file: Option<&PathBuf>,
        stderr_dir: Option<&PathBuf>,
    ) -> Outcome {
        let source_file = match source_file {
            Some(path) => {
                let path = self.project.join(path);
                let path = if path.is_absolute() {
                    path
                } else {
                    match std::env::current_dir() {
                        Ok(directory) => directory.join(path),
                        Err(error) => {
                            return Outcome::operational(Status::BackendError, error.to_string());
                        }
                    }
                };
                match std::fs::read(&path) {
                    Ok(bytes) if bytes == candidate.code.as_bytes() => Some(path),
                    Ok(_) => {
                        return Outcome::operational(
                            Status::BackendError,
                            "original source file differs from submitted bytes",
                        );
                    }
                    Err(error) => {
                        return Outcome::operational(Status::BackendError, error.to_string());
                    }
                }
            }
            None => None,
        };
        let mut command = Command::new(&self.program);
        command.args(args).arg("--json");
        if let Some(path) = &source_file {
            command.arg(path).stdin(Stdio::null());
        } else {
            command.arg("--stdin").stdin(Stdio::piped());
        }
        command
            .current_dir(&self.project)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .kill_on_drop(true);
        if let Err(error) = bind(&mut command, &execution.cpus) {
            return Outcome::operational(Status::BackendError, error);
        }
        let mut child = match command.spawn() {
            Ok(child) => child,
            Err(error) => return Outcome::operational(Status::BackendError, error.to_string()),
        };
        let pid = child.id().unwrap();
        let identity = match process_identity(pid) {
            Some(identity) => identity,
            None => {
                let _ = child.start_kill();
                let _ = child.wait().await;
                return Outcome::operational(
                    Status::BackendError,
                    "native CLI exited before ownership registration",
                );
            }
        };
        execution.registry.register(identity.clone());
        let stderr_path = stderr_dir.map(|directory| {
            self.project.join(directory).join(format!(
                "native-{}-{}.stderr",
                identity.pid, identity.start_ticks
            ))
        });
        let log_file = match &stderr_path {
            Some(path) => match tokio::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(path)
                .await
            {
                Ok(file) => {
                    execution.registry.note(BackendEvent {
                        stage: "stderr_log".into(),
                        detail: json!({"path":path, "pid":identity.pid,
                            "start_ticks":identity.start_ticks})
                        .to_string(),
                    });
                    Some(file)
                }
                Err(error) => {
                    kill_group(&identity);
                    let _ = child.start_kill();
                    let _ = child.wait().await;
                    execution.registry.unregister(&identity);
                    return Outcome::operational(
                        Status::BackendError,
                        format!(
                            "cannot create native stderr log {}: {error}",
                            path.display()
                        ),
                    );
                }
            },
            None => None,
        };
        let input = child.stdin.take();
        let mut output = child.stdout.take().unwrap();
        let mut stdout = tokio::spawn(async move {
            let mut bytes = Vec::new();
            output
                .read_to_end(&mut bytes)
                .await
                .map_err(|e| e.to_string())?;
            String::from_utf8(bytes).map_err(|e| e.to_string())
        });
        let reader = child.stderr.take().unwrap();
        let stderr = tokio::spawn(async move {
            match log_file {
                Some(file) => drain_to_file(reader, file).await,
                None => (drain(reader).await, None, 0),
            }
        });
        let mut stdout_joined = false;
        let io = async {
            if let Some(mut input) = input {
                input
                    .write_all(candidate.code.as_bytes())
                    .await
                    .map_err(|e| e.to_string())?;
                input.shutdown().await.map_err(|e| e.to_string())?;
                drop(input);
            }
            exited_unreaped(pid).await?;
            // The compiler has exited, but descendants may still hold either
            // pipe. Retire them while its PID/birth still authorizes the group.
            kill_group(&identity);
            observe_current_rss(&identity, execution.registry.as_ref());
            let status = child.wait().await.map_err(|e| e.to_string())?;
            let text = (&mut stdout).await;
            stdout_joined = true;
            Ok::<_, String>((status.code(), text.map_err(|e| e.to_string())??))
        };
        let deadline = tokio::time::Instant::now() + Duration::from_millis(candidate.timeout_ms);
        let outcome = super::request_io(io, execution.cancel.cancelled(), deadline)
            .await
            .ok();
        let interrupted = if outcome.is_none() {
            kill_group(&identity);
            let _ = child.start_kill();
            let _ = child.wait().await;
            Some(if execution.cancel.is_cancelled() {
                Outcome::operational(Status::Cancelled, "native CLI attempt cancelled")
            } else {
                Outcome::operational(Status::Timeout, "native CLI request timeout")
            })
        } else {
            // The completed io path has already awaited natural native exit.
            // On pipe/encoding failure the same owned group still needs retirement.
            if outcome.as_ref().is_some_and(Result::is_err) {
                kill_group(&identity);
                let _ = child.start_kill();
                let _ = child.wait().await;
            }
            None
        };
        if !stdout_joined {
            let _ = stdout.await;
        }
        let (diagnostic, log_error, bytes_read) = stderr
            .await
            .unwrap_or_else(|e| (format!("stderr reader: {e}"), Some(e.to_string()), 0));
        if let Some(path) = &stderr_path {
            execution.registry.note(BackendEvent {
                stage: if log_error.is_none() {
                    "stderr_log_complete"
                } else {
                    "stderr_log_error"
                }
                .into(),
                detail: json!({"path":path, "bytes_read":bytes_read,
                    "complete":log_error.is_none(), "error":log_error})
                .to_string(),
            });
        }
        execution.registry.unregister(&identity);
        let mut result = match (outcome, interrupted) {
            (_, Some(result)) => result,
            (Some(Ok((exit_code, stdout))), _) => classify_source(exit_code, stdout, diagnostic),
            (Some(Err(error)), _) => Outcome::operational(
                if diagnostic.contains("bad_alloc") || diagnostic.contains("out of memory") {
                    Status::ResourceExhausted
                } else {
                    Status::BackendError
                },
                format!("{error}; {diagnostic}"),
            ),
            _ => unreachable!(),
        };
        if stderr_path.is_some()
            && let Some(error) = log_error
            && !matches!(result.status, Status::Cancelled | Status::Timeout)
        {
            result.status = Status::BackendError;
            result.error = Some(format!("native stderr log incomplete: {error}"));
        }
        result
    }
}
#[async_trait]
impl VerificationBackend for NativeLean {
    fn request_resource_preemption(&self, processes: &[ProcessIdentity]) {
        for identity in processes {
            kill_group(identity);
        }
    }
    fn identity(&self) -> String {
        format!(
            "lean-cli|{:?}|{:?}|{}",
            self.program, self.project, self.environment
        )
    }

    async fn verify(&self, candidate: &Candidate, execution: Execution) -> Outcome {
        self.verify_args(candidate, execution, &[], None, None)
            .await
    }
}
/// Configured stock source frontend; defaults remain those of NativeLean.
/// Extra observability does not reinterpret diagnostic stderr as proof acceptance.
#[derive(Clone, Debug)]
pub struct ConfiguredLean {
    backend: NativeLean,
    args: Vec<String>,
    source_file: Option<PathBuf>,
    stderr_dir: Option<PathBuf>,
}
impl ConfiguredLean {
    /// Retain complete unmodified stderr in an existing directory.
    ///
    /// Each actual attempt creates a new PID/birth-scoped file and records its
    /// path/completion in backend events. Relative directories use project context.
    /// Log setup/I/O failures are operational faults. Flush is included in attempt
    /// retirement, without an fsync/power-loss durability claim. Use reuse=false
    /// to measure fresh diagnostics; cache hits do not create a native log.
    pub fn with_stderr_dir(mut self, directory: PathBuf) -> Self {
        self.stderr_dir = Some(directory);
        self
    }
}
#[async_trait]
impl VerificationBackend for ConfiguredLean {
    fn request_resource_preemption(&self, processes: &[ProcessIdentity]) {
        self.backend.request_resource_preemption(processes);
    }
    fn identity(&self) -> String {
        let mut identity = if self.args.is_empty() {
            self.backend.identity()
        } else {
            format!("{}|args:{:?}", self.backend.identity(), self.args)
        };
        if let Some(path) = &self.source_file {
            identity.push_str(&format!("|source-file:{path:?}"));
        }
        if let Some(directory) = &self.stderr_dir {
            identity.push_str(&format!("|stderr-dir:{directory:?}"));
        }
        identity
    }
    async fn verify(&self, candidate: &Candidate, execution: Execution) -> Outcome {
        self.backend
            .verify_args(
                candidate,
                execution,
                &self.args,
                self.source_file.as_ref(),
                self.stderr_dir.as_ref(),
            )
            .await
    }
}

/// Preserve complete bytes while keeping response memory bounded. Log errors do
/// not stop draining the native pipe; they remain explicit operational evidence.
async fn drain_to_file<R: tokio::io::AsyncRead + Unpin>(
    mut reader: R,
    mut file: tokio::fs::File,
) -> (String, Option<String>, u64) {
    let mut tail = Vec::new();
    let mut chunk = [0u8; 4096];
    let mut error = None;
    let mut bytes = 0u64;
    let mut truncated = false;
    loop {
        let n = match reader.read(&mut chunk).await {
            Ok(0) => break,
            Ok(n) => n,
            Err(e) => {
                error.get_or_insert_with(|| format!("stderr read: {e}"));
                break;
            }
        };
        bytes += n as u64;
        if error.is_none()
            && let Err(e) = file.write_all(&chunk[..n]).await
        {
            error = Some(format!("stderr write: {e}"));
        }
        tail.extend_from_slice(&chunk[..n]);
        if tail.len() > 65536 {
            tail.drain(..tail.len() - 65536);
            truncated = true;
        }
    }
    if let Err(e) = file.flush().await {
        error.get_or_insert_with(|| format!("stderr flush: {e}"));
    }
    let text = String::from_utf8_lossy(&tail);
    let text = if truncated {
        format!("[stderr tail truncated] {text}")
    } else {
        text.into_owned()
    };
    (text, error, bytes)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn stderr_log_write_failure_stays_explicit_after_drain() {
        // Linux /dev/full reports a real ENOSPC without filling any project disk.
        let file = tokio::fs::OpenOptions::new()
            .write(true)
            .open("/dev/full")
            .await
            .unwrap();
        let bytes = b"retained event\\n";
        let (tail, error, read) = drain_to_file(&bytes[..], file).await;
        assert_eq!(tail.as_bytes(), bytes);
        assert_eq!(read, bytes.len() as u64);
        assert!(error.is_some_and(|e| e.contains("stderr write:") || e.contains("stderr flush:")));
    }
    #[test]
    fn observed_runtime_exits_are_not_logical_rejections() {
        // Exact retained native responses from the actual simp_all diagnostic
        // run. Runtime recursion failures supplied no Lean JSON proof errors.
        let fixture: Value = serde_json::from_str(include_str!(
            "../tests/fixtures/source-runtime-failures.json"
        ))
        .unwrap();
        for case in fixture["cases"].as_array().unwrap() {
            let native = &case["native_response"];
            let result = classify_source(
                native["exit_code"].as_i64().map(|code| code as i32),
                native["stdout"].as_str().unwrap().into(),
                native["stderr"].as_str().unwrap().into(),
            );
            assert_eq!(result.status, Status::BackendError, "{}", case["id"]);
            assert_eq!(result.response.as_ref(), Some(native));
            assert!(result.error.is_some());
        }
    }
    #[test]
    fn native_exit_and_diagnostic_shapes_are_distinct() {
        assert_eq!(
            classify_source(Some(0), "".into(), "".into()).status,
            Status::Accepted
        );
        assert_eq!(
            classify_source(
                Some(1),
                r#"{"severity":"error","data":"unsolved goals"}"#.into(),
                "".into()
            )
            .status,
            Status::Rejected
        );
        assert_eq!(
            classify_source(
                Some(0),
                r#"{"severity":"warning","data":"declaration uses 'sorry'"}"#.into(),
                "".into()
            )
            .status,
            Status::Incomplete
        );
        assert_eq!(
            classify_source(Some(0), "true\n".into(), "".into()).status,
            Status::BackendError
        );
        assert_eq!(
            classify_source(Some(0), r#"{"unexpected":"value"}"#.into(), "".into()).status,
            Status::BackendError
        );
        assert_eq!(
            classify_source(None, "".into(), "".into()).status,
            Status::BackendError
        );
        assert_eq!(
            classify_source(None, "".into(), "std::bad_alloc".into()).status,
            Status::ResourceExhausted
        );
    }
}
