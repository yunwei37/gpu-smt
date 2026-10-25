# Step0013 — native import preparation in the Rust engine

Phase: BUILD_AND_EVALUATE. Root-only implementation and self-review, no independent audit. Previous turn produced executable Rust engine/measurement changes and exact-source evidence; it was progress. Current retained full7808 PID283334 is verified live in /proc, state S, birth tick134434505, with no terminal file. No restart or second native collection.

## Current dependency result — 2026-10-25 10:35 UTC

Implementation commit e2e54b6 passes engine CI40185069274, including both actual
native differential/lifecycle tests and observed concurrent native children.
Rust/benchmark-smoke CI also succeeds.
[Result/self-review](../../../../artifacts/prepared-engine-2026-10-25/result-review.md)
is the current evidence boundary. The chronological build/failure notes below
retain earlier versions and do not override the terminal result. Parent import
preparation now uses the normal joined task manager and deferred child libuv,
not the earlier zero-manager version. Full Mathlib/resource/throughput evidence
is still open; the existing native collection remains authoritative and active.

## EXPERIMENT_GATE

Entry: read current user-instruction.md, questions-for-author.md, native runtime/old prepared sources and fixed paper RQs. User priority is reusable engine, all four continuing directions, no delegation, aggregate48GiB/new dynamic point after the live group; no CPUoracle or E038 optimization. Selected RQ2: Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?

This node is dependency implementation for the future complete RQ2/RQ3 measurement, not a standalone admitted paper experiment. Wrote native/lean/GpuSmtPrepared.lean and prepared_host.c: parent prepares only parsed imports with a zero-worker runtime; children execute original source commands in their own process. Original REPL frontend/serializer functions are called, not reimplemented numerically. Rust PreparedRepl owns lazy preparation, assigned affinity, active registration, native-parent promotion to idle owned state, child retirement, timeout/cancellation and fresh fallback. Mutex covers preparation/handle lookup only, never candidate solve.

C compilation against the actual configured4.9SDK headers passes warnings-as-errors. First attempt using source-only headers failed due absent generated config.h; retained. First Rust check failed E0505/E0503/E0499; fixed lexical future scopes; no native execution occurred. Successful checks and raw follow-ups are in artifacts/prepared-engine-2026-10-25. Current default25tests pass; actual new native integration is reserved for pinned official CI while local research slot remains occupied.

The new explicit prepared CLI options are opt-in. Ordinary fresh behavior remains default. Init/native controls will verify parent/child engagement rather than letting fallback impersonate COW. Full Mathlib matching/resources/throughput remain unresolved. No scientific contract or novelty claim changes.

## WRITE_GATE

Targeted implementation/API/native-build documentation only at this boundary. Paper retains no-COW-qualified/full-result limits until actual nativeCI evidence exists. Full writing/refactoring and milestone review do not meet entry conditions: all four RQs remain open. No iter-refine-ideas invoked.

## REVIEW_GATE

Self-review replaces independent reviewer only because the user expressly prohibits all other agents. Direction: RQ/scientific contract unchanged, resource-only fork is prior technique and does not revive a closed CPU optimization. Efficiency: no full-run duplicate; direct native integration is required to meet the user's engine requirement. Checks are dependency evidence and do not count as a new paper contribution. Current limitations: audited deterministic import context, native FFI fork argument, actual Mathlib qualification, concurrent branch tests, complete native/full resource pairs, source predictor and multi-node remain open. Next action is actual pinned-native CI, fix real defects, then return to the full native/resource experiment after the sole old group retires. Goal remains active with no gate/deadline/closure criterion.

Local final boundary: all6validation commands pass,25tests pass,2real-native
tests are explicitly skipped locally and configured in pinned officialCI.
Raw logs: artifacts/rust-engine-2026-10-25/validation-20261025T092246.
Chost uses actual child-reported birth ticks to prevent PID-reuse confusion;
native wait4 leader high-water supplements admission observations without
replacing aggregateRSS samples. Prepared-state readiness checks actual parent
identity. No standalone performance conclusion. Publish then inspect exact
nativeCI and repair actual source defects forward-only.

Actual first nativeCI failed before glue compilation: default lake build produced no staticREPL archive. RustCI passed. Builder now asks upstream for REPL:static and discovers its archive; raw failingCI log is preserved. No native parity/COW result is claimed. Also bound branch connection to the original timeout, and added unavailable-host fallback/retirement coverage.

Forward repair validated: default upstream executable lacked its static archive,
so the builder now invokes its actual REPL:static facet and discovers output
instead of assuming a library path. Retained fullCI failure shows native tests
were skipped, not passed. Current local validation20261025T092817 has26passing
checks and2explicit native skips; connection cancellation/deadline and missing
host fallback retirement are included. Paper source/PDF compile successfully.
The original capture PID/birth remain live; projectPVC has1.194GiB available,
all native targets stay in OS temp, and no additional native collection starts.

Second actual nativeCI builds the static dependency and all Lean/C glue, then
fails link because upstream REPL.Main also exports executable main. Raw linker
log retained. Builder now renames only upstream main in a private archive via
binutils; dependency source/original archive stay untouched, no duplicate-symbol
errors are suppressed. This is a build repair, not a native passing result.
Prepared original7808all/first-success Batch inputs are now materialized with
actual task metadata/source validation, unchanged300s/reuse=false and allNone
failures retained. No additional native collection started.

Prepared full input measures14,834,061UTF8JSON bytes. A real Axum request
regression reproduced default413rejection before engine scheduling at2MiB.
Removed the framework extractor cutoff for the authorized local engine API,
retaining the existing aggregateRSS/CPU contract. The before-failure log is
preserved; this fixes actual full-batch transport, not a performance result.

The SDK bundled compiler uses a minimal sysroot lacking dirent.h; that failed
attempt is retained. Upstream Leanc explicitly supports LEAN_CC, clearing bundled
internal sysroot flags while preserving runtime/library flags. Builder now uses
one system compiler for C and linking through that supported interface. Native
OS glue requires full POSIX headers; no glibc shim, symbol stub or suppressed
link error enters the real backend. A separate non-verifier ABI-control stub
is used only to check link flags locally, never executed as Lean or counted as
a native result. Real pinned-native integration still decides qualification.

Forward ABI repair complete locally: upstream-supported LEAN_CC for both C and
link plus the actual SDK C++ library directory passes a full ABI link control.
The control stub source is retained and cannot be used as a native proof result.
Latest27localchecks/format/Clippy/docs/help pass with2localnative skips
(validation20261025T093746). LargeHTTPregression now passes after413was reproduced.
Actual realLean nativeCI must run on the new head; all failures remain explicit.

ActualCI on12ed2f8 builds all real Lean/C glue successfully and runs both native
tests. Fresh native raw parity passes; prepared-parent engagement fails its
surviving-parent assertion, so fallback is not misreported as COW success.
Added retained backend lifecycle events/failed-preparation stderr and explicit
candidate-origin/execution/PID/birth resource mapping. Runtime primary source
object.cpp v4.18 shows native promises require g_task_manager. Preparing with
a zero manager is therefore unsafe for stock environment construction; imports
now use the normal manager and finalize/join it before the same one-thread/FD
branch checks. This is a runtime initialization repair, with arbitraryFFI
limitations unchanged. Next actualCI must validate engagement and isolation.

Repaired source passes all6localvalidation commands and27tests
(validation20261025T095251);2realnativechecks remain explicitly skipped locally
and run in actualCI. NewBackendEvent is optional on old captured attempts and
preserves fallback observations independently of native payloads. Resource
events associate origin/execution/PID/birth; counter scope is per-caller history,
with coalesced histories explicitly not counted as distinct physical work.
This boundary needs fresh real nativeCI; no Mathlib/performance result claimed.

Actualc6b1cf8CI records preparation refusal: threads=3 extra_fds=10 even after
task-manager join. Primary Lean4.18runtime source identifies unconditional libuv
service threads in initialize_libuv, with no matching runtime shutdown API.
The optional import-only context now defers that specific initializer until
each disposable child; builder discovers its symbol in the pinned leanrt archive.
This implements the requested native branch boundary, not a generic safe fork
of existing UV services. Prepared imports must be audited synchronous code.
The real native test adds a libuv Timer/Promise response against fresh native,
so an inert or disabled child service cannot pass as engagement. Original
one-thread/FD refusal remains; no guard was weakened. No new local collection.

Conditional libuv constructor deferral is compiled with warnings-as-errors.
ActualSDK runtime archive symbol discovery chooses the hook; pre-libuvSDKs do
not acquire a fake service. Real Timer/Promise source is compared against fresh
native under matching imports. Local20261025T100417 is fully successful
(27tests,2native skips). Publish the repaired constructor and inspect actualCI;
arbitrary asynchronous import initializers remain outside declared context.

Actual2f926e0CI confirms service deferral reaches one parent thread, while two
descriptors remain; guard correctly refuses and raw fresh fallback stays valid.
No nativeCOW result claimed. Added descriptor type/flags/target metadata only
on preparation refusal to identify those actual owned descriptors before
changing lifecycle handling. The one-thread/FD check remains unchanged. CI
failures and all fallback reasons remain retained; no speculative guard removal.

149f8b7CI identifies the remaining descriptors as high-numbered read/write
launcher pipes142/145, not a live native thread. The executable protocol accepts
only stdin/stdout/stderr, so it now closes unexpected inherited descriptors at
main entry, before any Lean runtime/import resource exists. It never sweeps
post-initialization Lean descriptors; the subsequent guard still refuses any
native/import residue. Successful preparation now retains its ready metadata
(parentPID/threadcount/one preparation/closed inherited count/UVdeferral) as
BackendEvent rather than making engagement depend on fallback success.

Local inherited-descriptor repair validation: artifacts/rust-engine-2026-10-25/validation-20261025T102154/validation.json; formatting, Clippy, 27 non-native tests, API docs and CLI help pass. Two native tests remain explicitly ignored locally to preserve the existing collection; engagement still requires the new exact-head native CI. C compilation with the optional libuv hook passes. No throughput result follows from these checks.

## Native contract result (34225c1)

Actual engine CI40184524032 is successful: Rust checks plus both real native tests (2passed,0ignored). Pinned-parent engagement, raw native decisions, isolation, real async Timer/Promise, timeout/remaining fallback and final retirement pass. See artifacts/prepared-engine-2026-10-25/result-review.md and retained raw CI log. This closes this implementation-contract repair only; Mathlib/resource/throughput and all paper RQs remain open. No second local collection or delegated execution. Goal stays active. OSS native-test commands are split so a fresh-only invocation does not require optional prepared-host environment variables.

The next dependency check extends actual native CI to two eligible cores and observes two simultaneously live child processes under the same prepared parent. Equal-source reuse is disabled, so coalescing cannot impersonate concurrency. No timing ratio is asserted. This check remains locally ignored while the existing native group runs; its exact-head CI result will be retained separately from the already successful sequential/timeout contract.

## Latest terminal dependency result — e2e54b6

Engine CI40185069274 and benchmark-smoke40185069246 succeed. Both actual native
tests execute/pass with0ignored. The expanded two-core control directly
observes2simultaneously live disposable children under one import parent,
with reuse=false and no fresh fallback; native outcomes, retirement, timeout
recovery and final shutdown pass. See retained ci-e2e54b6-final.json/native.log.gz
and result-review.md. The preceding sequential implementation result34225c1
remains valid; this adds actual concurrent engagement, not measured throughput.
Targeted paper update compiles (paper-check-native-qualified); no complete
writing/milestone or independent audit is claimed. Current source/metadata/docs
boundary is complete, while native Mathlib/resource/full pairs remain open.
