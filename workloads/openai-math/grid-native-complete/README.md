# Full Grid module: native completion at a separate resource point

Pinned OpenAI/math 4eaee875, original Grid source 1,815,532 bytes; Lean4.34.1,
Mathlibd13f. Native invocation100000HB, M8192, -j8 and LEAN_NUM_THREADS8,
CPU0–7, unprofiled, self-wall1200s. Existing three compiled dependencies reused.
Return0, no sorry warning. Native wall634.28007s, user399.93377s,
system440.56261s, wait4 peak8,072,544KiB (7.70GiB).
Combined owned-tree sampling includes censored EPFL13733 and parents:
13,141,098,496bytes (12.24GiB), maximum2Lean processes.
Capture elapsed640.82298s includes orchestration. Native and controller retired.

The earlier120s unprofiled-j1 and300s profiled-j1 captures are retained as
right-censored points. Worker configuration, instrumentation, and self-wall
budget changed together; this is not an isolated worker-count speedup or a
matched profiler-overhead experiment. No default-unbounded timing claim,
global CPU/GPU bound, full-build estimate, or false-goal conclusion follows.
M8192 and1Hz sampling are not hard kernel RSS quotas.
45,375,721 voluntary and529,643 involuntary context switches,3,033,828 minor
and0major faults do not identify a specific syscall/root cause.

All raw source replay, full logs, memory samples, counters, and launch data:
PVC /workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-grid-j8-1200.
The selection.json inherited a stale purpose string from the300s diagnostic;
actual frozen run.py, native row and self-timer define this point.
Only small derived tables are committed. The original53target frame remains
incomplete. A finite incremental continuation can now use the genuinely
compiled Grid object; no missing dependency is replaced by an axiom/sorry.
