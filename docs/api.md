# Engine API0.1

Rust documentation is generated with cargo doc --workspace --no-deps.
The API is experimental; backward compatibility is an engineering goal, not
an assertion that the current prototype is production-stable.

## Library interfaces

- gpu-smt-core: Candidate, Batch, Mode, Outcome, Status, Verification,
  Attempt, Execution, exact CacheKey and extension traits.
- gpu-smt-engine: Engine, Config and built-in FIFO/source-size policies,
  exact cache, measured-headroom admission and Linux /proc monitor.
- gpu-smt-lean: fresh stock REPL backend, optional PreparedRepl and strict classifier.
- gpu-smt-server: embeddable Axum router and gpu-smt executable.

Backend/policy/monitor/admission/cache are injected at Engine::new.
PreparedState and FailureDetector define future native-state extensions;
the import-parent implementation is a separate optional VerificationBackend.
An actual rejection detector is not implemented. A trait is not an acceleration result.

## HTTP

POST/v1/verify accepts the typed Batch JSON contract. Results retain original
order, caller IDs, native JSON, final status, attempt history, complete elapsed
time and cache/coalescing provenance. all mode executes every subscriber;
first_success requires task_id and cancels only after a checked same-task win.

POST/check accepts snippets(id,code), timeout seconds, reuse, debug=false,
infotree=null. POST/verify and /one_pass_verify_batch accept codes with
custom_id and code or proof, timeout, disable_cache and infotree_type=null.
Core response fields follow Kimina: results containing id/custom_id, native
response, time and optional operational error. Debug/infotree extensions
return an explicit error. Authentication and persistent remote env handles
are not implemented; this is a local interface, not a public production service.

Fresh native execution means every independent source includes its imports.
There is no implicit persistent caller state. Native env fields are retained
as output provenance, not reusable handles in a remote process.
reuse=false/disable_cache=true bypass both completed and in-flight reuse.

The classifier separates admissions from accepted proofs and operational
timeouts/resource exhaustion from logical rejection. Native warning/message
payloads remain available. Compatibility tests cover core shapes; they do
not establish compatibility with every optional Kimina feature.

## Memory, CPU and lifecycle

Config takes actual CPU IDs, measured cores_per_worker and aggregate byte
budget. No RLIMIT_AS is installed. Unknown memory starts conservatively;
observed peaks and optional source forecasts guide admission. Shared global
admission covers all HTTP batches using one Engine.

A1s actual RSS watchdog preempts an owned process, waits for backend reaping
and retries that candidate exclusively. A solo attempt exceeding the budget
returns resource_exhausted; concurrent preemptions remain in attempts.
Predictions never reject oversized work without an actual solo execution.
Queueing, retry and retirement are charged. Sampling is not a kernel quota.

Current backend scope is Linux and a cooperative persistent native REPL;
it is not a sandbox for hostile sources that daemonize or escape ownership.
The optional pinned-context import parent uses native process branching, with
explicit context limitations and fallback; it is not a generic arbitrary-FFI
fork contract. A cross-node supervisor remains future work.

## Resource-event recording

The executable writes structured JSON logs to stderr, keeping JSONL results
on stdout. Default resource INFO events preserve1s actual RSS/budget and
registered PID/birth accounting; preemption events identify the interrupted
attempt. Standard RUST_LOG can select other verbosity. Formal captures retain
the complete stderr event stream alongside result/attempt JSON, commands,
environment and outer cold lifecycle. This telemetry is not a hard RSS quota.

The executable binds its calling thread before constructing Tokio, so runtime
and descendant threads inherit the selected CPU mask. Library embedders own
their runtime/thread affinity and must bind before creating it if benchmarking
a fixed hardware domain. A whole-core allocation is an exclusive execution
point; four one-core workers are a distinct throughput point.

Exact-result reuse assumes deterministic native behavior in the pinned
environment. Sources using mutable external state or nondeterministic IO must
request reuse=false; byte identity alone does not prove arbitrary Lean
metaprograms pure. Fresh uncached native differential execution remains the
reference, and resource failures/timeouts are never cached as logical results.

## Measurement API

The server library exposes measurement::Capture and measurement::compare for
saved exact-input comparisons. The CLI measure command captures one Batch
through native retirement; compare reads two saved captures without running
a verifier. See [measurement scope, clocks and parity](benchmarking.md).

## Optional native import parent

Supply --prepared-host and --sysroot together to opt into the matching compiled
Lean+C adapter. The default stays fresh-process. See [native build/lifecycle and
limitations](../native/lean/README.md). Preparation and child checks share the
original request timeout; remaining time is passed to any fresh fallback.
Attempt histories include the parent during active preparation; after readiness
it becomes shared backend-owned state until shutdown. Disposable candidate
children retire before each result. Backend readiness is reported separately
from general resource health.

Full-population Batch bodies can exceed the HTTP framework's default2MiB JSON
cutoff (the original7808body is14,834,061bytes). The local adapter removes that
extractor cutoff; engine resources remain governed by the declared aggregate
RSS/CPU point. This is not an authenticated public deployment or a hard parser
memory quota. CLI measure avoids HTTP when only a local capture is needed.

Attempt.backend_events preserves preparation/fallback reasons independently of
the unmodified native response. Successful fresh fallback cannot hide a refused
prepared context. Resource logs map origin caller ID, execution ID and PID/birth
to active ownership and preemption. Shared/coalesced result histories can repeat
one physical attempt in several caller rows; measurement counters state that
scope explicitly.
