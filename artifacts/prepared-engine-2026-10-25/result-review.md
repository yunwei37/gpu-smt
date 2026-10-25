# Import-parent result review (root self-review)

Observed 2026-10-25 UTC. This is implementation qualification for the fourth
continuing engine direction; no new paper RQ, novelty or performance result.

## Evidence

- Engine implementation commit: 34225c194da290292ca5ab7b3408c84b20f9cb26.
- Actual engine CI40184524032 succeeds, Rust job121142379094 and real native
  job121142379186. Retained native log: ci-34225c1-native.log.gz.
- Both native tests execute (2passed,0ignored) against stock Lean4.18 and
  official REPL commit2f0a3cb876b045cc0fe550ca3a625bc479816739.
- Same import parent remains live while each candidate child retires.
  The controls compare raw JSON with fresh native responses, including
  acceptance/rejection/admission, independent declarations, actual UVTimer/
  Promise, changed imports, timeout and reuse after timeout. Engine shutdown
  leaves none of the recorded native parent/child PIDs live.
- Local fmt,Clippy,27 non-native tests,API docs and CLI help pass. The two
  native tests are explicitly skipped locally to preserve the active original
  native population collection; they execute in dedicated native CI.
- C compilation with the real SDK headers and libuv hook passes.
- The core OSS documentation has45checked relative links, all target paths
  present (anchor contents/external URL availability were not audited here).

## Failure lineage and mechanism

The default REPL executable facet lacked an embedding archive. Building the
upstream static facet exposed its main-symbol collision, corrected in a private
archive without editing upstream source. The system C/SDK libc mixture required
upstream-supported LEAN_CC and the matching SDK runtime library directory.

The first executable backend still fell back: native import construction needs
an ordinary task manager for promises. Joining it did not stop the separate
global libuv threads. For audited synchronous-import contexts, their initializer
is deferred until disposable candidate children; the parent is checked before
forking. Two remaining high-numbered pipe FDs came through the launch context:
closing nonstandard inherited channels at C main entry, before any Lean resource
is initialized, makes the pinned native engagement checks pass. Imported-resource
checks are still enforced. A successful native fallback was never reported as
prepared-parent engagement.

## Limits and next execution

These controls do not prove arbitrary FFI safe, nor qualify a Mathlib context.
Imports must be deterministic/audited and must not use external asynchronous
services in the parent. Source IO depending on process identity/stdin is outside
the context contract. Fresh execution stays the default; failures/mismatches
fall back using the remaining original timeout.

RSS counts shared COW pages in each process; sharing needs separate PSS evidence.
Preparation, branches, queueing, fallback, timeout, retirement and shared-parent
shutdown remain charged. No speedup, useful 48GiB throughput gain, multi-node
scaling or workload-layer novelty is established here.

The existing original7808 three-cell native scheduling group stays alive with
its frozen old point. No second local native group has started. Once it retires,
collect it once, then run the prepared42isolated original resource failures and
new-resource native qualification/full pair. New48GiB dynamic admission clocks
must remain separate from old2worker/24GiB-AS clocks.

All changes and this review are performed by the root thread. This is self-review,
not independent audit. Four directions and the user goal remain active.
