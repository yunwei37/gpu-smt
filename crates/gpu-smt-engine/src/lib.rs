//! Joint resource admission, exact-result sharing and explicit consumer semantics.
//! The watchdog samples once per second; it is not a kernel memory quota.
#![warn(missing_docs)]
pub mod linux;

use gpu_smt_core::*;
use std::{
    collections::{BTreeSet, HashMap, HashSet},
    sync::{
        Arc, Mutex, Weak,
        atomic::{AtomicBool, AtomicU64, Ordering},
    },
    time::Instant,
};
use tokio::{
    sync::{Notify, watch},
    task::JoinSet,
};
use tokio_util::sync::CancellationToken;

/// Default stable submission-order policy; exclusive resource retries take precedence.
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
    solo_waiters: usize,
    queued: BTreeSet<(u64, u64)>,
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

struct Inner {
    config: Config,
    backend: Arc<dyn VerificationBackend>,
    policy: Arc<dyn SchedulingPolicy>,
    admission: Arc<dyn AdmissionPolicy>,
    monitor: Arc<dyn ResourceMonitor>,
    cache: Arc<dyn ResultCache>,
    state: Mutex<State>,
    inflight: Mutex<HashMap<CacheKey, Flight>>,
    observed_peaks: Mutex<Vec<u64>>,
    next: AtomicU64,
    notify: Notify,
    fatal: Mutex<Option<String>>,
}
struct Lease {
    inner: Arc<Inner>,
    id: u64,
}
impl Drop for Lease {
    fn drop(&mut self) {
        let mut s = self.inner.state.lock().unwrap();
        if let Some(a) = s.active.remove(&self.id) {
            s.free.extend(a.cpus);
        }
        drop(s);
        self.inner.notify.notify_waiters();
    }
}
struct Queued {
    inner: Arc<Inner>,
    ticket: (u64, u64),
}
impl Drop for Queued {
    fn drop(&mut self) {
        self.inner.state.lock().unwrap().queued.remove(&self.ticket);
        self.inner.notify.notify_waiters();
    }
}
struct Solo {
    inner: Arc<Inner>,
}
impl Drop for Solo {
    fn drop(&mut self) {
        self.inner.state.lock().unwrap().solo_waiters -= 1;
        self.inner.notify.notify_waiters();
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
                for a in self.state.lock().unwrap().active.values() {
                    a.registry.cancel.cancel();
                }
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
        drop(s);
        self.notify.notify_waiters();
    }
    fn enqueue(self: &Arc<Self>, priority: u64) -> Queued {
        let ticket = (priority, self.next.fetch_add(1, Ordering::Relaxed));
        self.state.lock().unwrap().queued.insert(ticket);
        Queued {
            inner: self.clone(),
            ticket,
        }
    }
    async fn acquire(
        self: &Arc<Self>,
        estimate: Option<u64>,
        origin: &str,
        solo: bool,
        queued: Queued,
    ) -> Result<(Lease, Arc<Registry>, Vec<usize>, bool), String> {
        let ticket = queued.ticket;
        let _queued = queued;
        loop {
            let notified = self.notify.notified();
            if let Some(e) = self.fatal.lock().unwrap().clone() {
                return Err(e);
            }
            // Only an eligible queue head samples /proc. A watchdog tick must
            // not cause every queued candidate to scan the process table.
            let head_ready = {
                let s = self.state.lock().unwrap();
                (solo || s.queued.first() == Some(&ticket))
                    && s.free.len() >= self.config.cores_per_worker
            };
            if !head_ready {
                notified.await;
                continue;
            }
            let sample = self.snapshot()?;
            {
                let mut s = self.state.lock().unwrap();
                // Waiting jobs must refresh learned costs; freezing an unknown
                // forecast here serializes the entire first submitted batch.
                let estimate = estimate
                    .or_else(|| {
                        let mut peaks = self.observed_peaks.lock().unwrap().clone();
                        peaks.sort_unstable();
                        peaks.get(peaks.len() / 2).copied()
                    })
                    .or_else(|| {
                        s.active
                            .values()
                            .map(|a| a.registry.peak.load(Ordering::Relaxed))
                            .filter(|n| *n > 0)
                            .max()
                    });
                let actual_exclusive = solo
                    || self.config.cores_per_worker == self.config.cpus.len()
                    || estimate.is_some_and(|n| n >= self.config.memory_bytes);
                let unknown = estimate.is_none() && !s.active.is_empty();
                let exclusive_block = s.active.values().any(|a| a.exclusive)
                    || if actual_exclusive {
                        !s.active.is_empty()
                    } else {
                        s.solo_waiters > 0
                    };
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
                let queue_turn = solo || s.queued.first() == Some(&ticket);
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
        let mut queued = Some(queued);
        let mut attempts = vec![];
        let mut solo = false;
        let result = loop {
            if tx.is_closed() {
                break Outcome::operational(Status::Cancelled, "no live subscribers");
            }
            let predicted = self.policy.predicted_rss(&c).or_else(|| {
                let mut peaks = self.observed_peaks.lock().unwrap().clone();
                peaks.sort_unstable();
                peaks.get(peaks.len() / 2).copied()
            });
            let exclusive = solo || predicted.is_some_and(|n| n >= self.config.memory_bytes);
            let _solo = if exclusive {
                self.state.lock().unwrap().solo_waiters += 1;
                Some(Solo {
                    inner: self.clone(),
                })
            } else {
                None
            };
            let queued = queued
                .take()
                .unwrap_or_else(|| self.enqueue(self.policy.priority(&c)));
            let acquired = tokio::select! {
                r=self.acquire(predicted,&c.id,exclusive,queued)=>r,
                _=tx.closed()=>break Outcome::operational(Status::Cancelled,"no live subscribers"),
            };
            let (_lease, registry, cpus, exclusive) = match acquired {
                Ok(v) => v,
                Err(e) => break Outcome::operational(Status::BackendError, e),
            };
            let start = Instant::now();
            let execution = Execution {
                cancel: registry.cancel.clone(),
                cpus,
                registry: registry.clone(),
            };
            let future = self.backend.verify(&c, execution);
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
                solo_waiters: 0,
                queued: BTreeSet::new(),
            }),
            config,
            backend,
            policy,
            monitor,
            admission,
            cache,
            inflight: Mutex::new(HashMap::new()),
            observed_peaks: Mutex::new(vec![]),
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
        for a in self.0.state.lock().unwrap().active.values() {
            a.registry.cancel.cancel();
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
        let mut ids = HashSet::new();
        for c in &batch.candidates {
            if !ids.insert(c.id.clone()) || c.timeout_ms == 0 {
                return Err("unique IDs and nonzero timeout required".into());
            }
            if batch.mode == Mode::FirstSuccess && c.task_id.is_none() {
                return Err("first_success requires task_id".into());
            }
        }
        let mut pending: Vec<_> = batch
            .candidates
            .into_iter()
            .enumerate()
            .map(|(index, c)| (self.0.policy.priority(&c), index, c))
            .collect();
        let n = pending.len();
        pending.sort_by_key(|(priority, index, _)| (*priority, *index));
        // Register the complete ranked frontier before any physical executor
        // starts. Cost-model latency and Tokio wake order cannot reorder it.
        let pending: Vec<_> = pending
            .into_iter()
            .map(|(priority, index, c)| (self.0.enqueue(priority), index, c))
            .collect();
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
        let mut results: Vec<Option<Verification>> = vec![None; n];
        while let Some(next) = tasks.join_next().await {
            let (index, task, mut result) = next.map_err(|e| e.to_string())?;
            result.elapsed_seconds = submitted.elapsed().as_secs_f64();
            if batch.mode == Mode::FirstSuccess
                && result.outcome.status == Status::Accepted
                && let Some(task) = task
            {
                for cancel in &groups[&task] {
                    cancel.cancel();
                }
            }
            results[index] = Some(result);
        }
        Ok(results.into_iter().map(Option::unwrap).collect())
    }
}
