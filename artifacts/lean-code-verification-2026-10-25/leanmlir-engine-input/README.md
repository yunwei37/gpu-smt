# Original lean-mlir engine input

One complete original module at b8c4a771319a044854a4bbb49b8821381ef86ff8,
including all definitions, proofs, options and scoped syntax. No theorem or
tactic splitting, admission removal or source rewrite. All mode, reuse=false,
unchanged engine default timeout (300s). The 82,628 source bytes match the
prepared input exactly. This is not an executed workload result.

## Manual execution

Run execute.py manually after the current original71 group actually retires
and its results are ingested. The entrypoint refuses to overlap its controller,
cell CLIs or pinned native executables. It has no waiting loop or scheduler.
--validate-only checks the existing inputs without running a proof.

Three sequential conditions use the existing Rust NativeLean backend:

1. The unchanged file at its original project path.
2. The exact same source through stdin.
3. The original file with the pinned native trace profiler enabled.

File and stdin have different module/diagnostic filenames. Their real outcomes
must be compared before treating them as equivalent. Keep --tstack=400000 from
the original root manifest on every condition. Profiling enables native
trace.profiler and full trace messages; no source, kernel trust, SAT timeout,
trimming or heartbeat setting changes. The profiler has its own measured
overhead and may not export anything if killed or timed out. Missing data is
censored, not zero SAT/LRAT cost. See the retained native-bv-stage-map-20261026
source observation for nested trace interpretation.

Each condition checks one whole module with an exclusive four-core lease on
CPUs8–11, actual aggregate48GiB RSS, the existing sampled watchdog, and no fixed
address-space cap. Four eligible cores do not imply four busy cores or four
concurrent candidates. This point is separate from the miniF2F four-worker
point. The 300s is the existing engine default, not a published workload limit.

The driver discovers LEAN_PATH through the original root Lake configuration,
using --no-build env printenv LEAN_PATH. The actual environment query exits0
and resolves the root paths. It warns that the Cli manifest input revision
differs; that warning is retained. Existing root source/manifest/55c3729 Cli
revision are not updated to chase a moving branch. This successful query does
not validate the candidate body or prove every dependency is loadable.

The query takes1.003489s including the existing support monitor loop; three
combined native71/query samples peak at34,827,231,232B. No pressure abort or
monitor error. This is sampled accounting, not a hardquota or globalOOM proof.
The short CPU11 query overlaps native71 reference timing and is recorded as a
confound. No candidate body, dependency target or additional collection runs.

Only after original71 retires does the driver build a fresh Rust CLI, including
the source lifecycle repair. It cannot replace the current capture binary
halfway through its conditions. Discovery/build/cell/archival clocks are
retained. Large raw diagnostics/profile exports use existing /tmp storage;
closed streams reuse existing lossless gzip and decompressed-byte checks.
Temporary retention alone is not committed result delivery. Service verdicts
and raw native exit/JSON/stderr remain separate; diagnostic stderr is not
silently converted into engine acceptance.

Static execution validation succeeds with zero native candidate executions.
Whole-file outcome, theorem coverage, SAT/LRAT timing, profiler overhead,
accepted-set parity and any GPU opportunity remain unmeasured. No extra
observer, logging framework, AI agent, service or competitor system is added.
