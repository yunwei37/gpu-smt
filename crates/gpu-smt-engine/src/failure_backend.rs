//! Explicit opt-in bridge from admitted verification to backend-owned tactic replay.

use crate::FailureCache;
use async_trait::async_trait;
use gpu_smt_core::{
    Candidate, Execution, FailureReplayBackend, Outcome, ProcessIdentity, VerificationBackend,
};
use std::sync::Arc;

/// Typed failure storage for a backend, without requiring a concrete replay object.
pub type BackendFailureCache<B> = FailureCache<
    dyn FailureReplayBackend<
            Key = <B as FailureReplayBackend>::Key,
            Record = <B as FailureReplayBackend>::Record,
            State = <B as FailureReplayBackend>::State,
            Exception = <B as FailureReplayBackend>::Exception,
        >,
>;

/// Optional bridge implemented only by backends with qualified native tactic hooks.
///
/// The backend owns the state and ordinary exception path. A cache hit is never
/// a source verdict: continue backtracking/fallback and final native checking.
/// Misses/unsupported inputs run the original action. Operational errors must
/// remain operational; no timeout, memory failure or cancellation is recorded.
/// Returning from this hook has the same retirement obligations as verify.
/// Stock Lean backends do not implement this extension.
#[async_trait]
pub trait FailureCacheVerificationBackend: VerificationBackend + FailureReplayBackend {
    /// Verify a complete source with access to an owned ordinary-failure store.
    ///
    /// Capture each producer input before its fresh tactic action. Record only
    /// qualified ordinary failures, validate/charge replay through the native
    /// hook and propagate its exception through the original failure path.
    /// Original request limits, cancellation and final checking still apply.
    async fn verify_with_failure_cache(
        &self,
        candidate: &Candidate,
        execution: Execution,
        cache: &BackendFailureCache<Self>,
    ) -> Outcome;
}

/// Admitted backend adapter. Default construction delegates unchanged, without
/// allocating a failure store; enabling requires an explicit qualified backend.
///
/// Pass an Arc of this adapter to Engine::new like any VerificationBackend.
/// CLI/HTTP configuration and stock native adapters remain unchanged.
/// Retained records have no automatic eviction/size guarantee and count toward
/// the owning process's memory; use the normal resource monitor and lifecycle.
///
/// Default-off wiring through the existing engine backend interface:
///
/// ```
/// use gpu_smt_core::VerificationBackend;
/// use gpu_smt_engine::{FailureCacheAdapter, FailureCacheVerificationBackend};
/// use std::sync::Arc;
///
/// fn backend_for_engine<B>(backend: Arc<B>) -> Arc<dyn VerificationBackend>
/// where
///     B: FailureCacheVerificationBackend + 'static,
/// {
///     Arc::new(FailureCacheAdapter::new(backend))
/// }
/// ```
///
/// Explicit enablement uses [Self::enabled] after backend-specific native
/// qualification. This example checks public API wiring, not replay safety.
pub struct FailureCacheAdapter<B: FailureCacheVerificationBackend + ?Sized> {
    // Release native record references before the final backend Arc on drop.
    cache: Option<BackendFailureCache<B>>,
    backend: Arc<B>,
}

impl<B: FailureCacheVerificationBackend + ?Sized> FailureCacheAdapter<B> {
    /// Default-off adapter: no tactic store or hook invocation.
    pub fn new(backend: Arc<B>) -> Self {
        Self {
            cache: None,
            backend,
        }
    }

    /// Explicitly enable backend-owned tactic replay for this adapter lifetime.
    /// This is not a declaration of native qualification or measured benefit.
    pub fn enabled(backend: Arc<B>) -> Self {
        Self {
            cache: Some(BackendFailureCache::<B>::default()),
            backend,
        }
    }
}

#[async_trait]
impl<B: FailureCacheVerificationBackend + ?Sized> VerificationBackend for FailureCacheAdapter<B> {
    fn identity(&self) -> String {
        let original = self.backend.identity();
        if self.cache.is_some() {
            // Keep opt-in verification separate in any shared whole-source cache.
            serde_json::to_string(&("ordinary-failure-cache-v1", original))
                .expect("identity serializes")
        } else {
            original
        }
    }

    fn prepared_state_ready(&self) -> bool {
        self.backend.prepared_state_ready()
    }

    async fn verify(&self, candidate: &Candidate, execution: Execution) -> Outcome {
        match &self.cache {
            Some(cache) => {
                self.backend
                    .verify_with_failure_cache(candidate, execution, cache)
                    .await
            }
            None => self.backend.verify(candidate, execution).await,
        }
    }

    async fn verify_resource_retry(&self, candidate: &Candidate, execution: Execution) -> Outcome {
        // Engine grants this only after peer retirement. Release old native
        // references before the backend reclaims idle/prepared memory. Never
        // replace its resource-specific path with the optional replay hook.
        if let Some(cache) = &self.cache {
            cache.clear();
        }
        self.backend
            .verify_resource_retry(candidate, execution)
            .await
    }

    fn request_resource_preemption(&self, processes: &[ProcessIdentity]) {
        self.backend.request_resource_preemption(processes);
    }

    async fn shutdown(&self) {
        // Engine awaits active verification retirement before calling shutdown.
        if let Some(cache) = &self.cache {
            cache.clear();
        }
        self.backend.shutdown().await;
    }
}
