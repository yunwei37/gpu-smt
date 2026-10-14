# Experiment029: shared-process native Lean frontends

## Research Question
RQ3 exactly: How does prepared-state branching change end-to-end latency, throughput
and memory at equal resources compared with established warm-session reuse?
Uncertainty: does native candidate execution from shared prepared roots benefit from
a shared heap/runtime, compared with the existing copy-on-write warm process pool?
This implements another native branching placement, not a new RQ or claimed novelty.

## Paper-value admission
Role: decisive for the mechanism/resource tradeoff on the complete ProofNet stream.
The largest credible result is consequential complete verification throughput or memory
improvement after competent preparation reuse. Existing warm/snapshot/fork measurements
do not measure this shared-process alternative. The reject argument is that branching
merely duplicates warm startup and its process/runtime costs erase gains.
Current warm baseline already shares prepared roots through COW; it is deliberately
strong. Atomic references, shared runtime contention and mutable extensions can defeat
the shared-heap alternative. A positive result motivates broader native placement/load
and multi-context evaluation; a negative/mixed result closes this implementation and
keeps the full system/GPU/RQ goal open.

Best alternative: batch the existing GPU beta/zeta provider. Source inspection rejects
this as the next full experiment: cn_reduce is a dependent scalar loop; the native hook
blocks on every result, at most four frontend requests are in flight, and observed
successful GPU work is sparse. More tiny native6 variants would not expose substantial
parallel work and are already negative. Native shared frontends test real complete
parallel verification and a distinct resource cost, rather than metadata or GPU replay.

## Method and published assets
Reuse the exact Lean4.9.0-rc1/Mathlib/REPL native processCommandsIncrementally,
prepared Root, first-header imported-search preparation, candidate diagnostics,
declaration witnesses and current source capture. Published native snapshots and
Kimina warm services already establish logical reuse; this experiment claims no
novelty for threads or immutable environments.
Add only an embedding host with native lthread workers and independent per-worker
Root tables, calling the unchanged native processing code. Seed roots are shared;
candidate-updated snapshots remain worker-local. Native final kernel stays active.
No additional result cache or CPU replay; no device work is silently inferred.

## Comparison and fairness
Main baseline: existing original Lean49PreparedBranches warm-pool, four workers,
header-cache/first-header preparation and full-stream retirement. It represents the
strong measured native reuse competitor and needs a matched run on this workload.
Proposed: one native process with four native frontend worker threads, same preparation
and per-worker native incremental state.
Both use CPU0–3, native default task-manager settings, no LEAN_NUM_THREADS override,
original unlimited native memory and300s per-input allowance. Permitted CPUs are not
exclusive. One versus four native task managers is a disclosed mechanism difference,
not a changed capacity. Preparation/output/EOF/cleanup are in whole time.
No new Workspace, service, schedule, quota, model or hardware allocation.

## Workload and metrics
All5952 original retained ProofNet-lineage Lean4 source attempts, original order,
186 test tasks ×32 captured attempts, including rejection/incomplete/operational
rows. Exact source/task lineage is in the paper and existing input/provenance records.
Primary: complete corpus makespan/attempt throughput and source admission-to-response
latency. Separate resource profiles report sampled process-tree PSS/private memory
and CPU time with the existing observer caveats. Compare complete paired native
outcomes to the original reference; no result normalization or source exclusion.
Three alternating whole primary pairs, then one separate profile for each method:
8cells ×5952 =47616 outcomes. Profiles are not extra primary repetitions.
No whole-run deadline. Original300s allowance applies; process-wide crash/timeout
interference is reported, never counted as acceleration. If it prevents valid full
comparison, return incomplete/invalid without quietly dropping affected candidates.

## Execution
Native build and host live under artifacts/lean-parallel-verification-2026-10-12/
experiment029 and necessary source under bench/. Build commands/versions retained.
Preflight uses the original8 readiness inputs including source0 rejection,
257 acceptance,2913 incomplete,5879 operational and the subsequent5880 rejection.
This establishes executable native/parallel/observer paths only.
Full command: python3 artifacts/lean-parallel-verification-2026-10-12/
experiment029/run.py full.
Completion: every planned5952-source cell terminal, all original outcomes retained,
whole clocks include native initialization/transport/output/EOF and exit;
terminal after-clock ZIP archives preserve all raw bytes, with no timing stitching.
Failures and partials retain their original directory; recovery is recorded.

## Interpretation
Stable whole-time improvement against warm pool with matched native outcomes supports
the tested placement. Lower sampled PSS alone is only qualified resource evidence;
a slower but lower-memory result is a tradeoff, not fastest-verification acceleration.
Inconsistent paired effects are inconclusive. Operational mismatches or an avoidable
baseline fault invalidate superiority. Negative results bound this constructor/cohort,
not the full four-RQ system thesis. Target: two-method paired whole-time/resource table
inside the complete RQ3 evidence matrix; broader service/mini/SMT obligations remain.

## Recorded real-preflight repair — 2026-10-14T10:08Z
Original preflight1 demonstrates the same native Nat.pow panic in both methods.
The warm pool fails only its candidate; the shared process exits with two
outstanding original inputs after returning six. Both raw attempts are retained.
No source-ID filter, panic suppression, budget or oracle change is introduced.
After an actual nonzero shared-process exit, every original unreturned input
runs once through the original warm native pool. Both phases are charged.
No restart/retry loop is added. Resource observation spans both phases.
This does not establish independent branch failure/cancellation transparency.
Preflight2 tests the repaired full path and observer on the same8original inputs.
