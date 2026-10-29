//! Backend-owned tactic failure replay contracts, separate from source verdicts.

use async_trait::async_trait;
use std::hash::Hash;
use tokio_util::sync::CancellationToken;

/// Completion of a fresh tactic action, not a whole-source verification result.
pub enum TacticCompletion<R> {
    /// A qualified ordinary exception with its compatible failed transition.
    ///
    /// The backend record must include post-state, diagnostics, fresh identities
    /// and action heartbeat accounting needed for replay; error text alone is
    /// insufficient. Producing this variant is a trusted backend responsibility.
    OrdinaryFailure(R),
    /// Anything else, including returns, unqualified errors, timeouts, memory
    /// limits, cancellation, native process failure and internal exceptions.
    /// It must not become a reusable ordinary-failure entry.
    NotReplayable,
}

/// Optional native extension for replaying an ordinary tactic failure.
///
/// Current stock Lean adapters do not implement this trait. Implementing it and
/// passing fixture tests does not certify native replay or workload benefit.
#[async_trait]
pub trait FailureReplayBackend: Send + Sync {
    /// Exact backend-defined replay-compatible input, not a digest or merely an
    /// observed goal/context key.
    type Key: Clone + Eq + Hash + Send + Sync;
    /// Immutable owned failed transition; must keep native references valid.
    type Record: Send + Sync;
    /// Exclusively held native state/session handle, including resource context.
    type State: Send + Sync;

    /// Capture a coherent (scope, key) while the caller owns the input state.
    /// Scope includes backend/environment and process/allocation generation.
    /// Return None for unsupported or not-yet-qualified inputs.
    fn replay_input(&self, state: &Self::State) -> Option<(String, Self::Key)>;

    /// Revalidate the supplied input and record before committing a transition.
    ///
    /// True means an ordinary failure's post-state, diagnostics and original
    /// action heartbeats were applied exactly once, not acceptance or rejection
    /// of a source. Native budget/cancellation rules still apply. False requests
    /// original execution and must leave observable state and charged action
    /// heartbeats unchanged. Recheck scope/key/cancellation at commit; lookup
    /// alone cannot guarantee a live session. Err is operational and must not
    /// be converted to a tactic rejection or unsafe fallback on a damaged state.
    async fn replay_failure(
        &self,
        state: &mut Self::State,
        scope: &str,
        key: &Self::Key,
        record: &Self::Record,
        cancel: &CancellationToken,
    ) -> Result<bool, String>;
}
