use gpu_smt_core::*;
use gpu_smt_engine::{Config, Engine, Fifo, HeadroomAdmission, MemoryCache, linux::ProcMonitor};
use gpu_smt_lean::NativeRepl;
use std::{path::PathBuf, sync::Arc, time::Duration};

fn cpu() -> usize {
    let status = std::fs::read_to_string("/proc/self/status").unwrap();
    status
        .lines()
        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
        .unwrap()
        .trim()
        .split([',', '-'])
        .next()
        .unwrap()
        .parse()
        .unwrap()
}
fn candidate(id: &str, code: &str, ms: u64) -> Candidate {
    Candidate {
        id: id.into(),
        task_id: None,
        code: code.into(),
        timeout_ms: ms,
        reuse: false,
    }
}
fn engine() -> Engine {
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/repl.py");
    let backend = NativeRepl {
        program: PathBuf::from("/usr/bin/python3"),
        args: vec!["-u".into(), fixture.to_string_lossy().into()],
        project: std::env::temp_dir(),
        environment: "protocol-fixture-not-Lean".into(),
    };
    Engine::new(
        Config {
            memory_bytes: 1024 * 1024 * 1024,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap()
}
#[tokio::test]
async fn pipe_protocol_errors_admissions_and_stderr_drain() {
    let engine = engine();
    let result = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("accepted", "ok", 5000),
                candidate("rejected", "bad", 5000),
                candidate("incomplete", "sorry", 5000),
                candidate("stderr", "stderr", 5000),
            ],
        })
        .await
        .unwrap();
    assert_eq!(
        result
            .iter()
            .map(|r| r.outcome.status.clone())
            .collect::<Vec<_>>(),
        [
            Status::Accepted,
            Status::Rejected,
            Status::Incomplete,
            Status::Accepted
        ]
    );
    for row in &result {
        let observations: Vec<_> = row
            .attempts
            .iter()
            .flat_map(|a| &a.backend_events)
            .filter(|e| e.stage == "rss_observation")
            .map(|e| serde_json::from_str::<serde_json::Value>(&e.detail).unwrap())
            .collect();
        assert!(
            observations.iter().any(|v| {
                v["kind"] == "leader_current_rss"
                    && v["bytes"].as_u64().unwrap() > 0
                    && row.attempts.iter().flat_map(|a| &a.processes).any(|p| {
                        v["pid"].as_u64() == Some(p.pid as u64)
                            && v["start_ticks"].as_u64() == Some(p.start_ticks)
                    })
            }),
            "before-retirement sample lacks its process/kind provenance"
        );
    }
    engine.shutdown().await;
}
#[tokio::test]
async fn timeout_retires_process_before_next_attempt() {
    let engine = engine();
    let result = tokio::time::timeout(
        Duration::from_secs(10),
        engine.verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("timeout", "slow", 30),
                candidate("next", "ok", 5000),
            ],
        }),
    )
    .await
    .unwrap()
    .unwrap();
    assert_eq!(result[0].outcome.status, Status::Timeout);
    assert_eq!(result[1].outcome.status, Status::Accepted);
    engine.shutdown().await;
}

struct SmallForecast;
impl SchedulingPolicy for SmallForecast {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
        Some(4 * 1024 * 1024)
    }
}
#[tokio::test]
async fn real_owned_rss_watchdog_kills_reaps_and_retries_exclusively() {
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/repl.py");
    let status = std::fs::read_to_string("/proc/self/status").unwrap();
    let text = status
        .lines()
        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
        .unwrap()
        .trim();
    let first = text
        .split([',', '-'])
        .next()
        .unwrap()
        .parse::<usize>()
        .unwrap();
    // This process integration needs two actually eligible CPUs.
    let second = if text.contains('-') {
        first + 1
    } else {
        text.split(',').nth(1).unwrap().parse().unwrap()
    };
    let backend = NativeRepl {
        program: PathBuf::from("/usr/bin/python3"),
        args: vec!["-u".into(), fixture.to_string_lossy().into()],
        project: std::env::temp_dir(),
        environment: "real-rss-fixture".into(),
    };
    let e = Engine::new(
        Config {
            memory_bytes: 50 * 1024 * 1024,
            cpus: vec![first, second],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(SmallForecast),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let rows = tokio::time::timeout(
        Duration::from_secs(15),
        e.verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("a", "memory_a", 10000),
                candidate("b", "memory_b", 10000),
            ],
        }),
    )
    .await
    .unwrap()
    .unwrap();
    assert!(
        rows.iter().all(|r| r.outcome.status == Status::Accepted),
        "{rows:?}"
    );
    let retry = rows
        .iter()
        .find(|r| r.attempts.len() > 1)
        .expect("actual RSS excess must exercise requeue");
    assert_eq!(retry.attempts[0].status, Status::Preempted);
    assert!(retry.attempts[1].exclusive);
    e.shutdown().await;
}

#[tokio::test]
async fn unavailable_prepared_host_uses_unchanged_native_fallback() {
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/repl.py");
    let fresh = NativeRepl {
        program: "/usr/bin/python3".into(),
        args: vec!["-u".into(), fixture.to_string_lossy().into()],
        project: std::env::temp_dir(),
        environment: "prepared-fallback-fixture-not-Lean".into(),
    };
    let backend = gpu_smt_lean::PreparedRepl::new(
        fresh,
        "/no-such-gpu-smt-prepared-host".into(),
        "/no-such-sdk".into(),
    );
    let e = Engine::new(
        Config {
            memory_bytes: 1 << 30,
            cpus: vec![cpu()],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let result = e
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("a", "ok", 5000),
                candidate("b", "bad", 5000),
                candidate("c", "sorry", 5000),
            ],
        })
        .await
        .unwrap();
    assert_eq!(
        result
            .iter()
            .map(|r| r.outcome.status.clone())
            .collect::<Vec<_>>(),
        [Status::Accepted, Status::Rejected, Status::Incomplete]
    );
    assert!(!e.prepared_state_ready());
    assert!(result.iter().all(|r| {
        r.attempts[0]
            .backend_events
            .iter()
            .any(|e| e.stage == "fresh_fallback")
    }));
    for p in result
        .iter()
        .flat_map(|r| r.attempts.iter().flat_map(|a| &a.processes))
    {
        assert!(
            gpu_smt_engine::linux::identity(p.pid).is_err(),
            "fallback child not retired"
        );
    }
    e.shutdown().await;
}
