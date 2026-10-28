# Engine architecture

The engine is a Rust workspace independent of historical Python experiments.
Four continuing research directions remain open. Resource primitives are prior
work; novelty must come from measured workload-aware whole-flow savings.

## Layers and dependency direction

    gpu-smt-server (HTTP/CLI, Kimina adapter)
           │
    gpu-smt-engine (queue, admission, ownership, watchdog, preemption)
           │                         │
    gpu-smt-core ←──────────── gpu-smt-lean (native JSON protocol)

Core defines public requests, context identities, verdicts, cancellation and
attempt provenance. Backends never import services; the queue never imports
experiments or the frozen oracle. Initial public APIs are0.1, documented and
versioned; production stability is not asserted.

| Extension | Contract |
|---|---|
| VerificationBackend | Pinned environment identity, native response, full retirement/cancellation |
| SchedulingPolicy | Source/batch ranking, queued RSS refresh and completed-attempt feedback; predictions never prove rejection |
| ResourceMonitor | Actual owned-tree RSS and PID/birth identity; observable errors |
| AdmissionPolicy | Joint CPU capacity and RSS plus unconsumed predicted growth |
| ResultCache | Exact context/source/options keys, no reusable operational failures |
| FailureDetector | Unknown falls through; rejection requires validated sufficient witness |
| PreparedState | Backend-owned safe preparation/branch boundary, no arbitrary threaded fork |

## Resource layer

The current resource point uses48GiB aggregate actual RSS, no per-worker address
space cap, CPU8–11. Concurrency derives from measured active CPU per worker.
Unknown-memory jobs start conservatively; observed context peaks guide future
admission. Predictions are reservations, not a hard memory guarantee.

Every second the Rust watchdog samples registered owned trees only. Kernel
start ticks prevent signalling an unrelated reused PID. On excess preempt the
largest active owned process, reap its group and requeue its candidate for an
exclusive attempt after queued first attempts and active jobs retire. A solo attempt exceeding48GiB is
resource failure, not logical rejection or infinite retry. Queueing/retries/
cleanup enter complete latency and attempt history. No other Workspace changes.

RSS counts shared COW pages per process as requested; physical-sharing claims
need separate PSS. A1s sampled watchdog can overshoot between observations;
it is not a kernel quota.

The CLI installs SIGTERM/SIGINT handling before launching candidates and
awaits engine shutdown at handled termination. HTTP handlers drain; interrupted
JSONL/measurement execution exits nonzero. Admission rechecks fatal/shutdown
state after resource sampling while holding the lease-insertion lock: shutdown
either sees an admitted lease and awaits its retirement, or prevents the lease.
Native retirement is awaited before runtime shutdown, which does not wait on an
idle blocking stdin reader.
This is process lifecycle behavior, not crash/SIGKILL containment.

Fresh and prepared backends preserve a complete native reply received within
the original request budget while awaiting physical retirement. Late replies
remain timeouts; cancellation and malformed retirement remain operational.
Every process is reaped before unregistering. Retirement can extend observed
latency beyond the response deadline and is always charged; this grants no
additional proof execution time and does not hide cleanup costs.


The optional PreparedRepl backend uses an engine-owned Lean+C import parent:
only parsed imports execute there with the normal task manager, which is joined
and finalized before forking. For modern SDKs, global libuv services are
constructed only in disposable children; the prepared context requires audited
synchronous imports. Each candidate runs in
a disposable OS child, whose connection is retired only after native waitpid.
The parent remains in total owned RSS. Different imports and preparation faults
use the original fresh backend within the remaining request timeout.
After an RSS preemption,or an initial forecast that cannot fit idle headroom,
exclusive resource admission retires the idle import parent and uses fresh
native execution. Actual RSS admission and watchdog still apply. Parent teardown
and fallback share its request deadline and appear in attempt provenance.
Later ordinary work can prepare a new parent; ordinary candidate timeout or
consumer cancellation still preserves it. Eviction is a resource mechanism,
not a failure detector or novelty claim.
Pinned Lean4.18 native differential/lifecycle CI passes for the declared context.
Full Mathlib qualification remains open; this is not a generic safe fork argument
for arbitrary FFI. The default is fresh processes.
Independently loaded workers must not be called one Mathlib load. Multi-node
transport/ownership is extensible, not measured scaling.

## Workload layer

Deduplicate only exact backend/environment/header/source/options/timeout keys.
No whitespace normalization or prefix/certificate reuse. Each caller keeps its
identity and provenance; a cache hit is not a fresh zero-time proof.

Within a batch, ranking is evaluated once per candidate, with original-index
tie order. Queue tickets and cache/in-flight sharing disposition are established
before asynchronous forecast/execution tasks can reorder them. Cache hits and
shared subscribers release unused tickets; only physical work waits for CPU/RSS
admission. Resource retries follow the ordinary queue frontier registered at preemption.
They retain policy order within a frontier and stable retry registration order, wait for
all active attempts to retire, and reclaim idle prepared state as before.
A pending retry therefore does not itself block normal CPU/RSS admission.
This avoids repeated mid-batch drain barriers; it does not eliminate the
serial cost of candidates whose actual memory occupies the whole budget.
Preempted peaks are lower bounds, so they do not justify speculative overlap
during the exclusive retry. Each retry closes its current frontier; later batch arrivals wait behind it.
This prevents an endless arrival stream from overtaking an already queued retry,
without claiming a bounded delay for long or memory-constrained native work.
Independent concurrent batches enter the same queue at ticket registration;
this is not a timestamp reconstruction of network arrivals.

TaskInterleave<P> composes with an existing ranking/RSS policy. In first-success
mode it takes one ranked candidate from each task in turn before returning to
the same task. Groups follow their first ranked candidate; order inside each
group follows the wrapped source policy. This is batch-local round-robin, not
a fixed per-task concurrency cap or a continuous-arrival fairness guarantee.
All-mode delegates the wrapped keys unchanged. Ordinary interleaving is prior
technique, not the claimed scientific contribution.

TaskMemory<P> is an opt-in library wrapper for measured same-task memory.
It preserves ranking and refreshes waiting reservations from positive physical-
attempt peaks observed after retirement. Backend/resource context, task ID
and timeout partition history; anonymous tasks receive no shared estimate.
A refresh takes the maximum of existing and learned reservations. TaskInterleave
forwards both callbacks, so either wrapper order remains usable. Callbacks run
outside engine state locks and must remain short; cache hits and additional
coalesced subscribers do not manufacture observations.

History contains no proof outcome: a rejected teacher can have an accepted
sibling. A preempted peak is a lower bound, not a complete demand measurement.
One expensive sibling can overreserve smaller ones, and retained history itself
consumes memory. Scope the wrapper to a workload/engine lifetime or clear_memory.
The default remains unchanged; watchdog, exclusive retry and parent retirement
are still required. Causal fixture tests establish queue refresh/composition,
not native benefit, safe memory prediction or a scientific novelty result.
Pinned4.18native CI now executes feedback/response/retirement controls;
[exact evidence](tmp/build-and-evaluate/step-0072-20261027T044950+0000/experiment-001/result-review.md)
is separate from the [completed original4.9development pair](../artifacts/engine-resource-profile-2026-10-25/task-memory32-20261027T193536Z/result-review.md):
all32rawoutcomes match,with fourfewer retries in a tail-selected cohort.
Representative throughput atop preparedMathlib remains unmeasured.

RL mode produces every candidate outcome. Pass@k cancels siblings only after an
actually checked same-task acceptance. Cancellation is a consumer outcome, never
Lean rejection. In-flight deduplication retains RL subscribers if a pass@k
subscriber cancels. Source cost predictions affect order/admission only.

Failure detectors remain unknown without a sufficient checked witness under
the actual Lean state, including backtracking/fallback. Token patterns, large
branch counts and shorter timeouts do not prove failure.

## Semantic guarantee layer

Keep native responses. Separate accepted, rejected, sorry/incomplete, timeout,
preempted, final resource exhaustion, cancellation and backend faults.
Unknown response shapes and sorry-bearing proofs must never be accepted.
Differential tests compare executed candidates against the same native
binary/environment, with exact accepted IDs, not just counts.

Kimina core/check and legacy/verify shapes and Lean REPL JSON transport are
separate contracts; unsupported infotrees/debug/auth/state handles must not
be silently presented as full compatibility. The completed old7808 scheduling
matrix retains its frozen source/resource point;new-rule data are separate.

## Layout and remaining evidence

- crates/: engine contracts, runtime, backend and service.
- crates/*/tests/: unit/contract/subprocess/differential tests.
- examples/: reproducible library/HTTP examples, no invented performance.
- artifacts/, results/, bench/, tools/: retained research data and experiments.
- docs/paper/: current manuscript.

The earlier native-complete/prepared-ENOSPC pair remains partial. The later
[complete frozen7808resource pair](../artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/result-review.md)
has equal status/accepted sets,with a disclosed emptyAST-envelope difference,
operationalerror-string changes and1.24028x descriptive own-engine ratio.
One historical acceptance still times out across different resource points.
The42solo reruns remain41budgetfailures/1timeout. Broaderartifact/strongestwarm
coverage,representative load-aware results and actual multi-node measurements
remain open. Tests/CI do not prove contribution or venue acceptance.

### Exact historical RSS median

The default admission fallback still uses the upper median of all positive
completed-attempt peak observations (sorted index n/2). Two heaps maintain
that exact value incrementally: insertion is logarithmic and querying requires
no history copy or sort under the admission lock. Storage remains linear in
observations. This changes neither the forecast definition nor the watchdog,
retry, timeout or result semantics; it is resource-layer maintenance without
a measured end-to-end gain claim. A preempted peak remains a lower bound.
