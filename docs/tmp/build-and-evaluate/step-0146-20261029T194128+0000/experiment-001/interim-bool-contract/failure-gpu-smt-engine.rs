//! Standalone ordinary-failure storage. Not connected to Engine verification.

use gpu_smt_core::{FailureReplayBackend, TacticCompletion};
use std::{
    collections::HashMap,
    sync::{Arc, Mutex},
};
use tokio_util::sync::CancellationToken;

/// Backend input captured before the original action, with private scope/key.
/// A producer cannot silently acquire a restarted backend's scope at insertion.
#[derive(Clone, PartialEq, Eq, Hash)]
pub struct FailureInput<K> {
    scope: String,
    key: K,
}

type Entries<K, R> = HashMap<FailureInput<K>, Arc<R>>;

/// Development skeleton for qualified backend-owned ordinary-failure records.
///
/// This is separate from the whole-source ResultCache and is not constructed by
/// Engine, CLI or HTTP. No stock Lean replay adapter is supplied. Native state
/// compatibility and transition validation remain backend responsibilities.
/// Retained records consume memory; scope this store to an owned lifecycle and
/// clear/drop it when obsolete. There is no automatic eviction/size guarantee.
pub struct FailureCache<B: FailureReplayBackend> {
    entries: Mutex<Entries<B::Key, B::Record>>,
}

impl<B: FailureReplayBackend> Default for FailureCache<B> {
    fn default() -> Self {
        Self {
            entries: Mutex::new(HashMap::new()),
        }
    }
}

impl<B: FailureReplayBackend> FailureCache<B> {
    /// Capture a backend-qualified input before fresh original execution.
    pub fn capture(&self, backend: &B, state: &B::State) -> Option<FailureInput<B::Key>> {
        backend
            .replay_input(state)
            .map(|(scope, key)| FailureInput { scope, key })
    }

    /// Record a fresh action's completion under its previously captured input.
    /// Ineligible completions invalidate any prior entry for that input. A
    /// replay itself is not a new native producer. No source verdict is stored.
    pub fn remember(
        &self,
        input: FailureInput<B::Key>,
        completion: TacticCompletion<B::Record>,
    ) -> bool {
        let replacement = match completion {
            TacticCompletion::OrdinaryFailure(record) => Some(Arc::new(record)),
            TacticCompletion::NotReplayable => None,
        };
        let stored = replacement.is_some();
        let old = {
            let mut entries = self.entries.lock().unwrap();
            match replacement {
                Some(record) => entries.insert(input, record),
                None => entries.remove(&input),
            }
        };
        // Backend-owned record destruction may release native references.
        drop(old);
        stored
    }

    /// Try backend-validated replay; false falls through to original execution.
    /// The metadata lock is released before awaiting the backend. A cancellation
    /// or stale-state race is also checked by the backend before committing.
    pub async fn try_replay(
        &self,
        backend: &B,
        state: &mut B::State,
        cancel: &CancellationToken,
    ) -> Result<bool, String> {
        if cancel.is_cancelled() {
            return Ok(false);
        }
        let Some(input) = self.capture(backend, state) else {
            return Ok(false);
        };
        let record = self.entries.lock().unwrap().get(&input).cloned();
        match record {
            Some(record) => {
                backend
                    .replay_failure(state, &input.scope, &input.key, &record, cancel)
                    .await
            }
            None => Ok(false),
        }
    }

    /// Release retained records. Does not cancel an already in-flight replay;
    /// native execution ownership/cancellation remains the caller's obligation.
    pub fn clear(&self) {
        let records = std::mem::take(&mut *self.entries.lock().unwrap());
        drop(records);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use async_trait::async_trait;
    use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering};

    // Explicit simulator. These tests do not certify any Lean state projection.
    #[derive(Clone, Debug, PartialEq, Eq)]
    struct State {
        environment: &'static str,
        generation: u64,
        goal: u64,
        fresh: u64,
        heartbeats: u64,
        errors: Vec<&'static str>,
        supported: bool,
    }
    impl Default for State {
        fn default() -> Self {
            Self {
                environment: "fixture",
                generation: 1,
                goal: 7,
                fresh: 11,
                heartbeats: 100,
                errors: vec![],
                supported: true,
            }
        }
    }
    struct Record {
        goal: u64,
        fresh_delta: u64,
        heartbeats: u64,
        error: &'static str,
        on_drop: Option<Arc<dyn Fn() + Send + Sync>>,
    }
    impl Default for Record {
        fn default() -> Self {
            Self {
                goal: 8,
                fresh_delta: 2,
                heartbeats: 9,
                error: "simulated ordinary failure",
                on_drop: None,
            }
        }
    }
    impl Drop for Record {
        fn drop(&mut self) {
            if let Some(callback) = &self.on_drop {
                callback();
            }
        }
    }
    #[derive(Default)]
    struct Backend {
        epoch: Arc<AtomicU64>,
        calls: AtomicUsize,
        reject: AtomicBool,
        fault: AtomicBool,
        on_replay: Mutex<Option<Arc<dyn Fn() + Send + Sync>>>,
    }
    #[async_trait]
    impl FailureReplayBackend for Backend {
        type Key = (u64, u64);
        type Record = Record; // Deliberately not Clone.
        type State = State;

        fn replay_input(&self, state: &State) -> Option<(String, Self::Key)> {
            state.supported.then(|| {
                (
                    format!(
                        "{}|{}|{}",
                        state.environment,
                        state.generation,
                        self.epoch.load(Ordering::SeqCst)
                    ),
                    (state.goal, state.fresh),
                )
            })
        }
        async fn replay_failure(
            &self,
            state: &mut State,
            scope: &str,
            key: &Self::Key,
            record: &Record,
            cancel: &CancellationToken,
        ) -> Result<bool, String> {
            self.calls.fetch_add(1, Ordering::SeqCst);
            let callback = self.on_replay.lock().unwrap().clone();
            if let Some(callback) = callback {
                callback();
            }
            if cancel.is_cancelled()
                || self.reject.load(Ordering::SeqCst)
                || self.replay_input(state) != Some((scope.into(), *key))
                || state.heartbeats < record.heartbeats
            {
                return Ok(false);
            }
            if self.fault.load(Ordering::SeqCst) {
                return Err("simulated backend fault".into());
            }
            let mut next = state.clone();
            next.goal = record.goal;
            next.fresh += record.fresh_delta;
            next.heartbeats -= record.heartbeats;
            next.errors.push(record.error);
            *state = next;
            Ok(true)
        }
    }
    fn record(cache: &FailureCache<Backend>, backend: &Backend, state: &State) {
        let input = cache.capture(backend, state).unwrap();
        assert!(cache.remember(input, TacticCompletion::OrdinaryFailure(Record::default())));
    }

    #[tokio::test]
    async fn applies_failed_transition_and_debits_once_without_a_source_verdict() {
        let backend = Backend::default();
        let cache = FailureCache::default();
        let mut state = State::default();
        record(&cache, &backend, &state);
        assert!(
            cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!((state.goal, state.fresh, state.heartbeats), (8, 13, 91));
        assert_eq!(state.errors, ["simulated ordinary failure"]);
        let after = state.clone();
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(state, after);
        assert_eq!(backend.calls.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn misses_and_unsupported_inputs_preserve_original_execution() {
        let backend = Backend::default();
        let cache = FailureCache::default();
        let mut state = State::default();
        let before = state.clone();
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(state, before);
        state.supported = false;
        let before = state.clone();
        assert!(cache.capture(&backend, &state).is_none());
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(state, before);
        assert_eq!(backend.calls.load(Ordering::SeqCst), 0);
    }

    #[tokio::test]
    async fn insufficient_budget_and_backend_rejection_commit_no_effects() {
        let backend = Backend::default();
        let cache = FailureCache::default();
        let original = State::default();
        record(&cache, &backend, &original);
        let mut state = State {
            heartbeats: 8,
            ..original.clone()
        };
        let before = state.clone();
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(state, before);
        state = original.clone();
        backend.reject.store(true, Ordering::SeqCst);
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(state, original);
    }

    #[tokio::test]
    async fn nonreplayable_completion_cannot_retain_a_previous_ordinary_failure() {
        let backend = Backend::default();
        let cache = FailureCache::default();
        let mut state = State::default();
        let input = cache.capture(&backend, &state).unwrap();
        assert!(!cache.remember(input.clone(), TacticCompletion::NotReplayable));
        assert!(cache.remember(
            input.clone(),
            TacticCompletion::OrdinaryFailure(Record::default())
        ));
        assert!(!cache.remember(input, TacticCompletion::NotReplayable));
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(backend.calls.load(Ordering::SeqCst), 0);
    }

    #[tokio::test]
    async fn producer_scope_is_captured_before_restart_not_relabelled_at_insertion() {
        let backend = Backend::default();
        let cache = FailureCache::default();
        let mut state = State::default();
        let old_input = cache.capture(&backend, &state).unwrap();
        backend.epoch.store(1, Ordering::SeqCst);
        cache.remember(
            old_input,
            TacticCompletion::OrdinaryFailure(Record::default()),
        );
        let before = state.clone();
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(state, before);
        backend.epoch.store(0, Ordering::SeqCst);
        state.environment = "different";
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        state.environment = "fixture";
        state.generation += 1;
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        state.generation = 1;
        state.goal += 1;
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(backend.calls.load(Ordering::SeqCst), 0);
    }

    #[tokio::test]
    async fn cancellation_before_lookup_and_during_validation_preserves_state() {
        let backend = Backend::default();
        let cache = FailureCache::default();
        let mut state = State::default();
        record(&cache, &backend, &state);
        let cancel = CancellationToken::new();
        cancel.cancel();
        let before = state.clone();
        assert!(
            !cache
                .try_replay(&backend, &mut state, &cancel)
                .await
                .unwrap()
        );
        assert_eq!(backend.calls.load(Ordering::SeqCst), 0);
        let cancel = CancellationToken::new();
        let during = cancel.clone();
        *backend.on_replay.lock().unwrap() = Some(Arc::new(move || during.cancel()));
        assert!(
            !cache
                .try_replay(&backend, &mut state, &cancel)
                .await
                .unwrap()
        );
        assert_eq!(state, before);
        assert_eq!(backend.calls.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn backend_revalidates_scope_after_lookup_and_propagates_faults() {
        let backend = Backend::default();
        let cache = FailureCache::default();
        let mut state = State::default();
        record(&cache, &backend, &state);
        let epoch = backend.epoch.clone();
        *backend.on_replay.lock().unwrap() = Some(Arc::new(move || {
            epoch.fetch_add(1, Ordering::SeqCst);
        }));
        let before = state.clone();
        assert!(
            !cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        assert_eq!(state, before);
        *backend.on_replay.lock().unwrap() = None;
        backend.epoch.store(0, Ordering::SeqCst);
        backend.fault.store(true, Ordering::SeqCst);
        assert_eq!(
            cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await,
            Err("simulated backend fault".into())
        );
    }

    #[tokio::test]
    async fn replay_and_record_destruction_run_outside_the_metadata_lock() {
        let backend = Backend::default();
        let cache = Arc::new(FailureCache::default());
        let mut state = State::default();
        let input = cache.capture(&backend, &state).unwrap();
        let drops = Arc::new(AtomicUsize::new(0));
        let make_record = || {
            let weak = Arc::downgrade(&cache);
            let drops = drops.clone();
            Record {
                on_drop: Some(Arc::new(move || {
                    let cache = weak.upgrade().unwrap();
                    assert!(
                        cache.entries.try_lock().is_ok(),
                        "record dropped under store lock"
                    );
                    drops.fetch_add(1, Ordering::SeqCst);
                })),
                ..Record::default()
            }
        };
        cache.remember(
            input.clone(),
            TacticCompletion::OrdinaryFailure(make_record()),
        );
        let weak = Arc::downgrade(&cache);
        *backend.on_replay.lock().unwrap() = Some(Arc::new(move || {
            let cache = weak.upgrade().unwrap();
            assert!(
                cache.entries.try_lock().is_ok(),
                "backend replay under store lock"
            );
        }));
        assert!(
            cache
                .try_replay(&backend, &mut state, &CancellationToken::new())
                .await
                .unwrap()
        );
        cache.remember(
            input.clone(),
            TacticCompletion::OrdinaryFailure(make_record()),
        );
        assert_eq!(drops.load(Ordering::SeqCst), 1);
        cache.clear();
        assert_eq!(drops.load(Ordering::SeqCst), 2);
        cache.remember(
            input.clone(),
            TacticCompletion::OrdinaryFailure(make_record()),
        );
        cache.remember(input, TacticCompletion::NotReplayable);
        assert_eq!(drops.load(Ordering::SeqCst), 3);
    }
}
