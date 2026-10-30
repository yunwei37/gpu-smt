# Engine API0.1

Rust documentation is generated with cargo doc --workspace --no-deps.
The API is experimental; backward compatibility is an engineering goal, not
an assertion that the current prototype is production-stable.

## Library interfaces

- proofserve-core: Candidate, Batch, Mode, Outcome, Status, Verification,
  Attempt, BatchEvent, Execution, exact CacheKey and extension traits.
- proofserve-engine: Engine, Config and built-in FIFO/source-size policies,
  exact cache, composable TaskInterleave<P>, measured-headroom admission
  and Linux /proc monitor.
- proofserve-lean: fresh stock REPL backend, optional PreparedRepl and strict classifier.
- proofserve: embeddable Axum router and proofserve executable.

Backend/policy/monitor/admission/cache are injected at Engine::new.
PreparedState and FailureDetector define future native-state extensions;
the import-parent implementation is a separate optional VerificationBackend.
An actual rejection detector is not implemented. A trait is not an acceleration result.

## Standalone tactic-failure replay skeleton

proofserve-core exports FailureReplayBackend and TacticCompletion; proofserve-engine
exports FailureCache and its opaque FailureInput. This additive experimental
0.1 library API has no CLI/HTTP option. FailureCacheAdapter connects a qualified
FailureCacheVerificationBackend to Engine through the existing VerificationBackend
extension; default construction is off and delegates the original backend.

FailureCacheAdapter::new(backend) allocates no tactic store and does not call
the replay-enabled verification hook. FailureCacheAdapter::enabled(backend)
explicitly opts in for the adapter lifetime; both are passed as the ordinary
backend Arc to Engine::new. BackendFailureCache specifies the bridge's typed
store and supports dynamically dispatched backends with known associated types.
The enabled adapter namespaces its whole-source cache identity, so an older
baseline entry in a shared ResultCache cannot mask the opt-in path.

The backend's verify_with_failure_cache hook runs only after normal admission
and retains the original execution cancellation, CPU/process accounting and
retirement contract. It owns tactic state and must route replayed exceptions
through ordinary backtracking, then perform the remaining source verification.
Candidate.reuse controls whole-source sharing, not this separately enabled
tactic store. Resource-exclusive execution clears retained transitions before
calling the original verify_resource_retry, bypassing replay while the backend
reclaims memory. Engine shutdown awaits active retirement, then the adapter
clears records before delegating native shutdown. Prepared-state reporting and
watchdog interruption are forwarded unchanged.

[Engine pipeline tests](../crates/proofserve-engine/tests/failure_backend.rs) exercise
default-off behavior, dynamic opt-in, separate final decisions after a repeated
ordinary tactic failure, operational exclusions, resource retry/cleanup and
whole-source identity separation. These are simulated API/lifecycle checks,
not a native replay implementation or throughput measurement. Stock Lean
backends cannot opt in because they do not implement the bridge.

The store accepts a concrete backend or dyn FailureReplayBackend with its
associated types specified. Native State is exclusively owned and needs Send,
not Sync; no extra sharing guarantee is inferred. Public integration fixtures
exercise two suspended simulated replays:clear preserves their owned records
but prevents new hits,generation changes require unchanged fallback,and one
consumer's cancellation does not cancel another. These are API/lifetime
contracts,not native state qualification or workload parallel speedup.

The backend defines its exact Key, owned Record, exclusive State and native
Exception types.
replay_input returns a coherent scope/key only for supported, replay-qualified
inputs. Scope includes verifier/environment and process/allocation generation.
The key covers tactic text, goal/local context, options and relevant hidden state
dependencies. Key Hash/Eq/destruction must be nonblocking metadata operations.
An observed canonical goal/context match is insufficient. Records include the
failed state transition and diagnostics/identity/resource effects; whole-source
Outcome and error text are not implicitly converted into entries.

Before original execution, capture returns the private scoped input. remember
uses that captured scope, even if the backend restarts before insertion.
OrdinaryFailure stores a qualified fresh producer's record; NotReplayable covers
returns, unqualified errors and every operational/resource/interrupt case and
invalidates a previous entry for that input. Do not record a replay as a new
native producer.

try_replay returns None on a miss/unsupported input/pre-existing cancellation.
For a record it calls replay_failure after releasing the metadata lock. That
backend revalidates supplied scope/key and live state, cancellation and budget
before committing. Some(exception) means one ordinary-failure transition was
applied, including original action heartbeat accounting. The caller must
propagate that destination-native exception through the original native
failure/backtracking path, never return tactic success or a source verdict.
None leaves observable state/action charges unchanged and requests original
execution. Err is operational: do not turn it into rejection or blindly fall
back on a possibly damaged native state.

clear drops stored records outside the lock, but does not cancel an in-flight
replay or retire native ownership. Retained records consume memory; scope the
store to a backend lifecycle. No automatic eviction/size guarantee is supplied.
The [simulated library example](../examples/README.md#tactic-failure-replay-skeleton)
runs without a verifier. There is no qualified Lean replay implementation or
native performance result yet.

## HTTP

POST/v1/verify accepts the typed Batch JSON contract. Results retain original
order, caller IDs, native JSON, final status, attempt history, complete elapsed
time and cache/coalescing provenance. all mode executes every subscriber;
first_success requires task_id and cancels only after a checked same-task win.
Equal-priority candidates retain original submission order at admission;
forecast latency or executor wake order does not define a new scheduling
policy. CPU/RSS admission and exclusive resource retries still apply.

POST/v1/verify/stream accepts the same typed Batch and returns
application/x-ndjson. It validates IDs/task mode/policy before launching work.
Each completed caller emits a result event with original zero-based index and
the full Verification. Arrival order is completion order; existing collected
routes still return submission order. Successful completion requires a final
complete event with count equal to input size. An error event means incomplete
execution; EOF without complete is not success and missing rows are unknown.

For example:

    {"event":"result","index":1,"verification":{"id":"fast","outcome":{"status":"accepted","response":null,"error":null},"attempts":[],"elapsed_seconds":0.1,"cached":true,"coalesced":false}}
    {"event":"result","index":0,"verification":{"id":"slow","outcome":{"status":"rejected","response":null,"error":null},"attempts":[],"elapsed_seconds":1.0,"cached":true,"coalesced":false}}
    {"event":"complete","count":2}

These are illustrative cached protocol records, not measurements or native proofs.

The library counterpart is Engine::verify_stream and BatchStream::recv/poll_recv.
Dropping the response/receiver cancels its consumer subscription. Only the last
subscriber's disappearance cancels physical work; a separate RL subscriber
retains its check. Owned cancellation and cleanup remain visible to the engine.
Use engine.shutdown at service teardown; disconnect is not a claim that every
owned prepared process has already exited at that instant.

One result per input plus a terminal can buffer, as with collected result
storage; this memory participates in owned RSS. Delivery uses nonblocking sends,
so a slow reader does not delay checked first-success cancellation. This is
bounded by the submitted batch, not a new source quota or unlimited-memory
promise. Cache/coalesced/cancelled rows stay explicit. Serialization/network
delivery time is not included in Verification.elapsed_seconds, which retains
internal batch availability/queue/retry/retirement scope. Measure client arrival
separately; a protocol test is not a native latency/speedup result.

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
payloads remain available. Diagnostic entries must have a known native severity
(trace/info/warning/error) and string data; present message/error fields must
also be strings. Malformed diagnostics return an uncacheable backend_error
with their original JSON, even if an env handle or an earlier valid error is
present. Positions and other uninterpreted native metadata remain unchanged.
Compatibility tests cover core shapes; they do not establish compatibility with
every optional Kimina feature.

Timeout is a cooperative native response budget, not a whole-delivery wall
bound. A single synchronous IO poll can finish late; such a completion is a
timeout even if its timer has not yet been polled again. Fresh REPL completion
means complete native JSON, while source CLI IO includes stdout and natural
process exit. Parsing cannot be interrupted by this check. Queueing, retries,
post-response work and mandatory retirement remain visible in elapsed costs;
a timed-out attempt still pays cleanup. See [deadline scope](architecture.md#cooperative-native-io-deadlines).


## Memory, CPU and lifecycle

The executable handles SIGTERM and SIGINT through engine shutdown before
exiting: admissions stop and active owned attempts retire. serve drains its
HTTP handlers; interrupted check/measure exit nonzero. If verification is
interrupted, measure emits no complete capture; interruption during later output
may leave a partial record, so consumers also check exit status. An idle stdin reader does not require
caller EOF to let the CLI exit. This covers handled signals after runtime
initialization, not SIGKILL or an external process/container crash.
Library/router users still call Engine::shutdown at their own lifecycle boundary.

Config takes actual CPU IDs, measured cores_per_worker and aggregate byte
budget. No RLIMIT_AS is installed. Unknown memory starts conservatively;
observed peaks and optional source forecasts guide admission. Shared global
admission covers all HTTP batches using one Engine.

A1s actual RSS watchdog preempts an owned process, waits for backend reaping
and retries that candidate exclusively. A solo attempt exceeding the budget
returns resource_exhausted; concurrent preemptions remain in attempts.
Predictions never reject oversized work without an actual solo execution.
Queueing, retry and retirement are charged. Sampling is not a kernel quota.

VerificationBackend::verify_resource_retry defaults to verify. Engine invokes
it after peers retire for a resource retry or an initial exclusive request whose
forecast cannot fit idle headroom. Implementations overriding this0.1hook must
not require a preceding failed attempt;the signature/default remain unchanged.
PreparedRepl reclaims its idle parent and runs fresh native verification,
retaining prepared_evicted and fresh_fallback events. The same request deadline
includes teardown;later ordinary requests may prepare again.

When no attempt is active,a below-budget forecast can still exceed remaining
headroom because the engine/prepared parent consumes actual memory. Such work
gets exclusive reclamation,not an indefinite reservation wait or predicted
rejection. Actual measured RSS must still satisfy the admission policy;the
watchdog/CPU budget remains unchanged. Attempt.exclusive does not imply an
earlier failure,and exclusive_headroom records initial forecast/RSS/budget.
Candidate/Execution JSON and source semantics are unchanged.

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
it becomes shared backend-owned state until shutdown or exclusive-resource eviction. Disposable candidate
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


## Batch-aware scheduling

SchedulingPolicy::batch_priorities has a default implementation using the
existing per-source priority. Implementers need not add a method. It returns
one key per candidate; an invalid length is an interface error before any
physical work, not a native rejection. Ranked ties use original input order.

TaskInterleave::new(Fifo) is available as --policy task-interleave. For
first_success it interleaves task groups using their declared IDs; it never
reads future verdicts. A custom wrapped policy supplies within-task ranking,
group-first ordering and RSS forecasts. all-mode uses its wrapped policy
unchanged. There is no per-task permission/resource cap. CPU/RSS admission,
checked cancellation, reuse and paid retirement retain the same contracts.

## RSS observation kinds

Attempt peak_rss_bytes is a conservative maximum of registered-tree samples and
backend supplements. It is not a complete aggregate or kernel tree high-water.
rss_observation backend events record kind,PID,kernel start ticks and bytes.
The fresh backend records birth-matched current leader RSS before retirement;
the prepared backend records the native parent's wait4 leader ru_maxrss.
Leader data exclude a complete descendant/shared-parent total.

The comparison key peak_attempt_observed_rss_bytes states this combined scope.
The older sampled_peak_attempt_rss_bytes remains a legacy alias with the same
value. Old captures without kind events remain untyped; no observation kind is
invented when reading them. Aggregate48GiB enforcement still uses the complete
owned-tree sampler, not these individual supplemental values.


## Measured task-memory policy

TaskMemory::new(Fifo) is selected by --policy task-memory at startup of check,
measure or serve. Default FIFO is unchanged. The choice affects RSS forecasts
only,not ranking,native code,consumer modes or verdicts. No new HTTP field,
Batch/Candidate/Capture schema or native argument is added. Capture.policy
records task-memory;measure starts cold history,while check/serve keep history
for that engine lifetime.

The policy observes positive retired-attempt measured peaks and refreshes
same-task waiting reservations. Backend/resource context and timeout partition
history. No proof result is borrowed. Peaks can be censored and heterogeneous
siblings can overreserve,so existing watchdog/exclusive retry remains required.
Library callers can clear_memory or compose TaskInterleave;the single CLI
task-memory variant wraps FIFO. [Matched execution and limitations](benchmarking.md#measured-same-task-memory-policy)
remain separate from native control semantics and measured performance.

## Stock source frontend

NativeLean is a separate VerificationBackend for the SDK's lean executable.
It sends exact source bytes to lean --json --stdin in the pinned project/import
environment. The same engine admission, watchdog, retry and cancellation apply.
The CLI selects it with --lean PATH instead of --repl PATH; the REPL path remains
unchanged and prepared-host/sysroot are REPL-only. No native memory,trust,heartbeat
or thread override is added; eligible CPU assignments still bound child execution.

NativeLean drains stdout and stderr concurrently. After the compiler exits,
the backend stops remaining members of its owned process group before reaping
the birth-matched leader and completing pipe retirement. A descendant holding
a pipe cannot turn successful compiler exit into an indefinite cleanup wait.
This retains the existing owned-group boundary; it is not containment for a
source that deliberately escapes that group. Retirement is awaited and charged.

NativeLean responses retain exit_code, complete stdout, the labelled stderr tail
and parsed messages. Successful native exit with recognized diagnostics is
accepted; sorry warnings remain incomplete and native errors rejected. Unknown
JSON shapes/non-JSON stdout, signals and transport failures remain operational;
arbitrary source #eval printing therefore may be unsupported. A reported native
INTERNAL PANIC stays a backend error even if JSON error diagnostics preceded
it;raw output is retained and this incomplete execution is not cached as a
completed rejection. Ordinary JSON errors without a runtime panic keep their
existing classification. No environment handle is fabricated. This is native frontend checking, not an imported-axiom
audit. It writes no source,olean or auxiliary output into the original project.

Stdin has its own native diagnostic filename/module context. Sources depending
on their original file path,relative file IO or filesystem effects are not proven
equivalent to invoking lean on their original filename. Run same-context raw CLI
differentials and preserve those differences for each workload. CLI response
envelopes and REPL JSON are different contracts; do not compare their raw payloads
as though they were the same protocol or cache across backend identities.

### Declared source compiler arguments

The default NativeLean struct literals and identity remain unchanged.
NativeLean::with_args(Vec<String>) returns a configured backend;the CLI accepts
repeatable --lean-arg ARG tokens. Each token is forwarded without shell parsing,
before --json --stdin. Nonempty arguments become part of backend identity/cache
scope;an empty vector keeps the default identity. REPL backends do not consume
--lean-arg. Nothing silently adds a compiler or thread option.

For example,the retained lean-mlir root declares --tstack=400000 upstream.
Use --lean /absolute/pinned-sdk/bin/lean --lean-arg --tstack=400000 for the
matching source context,instead of dropping that option or patching source.
Other source-path/stdin limitations above remain. Callers must compare the
same declared argv against raw native execution;argument support is not
proof that the whole project has been measured or that arbitrary modes
produce compatible JSON diagnostics.

### Original source-file context

`NativeLean::with_source_file(path, args)` uses the original file rather than
stdin. The CLI exposes `--source-file FILE` with `--lean`; relative paths are
resolved from the project without canonicalizing away a supplied symlink name.
Before spawning, the file bytes must equal `Candidate.code`. A missing/different
file is a backend error, never a native rejection. The backend creates or edits
no source file and uses the same resource, interruption and retirement path.

The file path and declared argv scope cache identity. As with imported modules,
the caller must keep the pinned source/project immutable during execution and
cache lifetime; this pre-read does not guarantee atomicity against concurrent
file mutation. For baseline measurement use `reuse=false`. Original-file and
stdin contexts remain distinct; qualify them on the actual workload instead of
assuming diagnostic filenames/module names are interchangeable.

### Complete diagnostic stderr

The configured source backend can retain full stderr with
`NativeLean::with_args(args).with_stderr_dir(directory)` or
`NativeLean::with_source_file(path, args).with_stderr_dir(directory)`.
The CLI accepts `--stderr-dir DIR` with `--lean`. The directory must already
exist; no file or directory is added by default. Each actual attempt creates
`native-PID-START_TICKS.stderr` with create-new semantics. Backend events link
the exact file to the attempt's process identity and record transport
completion/error plus bytes read. No candidate ID is used as a filesystem path.

The response retains its labelled64KiB tail, while the file contains the
unmodified complete stream when transport completion succeeds. Writing/flush
and retirement costs enter attempt/lifecycle time. Setup or I/O failure is
operational; partial files and error events remain. Flush is not an fsync or
power-loss guarantee. A transport-complete file after timeout/cancellation can
still contain incomplete phase records: EOF is not a completed proof/profile.

Logging never interprets diagnostic stderr as acceptance. Original strict
classification remains; structured profiler stderr may therefore give an
operational response even when native exit/JSON diagnostics otherwise complete.
Analyze such diagnostic runs from their full raw records, separately from
uninstrumented accepted-set/performance captures. Use `reuse=false` for fresh
measurement; cache/coalesced consumers need not create an independent log.
Logging directory participates in configured identity. Main defaults are unchanged.

## Experimental native transition primitive

The [Lean4.9 component](../native/lean/failure-replay/README.md) is a low-level
dependency for future FailureCacheVerificationBackend implementations. It has
default-off capture/replay and a strict same-retained-input guard. Native finite
controls exercise post-state/exception and action-charge preservation. The
50-cell authored candidate differential also matches complete ordered JSON
diagnostics and native verdict/exit fields, with six forced same-entry hits.
Those controlled hits do not measure workload opportunity.
It is not connected to the stock adapter or Rust service. Pointer identity,
including reader/state layers, does not itself certify mutable/opaque/IO effects,
cross-candidate compatibility or exact timeout parity. The selected-state
population measurement and complete accepted-set differential remain open.
The retained-pointer guard also misses independently created Core contexts;
different source FileMaps prevent cross-source replay through this primitive.
Semantic rebasing is not implemented. Do not describe it as an enabled
cross-candidate goal-state cache or use its restricted scope to rule out one.


## Automatic resource defaults

The Linux CLI discovers its eligible CPU IDs and reduces the default worker
budget to any visible cgroup-v2 ancestor CPU quota (fractional quotas use at
least one worker). The startup RSS budget is 80% of the smaller of current
MemAvailable and remaining visible cgroup-v2 memory capacity. This leaves
headroom and does not change host/container limits. The existing sampled
watchdog and dynamic admission still enforce the selected engine budget.
Sampling may overshoot; this is not a kernel hard quota.

Use --cpus, --worker-cores and --memory-gib only when choosing a specific
resource point. Explicit values retain their existing meaning; CPUs must be
eligible. Original captures keep their original parameters and clocks.
Historical G10 captures retain their explicit12GiB serial point; current
development allocations are in research-plan.md. Automatic service defaults do
not change any frozen capture resource point. Legacy cgroup-v1 controllers are not currently auto-discovered.
