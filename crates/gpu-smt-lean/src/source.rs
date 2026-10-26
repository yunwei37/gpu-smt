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
    } else if exit_code != Some(0) || messages.iter().any(|m| m["severity"] == "error") {
        Status::Rejected
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
    pub fn with_args(self, args: Vec<String>) -> impl VerificationBackend {
        SourceWithArgs {
            backend: self,
            args,
        }
    }
    async fn verify_args(
        &self,
        candidate: &Candidate,
        execution: Execution,
        args: &[String],
    ) -> Outcome {
        let mut command = Command::new(&self.program);
        command
            .args(args)
            .args(["--json", "--stdin"])
            .current_dir(&self.project)
            .stdin(Stdio::piped())
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
        let mut input = child.stdin.take().unwrap();
        let mut output = child.stdout.take().unwrap();
        let stderr = tokio::spawn(drain(child.stderr.take().unwrap()));
        let io = async {
            input
                .write_all(candidate.code.as_bytes())
                .await
                .map_err(|e| e.to_string())?;
            input.shutdown().await.map_err(|e| e.to_string())?;
            drop(input);
            let mut bytes = Vec::new();
            output
                .read_to_end(&mut bytes)
                .await
                .map_err(|e| e.to_string())?;
            let text = String::from_utf8(bytes).map_err(|e| e.to_string())?;
            observe_current_rss(&identity, execution.registry.as_ref());
            let status = child.wait().await.map_err(|e| e.to_string())?;
            Ok::<_, String>((status.code(), text))
        };
        let outcome = tokio::select! {
            result = io => Some(result),
            _ = tokio::time::sleep(Duration::from_millis(candidate.timeout_ms)) => None,
            _ = execution.cancel.cancelled() => None,
        };
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
        let diagnostic = stderr
            .await
            .unwrap_or_else(|e| format!("stderr reader: {e}"));
        execution.registry.unregister(&identity);
        match (outcome, interrupted) {
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
        }
    }
}
#[async_trait]
impl VerificationBackend for NativeLean {
    fn identity(&self) -> String {
        format!(
            "lean-cli|{:?}|{:?}|{}",
            self.program, self.project, self.environment
        )
    }

    async fn verify(&self, candidate: &Candidate, execution: Execution) -> Outcome {
        self.verify_args(candidate, execution, &[]).await
    }
}
struct SourceWithArgs {
    backend: NativeLean,
    args: Vec<String>,
}
#[async_trait]
impl VerificationBackend for SourceWithArgs {
    fn identity(&self) -> String {
        if self.args.is_empty() {
            self.backend.identity()
        } else {
            format!("{}|args:{:?}", self.backend.identity(), self.args)
        }
    }
    async fn verify(&self, candidate: &Candidate, execution: Execution) -> Outcome {
        self.backend
            .verify_args(candidate, execution, &self.args)
            .await
    }
}

#[cfg(test)]
mod tests {
    use super::*;
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
