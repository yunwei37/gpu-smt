# Implementation: Rust engine and retained research adapters

Updated2026-10-27. All source/build/test work occurs in the retained
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

## Completion delivery

The typed HTTP service and Engine::verify_stream now optionally deliver retired
results in completion order, with original index and explicit Complete/Error
events. Collected APIs keep original order. Both share validation, ranking,
admission, coalescing and first-success logic. Receiver disconnect drops only its
subscriptions; physical cancellation occurs after the last subscriber and stays
owned through native retirement. Buffered event memory enters process RSS.
Internal availability is not client delivery time. This is ordinary service
engineering, not a new verifier algorithm or demonstrated workload speedup.
Actual pinnedLean4.18 stream/raw accepted/rejected controls pass at faa2a0f;
full population and client delivery measurement remain separate requirements.

## Resource contract

New groups:48GiB total actual owned RSS, no per-process AS cap, CPU8–11.
A15second actual legacy-worker observation sees one thread and~one active
core per REPL; next-point capacity starts at four one-core workers, subject
to measured-memory admission. The Rust default learns positive observed
peaks; source-policy predictions can override reservations. Unknown costs
start conservatively. Prediction never proves rejection.

An opt-in TaskMemory<P> Rust policy now learns positive completed-attempt peaks
from same-task siblings, separated by backend/resource context and timeout.
SchedulingPolicy supplies default no-op observe_rss and identity refresh_rss
callbacks; waiting jobs refresh outside engine locks before admission.
TaskInterleave forwards them without changing all/first-success ordering.
No acceptance/rejection is shared. Existing reservations can only increase;
anonymous tasks and unobserved peaks keep the wrapped prediction. Lower-bound
peaks and heterogeneous siblings can still underpredict or overreserve.
History can be explicitly cleared and should be scoped to an engine/workload.
This library mechanism is not active in the frozen full pair; fixture tests
prove causality/composition only, with native memory/throughput qualification
still pending. The executable exposes this optional FIFO-wrapped policy as
--policy task-memory for check/measure/serve,using existing Capture.policy
provenance. Defaults and current frozen capture are unchanged;there is no new
schema,collector,service or native workload claim.
The extended existing pinned-native CI test now executes at81fe7cc:real
retired-attempt feedback matches recorded RSS,same-task forecasts remain
scoped,and an accepted sibling follows native rejection/incompleteness.
All4native test functions pass with0ignored under officialLean4.18/REPL2f0a3cb.
[Exact source/job/log evidence](tmp/build-and-evaluate/step-0072-20261027T044950+0000/experiment-001/result-review.md)
qualifies this small semantic context,not original4.9Mathlib throughput or
full accepted-set equivalence. The active full pair remains unchanged.

Every second actual owned-tree RSS is sampled, including idle preparation
descendants. Concurrent preemptions kill/reap and requeue for an exclusive
attempt. An otherwise idle queue also promotes a forecast that cannot fit
resident headroom to exclusive admission instead of waiting forever.
PreparedRepl evicts its idle parent for this initial admission or resource retry,
runs fresh under the same request deadline,and allows preparation again on
later ordinary work. The a3052a0pinned-native CI case executes this initial
engine-driven eviction path and preserves the raw reference response;it is a
bounded4.18lifecycle contract,not the pending full4.9Mathlib result.
This restores the budget formerly consumed by idle state;
eviction/fallback remain in attempt provenance. That attempt still exceeding the total budget becomes an explicit
resource failure, with all attempt costs retained. Last-subscriber cancellation
waits for backend cleanup; an RL subscriber keeps shared work alive.
Sampling is not a kernel quota and can overshoot between observations.
The backend refuses an inherited finite AS cap rather than silently claiming
the new resource point. No Workspace quota or other Workspace is changed.

The completed three-policy capture retains its original two-worker,
24GiB-AS-per-process,48GiB aggregate point. The later dynamic four-core native
cell completed, but its prepared cell failed with ENOSPC; it is not a complete
throughput pair. All42 historical allocation failures have since completed
exclusive uncapped retries:41 aggregate-budget failures and one timeout,
with no accepted result. [Current results](evaluation.md) keep these resource
points separate. The48 interval_cases import/prototype repair has also completed, with all48
timeouts on each side and no early-failure coverage. The first original lean-mlir module has now completed file/stdin/native-profile
execution with equal successful responses; its42 trace threads are not measured
CPU utilization or an Amdahl partition.
A [new same-version full native/Mathlib-derived pair](../artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/README.md)
completes both7,808-source cells at frozen1f38be7with status/accepted-set
equality. Other response fields match after accounting for omitted empty ast:[]
in7,660prepared replies;raw-byte/AST compatibility is limited.
The full population records14single-thread preparations of5,545modules,
13evictions and62fresh-fallback event rows,not one eternal Mathlib load.
Whole-cell1.24028x is a descriptive component observation,not novel reuse or
strongest warm-service superiority. Original/tmp streams and all failures are
committed losslessly;sampled peaks overshoot48GiB,not a hard RSS quota.
All15,736recorded PID/birth pairs and the controller have retired.

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

Full Mathlib/native qualification of import preparation/COW, sufficient
failure detectors, source memory/time models, multi-node execution and a valid
complete throughput pair at the dynamic resource point remain open.
PreparedState/FailureDetector are extension contracts; no active rejection
path or COW performance is implied by their definitions.

Optional source diagnostics now retain per-attempt full raw stderr files via
the configured backend/CLI, linked by PID/birth in attempt events; the normal
response remains a labelled64KiB tail. Log setup/I/O errors are operational,
flush/cleanup costs stay in the attempt, no default file is created. This
supports later complete phase attribution; it is not proof/profile completion
or an active failure detector.
PinnedLean4.18 native file/logging accepted/rejected controls execute successfully
at d169813, separately from the pending original workloads.

The source CLI backend now accepts explicitly declared upstream arguments via
NativeLean::with_args and repeated --lean-arg. Defaults remain unchanged;
nonempty argv partitions cache identity. Process/CLI transport tests pass, and
same-argv pinned-Lean4.18 native differential cases execute successfully in
existing CI for source25debfc.
This preserves lean-mlir upstream --tstack=400000. The optional source-file
backend/CLI now verifies original file bytes before invoking that exact path,
scopes identity by file path and shares existing resource/retirement handling.
Pinned-Lean4.18 original-file native differential cases execute successfully
at ad7ecdc. The first nightly original-file/stdin/profile module now returns equal native
success; full workload scope and acceleration remain open.

A [separate interval-continuation prototype](../bench/lean-failure-profile/interval-continuation/README.md)
now compiles against the retained4.9API. It defers proof-tree leaves until a
closing callback needs them; it does not hook original tactics or reject
requests. Nine small native/prototype paired controls execute with matching status.
Original48 variants have native grammar and exact-edit validation.
The first-stage IntervalMap permits open survivors and leaves later suffix
stages outside the per-leaf callback. All48sources/116calls parse. The first
cohort attempt had a missing import path, so its48 fast failures are invalid.
With both Map and Continuation paths restored,22 actual control sources
match their expected native/prototype statuses. Both complete48 comparison
cells still return48timeouts; no reliable early failure is established.
[Implementation](../artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/first-stage-map/README.md),
[actual controls and repair](../artifacts/hotspot-mechanisms-2026-10-25/interval48-import-repair-20261026T162128Z/README.md).
Native left-associative
stage accumulation and nested continuations differ, so failed speculative leaves
do not yet constitute a reliable early-failure witness.
The existing simp_all observer has now run on the original23 sources.
Eight repeated-outer-call cases and six repeated-inner-round cases account
for the prior14 short-call sources. Three instrumented runs crash at runtime
and20 time out; the observer is not transparent on this cohort and establishes
no failure certificate. Its action-completion flag is not qualified by the
successful controls. [Actual phase evidence](../artifacts/hotspot-mechanisms-2026-10-25/original71-native-20261026T125951Z/simp23-analysis/README.md).
The source frontend now requires a recognized native JSON error to classify
a nonzero exit as rejection; otherwise it reports a backend fault and retains
the raw response. [Observed-response regression and scope](../artifacts/engine-lifecycle-2026-10-26/native-runtime-classification/README.md).
The active capture continues using its original executable; the fix applies
to subsequent builds.

The pinned4.27source also shows that verifyBVExpr rebuilds bitblast/CNF and
verifyCert parses LRAT inside the enclosing certificate-check reflection.
[Source evidence and uncompiled contract draft](../artifacts/lean-code-verification-2026-10-25/shared-cnf-contract-20261027/README.md)
prepare a possible within-proof shared closed-CNF declaration with exact native
correspondence and unchanged certificate checking.
[Actual pinned4.27contract controls](../artifacts/lean-code-verification-2026-10-25/shared-cnf-controls-20261027/README.md)
now compile the generic bridge,pass5Boolean controls/valid certificate proof
and reject wrong correspondence/invalid-certificate proof. Stock native
reflection retains its compiler/interpreter trust basis.
The [explicit opt-in frontend](../bench/lean-bv-shared-cnf/README.md) now compiles
and executes direct/public/backtracking development proofs plus SAT rejection.
It evaluates one closed CNF declaration for the existing solver and references
that declaration in unchanged native certificate checking. Core/public/reference
false controls return the same counterexample body. Unsafe meta evaluation
does not replace the checked logical witness. The engine/default tactic is
unchanged;physical value reuse and complete-module performance remain unmeasured.
Sequential LRAT formula updates constrain batching;their dependency width and
the actual stage-cost split are unknown. Ordinary sharing alone is not novelty.

The code-verification/math workloads and all four paper RQs remain open.

CPU oracle source/data are frozen baselines and must not be optimized or
extended. Old narrow GPU/kernel branches and all raw/failure records remain;
[Evaluation](evaluation.md) owns scientific result scope.
The exact previous491-line implementation record is preserved in the
[dated archive](tmp/bootstrap/step-0012-20261025T0735-engine/implementation-history-through-20261025T0815.md.gz).
