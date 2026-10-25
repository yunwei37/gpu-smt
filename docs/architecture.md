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
| SchedulingPolicy | Candidate ranking; predictions never prove rejection |
| ResourceMonitor | Actual owned-tree RSS and PID/birth identity; observable errors |
| AdmissionPolicy | Joint CPU capacity and RSS plus unconsumed predicted growth |
| ResultCache | Exact context/source/options keys, no reusable operational failures |
| FailureDetector | Unknown falls through; rejection requires validated sufficient witness |
| PreparedState | Backend-owned safe preparation/branch boundary, no arbitrary threaded fork |

## Resource layer

The next resource point uses48GiB aggregate actual RSS, no per-worker address
space cap, CPU8–11. Concurrency derives from measured active CPU per worker.
Unknown-memory jobs start conservatively; observed context peaks guide future
admission. Predictions are reservations, not a hard memory guarantee.

Every second the Rust watchdog samples registered owned trees only. Kernel
start ticks prevent signalling an unrelated reused PID. On excess preempt the
largest active owned process, reap its group and requeue its candidate for an
exclusive attempt after other jobs retire. A solo attempt exceeding48GiB is
resource failure, not logical rejection or infinite retry. Queueing/retries/
cleanup enter complete latency and attempt history. No other Workspace changes.

RSS counts shared COW pages per process as requested; physical-sharing claims
need separate PSS. A1s sampled watchdog can overshoot between observations;
it is not a kernel quota.

The optional PreparedRepl backend uses an engine-owned Lean+C import parent:
only parsed imports execute there with the normal task manager, which is joined
and finalized before forking. For modern SDKs, global libuv services are
constructed only in disposable children; the prepared context requires audited
synchronous imports. Each candidate runs in
a disposable OS child, whose connection is retired only after native waitpid.
The parent remains in total owned RSS. Different imports and preparation faults
use the original fresh backend within the remaining request timeout.
Pinned Lean4.18 native differential/lifecycle CI passes for the declared context.
Full Mathlib qualification remains open; this is not a generic safe fork argument
for arbitrary FFI. The default is fresh processes.
Independently loaded workers must not be called one Mathlib load. Multi-node
transport/ownership is extensible, not measured scaling.

## Workload layer

Deduplicate only exact backend/environment/header/source/options/timeout keys.
No whitespace normalization or prefix/certificate reuse. Each caller keeps its
identity and provenance; a cache hit is not a fresh zero-time proof.

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
be silently presented as full compatibility. The healthy old7808 capture
keeps its frozen source and resource point; new-rule data are separate.

## Layout and remaining evidence

- crates/: engine contracts, runtime, backend and service.
- crates/*/tests/: unit/contract/subprocess/differential tests.
- examples/: reproducible library/HTTP examples, no invented performance.
- artifacts/, results/, bench/, tools/: retained research data and experiments.
- docs/paper/: current manuscript.

Full Mathlib COW qualification, real native new-resource parity,42isolated reruns, full throughput
pairs and multi-node measurements remain separately tracked. Tests/CI do not
prove a systems contribution or venue acceptance.
