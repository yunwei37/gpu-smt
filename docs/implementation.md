# Implementation: Rust engine and retained research adapters

Updated2026-10-25. All source/build/test work occurs in the retained
yunwei356/gpu-smt-dev Workspace, /workspaces/repository on main, by this
thread only. No OMP/subagents/native AI-session resumes. Reviews are self-review.

## Reusable engine

The Rust workspace has four crates:

| Crate | Implemented responsibility |
|---|---|
|gpu-smt-core|Typed source/consumer/verdict/attempt contracts; backend, policy, monitor, admission, cache, detector and prepared-state traits|
|gpu-smt-engine|Global CPU slots, priority admission queue, actual RSS reservations, watchdog, exclusive retry, exact cache/in-flight sharing, all/first-success semantics|
|gpu-smt-lean|Original native JSON command transport in isolated fresh process groups, assigned CPU affinity, timeout/cancellation and reaping|
|gpu-smt-server|Local HTTP core/check and legacy/verify adapters, typed/v1/verify, JSONL/HTTP executable and reusable capture/comparison|

The initial native backend is fresh-process execution, not safe COW or
one-load Mathlib. Unsupported debug/infotree/state-handle features return an
explicit compatibility error or remain out of scope. Backend environment
identity is immutable for cache lifetime. No ordinary cache/queue/fork
primitive is a novelty claim. [Architecture](architecture.md), [API](api.md).

## Resource contract

New groups:48GiB total actual owned RSS, no per-process AS cap, CPU8–11.
A15second actual legacy-worker observation sees one thread and~one active
core per REPL; next-point capacity starts at four one-core workers, subject
to measured-memory admission. The Rust default learns positive observed
peaks; source-policy predictions can override reservations. Unknown costs
start conservatively. Prediction never proves rejection.

Every second actual owned-tree RSS is sampled, including idle preparation
descendants. Concurrent preemptions kill/reap and requeue for an exclusive
attempt. That attempt still exceeding the total budget becomes an explicit
resource failure, with all attempt costs retained. Last-subscriber cancellation
waits for backend cleanup; an RL subscriber keeps shared work alive.
Sampling is not a kernel quota and can overshoot between observations.
The backend refuses an inherited finite AS cap rather than silently claiming
the new resource point. No Workspace quota or other Workspace is changed.

The existing healthy full7808three-policy capture keeps its original
two-worker/24GiB-AS/48GiB point and source snapshot. Do not restart or mix its
clocks with the next point. Historical42bad_alloc records remain untouched.

## Semantic guarantees and tests

Exact keys include backend/environment, original source and timeout; no
normalization/prefix/certificate reuse. Completed native outcomes alone are
cacheable. Operational resource/timeout/cancel outcomes remain distinct.
Every all-mode caller gets a record, including coalesced duplicates.
First-success cancellation needs an actual same-task accepted native result.

Tests cover exact keys, every-candidate versus first-success, RL subscriptions
surviving sibling cancellation, queued cancellation/retirement accounting,
memory preemption/exclusive retries, owned process birth identity, real
low-threshold RSS fault injection, native JSON classification and HTTP schemas.
The subprocess fixture is not Lean. Actual raw-native differential tests are
separate and explicitly skipped locally while the sole research collection
runs; pinned official Lean4.18/REPL CI runs the native contract independently.
No test suite is a full native population parity or throughput result.

## Pending native work

Safe Lean+C preparation/COW, actual sufficient failure detectors, trained
source memory/time models, multi-node execution,42larger-memory isolated
reruns and full new-resource/native matched throughput remain open.
PreparedState/FailureDetector are extension contracts; no active rejection
path or COW performance is implied by their definitions.
The code-verification/math workloads and all four paper RQs remain open.

CPU oracle source/data are frozen baselines and must not be optimized or
extended. Old narrow GPU/kernel branches and all raw/failure records remain;
[Evaluation](evaluation.md) owns scientific result scope.
The exact previous491-line implementation record is preserved in the
[dated archive](tmp/bootstrap/step-0012-20261025T0735-engine/implementation-history-through-20261025T0815.md.gz).
