//! Explicit native environment test, not a mocked verifier.
use gpu_smt_core::*;
use gpu_smt_engine::{
    Config, Engine, Fifo, HeadroomAdmission, MemoryCache, TaskInterleave, TaskMemory,
    linux::ProcMonitor,
};
use gpu_smt_lean::NativeRepl;
use std::{path::PathBuf, process::Stdio, sync::Arc};
use tokio::io::AsyncWriteExt;

#[tokio::test]
#[ignore = "requires LEAN_REPL and LEAN_PROJECT; run when the sole native collection slot is free"]
async fn native_task_memory_accept_reject_and_sorry_match_raw_stock_repl() {
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
    // Test-local capture of the actual opaque observation context. No encoding
    // assumption, RSS injection or copied native verdict participates.
    struct NativeFeedback(Arc<std::sync::Mutex<Vec<(String, String, u64)>>>);
    impl SchedulingPolicy for NativeFeedback {
        fn priority(&self, _: &Candidate) -> u64 {
            0
        }
        fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
            Some(1)
        }
        fn observe_rss(&self, c: &Candidate, context: &str, bytes: u64) {
            self.0
                .lock()
                .unwrap()
                .push((c.id.clone(), context.into(), bytes));
        }
    }
    let observations = Arc::new(std::sync::Mutex::new(Vec::new()));
    let policy = Arc::new(TaskInterleave::new(TaskMemory::new(NativeFeedback(
        observations.clone(),
    ))));
    let engine = Engine::new(
        Config {
            memory_bytes: 48 * 1024 * 1024 * 1024,
            cpus: vec![cpu],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        policy.clone(),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let mut native_payloads = vec![];
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
            "import Init\nexample : 1 = 2 := by sorry",
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
        native_payloads.push(payload.clone());
        let result = engine
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![Candidate {
                    id: i.to_string(),
                    task_id: Some("native-memory-task".into()),
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
        assert!(!result[0].cached && !result[0].coalesced);
        assert_eq!(result[0].attempts.len(), 1);
        let measured = result[0].attempts[0].peak_rss_bytes;
        assert!(
            measured > 0,
            "real retired native attempt has no RSS observation"
        );
        let seen = observations.lock().unwrap();
        assert_eq!(seen.len(), i + 1, "one observation per physical attempt");
        let (id, context, bytes) = seen.last().unwrap();
        assert_eq!(id, &i.to_string());
        assert_eq!(*bytes, measured, "feedback differs from actual attempt");
        let sibling = Candidate {
            id: "unexecuted-forecast-probe".into(),
            task_id: Some("native-memory-task".into()),
            code: "unexecuted different source".into(),
            timeout_ms: 300000,
            reuse: false,
        };
        let observed_max = seen.iter().map(|(_, _, bytes)| *bytes).max().unwrap();
        assert_eq!(
            policy.refresh_rss(&sibling, context, Some(1)),
            Some(observed_max)
        );
        let mut unrelated = sibling.clone();
        unrelated.task_id = Some("another-task".into());
        assert_eq!(policy.refresh_rss(&unrelated, context, Some(1)), Some(1));
        unrelated = sibling.clone();
        unrelated.timeout_ms += 1;
        assert_eq!(policy.refresh_rss(&unrelated, context, Some(1)), Some(1));
        assert_eq!(
            policy.refresh_rss(&sibling, "unobserved-context", Some(1)),
            Some(1)
        );
        for process in &result[0].attempts[0].processes {
            assert!(
                gpu_smt_engine::linux::identity(process.pid).is_err(),
                "native child survives its published observation"
            );
        }
    }
    let input = |id: &str, task: &str, code: &str| Candidate {
        id: id.into(),
        task_id: Some(task.into()),
        code: code.into(),
        timeout_ms: 300000,
        reuse: false,
    };
    // Rejected and incomplete siblings above must not determine this verdict.
    let after_failure = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![input(
                "accepted-after-failure",
                "native-memory-task",
                "import Init\nexample : 1 + 1 = 2 := by decide",
            )],
        })
        .await
        .unwrap();
    assert_eq!(after_failure[0].outcome.status, Status::Accepted);
    assert_eq!(
        after_failure[0].outcome.response.as_ref(),
        Some(&native_payloads[0])
    );
    assert_eq!(after_failure[0].attempts.len(), 1);
    assert!(!after_failure[0].cached && !after_failure[0].coalesced);
    assert_eq!(observations.lock().unwrap().len(), 4);
    for process in after_failure
        .iter()
        .flat_map(|row| &row.attempts)
        .flat_map(|a| &a.processes)
    {
        assert!(gpu_smt_engine::linux::identity(process.pid).is_err());
    }
    let first = engine
        .verify_batch(Batch {
            mode: Mode::FirstSuccess,
            candidates: vec![
                input(
                    "winner",
                    "solvable",
                    "import Init\nexample : 1 + 1 = 2 := by decide",
                ),
                input(
                    "sibling",
                    "solvable",
                    "import Init\nexample : 1 + 1 = 2 := by decide",
                ),
                input(
                    "admitted",
                    "unsolved",
                    "import Init\nexample : 1 = 2 := by sorry",
                ),
                input(
                    "rejected",
                    "unsolved",
                    "import Init\nexample : 1 = 2 := by decide",
                ),
            ],
        })
        .await
        .unwrap();
    assert_eq!(first[0].outcome.status, Status::Accepted);
    assert_eq!(
        first[0].outcome.response.as_ref(),
        Some(&native_payloads[0])
    );
    assert!(matches!(
        first[1].outcome.status,
        Status::Cancelled | Status::Accepted
    ));
    if first[1].outcome.status == Status::Accepted {
        assert_eq!(
            first[1].outcome.response.as_ref(),
            Some(&native_payloads[0])
        );
    }
    assert_eq!(
        first[2].outcome.status,
        Status::Incomplete,
        "admission must not become a task winner"
    );
    assert_eq!(
        first[2].outcome.response.as_ref(),
        Some(&native_payloads[2])
    );
    assert_eq!(
        first[3].outcome.status,
        Status::Rejected,
        "unsolved task must exhaust its candidates"
    );
    assert_eq!(
        first[3].outcome.response.as_ref(),
        Some(&native_payloads[1])
    );
    engine.shutdown().await;
    for process in first
        .iter()
        .flat_map(|v| &v.attempts)
        .flat_map(|a| &a.processes)
    {
        assert!(
            gpu_smt_engine::linux::identity(process.pid).is_err(),
            "task-aware native process survives shutdown"
        );
    }
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
    let backend = Arc::new(gpu_smt_lean::PreparedRepl::new(
        fresh.clone(),
        PathBuf::from(std::env::var("LEAN_PREPARED_HOST").unwrap()),
        PathBuf::from(std::env::var("LEAN_SYSROOT").unwrap()),
    ));
    let mask = std::fs::read_to_string("/proc/self/status").unwrap();
    let cpus: Vec<usize> = mask
        .lines()
        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
        .unwrap()
        .trim()
        .split(',')
        .flat_map(|range| {
            let mut ends = range.split('-').map(|v| v.parse::<usize>().unwrap());
            let first = ends.next().unwrap();
            first..=ends.next().unwrap_or(first)
        })
        .take(2)
        .collect();
    assert_eq!(
        cpus.len(),
        2,
        "native concurrency contract requires two eligible cores"
    );
    // Explicit source forecast is a reservation, not an allocation/limit.
    // The later headroom control changes this policy for one request only.
    struct Forecast(std::sync::atomic::AtomicU64);
    impl SchedulingPolicy for Forecast {
        fn priority(&self, _: &Candidate) -> u64 {
            0
        }
        fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
            let bytes = self.0.load(std::sync::atomic::Ordering::Relaxed);
            (bytes > 0).then_some(bytes)
        }
    }
    let forecast = Arc::new(Forecast(std::sync::atomic::AtomicU64::new(0)));
    let engine = Engine::new(
        Config {
            memory_bytes: 48 << 30,
            cpus: cpus.clone(),
            cores_per_worker: 1,
        },
        backend.clone(),
        forecast.clone(),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let mut parent = None;
    let mut first_expected = None;
    let mut seen = vec![];
    for (i, (code, status)) in [
        ("import Init\nimport Std.Internal.UV.Timer\ndef candidate_private := 7", Status::Accepted),
        (
            "import Init\nimport Std.Internal.UV.Timer\nexample : candidate_private = 7 := by rfl",
            Status::Rejected,
        ),
        (
            "import Init\nimport Std.Internal.UV.Timer\ndef candidate_private := 8\nexample : candidate_private = 8 := by rfl",
            Status::Accepted,
        ),
        (
            "import Init\nimport Std.Internal.UV.Timer\nexample : 1 = 2 := by decide",
            Status::Rejected,
        ),
        (
            "import Init\nimport Std.Internal.UV.Timer\nexample : False := by sorry",
            Status::Incomplete,
        ),
        (
            "import Init\nimport Std.Internal.UV.Timer\n#eval show IO Bool from do\n  let timer ← Std.Internal.UV.Timer.mk 1 false\n  let promise ← timer.next\n  pure promise.result?.get.isSome",
            Status::Accepted,
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
        assert!(result[0].attempts.iter().flat_map(|a| &a.backend_events)
            .filter(|e| e.stage == "rss_observation")
            .filter_map(|e| serde_json::from_str::<serde_json::Value>(&e.detail).ok())
            .any(|v| v["kind"] == "leader_kernel_high_water_rss"
                && v["bytes"].as_u64().is_some_and(|n| n > 0)),
            "native retired child must retain the kernel leader high-water observation");
        if i == 0 {
            let context = result[0].attempts[0].backend_events.iter()
                .find(|event| event.stage == "prepared_ready")
                .map(|event| serde_json::from_str::<serde_json::Value>(&event.detail).unwrap())
                .expect("native import readiness event");
            assert_eq!(context["prepared_context"]["header_errors"], false);
            assert!(context["prepared_context"]["imported_modules"].as_u64().is_some_and(|n| n > 0));
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
            "one import parent must survive individual candidates; backend events: {:?}",
            result[0].attempts[0].backend_events
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
    // Confirm actual native siblings overlap, rather than merely accepting a
    // batch that the scheduler silently serialized. This is a lifecycle
    // contract, not a throughput ratio or a timing-based speed assertion.
    let parallel_code = "import Init\nimport Std.Internal.UV.Timer\n#eval IO.sleep 1000\nexample : True := by trivial";
    let parallel = engine.verify_batch(Batch {
        mode: Mode::All,
        candidates: (0..2)
            .map(|i| Candidate {
                id: format!("parallel-{i}"),
                task_id: None,
                code: parallel_code.into(),
                timeout_ms: 300000,
                reuse: false,
            })
            .collect(),
    });
    tokio::pin!(parallel);
    let mut samples = tokio::time::interval(std::time::Duration::from_millis(20));
    let parent_pid = parent.as_ref().unwrap().pid;
    let mut saw_two_live_children = false;
    let parallel_results = loop {
        tokio::select! {
            result = &mut parallel => break result.unwrap(),
            _ = samples.tick() => {
                let children = std::fs::read_to_string(format!(
                    "/proc/{parent_pid}/task/{parent_pid}/children"
                )).unwrap();
                let live = children.split_whitespace().filter(|pid| {
                    std::fs::read_to_string(format!("/proc/{pid}/stat"))
                        .ok()
                        .and_then(|s| s.rsplit_once(')').map(|(_, tail)| tail.trim_start().starts_with('Z')))
                        == Some(false)
                }).count();
                saw_two_live_children |= live >= 2;
            }
        }
    };
    assert!(
        saw_two_live_children,
        "prepared native batch did not overlap two live disposable children"
    );
    for result in parallel_results {
        assert_eq!(
            result.outcome.status,
            Status::Accepted,
            "{:?}",
            result.outcome
        );
        assert!(
            result
                .attempts
                .iter()
                .all(|a| a.backend_events.iter().all(|e| e.stage != "fresh_fallback"))
        );
        for process in result.attempts.iter().flat_map(|a| &a.processes) {
            assert!(
                gpu_smt_engine::linux::identity(process.pid).is_err(),
                "parallel candidate survives its result"
            );
            seen.push(process.clone());
        }
    }
    assert!(
        engine.prepared_state_ready(),
        "concurrent branches retired their shared import parent"
    );
    let interrupted = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![Candidate {
                id: "cancel-control".into(),
                task_id: None,
                code: "import Init\nimport Std.Internal.UV.Timer\n#eval IO.sleep 10000".into(),
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
                code: "import Init\nimport Std.Internal.UV.Timer\ndef candidate_private := 7"
                    .into(),
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
    // Exercise the actual engine's initial exclusive-headroom dispatch.
    // The prediction is below the total budget but exceeds idle headroom
    // because this process/import parent necessarily consumes more than1byte.
    // No memory is allocated for the forecast; this is a lifecycle control.
    forecast
        .0
        .store((48_u64 << 30) - 1, std::sync::atomic::Ordering::Relaxed);
    let retry_source = Candidate {
        id: "exclusive-retry".into(),
        task_id: None,
        code: "import Init\nimport Std.Internal.UV.Timer\ndef candidate_private := 7".into(),
        timeout_ms: 300000,
        reuse: false,
    };
    let mut retries = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![retry_source.clone()],
        })
        .await
        .unwrap();
    forecast.0.store(0, std::sync::atomic::Ordering::Relaxed);
    let retry = retries.remove(0);
    assert_eq!(retry.outcome.status, Status::Accepted);
    assert_eq!(retry.outcome.response, first_expected);
    assert_eq!(
        retry.attempts.len(),
        1,
        "forecast must not fabricate a failed attempt"
    );
    assert!(retry.attempts[0].exclusive);
    assert!(
        retry.attempts[0]
            .backend_events
            .iter()
            .any(|event| event.stage == "exclusive_headroom")
    );
    assert!(
        !engine.prepared_state_ready(),
        "exclusive retry recreated the parent"
    );
    assert!(
        gpu_smt_engine::linux::identity(parent.as_ref().unwrap().pid).is_err(),
        "old prepared parent consumes memory after exclusive retry"
    );
    assert!(retry.attempts[0].backend_events.iter().any(|event| {
        event.stage == "prepared_evicted"
            && serde_json::from_str::<serde_json::Value>(&event.detail)
                .is_ok_and(|v| v["parent_pid"] == parent.as_ref().unwrap().pid)
    }));
    let retry_processes: Vec<_> = retry
        .attempts
        .iter()
        .flat_map(|a| a.processes.iter().cloned())
        .collect();
    assert_eq!(
        retry_processes.len(),
        1,
        "retry must use one fresh native process"
    );
    for process in &retry_processes {
        assert!(
            gpu_smt_engine::linux::identity(process.pid).is_err(),
            "fresh retry survives its returned result"
        );
    }
    seen.extend(retry_processes);
    let next = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![Candidate {
                id: "after-resource-retry".into(),
                ..retry_source
            }],
        })
        .await
        .unwrap();
    assert_eq!(next[0].outcome.status, Status::Accepted);
    assert_eq!(next[0].outcome.response, first_expected);
    assert!(
        engine.prepared_state_ready(),
        "ordinary work did not prepare a new parent"
    );
    let prepared_again = next[0].attempts[0]
        .backend_events
        .iter()
        .find(|event| event.stage == "prepared_ready")
        .map(|event| serde_json::from_str::<serde_json::Value>(&event.detail).unwrap())
        .expect("new native import parent was not prepared");
    assert_ne!(prepared_again["parent_pid"], parent.as_ref().unwrap().pid);
    seen.extend(
        next[0]
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

#[tokio::test]
#[ignore = "requires LEAN_SYSROOT and LEAN_PROJECT; native CI runs this with the pinned CLI"]
async fn native_source_frontend_matches_cli_and_retires_interruptions() {
    let program = PathBuf::from(std::env::var("LEAN_SYSROOT").unwrap()).join("bin/lean");
    let project = PathBuf::from(std::env::var("LEAN_PROJECT").unwrap());
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
        Arc::new(gpu_smt_lean::NativeLean {
            program: program.clone(),
            project: project.clone(),
            environment: "native-source-contract".into(),
        }),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let make = |id: &str, code: &str, timeout_ms| Candidate {
        id: id.into(),
        task_id: None,
        code: code.into(),
        timeout_ms,
        reuse: false,
    };
    let mut seen = vec![];
    let mut raw_source_envelopes = std::collections::HashMap::new();
    for (index, (code, status)) in [
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
        ("import Init\n#check Nat", Status::Accepted),
    ]
    .into_iter()
    .enumerate()
    {
        let mut native = tokio::process::Command::new(&program)
            .args(["--json", "--stdin"])
            .current_dir(&project)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .kill_on_drop(true)
            .spawn()
            .unwrap();
        let mut input = native.stdin.take().unwrap();
        input.write_all(code.as_bytes()).await.unwrap();
        drop(input);
        let raw = tokio::time::timeout(
            std::time::Duration::from_secs(300),
            native.wait_with_output(),
        )
        .await
        .unwrap()
        .unwrap();
        let expected = gpu_smt_lean::classify_source(
            raw.status.code(),
            String::from_utf8(raw.stdout).unwrap(),
            String::from_utf8(raw.stderr).unwrap(),
        );
        assert_eq!(expected.status, status);
        raw_source_envelopes.insert(code.to_string(), expected.response.clone());
        let result = engine
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![make(&index.to_string(), code, 300000)],
            })
            .await
            .unwrap();
        assert_eq!(result[0].outcome.status, status, "{:?}", result[0].outcome);
        assert_eq!(
            result[0].outcome.response, expected.response,
            "CLI output differs"
        );
        seen.extend(
            result[0]
                .attempts
                .iter()
                .flat_map(|a| a.processes.iter().cloned()),
        );
    }
    let timeout = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![make("timeout", "import Init\n#eval IO.sleep 10000", 50)],
        })
        .await
        .unwrap();
    assert_eq!(timeout[0].outcome.status, Status::Timeout);
    seen.extend(
        timeout[0]
            .attempts
            .iter()
            .flat_map(|a| a.processes.iter().cloned()),
    );
    let after = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![make(
                "after",
                "import Init\nexample : True := by trivial",
                300000,
            )],
        })
        .await
        .unwrap();
    assert_eq!(after[0].outcome.status, Status::Accepted);
    seen.extend(
        after[0]
            .attempts
            .iter()
            .flat_map(|a| a.processes.iter().cloned()),
    );
    let stream_sources = [
        "import Init\nexample : 1 + 1 = 2 := by decide",
        "import Init\nexample : 1 = 2 := by decide",
    ];
    let mut stream = engine
        .verify_stream(Batch {
            mode: Mode::All,
            candidates: stream_sources
                .iter()
                .enumerate()
                .map(|(i, source)| make(&format!("stream-{i}"), source, 300000))
                .collect(),
        })
        .unwrap();
    let mut stream_indices = std::collections::BTreeSet::new();
    let mut stream_complete = false;
    while let Some(event) = tokio::time::timeout(std::time::Duration::from_secs(300), stream.recv())
        .await
        .unwrap()
    {
        match event {
            BatchEvent::Result {
                index,
                verification,
            } => {
                assert!(stream_indices.insert(index));
                assert_eq!(
                    verification.outcome.response,
                    raw_source_envelopes[stream_sources[index]]
                );
                assert_eq!(
                    verification.outcome.status,
                    if index == 0 {
                        Status::Accepted
                    } else {
                        Status::Rejected
                    }
                );
                seen.extend(
                    verification
                        .attempts
                        .iter()
                        .flat_map(|a| a.processes.iter().cloned()),
                );
            }
            BatchEvent::Complete { count } => {
                assert_eq!(count, 2);
                stream_complete = true;
            }
            BatchEvent::Error { message } => panic!("{message}"),
        }
    }
    assert!(stream_complete && stream_indices.len() == 2);
    engine.shutdown().await;
    let configured = Engine::new(
        Config {
            memory_bytes: 48 << 30,
            cpus: vec![cpu],
            cores_per_worker: 1,
        },
        Arc::new(
            gpu_smt_lean::NativeLean {
                program: program.clone(),
                project: project.clone(),
                environment: "native-source-argv-contract".into(),
            }
            .with_args(vec!["--tstack=400000".into()]),
        ),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    for (index, (code, status)) in [
        (
            "import Init\nexample : 1 + 1 = 2 := by decide",
            Status::Accepted,
        ),
        (
            "import Init\nexample : 1 = 2 := by decide",
            Status::Rejected,
        ),
    ]
    .into_iter()
    .enumerate()
    {
        let mut native = tokio::process::Command::new(&program)
            .args(["--tstack=400000", "--json", "--stdin"])
            .current_dir(&project)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .kill_on_drop(true)
            .spawn()
            .unwrap();
        let mut input = native.stdin.take().unwrap();
        input.write_all(code.as_bytes()).await.unwrap();
        drop(input);
        let raw = tokio::time::timeout(
            std::time::Duration::from_secs(300),
            native.wait_with_output(),
        )
        .await
        .unwrap()
        .unwrap();
        let expected = gpu_smt_lean::classify_source(
            raw.status.code(),
            String::from_utf8(raw.stdout).unwrap(),
            String::from_utf8(raw.stderr).unwrap(),
        );
        assert_eq!(expected.status, status);
        let result = configured
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![make(&format!("configured-{index}"), code, 300000)],
            })
            .await
            .unwrap();
        assert_eq!(result[0].outcome.status, status, "{:?}", result[0].outcome);
        assert_eq!(result[0].outcome.response, expected.response);
        seen.extend(
            result[0]
                .attempts
                .iter()
                .flat_map(|a| a.processes.iter().cloned()),
        );
    }
    configured.shutdown().await;
    let original = project.join(format!("GpuSmtFileContract{}.lean", std::process::id()));
    let log_directory = project.join(format!("GpuSmtNativeLogs{}", std::process::id()));
    std::fs::create_dir(&log_directory).unwrap();
    let mut native_logs = Vec::new();
    let file_engine = Engine::new(
        Config {
            memory_bytes: 48 << 30,
            cpus: vec![cpu],
            cores_per_worker: 1,
        },
        Arc::new(
            gpu_smt_lean::NativeLean {
                program: program.clone(),
                project: project.clone(),
                environment: "native-original-file-contract".into(),
            }
            .with_source_file(original.clone(), vec!["--tstack=400000".into()])
            .with_stderr_dir(log_directory.clone()),
        ),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    for (index, (code, status)) in [
        (
            "import Init\nexample : 1 + 1 = 2 := by decide",
            Status::Accepted,
        ),
        (
            "import Init\nexample : 1 = 2 := by decide",
            Status::Rejected,
        ),
    ]
    .into_iter()
    .enumerate()
    {
        std::fs::write(&original, code).unwrap();
        let raw = tokio::time::timeout(
            std::time::Duration::from_secs(300),
            tokio::process::Command::new(&program)
                .args(["--tstack=400000", "--json"])
                .arg(&original)
                .current_dir(&project)
                .stdin(Stdio::null())
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .kill_on_drop(true)
                .output(),
        )
        .await
        .unwrap()
        .unwrap();
        let expected = gpu_smt_lean::classify_source(
            raw.status.code(),
            String::from_utf8(raw.stdout).unwrap(),
            String::from_utf8(raw.stderr).unwrap(),
        );
        assert_eq!(expected.status, status, "{expected:?}");
        let result = file_engine
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![make(&format!("file-{index}"), code, 300000)],
            })
            .await
            .unwrap();
        assert_eq!(result[0].outcome.status, status, "{:?}", result[0].outcome);
        assert_eq!(result[0].outcome.response, expected.response);
        seen.extend(
            result[0]
                .attempts
                .iter()
                .flat_map(|a| a.processes.iter().cloned()),
        );
        assert_eq!(std::fs::read(&original).unwrap(), code.as_bytes());
        let event = result[0].attempts[0]
            .backend_events
            .iter()
            .find(|e| e.stage == "stderr_log_complete")
            .unwrap();
        let event: serde_json::Value = serde_json::from_str(&event.detail).unwrap();
        assert_eq!(event["complete"], true);
        let log = PathBuf::from(event["path"].as_str().unwrap());
        assert_eq!(
            std::fs::read(&log).unwrap().len() as u64,
            event["bytes_read"].as_u64().unwrap()
        );
        native_logs.push(log);
    }
    file_engine.shutdown().await;
    std::fs::remove_file(original).unwrap();
    for log in native_logs {
        std::fs::remove_file(log).unwrap();
    }
    std::fs::remove_dir(log_directory).unwrap();
    for p in seen {
        assert!(
            gpu_smt_engine::linux::identity(p.pid).is_err(),
            "native CLI survives result/shutdown"
        );
    }
}

#[tokio::test]
#[ignore = "requires matching native host/SDK; native CI executes failed-import regression"]
async fn native_import_error_never_becomes_prepared_readiness() {
    let backend = gpu_smt_lean::PreparedRepl::new(
        NativeRepl {
            program: PathBuf::from(std::env::var("LEAN_REPL").unwrap()),
            args: vec![],
            project: PathBuf::from(std::env::var("LEAN_PROJECT").unwrap()),
            environment: "native-import-error-contract".into(),
        },
        PathBuf::from(std::env::var("LEAN_PREPARED_HOST").unwrap()),
        PathBuf::from(std::env::var("LEAN_SYSROOT").unwrap()),
    );
    let mask = std::fs::read_to_string("/proc/self/status").unwrap();
    let cpu = mask
        .lines()
        .find_map(|line| line.strip_prefix("Cpus_allowed_list:"))
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
    let results = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![Candidate {
                id: "missing-import".into(),
                task_id: None,
                code: "import GpuSmtCertainlyAbsentModule\nexample : True := by trivial".into(),
                timeout_ms: 300000,
                reuse: false,
            }],
        })
        .await
        .unwrap();
    assert_eq!(
        results[0].outcome.status,
        Status::Rejected,
        "{:?}",
        results[0].outcome
    );
    assert!(
        !engine.prepared_state_ready(),
        "failed import claimed ready"
    );
    assert!(
        results[0]
            .attempts
            .iter()
            .flat_map(|a| &a.backend_events)
            .any(|event| event.stage == "fresh_fallback")
    );
    assert!(
        results[0]
            .attempts
            .iter()
            .flat_map(|a| &a.backend_events)
            .all(|event| event.stage != "prepared_ready")
    );
    engine.shutdown().await;
    for process in results
        .iter()
        .flat_map(|r| &r.attempts)
        .flat_map(|a| &a.processes)
    {
        assert!(
            gpu_smt_engine::linux::identity(process.pid).is_err(),
            "failed import/fallback process survives retirement"
        );
    }
}

#[tokio::test]
#[ignore = "requires LEAN_PREPARED_HOST/LEAN_SYSROOT/LEAN_PROJECT; native CI runs this"]
async fn native_library_load_is_before_imports_once_and_failures_never_ready() {
    use tokio::io::{AsyncBufReadExt, BufReader};
    let program = PathBuf::from(std::env::var("LEAN_PREPARED_HOST").unwrap());
    let sysroot = PathBuf::from(std::env::var("LEAN_SYSROOT").unwrap());
    let project = PathBuf::from(std::env::var("LEAN_PROJECT").unwrap());
    let directory = std::env::temp_dir().join(format!(
        "gpu-smt-native-library-{}-{}",
        std::process::id(),
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos()
    ));
    std::fs::create_dir(&directory).unwrap();
    let library = directory.join("probe.so");
    let marker = directory.join("loads");
    let socket = directory.join("control.sock");
    let source = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/native_load.c");
    assert!(
        std::process::Command::new("cc")
            .args(["-shared", "-fPIC", "-Wall", "-Wextra", "-Werror"])
            .arg(source)
            .arg("-o")
            .arg(&library)
            .status()
            .unwrap()
            .success()
    );
    let mut host = tokio::process::Command::new(&program)
        .args([socket.as_os_str(), sysroot.as_os_str()])
        .env("LEAN_SERVER_NATIVE_DYNLIB", &library)
        .env("GPU_SMT_NATIVE_LOAD_MARKER", &marker)
        .current_dir(&project)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .kill_on_drop(true)
        .spawn()
        .unwrap();
    let mut input = host.stdin.take().unwrap();
    input
        .write_all(format!("{}\n", serde_json::json!("import Init\n")).as_bytes())
        .await
        .unwrap();
    input.flush().await.unwrap();
    let mut output = BufReader::new(host.stdout.take().unwrap());
    let mut line = String::new();
    tokio::time::timeout(
        std::time::Duration::from_secs(300),
        output.read_line(&mut line),
    )
    .await
    .unwrap()
    .unwrap();
    let ready: serde_json::Value = serde_json::from_str(&line).unwrap();
    assert_eq!(ready["ready"], true);
    assert_eq!(ready["parent_threads"], 1);
    assert_eq!(
        ready["prepared_context"]["native_library"],
        serde_json::json!(library)
    );
    assert_eq!(std::fs::read_to_string(&marker).unwrap(), "loaded\n");
    let mask = std::fs::read_to_string("/proc/self/status").unwrap();
    let cpu = mask
        .lines()
        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
        .unwrap()
        .trim()
        .split([',', '-'])
        .next()
        .unwrap();
    for (code, status) in [
        (
            "import Init\nexample : True := by trivial",
            Status::Accepted,
        ),
        (
            "import Init\nexample : False := by decide",
            Status::Rejected,
        ),
    ] {
        let stream = tokio::net::UnixStream::connect(&socket).await.unwrap();
        let (read, mut write) = stream.into_split();
        let mut lines = BufReader::new(read).lines();
        let started = lines.next_line().await.unwrap().unwrap();
        let started: serde_json::Value = serde_json::from_str(&started).unwrap();
        write
            .write_all(format!("{cpu}\n{}\n", serde_json::json!(code)).as_bytes())
            .await
            .unwrap();
        write.flush().await.unwrap();
        let response = lines.next_line().await.unwrap().unwrap();
        let response: serde_json::Value = serde_json::from_str(&response).unwrap();
        let retired = lines.next_line().await.unwrap().unwrap();
        let retired: serde_json::Value = serde_json::from_str(&retired).unwrap();
        assert_eq!(retired["retired"], 0);
        assert_eq!(
            gpu_smt_lean::classify(response["native"].clone()).status,
            status
        );
        assert!(
            gpu_smt_engine::linux::identity(started["started"].as_u64().unwrap() as u32).is_err()
        );
        // Loading in every candidate would append another line. Missing the
        // loader entirely cannot satisfy this actual constructor side effect.
        assert_eq!(std::fs::read_to_string(&marker).unwrap(), "loaded\n");
    }
    drop(input);
    assert!(
        tokio::time::timeout(std::time::Duration::from_secs(300), host.wait())
            .await
            .unwrap()
            .unwrap()
            .success()
    );
    assert!(!socket.exists());
    let missing = directory.join("missing.so");
    let mut host = tokio::process::Command::new(program)
        .args([socket.as_os_str(), sysroot.as_os_str()])
        .env("LEAN_SERVER_NATIVE_DYNLIB", &missing)
        .current_dir(project)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .kill_on_drop(true)
        .spawn()
        .unwrap();
    let mut input = host.stdin.take().unwrap();
    input
        .write_all(format!("{}\n", serde_json::json!("import Init\n")).as_bytes())
        .await
        .unwrap();
    drop(input);
    let failed = tokio::time::timeout(std::time::Duration::from_secs(300), host.wait_with_output())
        .await
        .unwrap()
        .unwrap();
    assert!(!failed.status.success());
    assert!(
        failed.stdout.is_empty(),
        "failed native import claimed ready"
    );
    assert!(
        String::from_utf8_lossy(&failed.stderr).contains("missing.so"),
        "missing-library diagnostic lost: {:?}",
        failed.stderr
    );
    std::fs::remove_dir_all(directory).unwrap();
}
