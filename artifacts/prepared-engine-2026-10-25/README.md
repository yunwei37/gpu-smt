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
