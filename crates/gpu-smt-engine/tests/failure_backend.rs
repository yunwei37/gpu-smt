//! Actual Engine pipeline with a simulated tactic backend; no native replay claim.
use async_trait::async_trait;
use gpu_smt_core::*;
use gpu_smt_engine::*;
use serde_json::json;
use std::{
    cell::Cell,
    sync::{
        Arc,
        atomic::{AtomicUsize, Ordering},
    },
};
use tokio_util::sync::CancellationToken;

struct State {
    goal: Cell<u64>,
    remaining: u64,
}
struct Record(Arc<AtomicUsize>);
impl Drop for Record {
    fn drop(&mut self) {
        self.0.fetch_sub(1, Ordering::SeqCst);
    }
}
#[derive(Default)]
struct Backend {
    normal: AtomicUsize,
    hooks: AtomicUsize,
    fresh: AtomicUsize,
    checks: AtomicUsize,
    retries: AtomicUsize,
    interrupts: AtomicUsize,
    shutdowns: AtomicUsize,
    live: Arc<AtomicUsize>,
}
#[async_trait]
impl FailureReplayBackend for Backend {
    type Key = u64;
    type Record = Record;
    type State = State;
    type Exception = &'static str;
    fn replay_input(&self, s: &State) -> Option<(String, u64)> {
        (s.goal.get() == 7).then(|| ("fixture-generation-1".into(), s.goal.get()))
    }
    async fn replay_failure(
        &self,
        s: &mut State,
        scope: &str,
        key: &u64,
        _: &Record,
        cancel: &CancellationToken,
    ) -> Result<Option<&'static str>, String> {
        if cancel.is_cancelled()
            || s.remaining < 9
            || self.replay_input(s) != Some((scope.into(), *key))
        {
            return Ok(None);
        }
        s.goal.set(8);
        s.remaining -= 9;
        Ok(Some("ordinary exception"))
    }
}
impl Backend {
    async fn run(
        &self,
        c: &Candidate,
        x: Execution,
        cache: Option<&BackendFailureCache<Self>>,
    ) -> Outcome {
        let mut s = State {
            goal: Cell::new(7),
            remaining: 100,
        };
        if let Some(status) = match c.code.as_str() {
            "timeout" => Some(Status::Timeout),
            "memory" => Some(Status::ResourceExhausted),
            "fault" => Some(Status::BackendError),
            "cancel" => Some(Status::Cancelled),
            _ => None,
        } {
            if let Some(cache) = cache {
                let input = cache.capture(self, &s).unwrap();
                assert!(!cache.remember(input, TacticCompletion::NotReplayable));
            }
            return Outcome::operational(status, "simulated operational exit");
        }
        let replay = if let Some(cache) = cache {
            cache.try_replay(self, &mut s, &x.cancel).await.unwrap()
        } else {
            None
        };
        let exception = if let Some(exception) = replay {
            exception
        } else {
            let input = cache.and_then(|cache| cache.capture(self, &s));
            self.fresh.fetch_add(1, Ordering::SeqCst);
            s.goal.set(8);
            s.remaining -= 9;
            if let (Some(cache), Some(input)) = (cache, input) {
                self.live.fetch_add(1, Ordering::SeqCst);
                assert!(cache.remember(
                    input,
                    TacticCompletion::OrdinaryFailure(Record(self.live.clone()))
                ));
            }
            "ordinary exception"
        };
        // Simulate the original failure/backtracking handler and final check.
        // The same tactic exception may precede accepted OR rejected whole sources.
        assert_eq!(exception, "ordinary exception");
        assert_eq!((s.goal.get(), s.remaining), (8, 91));
        self.checks.fetch_add(1, Ordering::SeqCst);
        Outcome {
            status: if c.code.contains("reject") {
                Status::Rejected
            } else {
                Status::Accepted
            },
            response: Some(json!({"fixture":true})),
            error: None,
        }
    }
}
#[async_trait]
impl VerificationBackend for Backend {
    fn identity(&self) -> String {
        "simulated-native-v1".into()
    }
    fn prepared_state_ready(&self) -> bool {
        true
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        self.normal.fetch_add(1, Ordering::SeqCst);
        self.run(c, x, None).await
    }
    async fn verify_resource_retry(&self, c: &Candidate, x: Execution) -> Outcome {
        assert_eq!(
            self.live.load(Ordering::SeqCst),
            0,
            "release records before native reclaim"
        );
        self.retries.fetch_add(1, Ordering::SeqCst);
        self.run(c, x, None).await
    }
    fn request_resource_preemption(&self, p: &[ProcessIdentity]) {
        self.interrupts.fetch_add(p.len(), Ordering::SeqCst);
    }
    async fn shutdown(&self) {
        assert_eq!(
            self.live.load(Ordering::SeqCst),
            0,
            "release records before native shutdown"
        );
        self.shutdowns.fetch_add(1, Ordering::SeqCst);
    }
}
#[async_trait]
impl FailureCacheVerificationBackend for Backend {
    async fn verify_with_failure_cache(
        &self,
        c: &Candidate,
        x: Execution,
        cache: &BackendFailureCache<Self>,
    ) -> Outcome {
        self.hooks.fetch_add(1, Ordering::SeqCst);
        self.run(c, x, Some(cache)).await
    }
}
struct Monitor;
impl ResourceMonitor for Monitor {
    fn sample(&self, _: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        Ok(ResourceSnapshot {
            rss_bytes: 1,
            processes: vec![],
        })
    }
}
struct Policy;
impl SchedulingPolicy for Policy {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn predicted_rss(&self, c: &Candidate) -> Option<u64> {
        Some(if c.code == "retry" { 101 } else { 1 })
    }
}
fn engine(b: Arc<dyn VerificationBackend>, cache: Arc<dyn ResultCache>) -> Engine {
    Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0],
            cores_per_worker: 1,
        },
        b,
        Arc::new(Policy),
        Arc::new(Monitor),
        Arc::new(HeadroomAdmission),
        cache,
    )
    .unwrap()
}
async fn verify(e: &Engine, code: &str, reuse: bool) -> Outcome {
    let rows = e
        .verify_batch(Batch {
            mode: Mode::All,
            candidates: vec![Candidate {
                id: code.into(),
                code: code.into(),
                task_id: None,
                timeout_ms: 30000,
                reuse,
            }],
        })
        .await
        .unwrap();
    assert_eq!(rows.len(), 1);
    rows[0].outcome.clone()
}
fn count(n: &AtomicUsize) -> usize {
    n.load(Ordering::SeqCst)
}

#[tokio::test]
async fn default_off_delegates_without_tactic_storage_or_hook() {
    let b = Arc::new(Backend::default());
    let adapter = Arc::new(FailureCacheAdapter::new(b.clone()));
    assert_eq!(adapter.identity(), b.identity());
    assert!(adapter.prepared_state_ready());
    let e = engine(adapter, Arc::new(MemoryCache::default()));
    for source in ["first", "second"] {
        assert_eq!(verify(&e, source, false).await.status, Status::Accepted);
    }
    e.shutdown().await;
    assert_eq!(
        (
            count(&b.normal),
            count(&b.hooks),
            count(&b.fresh),
            count(&b.checks)
        ),
        (2, 0, 2, 2)
    );
    assert_eq!((count(&b.live), count(&b.shutdowns)), (0, 1));
}

type DynamicBackend = dyn FailureCacheVerificationBackend<
        Key = u64,
        Record = Record,
        State = State,
        Exception = &'static str,
    >;
#[tokio::test]
async fn enabled_engine_reuses_only_tactic_failure_and_checks_each_source() {
    let b = Arc::new(Backend::default());
    let dynamic: Arc<DynamicBackend> = b.clone();
    let adapter = Arc::new(FailureCacheAdapter::enabled(dynamic));
    assert_ne!(adapter.identity(), b.identity());
    let e = engine(adapter, Arc::new(MemoryCache::default()));
    for (source, status) in [
        ("first", Status::Accepted),
        ("second", Status::Accepted),
        ("reject", Status::Rejected),
    ] {
        assert_eq!(verify(&e, source, false).await.status, status);
    }
    assert_eq!(
        (
            count(&b.normal),
            count(&b.hooks),
            count(&b.fresh),
            count(&b.checks)
        ),
        (0, 3, 1, 3)
    );
    assert_eq!(count(&b.live), 1);
    e.shutdown().await;
    assert_eq!((count(&b.live), count(&b.shutdowns)), (0, 1));
}

#[tokio::test]
async fn operational_completion_is_not_replayed_as_ordinary_failure() {
    for (code, status) in [
        ("timeout", Status::Timeout),
        ("memory", Status::ResourceExhausted),
        ("fault", Status::BackendError),
        ("cancel", Status::Cancelled),
    ] {
        let b = Arc::new(Backend::default());
        let e = engine(
            Arc::new(FailureCacheAdapter::enabled(b.clone())),
            Arc::new(MemoryCache::default()),
        );
        assert_eq!(verify(&e, "producer", false).await.status, Status::Accepted);
        assert_eq!(verify(&e, code, false).await.status, status);
        assert_eq!(count(&b.live), 0);
        assert_eq!(verify(&e, "after", false).await.status, Status::Accepted);
        assert_eq!(count(&b.fresh), 2);
        e.shutdown().await;
    }
}

#[tokio::test]
async fn exclusive_resource_path_clears_records_and_delegates_original_retry() {
    let b = Arc::new(Backend::default());
    let adapter = Arc::new(FailureCacheAdapter::enabled(b.clone()));
    let e = engine(adapter.clone(), Arc::new(MemoryCache::default()));
    verify(&e, "producer", false).await;
    assert_eq!(count(&b.live), 1);
    assert_eq!(verify(&e, "retry", false).await.status, Status::Accepted);
    assert_eq!(
        (count(&b.retries), count(&b.hooks), count(&b.live)),
        (1, 1, 0)
    );
    adapter.request_resource_preemption(&[ProcessIdentity {
        pid: 123,
        start_ticks: 456,
    }]);
    assert_eq!(count(&b.interrupts), 1);
    e.shutdown().await;
}

#[tokio::test]
async fn opt_in_identity_separates_shared_whole_source_cache() {
    let b = Arc::new(Backend::default());
    let cache = Arc::new(MemoryCache::default());
    let off = engine(Arc::new(FailureCacheAdapter::new(b.clone())), cache.clone());
    assert_eq!(
        verify(&off, "same-source", true).await.status,
        Status::Accepted
    );
    off.shutdown().await;
    let on = engine(Arc::new(FailureCacheAdapter::enabled(b.clone())), cache);
    assert_eq!(
        verify(&on, "same-source", true).await.status,
        Status::Accepted
    );
    assert_eq!((count(&b.normal), count(&b.hooks)), (1, 1));
    on.shutdown().await;
}
