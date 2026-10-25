# Optional native import-parent engine backend

Implementation: native/lean and crates/gpu-smt-lean/src/prepared.rs.
This is dependency implementation, not a completed Mathlib/performance result.
Local full validation-20261025T092246 has all six commands successful,
25 passing tests and two explicit native integration skips. Skips preserve the
sole live native collection; official pinned nativeCI runs both real tests.
C warnings-as-errors compilation passes with the configured4.9SDK headers.
The source-only header attempt and initial Rust borrow/test-scope failures remain.

Native child PID/birth is emitted by the child, matched against /proc before
registration/signalling, and retained. Parent waits/reaps before retirement
acknowledgement; optional leader ru_maxrss supplements1s owned-tree samples
for admission learning. That kernel leader peak is not aggregate tree RSS.
Actual import-parent native engagement/full native payloads/cancellation are
pending exact-headCI, not established by these fixture checks.

First actual nativeCI on a6cb006 fails before glue compilation because upstream
default executable build did not produce a static library. Full failure log and
terminal job state are preserved. Builder now requests the actual Lake
REPL:static facet (confirmed in upstream Lake build source), discovers the
resulting archive and records every build command. Native semantics remain
pending the corrected CI, not a successful result. Latest local validation
20261025T092817: all six commands pass,26checks pass,2native tests explicitly
skip locally. Added real-process missing-host fallback and retirement regression;
branch connection time is charged to the same request deadline.

Actual3rdCI shows a libc ABI mismatch in systemGCC objects versus bundled SDK
linking. Bundled leanc alone cannot compile POSIX glue because its minimal
sysroot lacks dirent.h; that attempt is also retained. The official LEAN_CC
override, used for both compile/link plus the SDK C++ runtime search directory,
passes a local full ABI link control. Its clearly-labelled dummy export source
is retained as source-abi-control.c and is never used in the actual backend.
The next actual nativeCI still compiles the real Lean exports and decides parity.

Latest local validation20261025T093746 has27passing checks and2explicit local
native skips. The actual largeHTTP regression fails413before the change and now
passes: the original7808Batch is14,834,061bytes, above the framework default2MiB.
Native COW performance/fullMathlib result remains unproven.

12ed2f8 actual nativeCI now builds all real Lean/C code and executes native
tests: fresh raw-native parity passes, import-parent survival/engagement fails.
That failure is not counted as COW/native parity. Stock runtime promises need
a normal manager, so parent preparation now uses it and joins/finalizes before
forking. BackendEvent records retain failed preparation and fallback stderr
even on an ultimately accepted native response. Origin/execution/PID/birth
mapping is preserved in resource logs. Latest local20261025T095251 has all
six commands successful,27passing checks and2explicit native skips.
