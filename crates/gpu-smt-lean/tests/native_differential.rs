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

#[tokio::test]
#[ignore = "requires matching LEAN_PREPARED_HOST/LEAN_SYSROOT/LEAN_REPL/LEAN_PROJECT; native CI runs this"]
async fn native_import_parent_isolates_children_and_matches_raw_responses() {
    let fresh = NativeRepl {
        program: PathBuf::from(std::env::var("LEAN_REPL").unwrap()),
        args: vec![],
        project: PathBuf::from(std::env::var("LEAN_PROJECT").unwrap()),
        environment: "pinned-prepared-native-contract".into(),
    };
    let backend = gpu_smt_lean::PreparedRepl::new(
        fresh.clone(),
        PathBuf::from(std::env::var("LEAN_PREPARED_HOST").unwrap()),
        PathBuf::from(std::env::var("LEAN_SYSROOT").unwrap()),
    );
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
            memory_bytes: 48 << 30,
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
    let mut parent = None;
    let mut first_expected = None;
    let mut seen = vec![];
    for (i, (code, status)) in [
        ("import Init\ndef candidate_private := 7", Status::Accepted),
        (
            "import Init\nexample : candidate_private = 7 := by rfl",
            Status::Rejected,
        ),
        (
            "import Init\ndef candidate_private := 8\nexample : candidate_private = 8 := by rfl",
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
        (
            "import Lean\nexample : True := by trivial",
            Status::Accepted,
        ),
    ]
    .into_iter()
    .enumerate()
    {
        let mut child = tokio::process::Command::new(&fresh.program)
            .current_dir(&fresh.project)
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
        let expected: serde_json::Value = serde_json::from_slice(&raw.stdout).unwrap();
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
        assert_eq!(
            result[0].outcome.status, status,
            "{code}: {:?}",
            result[0].outcome
        );
        assert_eq!(
            result[0].outcome.response.as_ref(),
            Some(&expected),
            "{code}"
        );
        if i == 0 {
            let ids = &result[0].attempts[0].processes;
            assert_eq!(
                ids.len(),
                2,
                "import parent and disposable child must be registered; fallback alone is not engagement"
            );
            parent = Some(ids[0].clone());
            first_expected = Some(expected.clone());
        }
        seen.extend(
            result[0]
                .attempts
                .iter()
                .flat_map(|a| a.processes.iter().cloned()),
        );
        assert!(
            gpu_smt_engine::linux::identity(parent.as_ref().unwrap().pid).is_ok(),
            "one import parent must survive individual candidates"
        );
        for p in result[0].attempts.iter().flat_map(|a| &a.processes) {
            if Some(p) != parent.as_ref() {
                assert!(
                    gpu_smt_engine::linux::identity(p.pid).is_err(),
                    "candidate child still live after result"
                );
            }
        }
    }
    let interrupted = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![Candidate {
                id: "cancel-control".into(),
                task_id: None,
                code: "import Init\n#eval IO.sleep 10000".into(),
                timeout_ms: 50,
                reuse: false,
            }],
        })
        .await
        .unwrap();
    assert_eq!(
        interrupted[0].outcome.status,
        Status::Timeout,
        "{:?}",
        interrupted[0].outcome
    );
    seen.extend(
        interrupted[0]
            .attempts
            .iter()
            .flat_map(|a| a.processes.iter().cloned()),
    );
    assert!(
        engine.prepared_state_ready(),
        "native timeout must preserve import parent"
    );
    let after = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![Candidate {
                id: "after-cancel".into(),
                task_id: None,
                code: "import Init\ndef candidate_private := 7".into(),
                timeout_ms: 300000,
                reuse: false,
            }],
        })
        .await
        .unwrap();
    assert_eq!(after[0].outcome.status, Status::Accepted);
    assert_eq!(after[0].outcome.response, first_expected);
    seen.extend(
        after[0]
            .attempts
            .iter()
            .flat_map(|a| a.processes.iter().cloned()),
    );
    engine.shutdown().await;
    assert!(!engine.prepared_state_ready());
    for p in seen {
        assert!(
            gpu_smt_engine::linux::identity(p.pid).is_err(),
            "owned native process survives shutdown"
        );
    }
}
