//! Public simulated adapter tests. No Lean state or proof verdict is replayed.
use async_trait::async_trait;
use proofserve_core::{FailureReplayBackend, TacticCompletion};
use proofserve_engine::FailureCache;
use std::{
    cell::Cell,
    sync::{
        Arc,
        atomic::{AtomicU64, AtomicUsize, Ordering},
    },
    time::Duration,
};
use tokio::sync::{Barrier, Semaphore};
use tokio_util::sync::CancellationToken;

// Cell is Send,not Sync: this state is exclusively owned by each consumer.
#[derive(Debug, PartialEq, Eq)]
struct State {
    goal: Cell<u64>,
    fresh: Cell<u64>,
    heartbeats: u64,
    diagnostics: Vec<&'static str>,
}
impl State {
    fn new(heartbeats: u64) -> Self {
        Self {
            goal: Cell::new(7),
            fresh: Cell::new(11),
            heartbeats,
            diagnostics: vec![],
        }
    }
}
struct Transition {
    drops: Arc<AtomicUsize>,
}
impl Drop for Transition {
    fn drop(&mut self) {
        self.drops.fetch_add(1, Ordering::SeqCst);
    }
}
struct Simulation {
    generation: AtomicU64,
    entered: Barrier,
    release: Semaphore,
}
#[async_trait]
impl FailureReplayBackend for Simulation {
    type Key = (u64, u64);
    type Record = Transition;
    type State = State;
    type Exception = &'static str;

    fn replay_input(&self, state: &State) -> Option<(String, Self::Key)> {
        Some((
            format!("simulation|{}", self.generation.load(Ordering::SeqCst)),
            (state.goal.get(), state.fresh.get()),
        ))
    }
    async fn replay_failure(
        &self,
        state: &mut State,
        scope: &str,
        key: &Self::Key,
        _record: &Transition,
        cancel: &CancellationToken,
    ) -> Result<Option<Self::Exception>, String> {
        self.entered.wait().await;
        self.release
            .acquire()
            .await
            .map_err(|error| error.to_string())?
            .forget();
        if cancel.is_cancelled()
            || self.replay_input(state) != Some((scope.into(), *key))
            || state.heartbeats < 9
        {
            return Ok(None);
        }
        state.goal.set(8);
        state.fresh.set(state.fresh.get() + 2);
        state.heartbeats -= 9;
        state.diagnostics.push("simulated ordinary exception");
        Ok(Some("simulated ordinary exception"))
    }
}
type DynamicBackend = dyn FailureReplayBackend<
        Key = (u64, u64),
        Record = Transition,
        State = State,
        Exception = &'static str,
    >;
type Store = FailureCache<DynamicBackend>;

fn fixture(consumers: usize) -> (Arc<Simulation>, Arc<Store>, Arc<AtomicUsize>) {
    let backend = Arc::new(Simulation {
        generation: AtomicU64::new(0),
        entered: Barrier::new(consumers + 1),
        release: Semaphore::new(0),
    });
    let cache = Arc::new(Store::default());
    let drops = Arc::new(AtomicUsize::new(0));
    let input = cache.capture(backend.as_ref(), &State::new(100)).unwrap();
    assert!(cache.remember(
        input,
        TacticCompletion::OrdinaryFailure(Transition {
            drops: drops.clone()
        })
    ));
    (backend, cache, drops)
}
fn replay(
    cache: Arc<Store>,
    backend: Arc<Simulation>,
    cancel: CancellationToken,
    heartbeats: u64,
) -> tokio::task::JoinHandle<(Option<&'static str>, State)> {
    // Exercise the dynamic public API; the library must not require a concrete backend.
    let backend: Arc<DynamicBackend> = backend;
    tokio::spawn(async move {
        let mut state = State::new(heartbeats);
        let exception = cache
            .try_replay(backend.as_ref(), &mut state, &cancel)
            .await
            .unwrap();
        (exception, state)
    })
}
async fn entered(backend: &Simulation) {
    // Deadlock detection only,not a timing/performance assertion.
    tokio::time::timeout(Duration::from_secs(5), backend.entered.wait())
        .await
        .unwrap();
}
async fn settled(
    task: tokio::task::JoinHandle<(Option<&'static str>, State)>,
) -> (Option<&'static str>, State) {
    tokio::time::timeout(Duration::from_secs(5), task)
        .await
        .unwrap()
        .unwrap()
}
fn applied(remaining: u64) -> State {
    State {
        goal: Cell::new(8),
        fresh: Cell::new(13),
        heartbeats: remaining,
        diagnostics: vec!["simulated ordinary exception"],
    }
}

#[tokio::test]
async fn clear_during_two_suspended_replays_keeps_records_alive_and_does_not_serialize() {
    let (backend, cache, drops) = fixture(2);
    let first = replay(
        cache.clone(),
        backend.clone(),
        CancellationToken::new(),
        100,
    );
    let second = replay(cache.clone(), backend.clone(), CancellationToken::new(), 80);
    entered(&backend).await;
    cache.clear();
    assert_eq!(
        drops.load(Ordering::SeqCst),
        0,
        "in-flight records must stay owned"
    );
    let mut after_clear = State::new(100);
    assert_eq!(
        cache
            .try_replay(
                backend.as_ref(),
                &mut after_clear,
                &CancellationToken::new()
            )
            .await
            .unwrap(),
        None
    );
    assert_eq!(after_clear, State::new(100));
    backend.release.add_permits(2);
    assert_eq!(
        settled(first).await,
        (Some("simulated ordinary exception"), applied(91))
    );
    assert_eq!(
        settled(second).await,
        (Some("simulated ordinary exception"), applied(71))
    );
    assert_eq!(
        drops.load(Ordering::SeqCst),
        1,
        "release exactly once after the final reader"
    );
}

#[tokio::test]
async fn live_generation_change_after_lookup_preserves_the_consumers_input() {
    let (backend, cache, _drops) = fixture(1);
    let task = replay(cache, backend.clone(), CancellationToken::new(), 100);
    entered(&backend).await;
    backend.generation.fetch_add(1, Ordering::SeqCst);
    backend.release.add_permits(1);
    assert_eq!(settled(task).await, (None, State::new(100)));
}

#[tokio::test]
async fn cancelling_one_suspended_consumer_keeps_the_other_failure_transition() {
    let (backend, cache, _drops) = fixture(2);
    let cancel = CancellationToken::new();
    let first = replay(cache.clone(), backend.clone(), cancel.clone(), 100);
    let second = replay(cache, backend.clone(), CancellationToken::new(), 80);
    entered(&backend).await;
    cancel.cancel();
    backend.release.add_permits(2);
    assert_eq!(settled(first).await, (None, State::new(100)));
    assert_eq!(
        settled(second).await,
        (Some("simulated ordinary exception"), applied(71))
    );
}
