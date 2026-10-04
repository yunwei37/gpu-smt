# Persistent official Lean replay — 2026-10-04

Removing repeated executable startup substantially improves a **fixed small-fixture
throughput proxy** with official Lean checking still enabled. This result does
not measure a real proof-search candidate stream or whole-library acceleration.
It is the next implementation chosen after correcting the first-round report.

## Implementation

[`Main.lean`](../bench/lean-persistent/Main.lean) retains arena official's
`Export.parseStream`, `Lean.mkEmptyEnvironment`, three `Quot` map erasures and
`env.toKernelEnv.replay`. The process reads one path per stdin line and responds
with JSON containing that path, its decision, any exception message and service
nanoseconds. Every request reparses the file and creates a fresh environment.
No parsed-environment reuse, decision memoization or disabled kernel checking.
Kernel/parser revisions and the toolchain match the retained official source.

This changes the launch/protocol wrapper and exception handling, while using
unmodified parser and kernel libraries. It is not a production server. The harness
fails on protocol errors, timeout or unexpected official exit status; official
exit 1 is compared as rejection and its complete captured exception text remains
available. This mapping alone does not distinguish all possible backend errors
from proof rejection; test expectations and per-input results must also be inspected.

## Fixed-corpus throughput and response times

46 other/bugs/corner-case files repeated 20 times = 920 jobs; three repeats at
widths 1/8/16. Mask **8–23**, 16 lower-clock CPUs, for both modes. Trials ran
sequentially, reversing mode order in the middle repeat. Input order is fixed.
Cold mode dynamically dispatches through a thread pool, with a separate taskset
and official executable per input. Persistent mode creates a process per worker
and assigns deterministic round-robin chunks. Tiny-job results include these
scheduler differences; this is not a declaration scheduling experiment.
No benchmark-level competing jobs were intentionally launched during these
trials, but affinity does not establish exclusive cores or absence of host load.

Medians across the three repeats (speedup = ratio of median makespans):

| workers | cold makespan | persistent makespan | speedup | persistent jobs/s |
|---:|---:|---:|---:|---:|
| 1 | 24.7596 s | 1.9444 s | 12.73× | 473.1 |
| 8 | 3.1764 s | 0.2916 s | 10.89× | 3154.6 |
| 16 | 1.7598 s | 0.1850 s | 9.51× | 4973.6 |

At width 16, median dispatch-to-response p50/p95 is **29.00/41.98 ms cold**
versus **1.01/12.78 ms persistent**. Persistent makespan/jobs is **0.201 ms**
per job; that amortized throughput quotient is not its request latency. Recorded
response times exclude waiting in a client queue. The persistent measurements
include first-response runtime initialization; total makespan includes worker
startup/shutdown. There is no open-loop arrival process or serving SLO claim.

There were **zero per-job decision mismatches** across all 18 runs (16,560 job
records), versus the first cold official run, and zero recorded timeout/error
statuses. Each input's SHA256, byte size, job identity, actual decision and
response time is retained in [raw JSON](../artifacts/lean-2026-10-04/persistent-small.json).
The 46 distinct files total 1,882,324 bytes (40.9 decimal KB/file on average).
These are repeated public correctness fixtures, not independently generated agent
candidates. Their finite agreement does not prove a general semantic equivalence.

Persistent width-1 replay already reaches 473 jobs/s, close to the earlier
cold width-24 observation of 518 jobs/s; persistent width 16 reaches 4974 jobs/s.
The result makes launch amortization a stronger near-term serving route for
this fixture class than an unimplemented GPU tiny-export checker. It does not
rule out GPU work on measured kernel operations or large-library declarations.

## Broader fixture validation

A separate official/persistent pass completed on **215 distinct fixtures**:
9 other, 18 bugs, 19 corner-cases, all 141 tutorial good/bad exports and all
28 perf stress exports, one copy each, mask 0–7 and width 1. Both modes scored
all **197 definitive accept/reject expectations correct**. Their actual decisions
also matched on all 18 `either` cases; this is exact agreement with official on
these inputs, not a universal arena expectation. There were zero per-input
mismatches or recorded errors/timeouts. The persistent worker handled mixed
accept/reject inputs in one process, including the heavy perf inputs.

Individual outcomes, input hashes, exceptions and expected scores are in
[persistent-validation.json](../artifacts/lean-2026-10-04/persistent-validation.json);
[validation-summary.json](../artifacts/lean-2026-10-04/validation-summary.json)
retains group coverage. Non-tutorial expectations come from the pinned arena
snapshot; tutorial good/bad directory names supply their accept/reject expectation.

Cold/persistent makespans were 374.42/63.59 seconds, **excluded from speedup
claims**: the cold pass overlapped severe memory pressure, which subsided for
the persistent pass. During cold deep-n36, cgroup memory-pressure full-stall
avg10/avg60 was about 85%/72%, and host full-stall avg10 about 16%; the retained
snapshot records the sampled conditions. That single cold fixture took 290.76
seconds versus 29.36 seconds in the historical arena record. These observations
show the comparison was not stable; they do not identify a particular competing
process or prove the entire spread's cause. Nothing else on the host was stopped.

## Corrected frontend measurements

The paired profiling script retains complete source, command, stdout, stderr,
return code and source hashes in
[frontend-profiles](../artifacts/lean-2026-10-04/frontend-profiles/).
Toolchain v4.34.1, mask 0–7, each setting a single run. Source copies explicitly
set the desired check option; profiler settings come after the `module` header
where required. All four runs exited 0; linter warnings are retained.

| case | skipKernelTC | full frontend wall (GNU time) | cumulative tactic | cumulative type checking |
|---|---|---:|---:|---:|
| magma-list-deep-n36 | true | 21.10 s | 17.9 s | 0.499 ms |
| magma-list-deep-n36 | false | 81.02 s | 18.8 s | 61.8 s |
| grind-ring-5 | true | 0.29 s | 35.9 ms | 10.7 ms |
| grind-ring-5 | false | 0.83 s | 29.1 ms | 653 ms |

The disabled-check magma profile cannot establish the normal kernel/elaboration
split. On this normal-check sample the kernel category is large. Profiler
categories can overlap and the runs are not synchronized stage instrumentation;
retain this limitation rather than adding the categories as independent stages.
The normal source frontend and post-export replay are different paths/term
representations; their times are not interchangeable.

## Reproduction and provenance

Build in the owning repository (manifest pins exporter revision
`f297dfe2a8557e8674fe892bb49dffe4bfadc0e9`):

```bash
cd /workspaces/repository/bench/lean-persistent
PATH=/root/.elan/bin:$PATH lake build
```

From `/workspaces/repository`, with the original arena inputs/build retained:

```bash
python3 bench/lean_persistent_bench.py \
  --official /tmp/lean-kernel-arena/_build/checkers/official/src/.lake/build/bin/kernel \
  --persistent /workspaces/repository/bench/lean-persistent/.lake/build/bin/persistentKernel \
  --inputs '/tmp/lean-kernel-arena/_build/tests/other/*.ndjson' \
           '/tmp/lean-kernel-arena/_build/tests/bugs/*.ndjson' \
           '/tmp/lean-kernel-arena/_build/tests/corner-cases/*.ndjson' \
  --cores 8-23 --widths 1,8,16 --duplicate 20 --repeat 3 \
  --json artifacts/lean-2026-10-04/persistent-small.json

python3 bench/lean_profile_stages.py \
  --output artifacts/lean-2026-10-04/frontend-profiles
```

Raw JSON records exact invocation arguments and executable SHA256. Original arena
revision and full library input hashes are in the artifact manifest. Existing
solver-serving files/history are preserved. Six Lean-specific unit tests pass.
Full repository unittest discovery reports one existing SMT analyzer failure
(`test_context_overlap_can_detect_reordered_commands`, expected 2, observed 3);
that test and analyzer were unchanged by this continuation.

## Remaining work and GPU state

Large-library repeated timings and a real candidate stream are still needed.
A persistent wrapper does not itself reuse imported declarations across requests.
Such reuse requires dependency/context and rejection-state validation before a
serving claim. GPU mechanism/coverage and runtime/setup costs remain unmeasured.
No GPU checker or GPU speedup is claimed or ready for execution; the next GPU
resource request should attach a concrete executable and CPU reference. Resource
coordination must use the existing Kubernetes NVIDIA allocation/runtime path,
preserving the owning Workspace/PVC. See [resource status](../docs/lean-resource-status.md).


## Subsequent validated continuation

The GPU readiness statements above describe checkpoint `63c29e5`. Later on
2026-10-04, [real Mathlib proof/state reuse](2026-10-04-lean-mathlib-state-reuse.md),
[actual RTX 5090 metadata execution](2026-10-04-lean-gpu-dag.md), and
[real VeruSAGE trace/replay ablations](2026-10-04-verusage-real-traces.md) completed.
The GPU primitive is validated against official Lean metadata; a whole GPU
proof checker remains unimplemented. Earlier measurements and their scope are
preserved rather than replaced by these newer experiments.
