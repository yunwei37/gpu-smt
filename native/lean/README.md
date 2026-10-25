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
a full isolation proof, or a throughput result. The live original collection
keeps its old settings. Real Mathlib/resource/full-pair qualification follows
only after that sole group retires, with the new resource point reported
separately.

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
