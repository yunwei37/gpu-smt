//! Explicit native environment test, not a mocked verifier.
use gpu_smt_core::*;
use gpu_smt_engine::{Config, Engine, Fifo, HeadroomAdmission, MemoryCache, linux::ProcMonitor};
use gpu_smt_lean::NativeRepl;
use std::{path::PathBuf, process::Stdio, sync::Arc};
use tokio::io::AsyncWriteExt;

#[tokio::test]
#[ignore = "requires LEAN_REPL and LEAN_PROJECT; run when the sole native collection slot is free"]
async fn native_accept_reject_and_sorry_match_raw_stock_repl() {
    let program = PathBuf::from(std::env::var("LEAN_REPL").expect("LEAN_REPL"));
    let project = PathBuf::from(std::env::var("LEAN_PROJECT").expect("LEAN_PROJECT"));
    let backend = NativeRepl {
        program: program.clone(),
        args: vec![],
        project: project.clone(),
        environment: "explicit-native-differential".into(),
    };
    let mask = std::fs::read_to_string("/proc/self/status").unwrap();
    let cpu = mask
        .lines()
        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
        .unwrap()
        .trim()
        .split([',', '-'])
        .next()
        .unwrap()
        .parse()
        .unwrap();
    let engine = Engine::new(
        Config {
            memory_bytes: 48 * 1024 * 1024 * 1024,
            cpus: vec![cpu],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    for (i, (code, expected)) in [
        (
            "import Init\nexample : 1 + 1 = 2 := by decide",
            Status::Accepted,
        ),
        (
            "import Init\nexample : 1 = 2 := by decide",
            Status::Rejected,
        ),
        (
            "import Init\nexample : False := by sorry",
            Status::Incomplete,
        ),
    ]
    .into_iter()
    .enumerate()
    {
        let mut child = tokio::process::Command::new(&program)
            .current_dir(&project)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .kill_on_drop(true)
            .spawn()
            .unwrap();
        let mut stdin = child.stdin.take().unwrap();
        stdin
            .write_all(format!("{}\n\n", serde_json::json!({"cmd":code})).as_bytes())
            .await
            .unwrap();
        drop(stdin);
        let raw = tokio::time::timeout(
            std::time::Duration::from_secs(300),
            child.wait_with_output(),
        )
        .await
        .unwrap()
        .unwrap();
        let payload: serde_json::Value = serde_json::from_slice(&raw.stdout).unwrap();
        let result = engine
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![Candidate {
                    id: i.to_string(),
                    task_id: None,
                    code: code.into(),
                    timeout_ms: 300000,
                    reuse: false,
                }],
            })
            .await
            .unwrap();
        assert_eq!(result[0].outcome.status, expected);
        assert_eq!(
            result[0].outcome.response.as_ref(),
            Some(&payload),
            "raw native payload differs on source {i}"
        );
    }
    engine.shutdown().await;
}
