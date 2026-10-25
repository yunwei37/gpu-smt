# Reclaim prepared state for an exclusive resource retry

Source inspection finds the current Engine requeues RSS-preempted work alone,
but PreparedRepl then branches again from its resident import parent. Summed RSS
still charges both parent and child: the parent can deny the exclusive candidate
memory which a fresh native process would have. Fix this resource-layer defect
before the requested new-point whole-population run, without changing proof,
timeout, source, acceptance rules or the frozen CPU oracle.

Extend VerificationBackend with a defaulted exclusive-resource-retry operation
which delegates to verify, preserving existing implementations. Engine calls it
only after a preempted/resource-exhausted concurrent attempt retired and the
retry acquired exclusive admission. PreparedRepl retires its idle import parent,
then invokes the unchanged fresh native backend within the same request
deadline; retain eviction/fallback provenance and all cleanup costs.
Later ordinary requests may prepare a new parent. Ordinary timeouts/cancellation
still preserve their existing reusable parent. No public Execution struct field
or source input shape changes.

Verify engine retry routing/history using the existing preemption control.
Extend the pinned real-native prepared-parent differential test to check old
parent retirement, unchanged fresh response, later re-preparation, and shutdown
cleanup. Local non-Lean process/resource tests run in the owning Workspace;
actual Lean controls execute in the existing native CI, while the sole original
7808 collection stays unchanged. No new local candidate group. These tests
establish lifecycle behavior, not fullMathlib or whole-workload acceleration.
