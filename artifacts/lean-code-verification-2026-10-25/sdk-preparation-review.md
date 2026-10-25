# Native reference environment preparation — root self-review

Verina requires4.18.0 and Mathlibaa936c36, rather than silently porting source
to the existing4.9/4.27contexts. Exact official SDK333,619,526bytes and source
archive17,490,718bytes were downloaded to owningWorkspace /tmp, leaving the
projectPVC's roughly1.3GiBfree untouched except small receipts.
Initial system tar --zstd failed because zstd is absent. The existing Python
zstandard package streamed extraction with the data filter; no active venv,
host package, permission or other Workspace changed. Version query confirms
Lean4.18.0/11ccbced7964; it is not a theorem check.

Official lake exe cache get exits0 in42.381243s and fetches all6,471files.
The combined setup/full480sampled peak is22,400,139,264bytes,43samples,
2actualverification REPLs/0kills/0monitorerrors. Compile/cache setup is
outside future workload clocks, separately reported. Original480inputs,
binary, source ordering and resource point are untouched; shared-host
contention remains part of diagnostic interpretation.

A separate lean-mlir native nightly SDK/source preparation is preserved,
with exact b8c4a771/Mathlib2100ee66 and nightly-2025-12-01; its cache setup
remains a separate actual process until terminal. No proof workload or
second collection has run. Its actual SAT/LRAT stages are not known from
89source mentions. The nativeVerina profile runner is implemented/AST-parsed
but actual source results and profiler engagement remain pending.

Self-review checked inherited24GiBAS, twochild semaphore, sampled48GiB
guard, source/PID/birth activity, explicit admission classification, native
timeout and exception process-group retirement. preexec_fn was removed:
parent limits are inherited, avoiding fork callbacks after watchdog threads.
This is root self-review, not independent audit or measured acceleration.

## Nightly dependency availability and scoped source build

The SLLVM source pin requires native nightly-2025-12-01 plus
Mathlib2100ee66. Both exact SDK/source archives are prepared, but its public
cache supplies zero of7,675requested files. Exit0 here is not dependency
readiness. Before that result, root fixed a missing advertised Cli commit
with exact-origin git fetch, then supplied the real Mathlib Git metadata
and official nightly tag required by upstream cache discovery; source Git
status stays clean. The defaultAzure and one43module upstreamCloudflare
probe both have zerohits. No more URL/flag probes or a substitute version.

Source closure preparation identifies58project modules and498external
Mathlib/dependency modules for the real89bv_decide SLLVM file, rather than
building all7,675. Actual native build/profiling waits for the sole480capture
retirement, preserving its memory resources. The initial import regex picked
comments and then the Lean4.27 'import all' modifier; both intermediate raw
graphs remain and the final graph fixes that grammar before any native run.
Native builtin SDK imports are explicit exclusions, not missing source costs.
These are dependency-preparation results, not SAT timing or acceleration.
