# Engine API0.1

Rust documentation is generated with cargo doc --workspace --no-deps.
The API is experimental; backward compatibility is an engineering goal, not
an assertion that the current prototype is production-stable.

## Library interfaces

- gpu-smt-core: Candidate, Batch, Mode, Outcome, Status, Verification,
  Attempt, Execution, exact CacheKey and extension traits.
- gpu-smt-engine: Engine, Config and built-in FIFO/source-size policies,
  exact cache, measured-headroom admission and Linux /proc monitor.
- gpu-smt-lean: fresh stock REPL subprocess backend and strict classifier.
- gpu-smt-server: embeddable Axum router and gpu-smt executable.

Backend/policy/monitor/admission/cache are injected at Engine::new.
PreparedState and FailureDetector define future native-state extensions;
neither safe COW nor an actual rejection detector is implemented by the
initial runtime. A trait definition is not an acceleration result.

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
A safe COW backend and cross-node supervisor must implement their own native
lifecycle argument before replacing this transparent fresh-process fallback.
