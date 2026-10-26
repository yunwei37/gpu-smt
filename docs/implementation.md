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

The default native backend is fresh-process execution. An optional Lean+C
import-parent backend now has source and a Rust adapter, with actual pinned-native
qualification tracked separately from whole Mathlib COW/performance evidence. Unsupported debug/infotree/state-handle features return an
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
attempt. PreparedRepl evicts its idle import parent before that resource retry,
runs it fresh under the same request deadline, and allows preparation again on
later ordinary work. This restores the budget formerly consumed by idle state;
eviction/fallback remain in attempt provenance. That attempt still exceeding the total budget becomes an explicit
resource failure, with all attempt costs retained. Last-subscriber cancellation
waits for backend cleanup; an RL subscriber keeps shared work alive.
Sampling is not a kernel quota and can overshoot between observations.
The backend refuses an inherited finite AS cap rather than silently claiming
the new resource point. No Workspace quota or other Workspace is changed.

The completed full7808 three-policy capture retains its original
two-worker/24GiB-AS/48GiB point and source snapshot. The sole active capture is
now the fresh-native/Mathlib-derived full pair at the dynamic four-core point,
implementation42659a8. Do not mix their clocks. Historical42bad_alloc records
remain untouched pending separately reported exclusive retries.

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

Full Mathlib/native qualification of import preparation/COW, actual sufficient failure detectors, trained
source memory/time models, multi-node execution,42larger-memory isolated
reruns and full new-resource/native matched throughput remain open.
PreparedState/FailureDetector are extension contracts; no active rejection
path or COW performance is implied by their definitions.

The source CLI backend now accepts explicitly declared upstream arguments via
NativeLean::with_args and repeated --lean-arg. Defaults remain unchanged;
nonempty argv partitions cache identity. Process/CLI transport tests pass, and
same-argv pinned-native differential coverage is compiled for existing CI.
This preserves lean-mlir upstream --tstack=400000; it does not establish the
pending original-file/stdin or complete bv_decide workload result.

A [separate interval-continuation prototype](../bench/lean-failure-profile/interval-continuation/README.md)
now compiles against the retained4.9API. It defers proof-tree leaves until a
closing callback needs them; it does not hook original tactics or reject
requests. Native behavior/accepted-set and performance qualification remain
unexecuted,so no reliable early-failure mechanism is claimed.
The code-verification/math workloads and all four paper RQs remain open.

CPU oracle source/data are frozen baselines and must not be optimized or
extended. Old narrow GPU/kernel branches and all raw/failure records remain;
[Evaluation](evaluation.md) owns scientific result scope.
The exact previous491-line implementation record is preserved in the
[dated archive](tmp/bootstrap/step-0012-20261025T0735-engine/implementation-history-through-20261025T0815.md.gz).
