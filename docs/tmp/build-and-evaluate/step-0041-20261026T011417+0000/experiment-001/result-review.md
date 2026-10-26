# Compiler arguments — root self-review

The configured source backend forwards exact argv tokens before native JSON/stdin
flags and keeps original UTF8/CRLF source. Empty args preserve the old identity;
nonempty args partition backend/cache scope. The executable repeats --lean-arg,
rejecting its use with REPL instead of silently dropping it. Public NativeLean
struct literals still compile. No default argument, active full-run binary,
resource point, source bytes or native prover implementation changed.

Two real subprocess-fixture tests exercise backend and executable transport,
Capture identity and process retirement. The fixture deliberately does not prove
theorems. The final ordinary validation has39 passing tests, four explicit native
test skips, clean fmt/Clippy and warnings-as-errors API documentation. The existing
native source differential now compiles two additional same-argument Init proof
cases, for accepted and rejected source; actual execution is assigned to the
existing pinned-native CI, not another local native workload.

Raw checks:
- [initial validation](../../../../../artifacts/rust-engine-2026-10-25/validation-20261026T011536/validation.json);
- [final validation](../../../../../artifacts/rust-engine-2026-10-25/validation-20261026T012233/validation.json);
- [combined RSS](development-rss.json), plus compressed1s observations.

The final combined full-collection/build/test/monitor sampled peak is
16,018,681,856B within51,539,607,552B, no pressure withdrawal or monitor error.
This is sampled development evidence, not a hard RSS quota or performance run.
Rerunning the monitor replaced its preliminary RSS summary; the retained samples
are the final run, not a reconstructed history of both runs.

The initial raw validation receipt inherits the misleading prefix 'No native
full group during these ordinary checks', immediately followed by the correct
statement that full7808 remains the sole active collection. Keep raw receipt
unchanged; this is a metadata wording defect. The final receipt corrects that
caption; neither ordinary run executes the ignored native differential.

A transient control-plane ready-API error prevented one remote edit before
execution. A retry on the same owning-Workspace path succeeded; checking target
source established the edit had not occurred. No node, Pod or collection restart
was performed.

Scientific impact: this removes a source-context dependency for the next actual
lean-mlir measurement. It establishes neither bv_decide engagement, SAT/LRAT time,
full source/native equivalence, throughput gain nor a new paper contribution.
Original-file/stdin context qualification and diagnostic profiling remain pending.
The prepared300s timeout is an engine default, not an upstream lean-mlir protocol;
any such observed timeout is censored, not a certified failure.
