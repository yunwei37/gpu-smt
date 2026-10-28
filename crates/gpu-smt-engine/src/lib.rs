//! Joint resource admission, exact-result sharing and explicit consumer semantics.
//! The watchdog samples once per second; it is not a kernel memory quota.
#![warn(missing_docs)]
pub mod linux;

use gpu_smt_core::*;
use std::{
    cmp::Reverse,
    collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, HashSet, VecDeque},
    sync::{
        Arc, Mutex, Weak,
        atomic::{AtomicBool, AtomicU64, Ordering},
    },
    time::Instant,
};
use tokio::{
    sync::{Notify, mpsc, watch},
    task::JoinSet,
};
use tokio_util::sync::CancellationToken;

/// Default stable submission order; resource retries follow queued first attempts.
pub struct Fifo;
impl SchedulingPolicy for Fifo {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
}

/// Experimental source-size ordering; not a failure detector.
pub struct SourceSize;
impl SchedulingPolicy for SourceSize {
    fn priority(&self, c: &Candidate) -> u64 {
        c.code.len() as u64
    }
}

/// Interleave ranked candidates across tasks for first-success consumers.
/// This is ordinary scheduling, not a failure detector or a novelty claim.
/// All-mode delegates the wrapped policy unchanged; no RL rewards are skipped.
pub struct TaskInterleave<P> {
    inner: P,
}
impl<P> TaskInterleave<P> {
    /// Compose task awareness with an existing source-ranking/memory policy.
    pub fn new(inner: P) -> Self {
        Self { inner }
    }
}
impl<P: SchedulingPolicy> SchedulingPolicy for TaskInterleave<P> {
    fn priority(&self, c: &Candidate) -> u64 {
        self.inner.priority(c)
    }
    fn predicted_rss(&self, c: &Candidate) -> Option<u64> {
        self.inner.predicted_rss(c)
    }
    fn refresh_rss(&self, c: &Candidate, context: &str, initial: Option<u64>) -> Option<u64> {
        self.inner.refresh_rss(c, context, initial)
    }
    fn observe_rss(&self, c: &Candidate, context: &str, bytes: u64) {
        self.inner.observe_rss(c, context, bytes);
    }
    fn batch_priorities(&self, candidates: &[Candidate], mode: Mode) -> Vec<u64> {
        let base = self.inner.batch_priorities(candidates, mode);
        if mode != Mode::FirstSuccess || base.len() != candidates.len() {
            return base;
        }
        let mut ranked: Vec<_> = (0..candidates.len()).collect();
        ranked.sort_by_key(|i| (base[*i], *i));
        let mut groups: Vec<Vec<usize>> = vec![];
        let mut by_task = HashMap::<&str, usize>::new();
        for index in ranked {
            let task = candidates[index].task_id.as_deref();
            let group = if let Some(task) = task {
                *by_task.entry(task).or_insert_with(|| {
                    groups.push(vec![]);
                    groups.len() - 1
                })
            } else {
                // Missing task IDs are rejected by Engine for first-success,
                // but direct trait callers still get independent ungrouped rows.
                groups.push(vec![]);
                groups.len() - 1
            };
            groups[group].push(index);
        }
        let mut frontiers: VecDeque<_> = groups.into_iter().map(Vec::into_iter).collect();
        let mut priorities = vec![0; candidates.len()];
        let mut next = 0;
        while let Some(mut group) = frontiers.pop_front() {
            if let Some(index) = group.next() {
                priorities[index] = next;
                next += 1;
            }
            if !group.as_slice().is_empty() {
                frontiers.push_back(group);
            }
        }
        priorities
    }
}

/// Opt-in memory forecasts learned only from measured same-task attempts.
///
/// Wraps ranking unchanged. History is scoped by backend/resources, task ID
/// and timeout; no proof result, prefix or certificate is reused. Observed
/// maxima are lower bounds, not memory caps or guarantees. A large sibling can
/// overreserve/serialize smaller ones. Keep the normal watchdog and exclusive
/// retry path, qualify native benefit separately, and use a fresh wrapper per
/// engine/workload lifetime or explicitly clear its retained observations.
///
/// Compose opt-in measured feedback without changing the wrapped ordering:
///
/// ```
/// use gpu_smt_engine::{Fifo, TaskInterleave, TaskMemory};
/// let policy = TaskInterleave::new(TaskMemory::new(Fifo));
/// // Pass Arc::new(policy) as the scheduling policy to Engine::new.
/// ```
pub struct TaskMemory<P> {
    inner: P,
    peaks: Mutex<HashMap<(String, String, u64), u64>>,
}
impl<P> TaskMemory<P> {
    /// Compose measured-sibling memory with an existing ranking/forecast policy.
    pub fn new(inner: P) -> Self {
        Self {
            inner,
            peaks: Mutex::new(HashMap::new()),
        }
    }
    /// Clear only observations held by this wrapper; no job or verdict changes.
    pub fn clear_memory(&self) {
        self.peaks.lock().unwrap().clear();
    }
    fn key(c: &Candidate, context: &str) -> Option<(String, String, u64)> {
        c.task_id
            .as_ref()
            .filter(|task| !task.is_empty())
            .map(|task| (context.into(), task.clone(), c.timeout_ms))
    }
}
impl<P: SchedulingPolicy> SchedulingPolicy for TaskMemory<P> {
    fn priority(&self, c: &Candidate) -> u64 {
        self.inner.priority(c)
    }
    fn batch_priorities(&self, candidates: &[Candidate], mode: Mode) -> Vec<u64> {
        self.inner.batch_priorities(candidates, mode)
    }
    fn predicted_rss(&self, c: &Candidate) -> Option<u64> {
        self.inner.predicted_rss(c)
    }
    fn refresh_rss(&self, c: &Candidate, context: &str, initial: Option<u64>) -> Option<u64> {
        let initial = self.inner.refresh_rss(c, context, initial);
        let observed =
            Self::key(c, context).and_then(|key| self.peaks.lock().unwrap().get(&key).copied());
        initial.max(observed)
    }
    fn observe_rss(&self, c: &Candidate, context: &str, bytes: u64) {
        self.inner.observe_rss(c, context, bytes);
        if bytes > 0
            && let Some(key) = Self::key(c, context)
        {
            let mut peaks = self.peaks.lock().unwrap();
            let peak = peaks.entry(key).or_insert(0);
            *peak = (*peak).max(bytes);
        }
    }
}

/// Project actual RSS plus unconsumed reservations.
pub struct HeadroomAdmission;
impl AdmissionPolicy for HeadroomAdmission {
    fn admit(&self, s: &ResourceSnapshot, b: u64, growth: u64) -> bool {
        s.rss_bytes.checked_add(growth).is_some_and(|v| v <= b)
    }
}

/// Exact in-memory native-decision cache, scoped to engine lifetime.
#[derive(Default)]
pub struct MemoryCache(Mutex<HashMap<CacheKey, Outcome>>);
impl ResultCache for MemoryCache {
    fn get(&self, k: &CacheKey) -> Option<Outcome> {
        self.0.lock().unwrap().get(k).cloned()
    }
    fn insert(&self, k: CacheKey, o: Outcome) {
        if o.cacheable() {
            self.0.lock().unwrap().insert(k, o);
        }
    }
}

/// Explicit hardware/resource contract, with no per-process address-space limit.
#[derive(Clone, Debug, serde::Deserialize, serde::Serialize)]
#[serde(deny_unknown_fields)]
pub struct Config {
    /// Total actual owned RSS budget.
    pub memory_bytes: u64,
    /// Discovered or caller-selected CPU eligibility.
    pub cpus: Vec<usize>,
    /// Measured active CPU demand, rounded up per worker.
    pub cores_per_worker: usize,
}
impl Config {
    /// Validate actual CPU assignments and aggregate budget.
    pub fn validate(&self) -> Result<(), String> {
        if self.memory_bytes == 0
            || self.cores_per_worker == 0
            || self.cpus.len() < self.cores_per_worker
        {
            return Err("nonzero memory and enough CPU cores required".into());
        }
        if self.cpus.iter().collect::<HashSet<_>>().len() != self.cpus.len() {
            return Err("duplicate CPUs".into());
        }
        Ok(())
    }
}
struct Registry {
    origin: String,
    execution_id: u64,
    events: Mutex<Vec<BackendEvent>>,
    roots: Mutex<Vec<ProcessIdentity>>,
    seen: Mutex<Vec<ProcessIdentity>>,
    preemption_rss: AtomicU64,
    cancel: CancellationToken,
    preempted: AtomicBool,
    peak: AtomicU64,
}
impl Registry {
    fn new(origin: String, execution_id: u64) -> Self {
        Self {
            origin,
            execution_id,
            events: Mutex::new(vec![]),
            roots: Mutex::new(vec![]),
            seen: Mutex::new(vec![]),
            preemption_rss: AtomicU64::new(0),
            cancel: CancellationToken::new(),
            preempted: AtomicBool::new(false),
            peak: AtomicU64::new(0),
        }
    }
}
impl ProcessRegistry for Registry {
    fn note(&self, event: BackendEvent) {
        tracing::info!(target:"gpu_smt_engine::resources",origin_id=%self.origin,
            execution_id=self.execution_id,stage=%event.stage,detail=%event.detail,
            "backend lifecycle event");
        self.events.lock().unwrap().push(event);
    }
    fn register(&self, p: ProcessIdentity) {
        tracing::info!(target:"gpu_smt_engine::resources",origin_id=%self.origin,
            execution_id=self.execution_id,pid=p.pid,start_ticks=p.start_ticks,"register active process");
        self.seen.lock().unwrap().push(p.clone());
        let mut roots = self.roots.lock().unwrap();
        if !roots.contains(&p) {
            roots.push(p);
        }
    }
    fn observe_rss(&self, bytes: u64) {
        self.peak.fetch_max(bytes, Ordering::Relaxed);
    }
    fn unregister(&self, p: &ProcessIdentity) {
        tracing::info!(target:"gpu_smt_engine::resources",origin_id=%self.origin,
            execution_id=self.execution_id,pid=p.pid,start_ticks=p.start_ticks,"release active process ownership");
        self.roots.lock().unwrap().retain(|x| x != p);
    }
}
struct Active {
    registry: Arc<Registry>,
    cpus: Vec<usize>,
    estimate: Option<u64>,
    exclusive: bool,
}
struct State {
    free: BTreeSet<usize>,
    active: HashMap<u64, Active>,
    queued: BTreeMap<(u64, bool, u64, u64), Arc<Notify>>,
    queue_epoch: u64,
}
impl State {
    fn notify_queue_head(&self) {
        if let Some((_, ready)) = self.queued.first_key_value() {
            ready.notify_one();
        }
    }
    fn notify_all_queued(&self) {
        for ready in self.queued.values() {
            ready.notify_one();
        }
    }
}
#[derive(Clone)]
struct WorkResult {
    outcome: Outcome,
    attempts: Vec<Attempt>,
}
type Sender = watch::Sender<Option<Arc<WorkResult>>>;
struct Completion {
    done: AtomicBool,
    notify: Notify,
}
struct Flight {
    tx: Sender,
    completion: Arc<Completion>,
}
enum Subscription {
    Cached(Outcome),
    Flight {
        coalesced: bool,
        rx: watch::Receiver<Option<Arc<WorkResult>>>,
        sender: Sender,
        completion: Arc<Completion>,
    },
}

// Exact upper median, matching the former sorted[len / 2] fallback.
// Keep querying admission independent of the lifetime's observation count.
#[derive(Default)]
struct ObservedPeaks {
    lower: BinaryHeap<u64>,
    upper: BinaryHeap<Reverse<u64>>,
}
impl ObservedPeaks {
    fn push(&mut self, bytes: u64) {
        if self.upper.peek().is_none_or(|peak| bytes >= peak.0) {
            self.upper.push(Reverse(bytes));
        } else {
            self.lower.push(bytes);
        }
        if self.upper.len() > self.lower.len() + 1 {
            self.lower.push(self.upper.pop().unwrap().0);
        } else if self.lower.len() > self.upper.len() {
            self.upper.push(Reverse(self.lower.pop().unwrap()));
        }
    }
    fn median(&self) -> Option<u64> {
        self.upper.peek().map(|peak| peak.0)
    }
}

struct Inner {
    config: Config,
    backend: Arc<dyn VerificationBackend>,
    policy: Arc<dyn SchedulingPolicy>,
    admission: Arc<dyn AdmissionPolicy>,
    monitor: Arc<dyn ResourceMonitor>,
    cache: Arc<dyn ResultCache>,
    state: Mutex<State>,
    inflight: Mutex<HashMap<CacheKey, Flight>>,
    observed_peaks: Mutex<ObservedPeaks>,
    next: AtomicU64,
    notify: Notify,
    fatal: Mutex<Option<String>>,
}
struct Lease {
    inner: Arc<Inner>,
    id: u64,
    reclaim_idle: bool,
}
impl Drop for Lease {
    fn drop(&mut self) {
        let mut s = self.inner.state.lock().unwrap();
        if let Some(a) = s.active.remove(&self.id) {
            s.free.extend(a.cpus);
        }
        s.notify_queue_head();
        drop(s);
        self.inner.notify.notify_waiters();
    }
}
type RankedBatch = Vec<(Queued, usize, Candidate)>;

/// Completion-order batch subscription. Drop cancels only this subscription;
/// physical retirement remains owned/accounted by the shared engine.
pub struct BatchStream {
    receiver: mpsc::UnboundedReceiver<BatchEvent>,
}
impl BatchStream {
    /// Receive the next event; require Complete before treating EOF as success.
    pub async fn recv(&mut self) -> Option<BatchEvent> {
        self.receiver.recv().await
    }
    /// Poll an event when adapting to an HTTP body or another stream interface.
    pub fn poll_recv(
        &mut self,
        cx: &mut std::task::Context<'_>,
    ) -> std::task::Poll<Option<BatchEvent>> {
        self.receiver.poll_recv(cx)
    }
}

struct Queued {
    inner: Arc<Inner>,
    ticket: (u64, bool, u64, u64),
    ready: Arc<Notify>,
}
impl Drop for Queued {
    fn drop(&mut self) {
        let mut state = self.inner.state.lock().unwrap();
        state.queued.remove(&self.ticket);
        state.notify_queue_head();
    }
}
impl Inner {
    fn snapshot(&self) -> Result<ResourceSnapshot, String> {
        let roots: Vec<_> = self
            .state
            .lock()
            .unwrap()
            .active
            .values()
            .flat_map(|a| a.registry.roots.lock().unwrap().clone())
            .collect();
        self.monitor.sample(&roots)
    }
    fn watchdog(&self) {
        let sample = match self.snapshot() {
            Ok(s) => s,
            Err(e) => {
                *self.fatal.lock().unwrap() = Some(e);
                let state = self.state.lock().unwrap();
                for a in state.active.values() {
                    a.registry.cancel.cancel();
                }
                state.notify_all_queued();
                drop(state);
                self.notify.notify_waiters();
                return;
            }
        };
        tracing::info!(target:"gpu_smt_engine::resources",
            rss_bytes=sample.rss_bytes,budget_bytes=self.config.memory_bytes,
            processes=%serde_json::to_string(&sample.processes).expect("resource samples serialize"),
            "owned RSS sample");
        let s = self.state.lock().unwrap();
        let mut largest = None;
        for a in s.active.values() {
            let roots = a.registry.roots.lock().unwrap();
            let rss: u64 = sample
                .processes
                .iter()
                .filter(|p| roots.contains(&p.identity))
                .map(|p| p.rss_bytes)
                .sum();
            a.registry.peak.fetch_max(rss, Ordering::Relaxed);
            if !a.registry.preempted.load(Ordering::Acquire)
                && largest.as_ref().is_none_or(|(n, _)| rss > *n)
            {
                largest = Some((rss, a.registry.clone()));
            }
        }
        if sample.rss_bytes > self.config.memory_bytes {
            if let Some((_, registry)) = largest {
                tracing::warn!(target:"gpu_smt_engine::resources",rss_bytes=sample.rss_bytes,
                    origin_id=%registry.origin,execution_id=registry.execution_id,
                    budget_bytes=self.config.memory_bytes,
                    processes=%serde_json::to_string(&*registry.roots.lock().unwrap()).expect("process identities serialize"),
                    "preempt owned attempt and requeue exclusively");
                registry
                    .preemption_rss
                    .store(sample.rss_bytes, Ordering::Release);
                registry.preempted.store(true, Ordering::Release);
                registry.cancel.cancel();
            } else if s.active.is_empty() {
                *self.fatal.lock().unwrap() =
                    Some("engine RSS alone exceeds aggregate budget".into());
            }
        }
        if self.fatal.lock().unwrap().is_some() {
            s.notify_all_queued();
        } else {
            s.notify_queue_head();
        }
        drop(s);
        self.notify.notify_waiters();
    }
    fn enqueue(self: &Arc<Self>, priority: u64, retry: bool) -> Queued {
        // Finite batches drain ordinary work before paying full-budget retries.
        // Keep resource attempts exclusive; a preempted peak is no safe cap.
        let mut state = self.state.lock().unwrap();
        let ticket = (
            state.queue_epoch,
            retry,
            priority,
            self.next.fetch_add(1, Ordering::Relaxed),
        );
        if retry {
            // Freeze the ordinary frontier. Later batches cannot starve this retry.
            state.queue_epoch = self.next.fetch_add(1, Ordering::Relaxed);
        }
        let ready = Arc::new(Notify::new());
        state.queued.insert(ticket, ready.clone());
        drop(state);
        Queued {
            inner: self.clone(),
            ticket,
            ready,
        }
    }
    async fn acquire(
        self: &Arc<Self>,
        estimate: Option<u64>,
        candidate: &Candidate,
        context: &str,
        solo: bool,
        queued: Queued,
    ) -> Result<(Lease, Arc<Registry>, Vec<usize>, bool), String> {
        let origin = &candidate.id;
        let ticket = queued.ticket;
        let _queued = queued;
        loop {
            let notified = _queued.ready.notified();
            if let Some(e) = self.fatal.lock().unwrap().clone() {
                return Err(e);
            }
            // Only an eligible queue head samples /proc. A watchdog tick must
            // not cause every queued candidate to scan the process table.
            let head_ready = {
                let s = self.state.lock().unwrap();
                s.queued
                    .first_key_value()
                    .is_some_and(|(key, _)| *key == ticket)
                    && s.free.len() >= self.config.cores_per_worker
            };
            if !head_ready {
                notified.await;
                continue;
            }
            // Refresh after becoming eligible, not once at batch submission.
            // Policy callbacks run without holding the engine state lock.
            let estimate = self.policy.refresh_rss(candidate, context, estimate);
            let sample = self.snapshot()?;
            {
                let mut s = self.state.lock().unwrap();
                // Sampling may overlap shutdown or a fatal watchdog result.
                // Recheck while holding the lease-insertion lock: shutdown
                // either sees/cancels this lease or prevents its creation.
                if let Some(error) = self.fatal.lock().unwrap().clone() {
                    return Err(error);
                }
                // Waiting jobs must refresh learned costs; freezing an unknown
                // forecast here serializes the entire first submitted batch.
                let estimate = estimate
                    .or_else(|| self.observed_peaks.lock().unwrap().median())
                    .or_else(|| {
                        s.active
                            .values()
                            .map(|a| a.registry.peak.load(Ordering::Relaxed))
                            .filter(|n| *n > 0)
                            .max()
                    });
                // An idle prepared parent/engine also consumes headroom. A
                // forecast below the total budget must not wait forever when
                // no active attempt can retire to make that reservation fit.
                let forecast_exclusive = estimate.is_some_and(|n| {
                    n >= self.config.memory_bytes
                        || (s.active.is_empty()
                            && sample
                                .rss_bytes
                                .checked_add(n)
                                .is_none_or(|sum| sum > self.config.memory_bytes))
                });
                let actual_exclusive = solo
                    || self.config.cores_per_worker == self.config.cpus.len()
                    || forecast_exclusive;
                let unknown = estimate.is_none() && !s.active.is_empty();
                let exclusive_block = s.active.values().any(|a| a.exclusive)
                    || (actual_exclusive && !s.active.is_empty());
                let reserve: u64 = s
                    .active
                    .values()
                    .map(|a| {
                        let roots = a.registry.roots.lock().unwrap();
                        let rss: u64 = sample
                            .processes
                            .iter()
                            .filter(|p| roots.contains(&p.identity))
                            .map(|p| p.rss_bytes)
                            .sum();
                        a.estimate.unwrap_or(0).saturating_sub(rss)
                    })
                    .sum::<u64>()
                    .saturating_add(estimate.unwrap_or(0));
                // Oversized forecasts get an actual exclusive attempt, never predicted rejection.
                let reserve = if actual_exclusive && s.active.is_empty() {
                    0
                } else {
                    reserve
                };
                let queue_turn = s
                    .queued
                    .first_key_value()
                    .is_some_and(|(key, _)| *key == ticket);
                if queue_turn
                    && !unknown
                    && !exclusive_block
                    && s.free.len() >= self.config.cores_per_worker
                    && self
                        .admission
                        .admit(&sample, self.config.memory_bytes, reserve)
                {
                    let cpus: Vec<_> = s
                        .free
                        .iter()
                        .take(self.config.cores_per_worker)
                        .copied()
                        .collect();
                    for cpu in &cpus {
                        s.free.remove(cpu);
                    }
                    let id = self.next.fetch_add(1, Ordering::Relaxed);
                    let registry = Arc::new(Registry::new(origin.to_owned(), id));
                    if forecast_exclusive && !solo {
                        registry.note(BackendEvent {
                            stage: "exclusive_headroom".into(),
                            detail: serde_json::json!({
                                "forecast_bytes": estimate,
                                "actual_idle_rss_bytes": sample.rss_bytes,
                                "budget_bytes": self.config.memory_bytes,
                                "prior_attempt_required": false
                            })
                            .to_string(),
                        });
                    }
                    s.active.insert(
                        id,
                        Active {
                            registry: registry.clone(),
                            cpus: cpus.clone(),
                            estimate,
                            exclusive: actual_exclusive,
                        },
                    );
                    return Ok((
                        Lease {
                            inner: self.clone(),
                            id,
                            reclaim_idle: solo || forecast_exclusive,
                        },
                        registry,
                        cpus,
                        actual_exclusive,
                    ));
                }
            }
            notified.await;
        }
    }
    async fn run(
        self: Arc<Self>,
        c: Candidate,
        key: CacheKey,
        tx: Sender,
        completion: Arc<Completion>,
        queued: Queued,
    ) {
        let memory_context = serde_json::json!([self.backend.identity(), &self.config]).to_string();
        let mut queued = Some(queued);
        let mut attempts = vec![];
        let mut solo = false;
        let result = loop {
            if tx.is_closed() {
                break Outcome::operational(Status::Cancelled, "no live subscribers");
            }
            // Only a policy-supplied forecast belongs to this request.
            // The learned global fallback is refreshed inside acquire after
            // reaching the queue head; caching it here strands warm queued
            // requests on an obsolete median even as newer observations fall.
            let predicted = self.policy.predicted_rss(&c);
            let exclusive = solo || predicted.is_some_and(|n| n >= self.config.memory_bytes);
            let queued = queued
                .take()
                .unwrap_or_else(|| self.enqueue(self.policy.priority(&c), solo));
            let acquired = tokio::select! {
                r=self.acquire(predicted,&c,&memory_context,exclusive,queued)=>r,
                _=tx.closed()=>break Outcome::operational(Status::Cancelled,"no live subscribers"),
            };
            let (lease, registry, cpus, exclusive) = match acquired {
                Ok(v) => v,
                Err(e) => break Outcome::operational(Status::BackendError, e),
            };
            let start = Instant::now();
            let execution = Execution {
                cancel: registry.cancel.clone(),
                cpus,
                registry: registry.clone(),
            };
            let future = if lease.reclaim_idle {
                self.backend.verify_resource_retry(&c, execution)
            } else {
                self.backend.verify(&c, execution)
            };
            tokio::pin!(future);
            let mut outcome = tokio::select! {
                o=&mut future=>o,
                _=tx.closed()=>{
                    registry.cancel.cancel();
                    let _=future.await;
                    Outcome::operational(Status::Cancelled,"no live subscribers")
                }
            };
            if let Some(e) = self.fatal.lock().unwrap().clone() {
                outcome = Outcome::operational(Status::BackendError, e);
            }
            if registry.preempted.load(Ordering::Acquire) {
                outcome = Outcome::operational(
                    if exclusive {
                        Status::ResourceExhausted
                    } else {
                        Status::Preempted
                    },
                    "aggregate RSS watchdog preemption",
                );
            }
            let peak = registry.peak.load(Ordering::Relaxed);
            if peak > 0 {
                self.observed_peaks.lock().unwrap().push(peak);
                self.policy.observe_rss(&c, &memory_context, peak);
            }
            attempts.push(Attempt {
                status: outcome.status.clone(),
                elapsed_seconds: start.elapsed().as_secs_f64(),
                peak_rss_bytes: peak,
                exclusive,
                processes: registry.seen.lock().unwrap().clone(),
                backend_events: registry.events.lock().unwrap().clone(),
                preemption_rss_bytes: registry
                    .preempted
                    .load(Ordering::Acquire)
                    .then(|| registry.preemption_rss.load(Ordering::Acquire)),
            });
            if matches!(
                outcome.status,
                Status::Preempted | Status::ResourceExhausted
            ) && !exclusive
            {
                solo = true;
                continue;
            }
            break outcome;
        };
        if c.reuse && result.cacheable() {
            self.cache.insert(key.clone(), result.clone());
        }
        tx.send_replace(Some(Arc::new(WorkResult {
            outcome: result,
            attempts,
        })));
        self.inflight.lock().unwrap().remove(&key);
        completion.done.store(true, Ordering::Release);
        completion.notify.notify_waiters();
    }
}

/// Cloneable service sharing one global admission/accounting domain across HTTP batches.
#[derive(Clone)]
pub struct Engine(Arc<Inner>);
impl Engine {
    /// Construct inside a Tokio runtime; watchdog lifetime follows the engine.
    pub fn new(
        config: Config,
        backend: Arc<dyn VerificationBackend>,
        policy: Arc<dyn SchedulingPolicy>,
        monitor: Arc<dyn ResourceMonitor>,
        admission: Arc<dyn AdmissionPolicy>,
        cache: Arc<dyn ResultCache>,
    ) -> Result<Self, String> {
        config.validate()?;
        let inner = Arc::new(Inner {
            state: Mutex::new(State {
                free: config.cpus.iter().copied().collect(),
                active: HashMap::new(),
                queued: BTreeMap::new(),
                queue_epoch: 0,
            }),
            config,
            backend,
            policy,
            monitor,
            admission,
            cache,
            inflight: Mutex::new(HashMap::new()),
            observed_peaks: Mutex::new(ObservedPeaks::default()),
            next: AtomicU64::new(1),
            notify: Notify::new(),
            fatal: Mutex::new(None),
        });
        let weak: Weak<Inner> = Arc::downgrade(&inner);
        tokio::spawn(async move {
            let mut tick = tokio::time::interval(std::time::Duration::from_secs(1));
            loop {
                tick.tick().await;
                let Some(inner) = weak.upgrade() else { break };
                inner.watchdog();
            }
        });
        Ok(Self(inner))
    }
    // Establish sharing and cache disposition in submission order, before
    // spawned tasks or forecasts can race for the physical execution ticket.
    fn subscribe(&self, c: &Candidate, queued: Queued) -> Subscription {
        let mut backend = self.0.backend.identity();
        if !c.reuse {
            backend.push_str(&format!(
                "|fresh:{}",
                self.0.next.fetch_add(1, Ordering::Relaxed)
            ));
        }
        let key = CacheKey {
            backend,
            code: c.code.clone(),
            timeout_ms: c.timeout_ms,
        };
        let mut flights = self.0.inflight.lock().unwrap();
        if let Some(o) = c.reuse.then(|| self.0.cache.get(&key)).flatten() {
            return Subscription::Cached(o);
        }
        if let Some(flight) = flights.get(&key) {
            drop(queued);
            Subscription::Flight {
                coalesced: true,
                rx: flight.tx.subscribe(),
                sender: flight.tx.clone(),
                completion: flight.completion.clone(),
            }
        } else {
            let (tx, rx) = watch::channel(None);
            let completion = Arc::new(Completion {
                done: AtomicBool::new(false),
                notify: Notify::new(),
            });
            flights.insert(
                key.clone(),
                Flight {
                    tx: tx.clone(),
                    completion: completion.clone(),
                },
            );
            tokio::spawn(self.0.clone().run(
                c.clone(),
                key,
                tx.clone(),
                completion.clone(),
                queued,
            ));
            Subscription::Flight {
                coalesced: false,
                rx,
                sender: tx,
                completion,
            }
        }
    }
    async fn verify(
        &self,
        c: Candidate,
        cancel: CancellationToken,
        subscription: Subscription,
    ) -> Verification {
        let start = Instant::now();
        let (coalesced, mut rx, sender, completion) = match subscription {
            Subscription::Cached(outcome) => {
                return Verification {
                    id: c.id,
                    outcome,
                    attempts: vec![],
                    elapsed_seconds: start.elapsed().as_secs_f64(),
                    cached: true,
                    coalesced: false,
                };
            }
            Subscription::Flight {
                coalesced,
                rx,
                sender,
                completion,
            } => (coalesced, rx, sender, completion),
        };
        let mut work = loop {
            if let Some(done) = rx.borrow().clone() {
                break done;
            }
            tokio::select! {
                changed=rx.changed()=>if changed.is_err(){break Arc::new(WorkResult{
                    outcome:Outcome::operational(Status::BackendError,"executor stopped"),attempts:vec![]});},
                _=cancel.cancelled()=>break Arc::new(WorkResult{
                    outcome:Outcome::operational(Status::Cancelled,"same-task checked success"),attempts:vec![]}),
            }
        };
        if work.outcome.status == Status::Cancelled {
            drop(rx);
            // A separate completion notification does not keep a native-result
            // subscription alive. Last-subscriber cancellation pays retirement.
            if sender.receiver_count() == 0 {
                loop {
                    let notified = completion.notify.notified();
                    if completion.done.load(Ordering::Acquire) {
                        break;
                    }
                    notified.await;
                }
                if let Some(done) = sender.borrow().clone() {
                    work = Arc::new(WorkResult {
                        outcome: work.outcome.clone(),
                        attempts: done.attempts.clone(),
                    });
                }
            }
        }
        Verification {
            id: c.id,
            outcome: work.outcome.clone(),
            attempts: work.attempts.clone(),
            elapsed_seconds: start.elapsed().as_secs_f64(),
            cached: false,
            coalesced,
        }
    }
    /// Actual backend prepared-state readiness, independent of resource health.
    pub fn prepared_state_ready(&self) -> bool {
        self.0.backend.prepared_state_ready()
    }
    /// Current monitor/admission health; this does not claim a warm native backend.
    pub fn health(&self) -> Result<(), String> {
        if let Some(error) = self.0.fatal.lock().unwrap().clone() {
            return Err(error);
        }
        self.0.snapshot().map(|_| ())
    }
    /// Stop admissions, cancel active attempts and wait for backend retirement.
    pub async fn shutdown(&self) {
        *self.0.fatal.lock().unwrap() = Some("engine shutdown".into());
        {
            let state = self.0.state.lock().unwrap();
            for a in state.active.values() {
                a.registry.cancel.cancel();
            }
            state.notify_all_queued();
        }
        self.0.notify.notify_waiters();
        loop {
            let notified = self.0.notify.notified();
            if self.0.state.lock().unwrap().active.is_empty() {
                break;
            }
            notified.await;
        }
        self.0.backend.shutdown().await;
    }
    /// Return one record per caller in original order; checked winners alone cancel siblings.
    pub async fn verify_batch(&self, batch: Batch) -> Result<Vec<Verification>, String> {
        let submitted = Instant::now();
        let (mode, pending) = self.prepare_batch(batch)?;
        self.run_batch(mode, pending, submitted, None).await
    }

    /// Deliver each retired result in completion order, without waiting for peers.
    ///
    /// Input validation/ranking happens before any work is launched. Dropping
    /// the receiver cancels this consumer only; shared subscribers retain work.
    /// Results buffer at most one event per submitted input, plus a terminal.
    /// A Complete event is required; an interrupted EOF is not batch completion.
    pub fn verify_stream(&self, batch: Batch) -> Result<BatchStream, String> {
        let submitted = Instant::now();
        let (mode, pending) = self.prepare_batch(batch)?;
        let count = pending.len();
        let (output, receiver) = mpsc::unbounded_channel();
        let engine = self.clone();
        tokio::spawn(async move {
            tokio::select! {
                _ = output.closed() => {}
                result = engine.run_batch(mode, pending, submitted, Some(&output)) => {
                    let terminal = match result {
                        Ok(_) => BatchEvent::Complete { count },
                        Err(message) => BatchEvent::Error { message },
                    };
                    let _ = output.send(terminal);
                }
            }
        });
        Ok(BatchStream { receiver })
    }

    fn prepare_batch(&self, batch: Batch) -> Result<(Mode, RankedBatch), String> {
        let mut ids = HashSet::new();
        for c in &batch.candidates {
            if !ids.insert(c.id.clone()) || c.timeout_ms == 0 {
                return Err("unique IDs and nonzero timeout required".into());
            }
            if batch.mode == Mode::FirstSuccess && c.task_id.is_none() {
                return Err("first_success requires task_id".into());
            }
        }
        let priorities = self
            .0
            .policy
            .batch_priorities(&batch.candidates, batch.mode);
        if priorities.len() != batch.candidates.len() {
            return Err("batch policy must return exactly one priority per candidate".into());
        }
        let mut pending: Vec<_> = batch
            .candidates
            .into_iter()
            .zip(priorities)
            .enumerate()
            .map(|(index, (c, priority))| (priority, index, c))
            .collect();
        pending.sort_by_key(|(priority, index, _)| (*priority, *index));
        // Register the complete ranked frontier before any physical executor
        // starts. Cost-model latency and Tokio wake order cannot reorder it.
        let pending: Vec<_> = pending
            .into_iter()
            .map(|(priority, index, c)| (self.0.enqueue(priority, false), index, c))
            .collect();
        Ok((batch.mode, pending))
    }

    async fn run_batch(
        &self,
        mode: Mode,
        pending: RankedBatch,
        submitted: Instant,
        output: Option<&mpsc::UnboundedSender<BatchEvent>>,
    ) -> Result<Vec<Verification>, String> {
        let n = pending.len();
        let mut tasks = JoinSet::new();
        let mut groups: HashMap<String, Vec<CancellationToken>> = HashMap::new();
        for (queued, index, c) in pending {
            let cancel = CancellationToken::new();
            let task = c.task_id.clone();
            if let Some(id) = &task {
                groups.entry(id.clone()).or_default().push(cancel.clone());
            }
            let subscription = self.subscribe(&c, queued);
            let engine = self.clone();
            tasks.spawn(async move { (index, task, engine.verify(c, cancel, subscription).await) });
        }
        let mut results: Vec<Option<Verification>> = if output.is_none() {
            vec![None; n]
        } else {
            vec![]
        };
        while let Some(next) = tasks.join_next().await {
            let (index, task, mut result) = next.map_err(|e| e.to_string())?;
            result.elapsed_seconds = submitted.elapsed().as_secs_f64();
            if mode == Mode::FirstSuccess
                && result.outcome.status == Status::Accepted
                && let Some(task) = task
            {
                for cancel in &groups[&task] {
                    cancel.cancel();
                }
            }
            if let Some(output) = output {
                output
                    .send(BatchEvent::Result {
                        index,
                        verification: result,
                    })
                    .map_err(|_| "batch stream receiver closed".to_string())?;
            } else {
                results[index] = Some(result);
            }
        }
        Ok(results.into_iter().map(Option::unwrap).collect())
    }
}

#[cfg(test)]
mod shutdown_admission_tests {
    use super::*;
    use std::sync::Condvar;
    use tokio::sync::oneshot;

    struct PausedSample {
        entered: Mutex<Option<oneshot::Sender<()>>>,
        resume: Arc<(Mutex<bool>, Condvar)>,
    }
    impl ResourceMonitor for PausedSample {
        fn sample(&self, _: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
            if let Some(entered) = self.entered.lock().unwrap().take() {
                let _ = entered.send(());
                let (ready, changed) = &*self.resume;
                let mut ready = ready.lock().unwrap();
                while !*ready {
                    ready = changed.wait(ready).unwrap();
                }
            }
            Ok(ResourceSnapshot {
                rss_bytes: 0,
                processes: vec![],
            })
        }
    }
    struct CountBackend(AtomicU64);
    #[async_trait::async_trait]
    impl VerificationBackend for CountBackend {
        fn identity(&self) -> String {
            "shutdown-race-fixture".into()
        }
        async fn verify(&self, _: &Candidate, _: Execution) -> Outcome {
            self.0.fetch_add(1, Ordering::SeqCst);
            Outcome {
                status: Status::Accepted,
                response: None,
                error: None,
            }
        }
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn shutdown_during_admission_sample_cannot_start_backend_after_return() {
        let (entered, sampled) = oneshot::channel();
        let resume = Arc::new((Mutex::new(false), Condvar::new()));
        let backend = Arc::new(CountBackend(AtomicU64::new(0)));
        // Construct the private accounting state without a periodic watchdog:
        // only the admission sample can take this deterministic blocking hook.
        let engine = Engine(Arc::new(Inner {
            config: Config {
                memory_bytes: 100,
                cpus: vec![0],
                cores_per_worker: 1,
            },
            backend: backend.clone(),
            policy: Arc::new(Fifo),
            admission: Arc::new(HeadroomAdmission),
            monitor: Arc::new(PausedSample {
                entered: Mutex::new(Some(entered)),
                resume: resume.clone(),
            }),
            cache: Arc::new(MemoryCache::default()),
            state: Mutex::new(State {
                free: [0].into_iter().collect(),
                active: HashMap::new(),
                queued: BTreeMap::new(),
                queue_epoch: 0,
            }),
            inflight: Mutex::new(HashMap::new()),
            observed_peaks: Mutex::new(ObservedPeaks::default()),
            next: AtomicU64::new(1),
            notify: Notify::new(),
            fatal: Mutex::new(None),
        }));
        let running = engine.clone();
        let batch = tokio::spawn(async move {
            running
                .verify_batch(Batch {
                    mode: Mode::All,
                    candidates: vec![Candidate {
                        id: "after-shutdown".into(),
                        code: "fixture".into(),
                        task_id: None,
                        timeout_ms: 300000,
                        reuse: false,
                    }],
                })
                .await
        });
        sampled.await.unwrap();
        // acquire has checked health but has not obtained the active-state lock.
        engine.shutdown().await;
        {
            let (ready, changed) = &*resume;
            *ready.lock().unwrap() = true;
            changed.notify_all();
        }
        let result = tokio::time::timeout(std::time::Duration::from_secs(2), batch)
            .await
            .unwrap()
            .unwrap()
            .unwrap();
        assert_eq!(
            backend.0.load(Ordering::SeqCst),
            0,
            "shutdown returned before a stale admission started new backend work"
        );
        assert_eq!(result[0].outcome.status, Status::BackendError);
        assert!(result[0].attempts.is_empty());
        assert!(engine.0.state.lock().unwrap().active.is_empty());
    }
}

#[cfg(test)]
mod admission_fallback_tests {
    use super::*;
    use async_trait::async_trait;
    use std::sync::atomic::AtomicUsize;
    use std::time::Duration;

    struct UnknownPolicy(Arc<AtomicUsize>);
    impl SchedulingPolicy for UnknownPolicy {
        fn priority(&self, _: &Candidate) -> u64 {
            0
        }
        fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
            self.0.fetch_add(1, Ordering::SeqCst);
            None
        }
    }
    struct EmptyMonitor;
    impl ResourceMonitor for EmptyMonitor {
        fn sample(&self, _: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
            Ok(ResourceSnapshot::default())
        }
    }
    struct Backend {
        predictions: Arc<AtomicUsize>,
        entered_tail: Arc<AtomicUsize>,
        tail_changed: Arc<Notify>,
        release: CancellationToken,
    }
    #[async_trait]
    impl VerificationBackend for Backend {
        fn identity(&self) -> String {
            "warm-global-fallback-regression".into()
        }
        async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
            if c.id == "0" {
                // All five requests must have queued while the old fallback
                // was60. The first two real completions then lower its median.
                while self.predictions.load(Ordering::SeqCst) < 5 {
                    tokio::task::yield_now().await;
                }
            } else if c.id != "1" {
                self.entered_tail.fetch_add(1, Ordering::SeqCst);
                self.tail_changed.notify_waiters();
                tokio::select! {
                    _ = self.release.cancelled() => {},
                    _ = x.cancel.cancelled() => {},
                }
            }
            x.registry.observe_rss(1);
            Outcome {
                status: Status::Accepted,
                response: Some(serde_json::json!({"env":0})),
                error: None,
            }
        }
    }
    #[tokio::test]
    async fn queued_unknown_requests_refresh_a_falling_warm_fallback() {
        let predictions = Arc::new(AtomicUsize::new(0));
        let entered_tail = Arc::new(AtomicUsize::new(0));
        let tail_changed = Arc::new(Notify::new());
        let release = CancellationToken::new();
        let backend = Arc::new(Backend {
            predictions: predictions.clone(),
            entered_tail: entered_tail.clone(),
            tail_changed: tail_changed.clone(),
            release: release.clone(),
        });
        let engine = Engine::new(
            Config {
                memory_bytes: 100,
                cpus: vec![0, 1, 2],
                cores_per_worker: 1,
            },
            backend,
            Arc::new(UnknownPolicy(predictions)),
            Arc::new(EmptyMonitor),
            Arc::new(HeadroomAdmission),
            Arc::new(MemoryCache::default()),
        )
        .unwrap();
        engine.0.observed_peaks.lock().unwrap().push(60);
        let worker = engine.clone();
        let batch = tokio::spawn(async move {
            worker
                .verify_batch(Batch {
                    mode: Mode::All,
                    candidates: (0..5)
                        .map(|i| Candidate {
                            id: i.to_string(),
                            task_id: None,
                            code: format!("fixture-{i}"),
                            timeout_ms: 10000,
                            reuse: false,
                        })
                        .collect(),
                })
                .await
                .unwrap()
        });
        let concurrent = tokio::time::timeout(Duration::from_secs(2), async {
            loop {
                let changed = tail_changed.notified();
                if entered_tail.load(Ordering::SeqCst) == 3 {
                    break;
                }
                changed.await;
            }
        })
        .await
        .is_ok();
        // Also cleanly retire the fixture if the stale-forecast bug regresses.
        release.cancel();
        let results = batch.await.unwrap();
        engine.shutdown().await;
        assert_eq!(results.len(), 5);
        assert!(results.iter().all(|v| v.outcome.status == Status::Accepted));
        assert!(
            concurrent,
            "queued fallback must refresh from60 to1 instead of serializing the remaining three jobs"
        );
    }
}

#[cfg(test)]
mod observed_peak_median_tests {
    use super::*;

    fn compare_every_prefix(values: impl IntoIterator<Item = u64>) {
        let mut actual = ObservedPeaks::default();
        let mut reference = Vec::new();
        assert_eq!(actual.median(), None);
        for value in values {
            actual.push(value);
            reference.push(value);
            reference.sort_unstable();
            assert_eq!(
                actual.median(),
                Some(reference[reference.len() / 2]),
                "admission fallback changed after observation{}",
                reference.len()
            );
            assert_eq!(actual.lower.len() + actual.upper.len(), reference.len());
            assert!(actual.upper.len() >= actual.lower.len());
            assert!(actual.upper.len() <= actual.lower.len() + 1);
        }
    }

    #[test]
    fn exact_upper_median_matches_sorted_history_at_every_prefix() {
        compare_every_prefix(0..1024);
        compare_every_prefix((0..1024).rev());
        compare_every_prefix([0, u64::MAX, 1, u64::MAX, 0, 60, 1, 1, 1, 1, 1]);
        compare_every_prefix(std::iter::repeat_n(7, 1024));
        // Deterministic mixed and duplicate values, without a new dependency.
        let mut value = 1_u64;
        compare_every_prefix((0..4096).map(|_| {
            value = value.wrapping_mul(6364136223846793005).wrapping_add(1);
            value % 257
        }));
    }

    #[test]
    fn exact_upper_median_keeps_adapting_after_large_early_peaks() {
        let mut peaks = ObservedPeaks::default();
        peaks.push(60);
        peaks.push(1);
        assert_eq!(peaks.median(), Some(60));
        peaks.push(1);
        assert_eq!(peaks.median(), Some(1));
        peaks.push(u64::MAX);
        assert_eq!(peaks.median(), Some(60));
    }
}

#[cfg(test)]
mod queue_wakeup_tests {
    use super::*;
    use std::{
        future::Future,
        sync::atomic::AtomicUsize,
        task::{Context, Poll, Wake, Waker},
    };

    #[derive(Default)]
    struct CountWake(AtomicUsize);
    impl Wake for CountWake {
        fn wake(self: Arc<Self>) {
            self.0.fetch_add(1, Ordering::SeqCst);
        }
        fn wake_by_ref(self: &Arc<Self>) {
            self.0.fetch_add(1, Ordering::SeqCst);
        }
    }
    #[derive(Default)]
    struct Monitor(AtomicBool);
    impl ResourceMonitor for Monitor {
        fn sample(&self, _: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
            if self.0.load(Ordering::SeqCst) {
                Err("owned monitor failure fixture".into())
            } else {
                Ok(ResourceSnapshot::default())
            }
        }
    }
    struct NoBackend;
    #[async_trait::async_trait]
    impl VerificationBackend for NoBackend {
        fn identity(&self) -> String {
            "queue-wakeup-fixture".into()
        }
        async fn verify(&self, _: &Candidate, _: Execution) -> Outcome {
            panic!("private admission control must not execute a native backend");
        }
    }
    fn engine(monitor: Arc<Monitor>) -> Engine {
        let engine = Engine::new(
            Config {
                memory_bytes: 100,
                cpus: vec![0],
                cores_per_worker: 1,
            },
            Arc::new(NoBackend),
            Arc::new(Fifo),
            monitor,
            Arc::new(HeadroomAdmission),
            Arc::new(MemoryCache::default()),
        )
        .unwrap();
        // Keep every real acquire future pending until its Waker is registered.
        // The test controls this private free-core transition without a process.
        engine.0.state.lock().unwrap().free.clear();
        engine
    }
    fn candidates(n: usize) -> Vec<Candidate> {
        (0..n)
            .map(|i| Candidate {
                id: i.to_string(),
                task_id: None,
                code: "fixture".into(),
                timeout_ms: 300000,
                reuse: false,
            })
            .collect()
    }

    #[tokio::test]
    async fn full_queue_watchdog_wakes_only_the_head_and_retirement_passes_the_lease() {
        let engine = engine(Arc::new(Monitor::default()));
        let candidates = candidates(7808);
        let counts: Vec<_> = (0..candidates.len())
            .map(|_| Arc::new(CountWake::default()))
            .collect();
        let wakers: Vec<_> = counts.iter().cloned().map(Waker::from).collect();
        let mut waiting: Vec<_> = candidates
            .iter()
            .map(|c| {
                let queued = engine.0.enqueue(0, false);
                Box::pin(engine.0.acquire(Some(1), c, "fixture", false, queued))
            })
            .collect();
        for (future, waker) in waiting.iter_mut().zip(&wakers) {
            assert!(
                future
                    .as_mut()
                    .poll(&mut Context::from_waker(waker))
                    .is_pending()
            );
        }

        engine.0.state.lock().unwrap().free.insert(0);
        engine.0.watchdog();
        assert_eq!(counts[0].0.load(Ordering::SeqCst), 1);
        assert!(
            counts[1..].iter().all(|w| w.0.load(Ordering::SeqCst) == 0),
            "a resource tick woke ineligible tail requests"
        );

        let first = match waiting[0]
            .as_mut()
            .poll(&mut Context::from_waker(&wakers[0]))
        {
            Poll::Ready(Ok((lease, _, _, _))) => lease,
            _ => panic!("eligible head did not acquire"),
        };
        assert_eq!(engine.0.state.lock().unwrap().active.len(), 1);
        // Head removal can notify its successor before there is a free CPU.
        assert!(
            waiting[1]
                .as_mut()
                .poll(&mut Context::from_waker(&wakers[1]))
                .is_pending()
        );
        counts[1].0.store(0, Ordering::SeqCst);
        drop(first);
        assert_eq!(counts[1].0.load(Ordering::SeqCst), 1);
        let second = match waiting[1]
            .as_mut()
            .poll(&mut Context::from_waker(&wakers[1]))
        {
            Poll::Ready(Ok((lease, _, _, _))) => lease,
            _ => panic!("retired CPU lease did not reach the successor"),
        };
        drop(second);

        engine.shutdown().await;
        for (future, waker) in waiting.iter_mut().zip(&wakers).skip(2) {
            assert!(
                matches!(future.as_mut().poll(&mut Context::from_waker(waker)),
                Poll::Ready(Err(error)) if error == "engine shutdown")
            );
        }
        assert!(engine.0.state.lock().unwrap().queued.is_empty());
        assert!(engine.0.state.lock().unwrap().active.is_empty());
    }

    #[tokio::test]
    async fn head_cancellation_advances_and_monitor_failure_releases_every_waiter() {
        let monitor = Arc::new(Monitor::default());
        let engine = engine(monitor.clone());
        let candidates = candidates(32);
        let counts: Vec<_> = (0..candidates.len())
            .map(|_| Arc::new(CountWake::default()))
            .collect();
        let wakers: Vec<_> = counts.iter().cloned().map(Waker::from).collect();
        let mut waiting: Vec<_> = candidates
            .iter()
            .map(|c| {
                let queued = engine.0.enqueue(0, false);
                Box::pin(engine.0.acquire(Some(1), c, "fixture", false, queued))
            })
            .collect();
        for (future, waker) in waiting.iter_mut().zip(&wakers) {
            assert!(
                future
                    .as_mut()
                    .poll(&mut Context::from_waker(waker))
                    .is_pending()
            );
        }
        drop(waiting.remove(0));
        assert_eq!(counts[1].0.load(Ordering::SeqCst), 1);
        assert!(counts[2..].iter().all(|w| w.0.load(Ordering::SeqCst) == 0));
        assert!(
            waiting[0]
                .as_mut()
                .poll(&mut Context::from_waker(&wakers[1]))
                .is_pending()
        );
        counts[1].0.store(0, Ordering::SeqCst);

        monitor.0.store(true, Ordering::SeqCst);
        engine.0.watchdog();
        assert!(counts[1..].iter().all(|w| w.0.load(Ordering::SeqCst) == 1));
        for (future, waker) in waiting.iter_mut().zip(&wakers[1..]) {
            assert!(
                matches!(future.as_mut().poll(&mut Context::from_waker(waker)),
                Poll::Ready(Err(error)) if error == "owned monitor failure fixture")
            );
        }
        assert!(engine.0.state.lock().unwrap().queued.is_empty());
        assert!(engine.0.state.lock().unwrap().active.is_empty());
        engine.shutdown().await;
    }
}
