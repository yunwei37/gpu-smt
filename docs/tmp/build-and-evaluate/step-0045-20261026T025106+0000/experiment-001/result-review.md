# Completion-order service delivery — root self-review

## Evidence selection before implementation
The prior task-held-out lexical ranker already has a negative offline result:
its interleaved replay15051.031831s is worse than the same reference's short-code
14659.452074s. This is fixed-span retrospective modeling, not native performance.
Do not retrain the same inspected data or revive a redundant full cell.
[Existing crossfit review](../../../../../artifacts/candidate-scheduling-2026-10-25/crossfit/result-review.md)
and model/source retain that evidence. The completed legacy all cell has161final
activity files, with overwritten source_id/snippet_id null at closure and reused
native processes. We did not establish a reconstructable per-candidate RSS join;
overlapping aggregate samples alone are not such labels. No memory model is
trained from them or mixed with the unfinished new point.

Existing480runtime boundaries leave simp internal stages opaque, as already
reported; no new phase/cycle conclusion can be reconstructed from them.
The prepared original23/48 hooks and full stderr capture remain necessary.

## Implemented consumer path
Existing HTTP waits for all candidates. Add optional typed NDJSON delivery
while keeping every collected/legacy route unchanged. Engine::verify_stream
and collected verify_batch share validation/ranking/frontier registration,
native coalescing/admission and checked first-success cancellation.
Each caller emits original index plus complete Verification in completion order;
Complete(count) requires one result per input,Error/uncounted EOF is incomplete.

Nonblocking channel sends decouple native cancellation from client read speed.
At most one result per input plus a terminal can buffer, like collected storage;
it is not an unlimited-memory or source-quota promise. Receiver drop cancels only
its batch's subscriptions. Shared RL demand retains its native job. Remaining
physical cleanup stays owned by the engine, never a global shutdown of peers.

## Actual validation
New event-synchronized protocol tests prove:
- an HTTP body yields the fast result while the slow peer is held by a gate;
- sibling retirement occurs before the stream is read at all;
- disconnect preserves a shared RL subscriber and only one physical shared job;
- dropping an HTTP response retires an actual owned Python fixture subprocess
  BEFORE engine.shutdown, not merely because final teardown kills everything;
- invalid duplicate inputs return400 before native work.
These are body/process/API tests, not sampled client-wire latency or native
proof/performance claims. A Python process fixture is not Lean.

The first run validation-20261026T025503 passes build/fmt/Clippy but its HTTP
early-delivery test times out: a zero-RSS fixture with unknown memory cost is
deliberately serialized by existing conservative admission. Provide its explicit
test-only cost forecast; production admission remains unchanged.
Validation-20261026T025758 then passes48tests and all checks. Strengthen the
unread-sibling test from timer ordering to actual cancellation notification;
final validation-20261026T030154 also passes48tests/fmt/Clippy/docs/help,4native
tests compile but remain explicitly skipped locally.
[Final raw receipt](../../../../../artifacts/rust-engine-2026-10-25/validation-20261026T030154/validation.json)
and all failed/intermediate receipts/logs remain. Combined final full+development
sampled RSS peak14,789,058,560B, no pressure withdrawal/monitor error.
The native4.18 source contract now compiles completion-order accepted/rejected
records checked against raw native envelopes; actual execution awaits existing
CI at the published source. No local candidate group overlaps the fullpair.

Only a dependency edge to already-locked futures-core is added for HTTP stream
adaptation; offline initial check updates that edge, no package version changes.
Existing input ordering,mode semantics,source/native binary and the loaded
fullpair implementation42659a8 remain unchanged.

## Scientific effect and next action
This enables actual early consumer delivery, but is ordinary service engineering,
not verifier speed, source prediction, new rejection logic or systems novelty.
Verification.elapsed_seconds remains internal availability; actual client
delivery/encoding/network costs require separate measurement. The pending full
resource capture remains the sole group; retain it, collect at real terminal,
then the already-authorized original nightly code workload and failure cohorts.
All original RQs and major contribution/evidence requirements remain open.
