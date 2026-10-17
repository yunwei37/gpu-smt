# Native arithmetic oracle experiment

Status: experimental. CPU stage: 1.34668×; GPU stage: in progress. See the
[CPU-stage result and open GPU decision](../../../artifacts/linarith-oracle-2026-10-17/decision-20261017.md).
All three primary pairs and both full phase diagnostics are complete; see the
[strong-baseline analysis](../../../artifacts/linarith-oracle-2026-10-17/native-stages/strong-result-review.md)
and [prototype analysis](../../../artifacts/linarith-oracle-2026-10-17/native-stages/oracle-result-review.md).
These are CPU results. No production service or GPU acceleration is established.

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
/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python   bench/lean-native/linarith-oracle/run-comparison.py   --out /tmp/gpu-smt-linarith-oracle-20261017/new-preflight   --limit 24 --methods fast-hybrid oracle
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


The matched-cohort analysis also checks unique source ids and original order
against input-top1000.jsonl (override with --input for another admitted cohort).
It reports every cell's whole wall, observed CPU, sampled PSS, native outcomes
and deduplicated offline batch tails. The tails refer to whole grouped-array
batches, never individual proof service latencies or online SLOs.


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
