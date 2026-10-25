//! Verifier-neutral contracts. Predictions reorder work; they never reject it.
//! Public API0.1 is experimental. Logical and operational outcomes stay distinct.

#![warn(missing_docs)]
use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::sync::Arc;
use tokio_util::sync::CancellationToken;

/// Complete independent source; the backend environment is fixed for an engine lifetime.
#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Candidate {
    /// Caller identity, unique within its batch.
    pub id: String,
    /// Task identity for first-success consumers.
    #[serde(default)]
    pub task_id: Option<String>,
    /// Byte-exact full source, including imports.
    pub code: String,
    /// Native timeout; part of exact cache identity.
    #[serde(default = "default_timeout")]
    pub timeout_ms: u64,
    /// Permit exact completed/in-flight reuse; false requests a fresh execution.
    #[serde(default = "default_reuse")]
    pub reuse: bool,
}
fn default_reuse() -> bool {
    true
}
fn default_timeout() -> u64 {
    300_000
}

/// Consumer contract; cancellation is unavailable for individual rewards.
#[derive(Clone, Copy, Debug, Default, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Mode {
    /// Produce every candidate outcome.
    #[default]
    All,
    /// Cancel same-task subscribers after checked acceptance.
    FirstSuccess,
}

/// Complete submission.
#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Batch {
    /// Every-candidate or first-success semantics.
    #[serde(default)]
    pub mode: Mode,
    /// Original candidates.
    pub candidates: Vec<Candidate>,
}

/// Logical, consumer and operational outcomes.
#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Status {
    /// Native check completes without errors/admissions.
    Accepted,
    /// Native checking/elaboration error.
    Rejected,
    /// Admitted proof remains.
    Incomplete,
    /// Unchanged native timeout.
    Timeout,
    /// Exclusive retry exceeds the total resource budget.
    ResourceExhausted,
    /// Watchdog interruption before retry.
    Preempted,
    /// Consumer cancellation, never a native rejection.
    Cancelled,
    /// Transport/process/monitor fault.
    BackendError,
}

/// Native output with explicit operational classification.
#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct Outcome {
    /// Native/operational status.
    pub status: Status,
    /// Unmodified native JSON when available.
    pub response: Option<Value>,
    /// Operational explanation, never a fabricated native proof.
    pub error: Option<String>,
}
impl Outcome {
    /// Construct an operational outcome.
    pub fn operational(status: Status, error: impl Into<String>) -> Self {
        Self {
            status,
            response: None,
            error: Some(error.into()),
        }
    }
    /// Only stable native decisions are reusable.
    pub fn cacheable(&self) -> bool {
        matches!(
            self.status,
            Status::Accepted | Status::Rejected | Status::Incomplete
        )
    }
}

/// Backend lifecycle evidence, including a failed preparation before successful fallback.
#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct BackendEvent {
    /// Lifecycle stage such as preparation or fallback.
    pub stage: String,
    /// Observed reason, distinct from an unchanged native response.
    pub detail: String,
}

/// Accounting for one actual backend execution.
#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct Attempt {
    /// Preemptions remain in history.
    pub status: Status,
    /// Startup through complete retirement elapsed.
    pub elapsed_seconds: f64,
    /// Maximum of registered-tree RSS samples and backend supplements.
    /// Observation kinds remain in backend_events; this is not a complete
    /// aggregate or kernel process-tree high-water mark.
    pub peak_rss_bytes: u64,
    /// Exclusive retry after concurrent preemption.
    pub exclusive: bool,
    /// Actual process births, retained after reaping.
    pub processes: Vec<ProcessIdentity>,
    /// Aggregate measured RSS at watchdog interruption.
    pub preemption_rss_bytes: Option<u64>,
    /// Retained backend events; successful fallback must not hide failed preparation.
    #[serde(default)]
    pub backend_events: Vec<BackendEvent>,
}

/// Caller-specific result and provenance.
#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct Verification {
    /// Original caller ID.
    pub id: String,
    /// Final outcome.
    pub outcome: Outcome,
    /// Actual attempts; empty for completed cache hits.
    pub attempts: Vec<Attempt>,
    /// Queueing, retries, native work and cleanup.
    pub elapsed_seconds: f64,
    /// Reused completed native decision.
    pub cached: bool,
    /// Shared an exact in-flight verification.
    pub coalesced: bool,
}

/// Exact identity; no normalization or probabilistic equality.
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct CacheKey {
    /// Immutable backend/toolchain/project identity.
    pub backend: String,
    /// Byte-exact original source.
    pub code: String,
    /// Matching native timeout.
    pub timeout_ms: u64,
}

/// A kernel process identity is more than a reusable PID.
#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
pub struct ProcessIdentity {
    /// Owned process leader.
    pub pid: u32,
    /// Kernel start ticks.
    pub start_ticks: u64,
}

/// Owned job process accounting.
#[derive(Clone, Debug, Serialize)]
pub struct ProcessSample {
    /// Stable owned leader identity.
    pub identity: ProcessIdentity,
    /// Job tree summed RSS.
    pub rss_bytes: u64,
}

/// Actual total owned memory.
#[derive(Clone, Debug, Default)]
pub struct ResourceSnapshot {
    /// Includes owned trees and engine process.
    pub rss_bytes: u64,
    /// One entry per registered job.
    pub processes: Vec<ProcessSample>,
}

/// Backend-owned process registration.
pub trait ProcessRegistry: Send + Sync {
    /// Preserve lifecycle diagnostics without rewriting native proof output.
    fn note(&self, _event: BackendEvent) {}
    /// Register immediately after spawn, before expensive input.
    fn register(&self, process: ProcessIdentity);
    /// Supplement periodic sampling before a short-lived process is retired.
    fn observe_rss(&self, _bytes: u64) {}
    /// Remove only after full reaping.
    fn unregister(&self, process: &ProcessIdentity);
}

/// Per-attempt cancellation and resources.
#[derive(Clone)]
pub struct Execution {
    /// Backend kills and reaps before returning on cancellation.
    pub cancel: CancellationToken,
    /// Exclusively allocated CPU IDs.
    pub cpus: Vec<usize>,
    /// Process ownership for watchdog accounting.
    pub registry: Arc<dyn ProcessRegistry>,
}

/// Native verifier, solver or remote backend extension.
#[async_trait]
pub trait VerificationBackend: Send + Sync {
    /// Exact immutable environment identity.
    fn identity(&self) -> String;
    /// Whether backend-owned prepared state is ready; false by default.
    fn prepared_state_ready(&self) -> bool {
        false
    }
    /// Return after attempt children retire; shared prepared state retires at shutdown.
    async fn verify(&self, candidate: &Candidate, execution: Execution) -> Outcome;
    /// Execute a resource retry after the preceding attempt has fully retired
    /// and this engine has granted exclusive admission. Backends may reclaim
    /// idle prepared state; the default retains ordinary verification behavior.
    /// Cleanup must be included in the attempt and native request deadline.
    async fn verify_resource_retry(&self, candidate: &Candidate, execution: Execution) -> Outcome {
        self.verify(candidate, execution).await
    }
    /// Retire backend-owned idle/prepared state on engine shutdown.
    async fn shutdown(&self) {}
}

/// Ordering and predictions never return a proof verdict.
pub trait SchedulingPolicy: Send + Sync {
    /// Smaller first, stable submission order for ties.
    fn priority(&self, candidate: &Candidate) -> u64;
    /// One key per input candidate. Smaller first; original-index ties are stable.
    /// The default preserves existing per-source policies. Batch-aware wrappers
    /// may use task identity and consumer mode, never future native outcomes.
    /// An invalid length is rejected before submitting any physical work.
    fn batch_priorities(&self, candidates: &[Candidate], _mode: Mode) -> Vec<u64> {
        candidates.iter().map(|c| self.priority(c)).collect()
    }
    /// Predicted peak, not a fixed per-process memory cap.
    fn predicted_rss(&self, _candidate: &Candidate) -> Option<u64> {
        None
    }
}

/// Actual owned process sampling.
pub trait ResourceMonitor: Send + Sync {
    /// Errors are observable, never interpreted as zero usage.
    fn sample(&self, roots: &[ProcessIdentity]) -> Result<ResourceSnapshot, String>;
}

/// Joint memory/CPU admission extension.
pub trait AdmissionPolicy: Send + Sync {
    /// CPU allocation is checked separately against actual available core IDs.
    fn admit(&self, sample: &ResourceSnapshot, budget: u64, reserved_growth: u64) -> bool;
}

/// Exact completed-result store.
pub trait ResultCache: Send + Sync {
    /// Retrieve a stable native decision.
    fn get(&self, key: &CacheKey) -> Option<Outcome>;
    /// Store only stable native decisions.
    fn insert(&self, key: CacheKey, result: Outcome);
}

/// A sufficient witness is not a probability or runtime prediction.
pub struct FailureWitness {
    /// Native/version/state-scoped explanation.
    pub explanation: String,
}

/// Unknown falls back to native execution.
#[async_trait]
pub trait FailureDetector: Send + Sync {
    /// Finding alone cannot authorize rejection.
    async fn detect(&self, candidate: &Candidate) -> Option<FailureWitness>;
    /// Validate against actual native semantics before use.
    async fn validate(&self, candidate: &Candidate, witness: &FailureWitness) -> bool;
}

/// Native prepared-state extension, without an unsafe generic threaded fork.
#[async_trait]
pub trait PreparedState: Send + Sync {
    /// Create an isolated backend branch under explicit native quiescence rules.
    async fn branch(&self) -> Result<Arc<dyn VerificationBackend>, String>;
}
