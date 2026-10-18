# Native arithmetic oracle experiment

Status: experimental. Historical CPU stage: 1.34668×; admitted GPU variants have completed without a valid speedup. Corrected full CPU pairs are active. See the
[CPU-stage result and open GPU decision](../../../artifacts/linarith-oracle-2026-10-17/decision-20261017.md).
All three primary pairs and both full phase diagnostics are complete; see the
[strong-baseline analysis](../../../artifacts/linarith-oracle-2026-10-17/native-stages/strong-result-review.md)
and [prototype analysis](../../../artifacts/linarith-oracle-2026-10-17/native-stages/oracle-result-review.md).
These are CPU results. No production service or GPU acceleration is established.

The [first complete GPU capture](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/full1000-phase1/result-review.md) records3,374.15seconds and8operational failures on all1,000attempts; its GPU target is retired. The frozen same-plan CPU controls are complete: native 2,331.39 s and robust HiGHS 2,363.00 s, each with 992 complete and 8 rejected outcomes. The direct-feasibility repair failed numeric qualification and remains archived. Current source restores the measured phase-I model with owner cancellation for the necessary clean-header qualification; the original CPU oracle passed real clean-header qualification and its three matched full pairs are active. Historical phase-I source is retained by commit1ce9e09. The build-batch.py, build-grpc-client.py, support-proxy.py, build-candidate-timing.py and run-batch.py entrypoints are experimental integration paths. [Repair plan and limits](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target/direct-feasibility-preflight-plan.md). No fresh full1000 is started from this failed repair; those two earlier GPU target instances were deleted. The subsequent corrected-family instance has also been deleted after failed native qualification. [Failed repair and limits](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target/direct-feasibility-result-review.md).


The already-admitted original-population prefix comparison remains unfinished.
Its [launch receipt](../../../artifacts/linarith-oracle-2026-10-17/formal-default/launch.json)
and actual live process identify the existing capture. The
[complete miniF2F batch reference](../../../artifacts/linarith-oracle-2026-10-17/formal-default/minif2f/batch-result-review.md)
includes its operational failures. A reference alone is not a reuse speedup.
The [predeclared protocol](../../../artifacts/linarith-oracle-2026-10-17/plan.md)
retains the original decision rule.

- `build-stages.py`: copies the pinned Mathlib control/reconstruction functions into an instrumented namespace, records sequential thread CPU and invocation wall, and builds native code. Original Mathlib is unchanged.
- `Oracle.lean` / `oracle.rs`: one export of supported real/rational comparison expressions, native polynomial/product generation and LP, coefficient/provenance return, selected proof construction and one weighted contradiction check. Unsupported or failed cases restore state and run the original path.
- `Baseline.lean`: established Farkas Fast plus invocation-local product-application reuse with native hybrid/HiGHS certificate search.
- `run-stages.py` / `run-comparison.py`: use the existing Kimina native batch collector; preserve all source outcomes, costs and raw streams.
- `build-oracle.py`: rebuilds the native experiment from the retained sources and dependencies. No original repository or installed runtime is modified.

The scripts currently use the retained owning-Workspace dependency paths (Lean4.27, matching Mathlib/Farkas/Kimina), not a portable installer. Their pinned versions and original build procedures live in the reproduction guide and `artifacts/lean-modern-native-compilation-2026-10-14/`. The restored documented `/tmp/gpu-smt-linarith-oracle-20261017/` path resolves onto the existing Workspace PVC; its original ephemeral contents were lost during Pod replacement. Publish completed evidence back to `artifacts/linarith-oracle-2026-10-17/`.

## Historical build and capture entrypoints

The following recipe documents the completed arithmetic experiment. It is not
the current work queue. Use the owning Workspace, with no active worker using
the same libraries or build output filenames:

```bash
python3 bench/lean-native/linarith-oracle/build-stages.py
python3 bench/lean-native/linarith-oracle/build-oracle.py
/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python   bench/lean-native/linarith-oracle/run-batch.py   --out /tmp/gpu-smt-linarith-oracle-20261017/batch-oracle/new-preflight   --limit 24 --methods fast-hybrid oracle
```

Use fresh output directories. A preflight is qualification, not a full speedup claim.
Do not rebuild libraries that active experiment workers still use. Main performance
trials disable diagnostic telemetry. Whole clocks include native preparation,
packing/IPC, oracle work, checking, fallback and process retirement.


Formal-prefix support uses `build-prefix-repl.py`, `run-prefix.py` and
`analyze-prefix.py`. Source/input/parser evidence is under
`artifacts/linarith-oracle-2026-10-17/prefix-opportunity/`.
Its native batch and proof-step waves use the same width4; closed roots are
checked by Lean's kernel. Original unsupported/failed paths fall back.
Timeouts remain300srequest boundaries and count as operational outcomes;
process replacement invalidates all cached environment/proof-state ids.
Forced-retirement CPU is explicitly censored. The timeout repair was qualified on the actual failed batch: four retained
operational outcomes followed by four completed sources after replacement.
Earlier full attempts were interrupted by the shared-node/volume fault;
see the [retained failure record](../../../artifacts/linarith-oracle-2026-10-17/interruption-20261017T0617.md).
Earlier completed and failed records remain; no lost partial is counted as complete.

The historical heavy-cohort driver is `run-matrix.py EXISTING_PAIR_PID`.
It preserved the first pair and reused its closed receipts.
Read `artifacts/linarith-oracle-2026-10-17/matrix-launch.json` and actual
processes before continuing; this is not a command to start another collector.
Extra CPU competitors are conditional on passing the user's threshold against
Fast/hybrid. `analyze-matrix.py RUN_DIR` reports pending values as null.


build-strong-profile.py generates an instrumented copy of the existing
Fast/hybrid implementation and a separate exported strong-profile.so.
run-comparison.py --methods strong-profile --diagnostic selects it;
ordinary primary methods do not import or load that diagnostic library.
analyze-strong-stages.py CELL reports sequential stage thread CPU against
the observed collector/waited-child CPU denominator, with residuals explicit.
External LP-child CPU is not in the LP calling-thread counter. Invocation wall
sums overlap across sources and cannot be whole-wall percentages.

The real mixed Real/Nat diagnostic preflight matches full native JSON on all
four sources. It is not representative of the 1,000-source distribution.
The full strong diagnostic is complete and matches the third primary reference.
The earlier stock phase pilot does not describe Fast/hybrid.

analyze-prefix-runs.py RUN_DIR compares every original source index between
batch and each prefix method. It distinguishes pending, operational failures,
verdict differences and observed versus validated whole-time ratios. A completed
acquisition with timeout rows is not a successful verification comparison.


The historical analyze-matrix.py checks unique source ids/order against
input-top1000.jsonl and reports whole clocks, observed CPU, sampled PSS, native
outcomes and deduplicated grouped-array wave tails. Those are not individual
proof latencies or online SLOs. The newer analyze-batch.py uses actual per-task
entry/return timestamps, retaining missing ends as censored. For the exact full
original1000-source cohort it also joins the complete native baseline phase
profile to each method-selected top1%/10% candidate set. These are separate
diagnostic CPU counters, not GPU measured phases or percentages of primary wall.
[Real joins, uncertainty and regression](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/full1000-phase1/candidate-phase-link-result-review.md).


The optional --sample-seconds control defaults to the original one-second
process-tree memory observer. Nonpositive values disable only that observer
for measured overhead qualification, while retaining native checking, raw
capture, rusage and normal retirement. Disabled memory metrics are null.
The admitted primary comparisons retain the original default; the four-source
observer-on/off control is not a correction to their whole clocks.


After the recorded Pod replacement, `restore-native427.py` and
`restore-prefix49.py` rebuild the pinned dependency closures from retained
sources. They use the existing Workspace PVC and require the documented SDK
archive decompressor and retained Rust toolchain. They do not start a capture.
Read [actual recovery qualification](../../../artifacts/linarith-oracle-2026-10-17/recovery-20261017/self-review.md)
before use; never rebuild libraries while a capture loads them.

`run-matrix.py --resume-completed` reuses restored complete pairs and preserves
incomplete directories. The prefix matrix can reuse its existing closed real
preflight receipt without an obsolete process ID. Both remain finite experiment
drivers; no additional service or schedule is installed.

The hourly research automation is active. Prefix captures continue in the
background while the GPU-stage attribution and feasibility analysis proceed.
The final >1.5× decision uses the better CPU/GPU oracle result. Completed CPU
pairs remain preserved; they are not a queue to restart. All new captures use
the upstream 48 GiB limit and retain resource failures.

`analyze-oracle.py CELL` describes observed successful direct-check branches,
fallback records, source-body groups and native polynomial/product/LP timers.
It preserves the distinction between nested roundtrip timers and calling-thread
CPU. Failed/unsupported attempts lack these detailed timers; their cost is
unknown, never zero. Branch/fallback counts are not a mutually exclusive
tactic-success rate or a GPU upper bound. The analyzer matches the retained
actual73-check/1-fallback diagnostic fixture and all six published timing sums;
that fixture is qualification only. The complete1,000-source prototype result
and retained raw telemetry are now under the native-stages artifact; its full
native responses match primary prototype3.

For a full strong-stage capture, `analyze-strong-stages.py CELL --identities
RECEIPT.json` can associate sampled CPU with a numeric-service executable using
its actual live PID and birth time. This includes service parsing/repair and
does not identify pure simplex CPU. A missing identity match stays unavailable;
older missing identities are not inferred retrospectively. The first full
1,000-source strong capture and its actual identity receipt are under
`artifacts/linarith-oracle-2026-10-17/native-stages/`.

The formal comparison now leaves pinned SHRED's48GiBverifier default intact;
the unsafe localNoneoverride caused the retained
[global-OOM attempt](../../../artifacts/linarith-oracle-2026-10-17/prefix-oom-20261017/result-review.md).
This affects only the native verifier children in that benchmark. New captures
record the actual client value and usefull-default-*names; old unlimited
partial clocks/outcomes remain separate. Root/Agent/Workspace limits are not
changed. Actual failed8and normal32-source qualification precede continuation.


Completed-cell summaries from `analyze-prefix-runs.py` include paired sequential
client-request intervals and failed-request roundtrip wall. Their fractions
are emitted only after pairing and non-overlap checks; they are not native CPU
or tactic/solver-stage fractions. Missing comparison cells remain pending.
See the [complete miniF2F batch reference and limits](../../../artifacts/linarith-oracle-2026-10-17/formal-default/minif2f/batch-result-review.md).

## GPU-stage all-call diagnostics

The [frozen GPU-stage plan](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/plan.md)
extends attribution to every direct/fallback numeric request. Build with
build-cost.py after the existing build-stages/build-oracle/build-strong-profile
dependencies. It creates cost-profile.so and two diagnostic binaries in the
retained build tree, preserving primary binaries and active prefix files.

run-comparison.py --cost-profile --methods fast-hybrid oracle --out OUTPUT
uses the same frozen inputs, native worker and whole-clock boundary. New captures
use 48 GiB RLIMIT_AS; allocation failures remain resource/operational outcomes.
analyze-cost.py CELL joins per-call IDs and exact source bodies, separates
FP search/exact LP/repair/protocol costs, records matrix sparsity, and reports
overlap/batching and wave-based tails. These are diagnostics, not new primary
speedups. Missing joins disable a claimed bound. Reuse no active capture directory.

Supplemental provenance/worker accounting can build into an explicit separate
directory with build-cost.py --out BUILD_ROOT, then run-comparison.py
--cost-profile --cost-root BUILD_ROOT. The builder reuses pinned base modules
in the same Lean package root. Do not overwrite a loaded primary/diagnostic
library. replay-numeric-cost.py replays closed per-process request streams and
collects complete wait4 worker CPU; its elapsed time is not Lean/GPU performance.

## Arithmetic header correction
The measured integration imported legacy and batch tactic elaborators together,
which allowed repeated work after a failed elaborator. run-batch.py now selects
Baseline for the native control, Baseline+Oracle for the originalCPUoracle, and
BatchOracle with its own BatchBaseline for robust support. Actual native handler
inspection and24real-source full-response qualification are retained in
[the correction record](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/header-correction-preflight24/result-review.md).
Legacy diagnostic imports remain separately scoped; their phase vectors do not
become a clean-header primary phase decomposition.

Manifest/config filenames are invocation-specific and Unix sockets include
the process identity, so a qualification cannot replace an active capture's
inputs. Mapped native binaries remain unchanged. HistoricalCPUprimary receipts
record unboundedAS, while new runs inherit48GiB. No old data is relabelled.

Current support-proxy.py retains phase-I PDLP/crossover with owner-EOF
cancellation for corrected-header qualification. The failed original-feasibility
version remains in commitb80c8bb and its artifacts, not an active candidate.
No numerical solver parameter grid or fresh full matrix is admitted from the
failed formulation. Corrected-header HiGHS has no qualification benefit and
receives no new full run. Read actual corrected GPU qualification before
choosing the final full method set.

## Current matched captures
The corrected-family complete CPU comparison uses only native fast/hybrid and
the original CPU oracle: [plan, exact command and self-review](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/header-corrected-full1000/plan.md).
Three pairs alternate order under 48 GiB on the unchanged 1,000-source cohort.
The controller collects a pair only after actual native process exit.
Do not reuse the historical unbounded-AS 1.34668x as this block's result.

The CPU-only batch bridge ablation is named oracle-hint: it keeps the cheap
floating hint and native fallback, omitting the external support socket.
Its real24-source preflight takes52.189s vs native46.054s, with fullJSONagreement.
It receives no new full matrix, as does slower clean-header HiGHS.
GPU preflight uses phase-I PDLP/crossover with owner cancellation and shares
CPUs0--3 between its client and numeric server. No numeric warmup is hidden;
cold startup and retirement are reported separately from the warm-service
cell clock. These are experimental, owning-Workspace commands, not a portable
installer or a completed GPU acceleration result.

## Corrected GPU qualification disposition
The corrected header plus owner cancellation returns16complete/8operational
on24sources in630.367s, vs clean native46.054s/24complete. Actual106supportcalls
produce104completedGPUbatches (all singletons) andtwo expired-owner cancellations.
The variant is not admitted to another fullGPU matrix. Its raw Lean/numeric/
batch events and [result review](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/header-correction-preflight24/result-review.md)
are preserved. Backendstdout and exact lifecycle stopwatches are explicitly
missing after a Windows archive-argument overflow; fresh cluster checks confirm
ownJob/Podgone, otherGPUWorkspaceRunning/labReady, sampledsourcePIDsallgone.
No CPU-only threshold closure follows while the corrected CPU series runs.

The formal-prefix analyzer reports original32-candidate-block outcome counts
and source-associated transitions for each closed pair. It keeps operational
results unknown and retains its existing validated-whole-ratio rule.
Native-complete source counts are not benchmark pass@32. The implementation's
nativeCommandBatch discards candidate-returned state; width4 and state cleanup
are documented separately from the upstream full-service claim.
Actual fullminiF2F reference and32-source regression are published under
formal-default/minif2f/.


### Corrected-family wall attribution

Build with python3 build-cost.py --out /tmp/gpu-smt-linarith-oracle-20261017/corrected-wall-cost,
then use the retained Kimina Python interpreter with run-corrected-cost.py
--out <new-output> --cost-profile --cost-root <build-output>
--methods fast-hybrid oracle.
This selects only the matching diagnostic arithmetic family, serializes complete
telemetry rows and builds into its own directory. Profile clocks have their own
denominators; they cannot be relabelled as an earlier uninstrumented primary.
See [qualification and full launch](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/corrected-wall-profile/result-review.md).


### Large-LP racing

Build with python3 build-race.py in the owning Workspace. The current private
output is race-oracle-pooled. Run run-race.py with explicit
GPU_ARITHMETIC_RACE_MIN_ROWS from the retained LP distribution; the24-source
qualification used37. The inherited method name oracle-hint means the
CPU-only large-LP ablation here; oracle-gpu enables the GPU competitor.
The mutex covers only borrowing/returning independent native daemon handles.
Every large-LP loser is killed and waited; the GPU dispatcher is cancelled
and joined before cell retirement. Qualification used width8 with shared
CPU0--3 for client/server,48 GiB, RTX5090 and actual batches of at least2.
See the [race protocol and results](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/plan.md).


### Completed own-clock profile and full comparison

The complete [corrected native/oracle profile](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/corrected-wall-profile/full1000-result-review.md)
retains all1,000 sources, successful and failed calls, and actual candidate tails.
Native LP-only zero-cost sensitivity is1.93412x; this does not exclude1.5x.
The full-data row gate is11, from median10, with7,201 small LPs using0.0218CPU s.

In the current run-race.py entrypoint, fast-hybrid means the stronger native
BatchBaseline with concurrent daemon reuse and the unchanged pinned CPU
hybrid. In older run-batch.py records it means the serial native client;
do not pool these conditions. run-native-pooled.py qualifies this native-only
control without the AST oracle. oracle-hint is the CPU AST-oracle candidate,
and oracle-gpu adds the external GPU race. Full width8 CPU0--3 cells run
sequentially. The [full protocol](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/full1000-plan.md)
records48GiB, source-labelled batches, cancellation/rebatch, all costs and
the finite GPU lifecycle dependency. No numerical warmup is performed.
Cancelled jobs' unknown device compute is not zero; job-event accounting
retains submit/cancel/retire separately from delivered solve-time results.
