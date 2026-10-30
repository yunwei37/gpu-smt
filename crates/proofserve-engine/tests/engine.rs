use async_trait::async_trait;
use proofserve_core::*;
use proofserve_engine::*;
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
fn engine(backend: Arc<dyn VerificationBackend>, per_job: u64) -> Engine {
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
    struct RetryBackend {
        base: Backend,
        retries: AtomicUsize,
    }
    #[async_trait]
    impl VerificationBackend for RetryBackend {
        fn identity(&self) -> String {
            self.base.identity()
        }
        async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
            self.base.verify(c, x).await
        }
        async fn verify_resource_retry(&self, c: &Candidate, x: Execution) -> Outcome {
            self.retries.fetch_add(1, Ordering::SeqCst);
            self.base.verify(c, x).await
        }
    }
    let b = Arc::new(RetryBackend {
        base: Backend {
            calls: AtomicUsize::new(0),
            delay_ms: 1300,
        },
        retries: AtomicUsize::new(0),
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
    assert_eq!(b.base.calls.load(Ordering::SeqCst), 3);
    assert_eq!(b.retries.load(Ordering::SeqCst), 1);
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
#[tokio::test(flavor = "current_thread")]
async fn watchdog_preempts_while_the_request_executor_is_blocked() {
    struct BlockingBackend {
        cancelled_while_blocked: std::sync::atomic::AtomicBool,
        immediate_interrupt: std::sync::atomic::AtomicBool,
        solo_calls: AtomicUsize,
    }
    #[async_trait]
    impl VerificationBackend for BlockingBackend {
        fn request_resource_preemption(&self, processes: &[ProcessIdentity]) {
            assert_eq!(
                processes,
                &[ProcessIdentity {
                    pid: 54321,
                    start_ticks: 7
                }]
            );
            self.immediate_interrupt.store(true, Ordering::SeqCst);
        }
        fn identity(&self) -> String {
            "blocked-executor-fixture".into()
        }
        async fn verify(&self, _: &Candidate, x: Execution) -> Outcome {
            let identity = ProcessIdentity {
                pid: 54321,
                start_ticks: 7,
            };
            x.registry.register(identity.clone());
            // Occupy the only Tokio executor: an async timer/task on this
            // executor cannot enforce the budget during this bounded wait.
            let deadline = std::time::Instant::now() + Duration::from_secs(3);
            while !(x.cancel.is_cancelled() && self.immediate_interrupt.load(Ordering::SeqCst))
                && std::time::Instant::now() < deadline
            {
                std::thread::sleep(Duration::from_millis(5));
            }
            self.cancelled_while_blocked.store(
                x.cancel.is_cancelled() && self.immediate_interrupt.load(Ordering::SeqCst),
                Ordering::SeqCst,
            );
            x.registry.unregister(&identity);
            Outcome::operational(Status::Cancelled, "blocking fixture retired")
        }
        async fn verify_resource_retry(&self, _: &Candidate, _: Execution) -> Outcome {
            self.solo_calls.fetch_add(1, Ordering::SeqCst);
            Outcome::operational(Status::Rejected, "solo fixture retired")
        }
    }
    let backend = Arc::new(BlockingBackend {
        cancelled_while_blocked: std::sync::atomic::AtomicBool::new(false),
        immediate_interrupt: std::sync::atomic::AtomicBool::new(false),
        solo_calls: AtomicUsize::new(0),
    });
    let e = engine(backend.clone(), 140);
    let result = e
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("blocked", "proof", "task")],
        })
        .await
        .unwrap();
    assert!(
        backend.cancelled_while_blocked.load(Ordering::SeqCst),
        "budget cancellation depended on the blocked request executor"
    );
    assert_eq!(result[0].outcome.status, Status::Rejected);
    assert_eq!(result[0].attempts.len(), 2);
    assert_eq!(result[0].attempts[0].status, Status::Preempted);
    assert!(result[0].attempts[1].exclusive);
    assert_eq!(backend.solo_calls.load(Ordering::SeqCst), 1);
    e.shutdown().await;
}

#[tokio::test(flavor = "current_thread")]
async fn dropping_the_last_engine_retires_its_sampling_thread() {
    struct DropMonitor(std::sync::mpsc::Sender<()>);
    impl ResourceMonitor for DropMonitor {
        fn sample(&self, _: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
            Ok(ResourceSnapshot::default())
        }
    }
    impl Drop for DropMonitor {
        fn drop(&mut self) {
            let _ = self.0.send(());
        }
    }
    let (retired, retirement) = std::sync::mpsc::channel();
    let e = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0],
            cores_per_worker: 1,
        },
        Arc::new(Backend {
            calls: AtomicUsize::new(0),
            delay_ms: 1,
        }),
        Arc::new(Policy),
        Arc::new(DropMonitor(retired)),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let clone = e.clone();
    drop(e);
    assert!(matches!(
        retirement.try_recv(),
        Err(std::sync::mpsc::TryRecvError::Empty)
    ));
    drop(clone);
    retirement
        .recv_timeout(Duration::from_secs(2))
        .expect("the sampling thread retained the last engine owner");
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

struct DelayedFirstForecast {
    second_seen: std::sync::Mutex<bool>,
    changed: std::sync::Condvar,
}
impl SchedulingPolicy for DelayedFirstForecast {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn predicted_rss(&self, c: &Candidate) -> Option<u64> {
        if c.id == "early" {
            let seen = self.second_seen.lock().unwrap();
            let (seen, _) = self
                .changed
                .wait_timeout_while(seen, Duration::from_secs(2), |seen| !*seen)
                .unwrap();
            assert!(*seen, "second forecast never became runnable");
            drop(seen);
            // Make the earlier forecast finish after the later forecast.
            std::thread::sleep(Duration::from_millis(50));
        } else {
            *self.second_seen.lock().unwrap() = true;
            self.changed.notify_all();
        }
        Some(1)
    }
}
struct ExecutionOrder(std::sync::Mutex<Vec<String>>);
#[async_trait]
impl VerificationBackend for ExecutionOrder {
    fn identity(&self) -> String {
        "execution-order-fixture".into()
    }
    async fn verify(&self, c: &Candidate, _: Execution) -> Outcome {
        self.0.lock().unwrap().push(c.id.clone());
        Outcome {
            status: if c.code.starts_with("bad") {
                Status::Rejected
            } else {
                Status::Accepted
            },
            response: Some(json!({"env":0,"messages":[]})),
            error: None,
        }
    }
}
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn submitted_order_survives_delayed_forecast_and_task_wakeup() {
    let backend = Arc::new(ExecutionOrder(std::sync::Mutex::new(vec![])));
    let engine = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0],
            cores_per_worker: 1,
        },
        backend.clone(),
        Arc::new(DelayedFirstForecast {
            second_seen: std::sync::Mutex::new(false),
            changed: std::sync::Condvar::new(),
        }),
        Arc::new(Monitor { per_job: 1 }),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let results = tokio::time::timeout(
        Duration::from_secs(5),
        engine.verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("early", "early source", "one"),
                candidate("late", "late source", "two"),
            ],
        }),
    )
    .await
    .unwrap()
    .unwrap();
    engine.shutdown().await;
    assert_eq!(results.len(), 2);
    assert_eq!(
        *backend.0.lock().unwrap(),
        vec!["early", "late"],
        "cost-model latency must not change stable submitted policy order"
    );
}

struct CoupledStarts {
    calls: AtomicUsize,
    together: tokio::sync::Barrier,
}
#[async_trait]
impl VerificationBackend for CoupledStarts {
    fn identity(&self) -> String {
        "coupled-starts-fixture".into()
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        self.calls.fetch_add(1, Ordering::SeqCst);
        if c.code != "cached" {
            tokio::select! {
                _ = self.together.wait() => {},
                _ = x.cancel.cancelled() => return Outcome::operational(
                    Status::Cancelled, "fixture cancelled and retired"),
            }
        }
        Outcome {
            status: Status::Accepted,
            response: Some(json!({"env":0,"messages":[]})),
            error: None,
        }
    }
}
#[tokio::test]
async fn cached_and_coalesced_tickets_do_not_block_independent_cpu_capacity() {
    let backend = Arc::new(CoupledStarts {
        calls: AtomicUsize::new(0),
        together: tokio::sync::Barrier::new(2),
    });
    let engine = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0, 1],
            cores_per_worker: 1,
        },
        backend.clone(),
        Arc::new(Policy),
        Arc::new(Monitor { per_job: 1 }),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![candidate("warm", "cached", "warm")],
        })
        .await
        .unwrap();
    let result = tokio::time::timeout(
        Duration::from_secs(2),
        engine.verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("cached", "cached", "zero"),
                candidate("physical", "work", "one"),
                candidate("shared", "work", "two"),
                candidate("independent", "other", "three"),
            ],
        }),
    )
    .await;
    engine.shutdown().await;
    let results = result
        .expect("unused queue ticket blocks the other core")
        .unwrap();
    assert!(results[0].cached);
    assert!(results[2].coalesced);
    assert!(results.iter().all(|v| v.outcome.status == Status::Accepted));
    assert_eq!(backend.calls.load(Ordering::SeqCst), 3);
}

#[test]
fn task_interleaving_composes_source_ranking_and_memory_forecasts() {
    let candidates = vec![
        candidate("a-long", "xxxxxx", "a"),
        candidate("a-short", "b", "a"),
        candidate("b-long", "ccc", "b"),
        candidate("b-short", "dd", "b"),
    ];
    let policy = TaskInterleave::new(SourceSize);
    let priorities = policy.batch_priorities(&candidates, Mode::FirstSuccess);
    let mut order: Vec<_> = (0..candidates.len()).collect();
    order.sort_by_key(|i| priorities[*i]);
    assert_eq!(
        order
            .iter()
            .map(|i| candidates[*i].id.as_str())
            .collect::<Vec<_>>(),
        vec!["a-short", "b-short", "a-long", "b-long"]
    );
    assert_eq!(
        policy.batch_priorities(&candidates, Mode::All),
        SourceSize.batch_priorities(&candidates, Mode::All)
    );
    assert_eq!(
        TaskInterleave::new(Policy).predicted_rss(&candidates[0]),
        Some(1)
    );
}

#[tokio::test]
async fn task_interleaving_drives_execution_without_changing_all_mode_order() {
    for (mode, expected) in [
        (Mode::FirstSuccess, vec!["a0", "b0", "c0", "a1", "b1", "c1"]),
        (Mode::All, vec!["a0", "a1", "b0", "b1", "c0", "c1"]),
    ] {
        let backend = Arc::new(ExecutionOrder(std::sync::Mutex::new(vec![])));
        let engine = Engine::new(
            Config {
                memory_bytes: 100,
                cpus: vec![0],
                cores_per_worker: 1,
            },
            backend.clone(),
            Arc::new(TaskInterleave::new(Fifo)),
            Arc::new(Monitor { per_job: 1 }),
            Arc::new(HeadroomAdmission),
            Arc::new(MemoryCache::default()),
        )
        .unwrap();
        let results = engine
            .verify_batch(Batch {
                mode,
                candidates: vec![
                    candidate("a0", "bad-a0", "a"),
                    candidate("a1", "bad-a1", "a"),
                    candidate("b0", "bad-b0", "b"),
                    candidate("b1", "bad-b1", "b"),
                    candidate("c0", "bad-c0", "c"),
                    candidate("c1", "bad-c1", "c"),
                ],
            })
            .await
            .unwrap();
        engine.shutdown().await;
        assert_eq!(*backend.0.lock().unwrap(), expected);
        assert!(results.iter().all(|v| v.outcome.status == Status::Rejected));
        assert_eq!(
            results.iter().map(|v| v.id.as_str()).collect::<Vec<_>>(),
            vec!["a0", "a1", "b0", "b1", "c0", "c1"]
        );
    }
}

struct InvalidBatchPolicy;
impl SchedulingPolicy for InvalidBatchPolicy {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn batch_priorities(&self, _: &[Candidate], _: Mode) -> Vec<u64> {
        vec![]
    }
}
#[tokio::test]
async fn invalid_batch_policy_is_an_interface_error_before_native_work() {
    let backend = Arc::new(Backend {
        calls: AtomicUsize::new(0),
        delay_ms: 1,
    });
    let engine = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0],
            cores_per_worker: 1,
        },
        backend.clone(),
        Arc::new(TaskInterleave::new(InvalidBatchPolicy)),
        Arc::new(Monitor { per_job: 1 }),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let result = engine
        .verify_batch(Batch {
            mode: Mode::FirstSuccess,
            candidates: vec![candidate("a", "ok", "one")],
        })
        .await;
    engine.shutdown().await;
    assert!(result.unwrap_err().contains("one priority"));
    assert_eq!(backend.calls.load(Ordering::SeqCst), 0);
}

struct StreamGate {
    started: tokio::sync::Notify,
    release: tokio::sync::Notify,
    retired: tokio::sync::Notify,
    cancelled: AtomicUsize,
    calls: AtomicUsize,
}
#[async_trait]
impl VerificationBackend for StreamGate {
    fn identity(&self) -> String {
        "stream-gate-fixture-not-Lean".into()
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        self.calls.fetch_add(1, Ordering::SeqCst);
        if c.code == "winner" {
            self.started.notified().await;
        }
        if c.code == "hold" {
            self.started.notify_one();
            tokio::select! {
                _ = self.release.notified() => {}
                _ = x.cancel.cancelled() => {
                    self.cancelled.fetch_add(1, Ordering::SeqCst);
                    self.retired.notify_one();
                    return Outcome::operational(Status::Cancelled, "fixture retired");
                }
            }
        }
        Outcome {
            status: Status::Accepted,
            response: Some(json!({"messages":[]})),
            error: None,
        }
    }
}
#[tokio::test]
async fn stream_disconnect_preserves_shared_rl_subscription() {
    let b = Arc::new(StreamGate {
        started: tokio::sync::Notify::new(),
        release: tokio::sync::Notify::new(),
        retired: tokio::sync::Notify::new(),
        cancelled: AtomicUsize::new(0),
        calls: AtomicUsize::new(0),
    });
    let e = engine(b.clone(), 0);
    let rl_engine = e.clone();
    let rl = tokio::spawn(async move {
        rl_engine
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![candidate("rl", "hold", "one")],
            })
            .await
            .unwrap()
    });
    b.started.notified().await;
    let mut stream = e
        .verify_stream(Batch {
            mode: Mode::All,
            candidates: vec![
                candidate("stream", "hold", "one"),
                candidate("fast", "ok", "two"),
            ],
        })
        .unwrap();
    let first = tokio::time::timeout(Duration::from_secs(5), stream.recv())
        .await
        .unwrap()
        .unwrap();
    assert!(matches!(first, BatchEvent::Result { index: 1, .. }));
    // Receiving fast proves this stream's shared hold subscription was installed.
    drop(stream);
    b.release.notify_one();
    let rows = tokio::time::timeout(Duration::from_secs(5), rl)
        .await
        .unwrap()
        .unwrap();
    assert_eq!(rows[0].outcome.status, Status::Accepted);
    assert_eq!(b.calls.load(Ordering::SeqCst), 2);
    assert_eq!(b.cancelled.load(Ordering::SeqCst), 0);
    e.shutdown().await;
}

#[tokio::test]
async fn unread_stream_cancels_checked_siblings_and_emits_complete_rows() {
    let b = Arc::new(StreamGate {
        started: tokio::sync::Notify::new(),
        release: tokio::sync::Notify::new(),
        retired: tokio::sync::Notify::new(),
        cancelled: AtomicUsize::new(0),
        calls: AtomicUsize::new(0),
    });
    let e = engine(b.clone(), 0);
    let mut stream = e
        .verify_stream(Batch {
            mode: Mode::FirstSuccess,
            candidates: vec![
                candidate("winner", "winner", "one"),
                candidate("sibling", "hold", "one"),
                candidate("other", "other", "two"),
            ],
        })
        .unwrap();
    // Require actual sibling retirement before reading any event. This uses
    // logical synchronization, not a performance/timer ordering assumption.
    tokio::time::timeout(Duration::from_secs(5), b.retired.notified())
        .await
        .unwrap();
    let mut results = std::collections::BTreeMap::new();
    let mut complete = false;
    while let Some(event) = stream.recv().await {
        match event {
            BatchEvent::Result {
                index,
                verification,
            } => {
                assert!(results.insert(index, verification).is_none());
            }
            BatchEvent::Complete { count } => {
                assert_eq!(count, 3);
                complete = true;
            }
            BatchEvent::Error { message } => panic!("{message}"),
        }
    }
    assert!(complete);
    assert_eq!(results[&0].outcome.status, Status::Accepted);
    assert_eq!(results[&1].outcome.status, Status::Cancelled);
    assert_eq!(results[&2].outcome.status, Status::Accepted);
    e.shutdown().await;
}

// A resident import parent/engine can strand an otherwise idle queue when
// a source forecast fits the total budget but not remaining headroom.
// Toy units and a fixture backend: this is not a native speed/acceptance test.
struct IdleHeadroom {
    rss: AtomicUsize,
    calls: AtomicUsize,
    reclaims: AtomicUsize,
}
impl ResourceMonitor for IdleHeadroom {
    fn sample(&self, _: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        Ok(ResourceSnapshot {
            rss_bytes: self.rss.load(Ordering::SeqCst) as u64,
            processes: vec![],
        })
    }
}
#[async_trait]
impl VerificationBackend for IdleHeadroom {
    fn identity(&self) -> String {
        "idle-headroom-fixture-not-Lean".into()
    }
    async fn verify(&self, _: &Candidate, _: Execution) -> Outcome {
        self.calls.fetch_add(1, Ordering::SeqCst);
        Outcome {
            status: Status::Accepted,
            response: Some(json!({"messages":[]})),
            error: None,
        }
    }
    async fn verify_resource_retry(&self, c: &Candidate, x: Execution) -> Outcome {
        self.reclaims.fetch_add(1, Ordering::SeqCst);
        self.rss.store(0, Ordering::SeqCst);
        self.verify(c, x).await
    }
}
struct FixedForecast(u64);
impl SchedulingPolicy for FixedForecast {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
        Some(self.0)
    }
}
#[tokio::test]
async fn idle_native_state_cannot_strand_a_large_forecast() {
    for (idle_rss, forecast, reclaims, accepted) in [
        (20, 1, 0, true),
        (20, 90, 1, true),
        (20, 100, 1, true),
        (20, 200, 1, true),
        (101, 90, 0, false),
    ] {
        let backend = Arc::new(IdleHeadroom {
            rss: AtomicUsize::new(idle_rss),
            calls: AtomicUsize::new(0),
            reclaims: AtomicUsize::new(0),
        });
        let engine = Engine::new(
            Config {
                memory_bytes: 100,
                cpus: vec![0, 1],
                cores_per_worker: 1,
            },
            backend.clone(),
            Arc::new(FixedForecast(forecast)),
            backend.clone(),
            Arc::new(HeadroomAdmission),
            Arc::new(MemoryCache::default()),
        )
        .unwrap();
        let result = tokio::time::timeout(
            Duration::from_secs(5),
            engine.verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![candidate("large", "source", "one")],
            }),
        )
        .await;
        engine.shutdown().await;
        let rows = result
            .expect("idle resident memory strands a below-total-budget forecast")
            .unwrap();
        assert_eq!(
            rows[0].outcome.status,
            if accepted {
                Status::Accepted
            } else {
                Status::BackendError
            }
        );
        assert_eq!(backend.calls.load(Ordering::SeqCst), usize::from(accepted));
        assert_eq!(backend.reclaims.load(Ordering::SeqCst), reclaims);
        if accepted {
            assert_eq!(rows[0].attempts.len(), 1);
            assert_eq!(rows[0].attempts[0].exclusive, reclaims > 0);
        } else {
            assert!(
                rows[0].attempts.is_empty(),
                "actual over-budget RSS must block execution"
            );
        }
    }
}

#[test]
fn task_memory_forecasts_are_scoped_and_never_lower_existing_reservations() {
    let policy = TaskMemory::new(SourceSize);
    let c = candidate("teacher", "source", "same-task");
    let sibling = candidate("sibling", "different-source", "same-task");
    assert_eq!(
        policy.refresh_rss(&sibling, "native-resource-A", None),
        None
    );
    policy.observe_rss(&c, "native-resource-A", 90);
    policy.observe_rss(&c, "native-resource-A", 0);
    policy.observe_rss(&c, "native-resource-A", 40);
    assert_eq!(
        policy.refresh_rss(&sibling, "native-resource-A", None),
        Some(90)
    );
    assert_eq!(
        policy.refresh_rss(&sibling, "native-resource-A", Some(200)),
        Some(200)
    );
    assert_eq!(
        policy.refresh_rss(&sibling, "prepared-resource-B", Some(1)),
        Some(1)
    );
    let mut changed_timeout = sibling.clone();
    changed_timeout.timeout_ms += 1;
    assert_eq!(
        policy.refresh_rss(&changed_timeout, "native-resource-A", None),
        None
    );
    for task in [None, Some(String::new())] {
        let mut anonymous = c.clone();
        anonymous.task_id = task;
        policy.observe_rss(&anonymous, "native-resource-A", 300);
        assert_eq!(
            policy.refresh_rss(&anonymous, "native-resource-A", Some(1)),
            Some(1)
        );
    }
    assert_eq!(policy.priority(&sibling), sibling.code.len() as u64);
    policy.clear_memory();
    assert_eq!(
        policy.refresh_rss(&sibling, "native-resource-A", None),
        None
    );

    let composed = TaskMemory::new(TaskInterleave::new(SourceSize));
    assert_eq!(
        composed.batch_priorities(
            &[
                candidate("long", "long-source", "a"),
                candidate("short", "x", "a"),
                candidate("other", "xx", "b"),
            ],
            Mode::FirstSuccess,
        ),
        vec![2, 0, 1],
    );
}

struct MemorySignals {
    second_forecast: tokio::sync::Notify,
    second_refresh: tokio::sync::Notify,
    finish_peer: tokio::sync::Notify,
    peer_alive: std::sync::atomic::AtomicBool,
    sibling_reclaims: AtomicUsize,
}
struct SignalledForecast(Arc<MemorySignals>);
impl SchedulingPolicy for SignalledForecast {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn predicted_rss(&self, c: &Candidate) -> Option<u64> {
        if c.id == "sibling" {
            // Teacher cannot finish until this stale initial forecast exists.
            self.0.second_forecast.notify_one();
        }
        Some(1)
    }
    fn refresh_rss(&self, c: &Candidate, _: &str, initial: Option<u64>) -> Option<u64> {
        if c.id == "sibling" {
            self.0.second_refresh.notify_one();
        }
        initial
    }
}
struct MemoryFeedbackBackend(Arc<MemorySignals>);
#[async_trait]
impl VerificationBackend for MemoryFeedbackBackend {
    fn identity(&self) -> String {
        "measured-memory-fixture-not-Lean".into()
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        if c.id == "teacher" {
            tokio::select! {
                _=self.0.second_forecast.notified()=>{},
                _=x.cancel.cancelled()=>return Outcome::operational(Status::Cancelled,"fixture retired"),
            }
            // Toy memory units from a completed physical backend attempt.
            // No native process or proof execution is represented by this fixture.
            x.registry.observe_rss(100);
            Outcome {
                status: Status::Rejected,
                response: Some(
                    json!({"messages":[{"severity":"error","data":"teacher fixture error"}]}),
                ),
                error: None,
            }
        } else {
            if c.id == "peer" {
                self.0.peer_alive.store(true, Ordering::SeqCst);
                tokio::select! {
                    _=self.0.finish_peer.notified()=>{},
                    _=x.cancel.cancelled()=>{},
                }
                self.0.peer_alive.store(false, Ordering::SeqCst);
            }
            Outcome {
                status: Status::Accepted,
                response: Some(json!({"env":0,"messages":[]})),
                error: None,
            }
        }
    }
    async fn verify_resource_retry(&self, c: &Candidate, x: Execution) -> Outcome {
        if c.id == "sibling" {
            assert!(!self.0.peer_alive.load(Ordering::SeqCst));
            self.0.sibling_reclaims.fetch_add(1, Ordering::SeqCst);
        }
        self.verify(c, x).await
    }
}
#[tokio::test]
async fn queued_sibling_refreshes_only_after_measured_memory_and_keeps_own_verdict() {
    let signals = Arc::new(MemorySignals {
        second_forecast: tokio::sync::Notify::new(),
        second_refresh: tokio::sync::Notify::new(),
        finish_peer: tokio::sync::Notify::new(),
        peer_alive: std::sync::atomic::AtomicBool::new(false),
        sibling_reclaims: AtomicUsize::new(0),
    });
    let e = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0, 1],
            cores_per_worker: 1,
        },
        Arc::new(MemoryFeedbackBackend(signals.clone())),
        Arc::new(TaskInterleave::new(TaskMemory::new(SignalledForecast(
            signals.clone(),
        )))),
        Arc::new(Monitor { per_job: 0 }),
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
                    candidate("teacher", "teacher-source", "same-task"),
                    candidate("peer", "peer-source", "another-task"),
                    candidate("sibling", "sibling-source", "same-task"),
                ],
            })
            .await
    });
    tokio::time::timeout(Duration::from_secs(2), signals.second_refresh.notified())
        .await
        .unwrap();
    signals.finish_peer.notify_one();
    let outcome = tokio::time::timeout(Duration::from_secs(2), run).await;
    e.shutdown().await;
    let rows = outcome.unwrap().unwrap().unwrap();
    assert_eq!(rows.len(), 3);
    assert_eq!(rows[0].outcome.status, Status::Rejected);
    assert_eq!(rows[1].outcome.status, Status::Accepted);
    assert_eq!(rows[2].outcome.status, Status::Accepted);
    assert_eq!(signals.sibling_reclaims.load(Ordering::SeqCst), 1);
    assert!(rows[2].attempts[0].exclusive);
    assert_eq!(
        rows[2].attempts.len(),
        1,
        "no predicted failure or speculative native retry"
    );
}

// A failed attempt must not put a drain barrier in front of already queued work.
#[tokio::test]
async fn resource_retry_waits_behind_normal_work_without_blocking_free_slots() {
    use std::sync::Mutex;
    use tokio::sync::Semaphore;
    struct TailBackend {
        peer_started: Semaphore,
        release_peer: Semaphore,
        small_finished: Semaphore,
        live: AtomicUsize,
        events: Mutex<Vec<String>>,
    }
    #[async_trait]
    impl VerificationBackend for TailBackend {
        fn identity(&self) -> String {
            "retry-tail-fixture".into()
        }
        async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
            self.live.fetch_add(1, Ordering::SeqCst);
            self.events.lock().unwrap().push(c.id.clone());
            let result = match c.id.as_str() {
                "retry" => {
                    tokio::select! {
                        permit = self.peer_started.acquire() => { permit.unwrap().forget(); }
                        _ = x.cancel.cancelled() => {}
                    }
                    Outcome::operational(
                        Status::ResourceExhausted,
                        "actual fixture resource failure",
                    )
                }
                "peer" => {
                    self.peer_started.add_permits(1);
                    tokio::select! {
                        permit = self.release_peer.acquire() => { permit.unwrap().forget(); }
                        _ = x.cancel.cancelled() => {}
                    }
                    Outcome::operational(Status::Rejected, "peer retired")
                }
                _ => {
                    self.small_finished.add_permits(1);
                    Outcome::operational(Status::Accepted, "small retired")
                }
            };
            self.live.fetch_sub(1, Ordering::SeqCst);
            result
        }
        async fn verify_resource_retry(&self, c: &Candidate, _: Execution) -> Outcome {
            assert_eq!(self.live.load(Ordering::SeqCst), 0, "retry overlaps a peer");
            self.events.lock().unwrap().push(format!("{}-solo", c.id));
            Outcome::operational(Status::Rejected, "exclusive result")
        }
    }
    let b = Arc::new(TailBackend {
        peer_started: Semaphore::new(0),
        release_peer: Semaphore::new(0),
        small_finished: Semaphore::new(0),
        live: AtomicUsize::new(0),
        events: Mutex::new(vec![]),
    });
    struct TailPolicy {
        retry_refreshes: AtomicUsize,
        retry_queued: Semaphore,
        later_queued: Semaphore,
    }
    impl SchedulingPolicy for TailPolicy {
        fn priority(&self, c: &Candidate) -> u64 {
            if c.id == "later" {
                self.later_queued.add_permits(1);
            }
            if c.id.starts_with("small") {
                u64::MAX
            } else {
                0
            }
        }
        fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
            Some(1)
        }
        fn refresh_rss(&self, c: &Candidate, _: &str, initial: Option<u64>) -> Option<u64> {
            if c.id == "retry" && self.retry_refreshes.fetch_add(1, Ordering::SeqCst) == 1 {
                self.retry_queued.add_permits(1);
            }
            initial
        }
    }
    let policy = Arc::new(TailPolicy {
        retry_refreshes: AtomicUsize::new(0),
        retry_queued: Semaphore::new(0),
        later_queued: Semaphore::new(0),
    });
    let e = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0, 1],
            cores_per_worker: 1,
        },
        b.clone(),
        policy.clone(),
        Arc::new(Monitor { per_job: 1 }),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let worker = e.clone();
    let batch = tokio::spawn(async move {
        worker
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![
                    candidate("retry", "retry", "one"),
                    candidate("peer", "peer", "two"),
                    candidate("small-a", "small-a", "three"),
                    candidate("small-b", "small-b", "four"),
                ],
            })
            .await
            .unwrap()
    });
    let normal_progress =
        tokio::time::timeout(Duration::from_secs(2), b.small_finished.acquire_many(2)).await;
    let progressed = normal_progress.is_ok();
    if let Ok(permit) = normal_progress {
        permit.unwrap().forget();
    }
    let later = if progressed {
        let permit = tokio::time::timeout(Duration::from_secs(2), policy.retry_queued.acquire())
            .await
            .unwrap()
            .unwrap();
        permit.forget();
        let worker = e.clone();
        let later = tokio::spawn(async move {
            worker
                .verify_batch(Batch {
                    mode: Mode::All,
                    candidates: vec![candidate("later", "later", "five")],
                })
                .await
                .unwrap()
        });
        let permit = tokio::time::timeout(Duration::from_secs(2), policy.later_queued.acquire())
            .await
            .unwrap()
            .unwrap();
        permit.forget();
        Some(later)
    } else {
        None
    };
    // Always release/retire the held peer, including the old-behavior control.
    b.release_peer.add_permits(1);
    let rows = tokio::time::timeout(Duration::from_secs(2), batch).await;
    if let Some(later) = later {
        let rows = tokio::time::timeout(Duration::from_secs(2), later)
            .await
            .unwrap()
            .unwrap();
        assert_eq!(rows[0].outcome.status, Status::Accepted);
    }
    e.shutdown().await;
    let rows = rows.unwrap().unwrap();
    assert!(
        progressed,
        "retry waiter blocked normal work in an available CPU/RSS slot"
    );
    assert_eq!(rows.len(), 4);
    assert_eq!(rows[0].outcome.status, Status::Rejected);
    assert_eq!(rows[0].attempts.len(), 2);
    assert_eq!(rows[0].attempts[0].status, Status::ResourceExhausted);
    assert!(!rows[0].attempts[0].exclusive);
    assert!(rows[0].attempts[1].exclusive);
    assert!(
        rows[2..]
            .iter()
            .all(|r| r.outcome.status == Status::Accepted)
    );
    let events = b.events.lock().unwrap();
    let retry = events.iter().position(|e| e == "retry-solo").unwrap();
    let later = events.iter().position(|e| e == "later").unwrap();
    assert!(events.iter().position(|e| e == "small-a").unwrap() < retry);
    assert!(events.iter().position(|e| e == "small-b").unwrap() < retry);
    assert!(
        retry < later,
        "later batches must not starve an already deferred retry"
    );
}

// Shutdown must wake a deferred ticket even while its peer owns a lease.
#[tokio::test]
async fn shutdown_cancels_a_deferred_retry_without_dispatching_it() {
    use tokio::sync::Semaphore;
    struct CancelBackend {
        failed: Semaphore,
        held: Semaphore,
        release: Semaphore,
        retries: AtomicUsize,
    }
    #[async_trait]
    impl VerificationBackend for CancelBackend {
        fn identity(&self) -> String {
            "cancel-retry-tail-fixture".into()
        }
        async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
            if c.id == "retry" {
                // Wait until another batch owns a lease, so a retry stays queued.
                let permit = self.held.acquire().await.unwrap();
                permit.forget();
                self.failed.add_permits(1);
                return Outcome::operational(Status::ResourceExhausted, "fixture failure");
            }
            self.held.add_permits(1);
            tokio::select! {
                permit = self.release.acquire() => { permit.unwrap().forget(); }
                _ = x.cancel.cancelled() => {}
            }
            Outcome::operational(Status::Accepted, "held work retired")
        }
        async fn verify_resource_retry(&self, _: &Candidate, _: Execution) -> Outcome {
            self.retries.fetch_add(1, Ordering::SeqCst);
            Outcome::operational(Status::Rejected, "should not execute cancelled retry")
        }
    }
    let b = Arc::new(CancelBackend {
        failed: Semaphore::new(0),
        held: Semaphore::new(0),
        release: Semaphore::new(0),
        retries: AtomicUsize::new(0),
    });
    let e = engine(b.clone(), 1);
    let stream = e
        .verify_stream(Batch {
            mode: Mode::All,
            candidates: vec![candidate("retry", "retry", "one")],
        })
        .unwrap();
    let worker = e.clone();
    let held = tokio::spawn(async move {
        worker
            .verify_batch(Batch {
                mode: Mode::All,
                candidates: vec![candidate("held", "held", "two")],
            })
            .await
            .unwrap()
    });
    let permit = tokio::time::timeout(Duration::from_secs(2), b.failed.acquire())
        .await
        .unwrap()
        .unwrap();
    permit.forget();
    tokio::time::timeout(Duration::from_secs(2), e.shutdown())
        .await
        .unwrap();
    drop(stream);
    let _ = tokio::time::timeout(Duration::from_secs(2), held)
        .await
        .unwrap()
        .unwrap();
    assert_eq!(b.retries.load(Ordering::SeqCst), 0);
}
