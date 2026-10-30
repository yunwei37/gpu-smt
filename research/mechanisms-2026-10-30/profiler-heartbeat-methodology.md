# Profiling changes heartbeat-limited Lean outcomes

M branch, 2026-10-30 UTC; self-review. This is a measurement-validity result,
not a verification speedup.

## Matched input and observed effect

The fixed 200-source stratum ran control and observe modes (400 complete
frontend calls), same installed Lean4.9.0-rc1, same imported Mathlib environment,
same source, same top-level heartbeat3000 diagnostic budget, one native process.
Observe enables trace.profiler with threshold0; control disables it. Both retain
InfoTrees. Each source runs control before observe: ordering and shared-process
cache history are limitations. This is not the original300-second service point.

| Mode | No error flag | Ordinary Lean error | Diagnostic budget interruption | Body wall seconds |
|---|---:|---:|---:|---:|
| control |31|19|150|779.387741|
| observe |24|16|160|80.075228|

Seven sources change from no error flag to an error flag. Their IDs and errors
are in profiler-7-differences.json; all400 small rows are in the CSV. No memory
diagnostic was identified by the retained classifier.

trace.profiler records nested trace objects in Lean itself. Lean heartbeats
count allocation work; tracing consumes this same budget. The installed
Lean/Util/Trace.lean withTraceNode implementation constructs and stores trace
nodes and contexts. The observed run reaches diagnostic limits sooner.
The apparent0.10274 observe/control time ratio is therefore not acceleration:
the two modes stop after different amounts of useful tactic work.

We did not record raw heartbeat deltas in this400 run, so do not infer a numeric
tracing allocation multiplier from its timings. Also, hasErrors is only a raw
frontend error flag, not the service's full sorry/artifact acceptance policy.
These seven differences are not advertised as a measured production pass-set
difference. Regardless, the changed execution invalidates a transparent
critical-path comparison.

## Required replacement

Use native C timing around stock tactic execution without allocating Lean
objects or enabling Lean trace.profiler. Preserve the original callback and
count unavoidable CPU/logging overhead. Compare diagnostics, raw InfoTrees,
heartbeats and decision flags against stock Lean before accepting timed data.
Only qualified measurements can support available-parallelism or speedup claims.

The first dynamic-interposition prototype is NOT qualified. Its four source
pairs have equal error flags, diagnostics and InfoTrees, but the output has
16 source markers and **zero tactic timing callbacks**. The first pair also
shows a heartbeat-count warm-up difference (13000/12316); the other three
match. A process exit0 is not proof that native instrumentation engaged.
Do not run the200-source timing collection with this inactive hook.

Next implementation uses existing compiled SDK objects and link-time
--wrap=lean_profileit, if those artifacts support a small relink. This is a
local measurement binary, not a new verifier or main-engine change. Source
rebuilds of Lean/Mathlib are not required or implied.

## Provenance and scope

Whole capture:1170.882824s,1142.78795CPU s, sampled owned RSS peak
8643375104bytes (about8.05GiB), all400 rows, native exit0 and retirement.
Raw19MB output and complete memory samples remain outside Git on the existing
PVC: /workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/captures/local-disk-dag200

The earlier WAN-backed capture stopped after194.153s and no rows during a
Workspace replacement; exact process exit remains unknown. Its partial records
are retained independently. New local clocks are never stitched to that run.
