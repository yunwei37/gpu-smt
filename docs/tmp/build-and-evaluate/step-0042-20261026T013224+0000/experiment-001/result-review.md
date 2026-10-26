# Original file context — root self-review

The backend and executable now support a pinned original file without copying,
rewriting or splitting source. Relative paths resolve from the original project;
the supplied symlink filename is not canonicalized away. Before native spawn,
the file bytes must match Candidate.code. Missing/different files yield
BackendError with no fabricated native response. Identity includes file path
and argv; all prior stdin/default behavior and public struct fields remain.

The configured backend uses the same owned process registration, CPU assignment,
watchdog, remaining native timeout, cancellation and reaping code as stdin.
The original file receives null stdin and --json plus declared arguments, without
the --stdin flag. File validation costs enter the actual attempt. Source/project
immutability remains the caller's existing context contract; the pre-read is not
an atomic defense against concurrent file mutation, and cache lifetime assumes
pinned inputs/dependencies. Measurement retains reuse=false.

Actual process and executable fixtures prove original file selection, unchanged
UTF8/CRLF bytes, exact argv, file-vs-stdin identity, mismatch-before-spawn and
process retirement. The fixture is Python, not Lean. Expanded pinned-native
differential source test compiles locally with accepted/rejected original-file
proofs, raw same-file comparison and cleanup; actual execution awaits existing
CI on the published source. No new owning-Workspace native workload executes.

[Ordinary validation](../../../../../artifacts/rust-engine-2026-10-25/validation-20261026T013423/validation.json):
41 tests pass,4 explicitly ignored native contracts compile; fmt/Clippy/docs
all pass. [Combined RSS](development-rss.json) covers the active full collection
and additional build/test/monitor trees, peak28,365,803,520B; no pressure withdrawal
or monitor error. It is a1s sampled observation, not a hard quota or throughput.

The [pinned SDK stage map](../../../../../artifacts/lean-code-verification-2026-10-25/native-bv-stage-map-20261026/source-observation.md)
retains actual source/line provenance for bv preprocessing, reflection,
bitblasting, DIMACS/SAT, LRAT parse/trim and proof checking. Default profiler
Firefox output drops phase messages and synthesizes threadCPUDelta from wall
slices. The next diagnostic needs declared message export/own overhead; no
sampling-CPU or additive inclusive-time claims are admitted.

Scientific effect: remove a real context-preservation dependency before measuring
the complete original lean-mlir module. No theorem population, speed, phase
fraction, reliable rejection certificate or new systems contribution is proven.
The active full7808pair remains frozen at42659a8; neither release binary nor
prepared parent is rebuilt. Next actual native source/profiler acquisition
waits for that collection's real terminal state.
