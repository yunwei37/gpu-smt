use async_trait::async_trait;
use gpu_smt_core::*;
use gpu_smt_engine::*;
use serde_json::json;
use std::{
    sync::{
        Arc,
        atomic::{AtomicUsize, Ordering},
    },
    time::Duration,
};

struct Policy;
impl SchedulingPolicy for Policy {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
        Some(1)
    }
}
struct Monitor {
    per_job: u64,
}
impl ResourceMonitor for Monitor {
    fn sample(&self, roots: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        Ok(ResourceSnapshot {
            rss_bytes: roots.len() as u64 * self.per_job,
            processes: roots
                .iter()
                .map(|p| ProcessSample {
                    identity: p.clone(),
                    rss_bytes: self.per_job,
                })
                .collect(),
        })
    }
}
struct Backend {
    calls: AtomicUsize,
    delay_ms: u64,
}
#[async_trait]
impl VerificationBackend for Backend {
    fn identity(&self) -> String {
        "fixture-v1".into()
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        let n = self.calls.fetch_add(1, Ordering::SeqCst);
        let p = ProcessIdentity {
            pid: 10000 + n as u32,
            start_ticks: n as u64,
        };
        x.registry.register(p.clone());
        let result = tokio::select! {
            _=tokio::time::sleep(Duration::from_millis(if c.code=="winner"{self.delay_ms/5}else{self.delay_ms}))=>Outcome{
                status:if c.code=="bad"{Status::Rejected}else{Status::Accepted},
                response:Some(json!({"env":0,"messages":[]})),error:None},
            _=x.cancel.cancelled()=>Outcome::operational(Status::Cancelled,"fixture retired"),
        };
        x.registry.unregister(&p);
        result
    }
}
fn candidate(id: &str, code: &str, task: &str) -> Candidate {
    Candidate {
        id: id.into(),
        code: code.into(),
        task_id: Some(task.into()),
        timeout_ms: 30000,
        reuse: true,
    }
}
fn engine(backend: Arc<Backend>, per_job: u64) -> Engine {
    Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0, 1],
            cores_per_worker: 1,
        },
        backend,
        Arc::new(Policy),
        Arc::new(Monitor { per_job }),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap()
}
#[tokio::test]
async fn exact_duplicates_preserve_all_reward_rows_and_bypass_operational_cache() {
    let b = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 30,
    });
    let e = engine(b.clone(), 1);
    let result = e
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("a", "ok", "one"), candidate("b", "ok", "two")],
        })
        .await
        .unwrap();
    assert_eq!(result.len(), 2);
    assert_eq!(b.calls.load(Ordering::SeqCst), 1);
    assert_eq!(result.iter().filter(|v| v.coalesced).count(), 1);
    let result = e
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("c", "ok", "three")],
        })
        .await
        .unwrap();
    assert!(result[0].cached);
    let mut fresh = candidate("d", "ok", "four");
    fresh.reuse = false;
    e.verify_batch(Batch {
        mode: Mode::All,
        candidates: vec![fresh],
    })
    .await
    .unwrap();
    assert_eq!(b.calls.load(Ordering::SeqCst), 2);
    e.shutdown().await;
}
#[tokio::test]
async fn changed_timeout_and_source_are_not_duplicate_keys() {
    let b = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 5,
    });
    let e = engine(b.clone(), 1);
    let mut other = candidate("b", "ok", "one");
    other.timeout_ms = 1000;
    e.verify_batch(Batch {
        mode: Mode::All,
        candidates: vec![
            candidate("a", "ok", "one"),
            other,
            candidate("c", "ok ", "one"),
        ],
    })
    .await
    .unwrap();
    assert_eq!(b.calls.load(Ordering::SeqCst), 3);
    e.shutdown().await;
}
#[tokio::test]
async fn first_success_is_separate_from_every_candidate_rewards() {
    let b = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 30,
    });
    let e = engine(b, 1);
    let result = e
        .verify_batch(Batch {
            mode: Mode::FirstSuccess,
            candidates: vec![
                candidate("a", "ok", "one"),
                candidate("b", "bad", "one"),
                candidate("c", "other", "one"),
                candidate("d", "bad", "unsolved"),
            ],
        })
        .await
        .unwrap();
    assert_eq!(result[0].outcome.status, Status::Accepted);
    assert_eq!(result[3].outcome.status, Status::Rejected);
    assert!(
        result[2].outcome.status == Status::Cancelled
            || result[2].outcome.status == Status::Accepted
    );
    e.shutdown().await;
}
#[tokio::test]
async fn preempted_candidate_is_requeued_exclusively_with_history() {
    let b = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 1300,
    });
    let e = engine(b.clone(), 70);
    let result = e
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("a", "first", "one"),
                candidate("b", "second", "two"),
            ],
        })
        .await
        .unwrap();
    assert!(result.iter().all(|v| v.outcome.status == Status::Accepted));
    let retried = result.iter().find(|v| v.attempts.len() == 2).unwrap();
    assert_eq!(retried.attempts[0].status, Status::Preempted);
    assert!(retried.attempts[1].exclusive);
    assert_eq!(b.calls.load(Ordering::SeqCst), 3);
    e.shutdown().await;
}
#[tokio::test]
async fn oversized_solo_is_resource_failure_not_infinite_retry_or_rejection() {
    let b = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 30000,
    });
    let e = engine(b.clone(), 140);
    let result = e
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("a", "huge", "one")],
        })
        .await
        .unwrap();
    assert_eq!(result[0].outcome.status, Status::ResourceExhausted);
    assert_eq!(result[0].attempts.len(), 2);
    assert_eq!(b.calls.load(Ordering::SeqCst), 2);
    e.shutdown().await;
}
#[test]
fn memory_cache_does_not_promote_operational_outcomes() {
    let cache = MemoryCache::default();
    let key = CacheKey {
        backend: "v1".into(),
        code: "source".into(),
        timeout_ms: 100,
    };
    for status in [
        Status::Timeout,
        Status::Cancelled,
        Status::Preempted,
        Status::ResourceExhausted,
        Status::BackendError,
    ] {
        cache.insert(key.clone(), Outcome::operational(status, "operational"));
        assert!(cache.get(&key).is_none());
    }
}
#[test]
fn proc_monitor_is_owned_and_birth_checked() {
    let p = linux::identity(std::process::id()).unwrap();
    let monitor = linux::ProcMonitor::default();
    let sample = monitor.sample(std::slice::from_ref(&p)).unwrap();
    assert!(sample.rss_bytes > 0);
    let wrong = ProcessIdentity {
        pid: p.pid,
        start_ticks: p.start_ticks + 1,
    };
    let sample = monitor.sample(&[wrong]).unwrap();
    assert_eq!(sample.processes[0].rss_bytes, 0);
}
#[tokio::test]
async fn cancellation_of_one_consumer_does_not_abort_rl_duplicate_subscribers() {
    let b = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 50,
    });
    let e = engine(b.clone(), 1);
    let first = e.clone();
    let rl = e.clone();
    let (a, r) = tokio::join!(
        first.verify_batch(Batch {
            mode: Mode::FirstSuccess,
            candidates: vec![
                candidate("a", "winner", "one"),
                candidate("b", "duplicate", "one")
            ]
        }),
        rl.verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("r", "duplicate", "elsewhere")]
        })
    );
    assert_eq!(r.unwrap()[0].outcome.status, Status::Accepted);
    let first = a.unwrap();
    assert_eq!(first[0].outcome.status, Status::Accepted);
    assert_eq!(first[1].outcome.status, Status::Cancelled);
    assert_eq!(b.calls.load(Ordering::SeqCst), 2);
    e.shutdown().await;
}

struct SlowRetirement(AtomicUsize);
#[async_trait]
impl VerificationBackend for SlowRetirement {
    fn identity(&self) -> String {
        "retirement-fixture".into()
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        if c.code == "winner" {
            tokio::time::sleep(Duration::from_millis(30)).await;
            Outcome {
                status: Status::Accepted,
                response: None,
                error: None,
            }
        } else {
            x.cancel.cancelled().await;
            tokio::time::sleep(Duration::from_millis(100)).await;
            self.0.store(1, Ordering::Release);
            Outcome::operational(Status::Cancelled, "retired")
        }
    }
}
#[tokio::test]
async fn first_success_waits_for_last_subscribers_backend_retirement() {
    let b = Arc::new(SlowRetirement(AtomicUsize::new(0)));
    let e = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0, 1],
            cores_per_worker: 1,
        },
        b.clone(),
        Arc::new(Policy),
        Arc::new(Monitor { per_job: 1 }),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let rows = e
        .verify_batch(Batch {
            mode: Mode::FirstSuccess,
            candidates: vec![
                candidate("a", "winner", "task"),
                candidate("b", "long", "task"),
            ],
        })
        .await
        .unwrap();
    assert_eq!(b.0.load(Ordering::Acquire), 1);
    assert_eq!(rows[1].outcome.status, Status::Cancelled);
    assert!(rows[1].elapsed_seconds >= 0.1);
    assert_eq!(rows[1].attempts.len(), 1);
    e.shutdown().await;
}

#[test]
fn owned_idle_preparation_is_included_in_total_rss() {
    use std::io::BufRead;
    let monitor = linux::ProcMonitor::default();
    let before = monitor.sample(&[]).unwrap().rss_bytes;
    let mut child = std::process::Command::new("/usr/bin/python3")
        .args([
            "-u",
            "-c",
            "import time; data=bytearray(8*1024*1024); print('ready',flush=True); time.sleep(5)",
        ])
        .stdout(std::process::Stdio::piped())
        .spawn()
        .unwrap();
    let mut line = String::new();
    std::io::BufReader::new(child.stdout.take().unwrap())
        .read_line(&mut line)
        .unwrap();
    let after = monitor.sample(&[]).unwrap().rss_bytes;
    child.kill().unwrap();
    child.wait().unwrap();
    assert!(
        after > before + 4 * 1024 * 1024,
        "idle native preparation must not disappear from aggregate RSS"
    );
}

#[tokio::test]
async fn unknown_forecasts_refresh_from_live_observations() {
    let b = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 1300,
    });
    let e = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0, 1],
            cores_per_worker: 1,
        },
        b.clone(),
        Arc::new(Fifo),
        Arc::new(Monitor { per_job: 1 }),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let worker = e.clone();
    let run = tokio::spawn(async move {
        worker
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![
                    candidate("a", "work_a", "one"),
                    candidate("b", "work_b", "two"),
                    candidate("c", "work_c", "three"),
                ],
            })
            .await
    });
    tokio::time::sleep(Duration::from_millis(1150)).await;
    assert!(
        b.calls.load(Ordering::SeqCst) >= 2,
        "first RSS observation must unlock remaining CPU capacity"
    );
    assert!(
        run.await
            .unwrap()
            .unwrap()
            .iter()
            .all(|v| v.outcome.status == Status::Accepted)
    );
    e.shutdown().await;
}

struct CountingMonitor(AtomicUsize);
impl ResourceMonitor for CountingMonitor {
    fn sample(&self, roots: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        self.0.fetch_add(1, Ordering::Relaxed);
        Monitor { per_job: 1 }.sample(roots)
    }
}
#[tokio::test]
async fn large_waiting_batch_does_not_rescan_process_table_per_candidate() {
    let backend = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 30000,
    });
    let monitor = Arc::new(CountingMonitor(AtomicUsize::new(0)));
    let e = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0, 1],
            cores_per_worker: 1,
        },
        backend,
        Arc::new(Policy),
        monitor.clone(),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let worker = e.clone();
    let run = tokio::spawn(async move {
        worker
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: (0..1024)
                    .map(|i| candidate(&i.to_string(), &format!("source{i}"), "task"))
                    .collect(),
            })
            .await
    });
    tokio::time::sleep(Duration::from_millis(1100)).await;
    assert!(
        monitor.0.load(Ordering::Relaxed) < 32,
        "queued workload must not multiply resource scans"
    );
    e.shutdown().await;
    assert_eq!(run.await.unwrap().unwrap().len(), 1024);
}
