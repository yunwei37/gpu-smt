# Step0020 — truthful native import readiness and actual Mathlib preparation

## EXPERIMENT_GATE

Previous19step completed native860header parsing and timeout/source controls;
the802external prerequisite build and sole original7808capture remain running.
Root-only implementation,48GiB combined sampled RSS,no fixed AS cap/new capture.

The own Lean create wrapper currently retains processHeader's error MessageLog
and returns Root; C only checks non-null Root/one-thread/no-extra-FD before ready.
Therefore a failed actual import can be misreported as prepared readiness.
Fix that fault locally: errors become failed preparation with existing fresh
fallback; expose actual Environment.header.moduleNames size and error flag.
No candidate-output or inference-algorithm change is intended.

Test exact pinned invalid-header fallback and positive real module metadata in
native CI. Build own glue against existing unchanged4.9REPL objects, then only
initialize Mathlib/Aesop imports and retire parent without opening its branch
socket. This is import-only dependency qualification,no candidate proof executed,
not a second native/full collection or full COW parity/performance result.
Observe combined original collection,other own setup,and this controller each
second; pressure aborts this new setup,not the healthy old owners.

## WRITE_GATE

Document truthful readiness and the actual tested context. Preserve all failed
native setup attempts. No whole-Mathlib COW/throughput claim without child tests.
Fixed Narrative/fourRQs unchanged;no full-writing/milestone pass.

## REVIEW_GATE

Root self-review only: successful bytes/import context,module count,failed
import fallback,total preparation cost,FD/thread observation and actual full
retirement. Generic FFI/fork safety and idle-state memory remain scoped.

## Actual setup result

# Native Mathlib import preparation — root self-review

The previous host could report ready after processHeader returned a MessageLog
with import errors. Own Lean glue now fails that preparation. Matching Rust
requires actual imported_modules metadata and header_errors=false; existing
fresh native fallback retains the original source/result on failures.
Native candidate JSON and CLI request API are unchanged. This is not a new
authentication/integrity gate or an imported-axiom audit.

Own glue compiles and links against the actual unchanged retained Lean4.9rc1/
11REPL exported objects; all original object sizes/mtimes still match. Sources,
commands,logs and combined old-collection/other-setup/own-build RSS are retained.
No active dependency source or collection version changes.

## Actual import-only observation

The private host prepares original minif2f-0's parsed Mathlib/Aesop imports.
No branch connection is opened; no candidate declaration executes.
Actual header-error-free environment has5545imported modules. Ready at2.539921s;
observed parent RSS3,756,408,832bytes(3.50GiB),one thread,zerochildren.
Native guard had checked no unexpected FDs before readiness. Closing stdin
retires parent normally(exit0)at2.676139s; no parent remains.
Combined sampled RSS peak24,833,953,792bytes(23.13GiB),no monitor error/kill;
1s sampling is not a kernel hard budget or subsecond exact peak.

This establishes actual Mathlib initialization/quiescence for this supplied
context only. It does not execute COW children,prove arbitrary initializer/FFI
safety,measure cross-candidate reuse/throughput,or replace complete matched
native differentials. Those remain pending until the old sole group retires.

## Validation scope

The new real native CI regression must reject failed-import readiness and
exercise the original fresh fallback. Positive native CI checks actual module
metadata while retaining raw responses/real concurrent children. Local ordinary
tests are separate from this native qualification.

An initial local wrapper restricted validation to one CPU; the existing
two-CPU RSS integration fixture correctly fails its explicit precondition.
Its log is retained,then validation runs with two eligible CPUs. No test is
weakened/skipped to mask the failure. No new native collection was started.

Final local validation at135059passes format,Clippy,34ordinary tests,docs and CLIhelp;4native tests intentionally ignored locally. Exact pushed native CI still required for this source version.
