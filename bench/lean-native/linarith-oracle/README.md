# Native arithmetic oracle experiment

Status: experimental, not a production Lean service or demonstrated GPU speedup.
See the [predeclared decision rule](../../../artifacts/linarith-oracle-2026-10-17/plan.md).

- `build-stages.py`: copies the pinned Mathlib control/reconstruction functions into an instrumented namespace, records sequential thread CPU and invocation wall, and builds native code. Original Mathlib is unchanged.
- `Oracle.lean` / `oracle.rs`: one export of supported real/rational comparison expressions, native polynomial/product generation and LP, coefficient/provenance return, selected proof construction and one weighted contradiction check. Unsupported or failed cases restore state and run the original path.
- `Baseline.lean`: established Farkas Fast plus invocation-local product-application reuse with native hybrid/HiGHS certificate search.
- `run-stages.py` / `run-comparison.py`: use the existing Kimina native batch collector; preserve all source outcomes, costs and raw streams.
- `build-oracle.py`: rebuilds the native experiment from the retained sources and dependencies. No original repository or installed runtime is modified.

The scripts currently use the retained owning-Workspace dependency paths (Lean4.27, matching Mathlib/Farkas/Kimina), not a portable installer. Their pinned versions and original build procedures live in the reproduction guide and `artifacts/lean-modern-native-compilation-2026-10-14/`. The restored documented `/tmp/gpu-smt-linarith-oracle-20261017/` path resolves onto the existing Workspace PVC; its original ephemeral contents were lost during Pod replacement. Publish completed evidence back to `artifacts/linarith-oracle-2026-10-17/`.

In the owning Workspace, with no active build using the same output filenames:

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
The recovered full captures were interrupted by the shared-node/volume fault;
see the [retained failure record](../../../artifacts/linarith-oracle-2026-10-17/interruption-20261017T0617.md).
Earlier completed and failed records remain; no lost partial is counted as complete.

The current heavy-cohort continuation is `run-matrix.py EXISTING_PAIR_PID`.
It preserves the already-running first pair and uses its closed receipts.
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
The bounded continuation queues the full strong diagnostic after primary timing;
it does not rerun the stock phase pilot as if it described Fast/hybrid.

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

The three admitted primary pairs are now complete: aggregate1.34668x, below
the more-than1.5xrule. The hourly app automation is deleted and this route is
closed as mainline. See the [decision and retained raw results](../../../artifacts/linarith-oracle-2026-10-17/decision-20261017.md).
Only the already-requested full phase/prefix captures continue to finish the
report; this guide is not authority to start a new variant or timing grid.

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
