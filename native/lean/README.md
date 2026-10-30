# Native import preparation

This engine-owned adapter builds against an existing pinned stock Lean REPL
project. It is a resource component, not a novelty claim or a replication of
another verifier service.

The C executable owns a single native import parent. It parses the first source imports through Lean with the ordinary task manager,
retains that environment, then finalizes/joins the manager before any fork. It does not execute candidate declarations or tactics.
Modern Lean also starts global libuv services during runtime initialization.
For audited synchronous-import contexts, the builder detects that initializer
in the actual SDK archive and defers it to each child through a link-time hook.
The real SDK services are initialized in each disposable child before candidate
commands. Parent imports must not use libuv or external asynchronous resources.
A one-thread and file-descriptor check at the branch point still refuses
observable initialization residue before opening the internal Unix socket.

The host accepts only standard input/output/error as inherited channels and
closes other launcher descriptors before Lean initialization. Descriptors
created during native imports remain subject to the branch-point check.

Rust owns CPU/memory admission and creates one connection per admitted attempt.
The parent forks a disposable child, which receives its assigned CPU mask and
the original complete source. The child re-parses the import boundary through
Lean and executes the remaining commands with the original source context.
Different import bytes return to the original fresh backend. No candidate's
terminal environment is reused by another candidate.

The parent retains the response connection until waitpid completes. Rust pays
for that retirement before releasing the CPU lease or returning a result.
Timeout/cancellation kills the owned child group; the parent survives.
Preparation, connection, fallback, remaining timeout and shutdown are charged.

The parent waits for listener/control-descriptor readiness and lifecycle signals
with ppoll,without a periodic poll timer. SIGCHLD/SIGTERM/SIGINT remain blocked
between reap/check and the atomic wait,then are enabled by its temporary mask.
This prevents a signal arriving in that gap from being lost. Handlers are
checked/reinstalled after audited import initialization. Each forked child
restores the launcher's original signal mask before native runtime services;
the parent's wait mask must not escape into candidate execution.
This uses the [ordinary ppoll contract](https://man7.org/linux/man-pages/man2/poll.2.html),
not a proof timeout or a new event service. Native CI compares the actual
child's SigBlk output with fresh Lean and refuses fresh-fallback agreement.
Removing periodic waiting is not a measured whole-workload speedup. The
ongoing13d4606resource pair keeps its old compiled host and cannot measure
this later source change.

A memory-preempted candidate's exclusive retry first retires the idle import
parent, then uses the unchanged fresh native backend. Otherwise the retained
parent's summed RSS would reduce the memory available to that supposedly solo
retry. The operation has no new AS cap, timeout or acceptance rule; parent
teardown consumes the existing request deadline and its eviction is recorded.
Ordinary work may prepare a new parent afterwards.

## Build and use

From this repository, with the native project already built:

    python3 native/lean/build.py \
      --project /absolute/path/to/pinned-repl \
      --sysroot /absolute/path/to/matching-lean-sdk \
      --out /tmp/a-new-prepared-host-build

Then, from that native project:

    lake env /absolute/path/gpu-smt measure \
      --repl /absolute/path/to/stock-repl \
      --project /absolute/path/to/pinned-repl \
      --environment immutable-toolchain-project-pin \
      --prepared-host /tmp/a-new-prepared-host-build/prepared-host \
      --sysroot /absolute/path/to/matching-lean-sdk \
      --cpus 8,9,10,11 --worker-cores 1 --memory-gib 48 \
      < population.json > capture.json 2> resources.jsonl

Without the two prepared options, the default backend stays fresh-process.
The builder uses Python, the pinned SDK/Lake, a system C compiler and binutils.
The SDK bundles a minimal C sysroot without the required POSIX headers.
The builder uses the upstream-supported LEAN_CC override (existing value, or cc)
for both C compilation and linking, preserving SDK runtime/library flags and
the SDK C++ runtime directory. This
avoids mixing host glibc objects with a different bundled libc at link time. It asks the
pinned dependency for its REPL:static library facet, then renames only the
upstream executable main symbol in a private archive to avoid the embedding
entry-point collision. The dependency source/archive stay unchanged; it
does not download dependencies or change a running binary.
CI builds this adapter against the pinned official Lean 4.18 REPL and checks
native payloads, declaration isolation, import-mismatch fallback, timeout,
surviving prepared state and final process retirement.

## Scope and limits

The prepared context must have deterministic audited imports. Single-thread
and descriptor checks do not prove arbitrary imported FFI, hidden global state,
external nondeterminism or allocator behavior safe for process cloning.
Candidates that depend on arbitrary stdin/process identities or inherited
external resources are outside this declared prepared-context contract.
The default fresh backend remains available.

The initial implementation prepares parsed imports only, not arbitrary public
header commands, search indices, candidate proof prefixes or certificates.
It does not resurrect the closed E038 runtime/reference-count optimization.
Shared COW pages count in each process's RSS under the user's aggregate-RSS
contract; lower physical memory needs separate PSS measurement.

Core Init controls in CI are not Mathlib whole-population qualification,
a full isolation proof, or a throughput result.
[Existing native Mathlib child controls](../../artifacts/mathlib-import-preparation-2026-10-25/child-qualification-001/result-review.md)
are complete at their declared development scope. The
[corrected warm/resource comparison](../../bench/lean-warm-resource/README.md)
owns full-population/resource status and its limitations. Every active
collection retains its frozen source/settings;later source repairs cannot be
credited to an earlier native timing result.

The adapter uses the stock REPL's public frontend and diagnostic serializers:
[frontend](https://github.com/leanprover-community/repl/blob/2f0a3cb876b045cc0fe550ca3a625bc479816739/REPL/Frontend.lean)
and [response construction](https://github.com/leanprover-community/repl/blob/2f0a3cb876b045cc0fe550ca3a625bc479816739/REPL/Main.lean).
Those dependencies retain their original copyright/license.

Native promise allocation requires a task manager in the pinned runtime
([upstream implementation](https://github.com/leanprover/lean4/blob/v4.18.0/src/runtime/object.cpp)).
The parent therefore prepares with the normal manager and joins/finalizes it
before inspecting the branch point. Those checks still do not certify arbitrary
FFI. Failed preparation and fresh fallback remain in each attempt's backend
events even when the final native response is accepted.

## Pinned native qualification

Commit e2e54b6ebfb1907af07c422de80d59c0dcd04aef passes the actual
[Lean4.18 native CI](https://github.com/yunwei37/gpu-smt/actions/runs/40185069274).
The tests compare raw native responses for acceptance, rejection and admitted
proofs, check declaration isolation/redefinition, exercise real Timer/Promise
services, force import-mismatch fallback and timeout, then confirm parent reuse
and complete final retirement. A two-core batch also observes two actually live
candidate children under the same parent, with reuse disabled and no fresh
fallback. Engagement requires both registered import parent
and candidate child, plus the live parent after candidate retirement.
Successful fresh fallback alone cannot satisfy that contract.

[Retained result and self-review](../../artifacts/prepared-engine-2026-10-25/result-review.md)
separate this fixed-context qualification from pending Mathlib/resource/throughput
measurements. Earlier failures and their raw CI logs remain in the same directory.


Preparation fails when the native header/import MessageLog contains errors.
The ready handshake includes the actual environment's imported_modules count
and header_errors=false; the Rust adapter requires this metadata from a matching
host. Missing/failed preparation uses the original fresh backend. A count is
import readiness evidence, not proof that arbitrary FFI is safe to fork.

The retained Lean4.9 Mathlib/Aesop import-only preparation loads5545modules,
observes one thread/no children,and retires on stdin EOF. That initial point
executes no candidate and opens no branch connection. The linked later child
controls supply actual differential/concurrency evidence at their limited
scope;neither point establishes whole-population performance.


## Match native compilation as well as the toolchain

For an explicitly configured native context,the import parent honors
LEAN_SERVER_NATIVE_DYNLIB using Lean.loadDynlib before parsing/importing.
The ready context records native_library (null by default). A load failure
prevents readiness; existing one-thread/descriptor checks still run afterward.
Dynamic library initializers/FFI need the same context-specific audit as imports.
Use the identical effective library in the fresh fallback and warm baseline;
a stock REPL without this environment-variable support must be configured
through its own supported loading path before comparing results.
The retained4.9warm-capable REPL supports this variable. No library is selected
by default,and this setting is part of the immutable environment identity.

Historical Kiminaoff loaded nativeMathlib through a disabled counterexample
wrapper. Omitting those native symbols in an engine comparison changes the
execution mechanism even though source/toolchain match. The corrected resource
comparison directly loads that existing ordinary Mathlib library in both
backends,without the counterexample wrapper or external arithmetic oracle.
This is baseline parity,not a new contribution or oracle optimization.

## Ordinary-failure transition component

The separate [opt-in Lean4.9 transition primitive](failure-replay/README.md)
captures and restores caller-qualified ordinary failures with full native
post-state and upstream action heartbeat accounting. It is not used by this
import parent, stock adapters or the service. Native controls are distinct from
Mathlib population opportunity, cross-candidate qualification and performance.
