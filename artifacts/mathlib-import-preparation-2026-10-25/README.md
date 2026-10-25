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


## Final pinned native qualification

15d084dd58374ac29a3338eccdac82ac276bfeb4passes engineCI40199783360(Rust and
native job121188306293)and smoke40199783408. All4actual native tests pass,
0ignored,including failed-header fallback/no-ready plus actual positive module
metadata and previous raw-source/REPL/concurrent-disposable-child contracts.
Raw logs and terminalmetadata retained. This is pinned4.18native CI,not actual
Mathlib child/whole-population performance. Real4.9Mathlib import-only data
remain separately scoped and root self-reviewed.
