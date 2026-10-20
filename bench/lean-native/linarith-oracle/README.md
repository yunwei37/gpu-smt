# Lean arithmetic oracle experiments

Experimental CPU certificate-oracle research, with retained GPU attempts.
[Current results, open RQs and resource point](../../../docs/evaluation.md)
are the status authority. The public component, historical measurements and
current whole-service capture have different reproducibility boundaries.

## Build and check the component

[Buildable source and commands](reproduction/README.md) contain the Lean/Rust
bodies, locked numerical dependencies, license and provenance. Supply an
existing matching Lean4.27Mathlib project and a separate build output.
The source builder discovers dependencies through Lake and Lean. The
standalone checker runs CPU HiGHS/exact repair and native proof checking.

This component has a completed64-real-source functional qualification.
It does not recreate benchmark placement, warm REPL state, the stronger
native-reference executable, or historical clocks. Its standalone build/check
commands do not install the experiment's aggregate-RSS watchdog. Do not use
them as an additional unbudgeted shared-lab collection while another runs.

## Reproduce the official HTTP comparison

The existing [kimina-http.py](kimina-http.py) command replays original
source records through the official Kimina app/SDK with declared adaptations.
[Complete instructions and prerequisites](../../../docs/reproduce-checkpoint.md#current-official-http-comparison)
cover the dependency patches, native REPL, strong reference, CPU support
environment, input contract and method boundary. Run --help with Kimina's
Python environment to inspect the actual CLI.

The [current full-population plan](../../../artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/README.md)
uses every original Goedel source and three alternating native/Powerpairs.
Its exact source commit, actual command, preflight, single full launch and
raw records remain adjacent. It is separate from the earlier stopped
eight-worker/per-worker48GiB queues. No completed partial prefix becomes
a population result and no current performance claim comes from --help.

The [current resource point](../../../docs/evaluation.md#current-resource-point)
and [implemented watchdog/qualification](../../../artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/README.md)
govern new research captures. Existing historical recipes are not a work queue
or authority to run another full group. The sampled monitor is not a kernel
hard RSS quota. Retain failures and retirement alongside timing results.

## Read or recompute the evidence

- [Corrected selected1,000 result](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics/full1000-result-review.md):
  whole-flow CPU observation, not global generalization or GPU benefit.
- [Complete selected1,000 official-service matrix](../../../artifacts/linarith-oracle-2026-10-17/kimina-http/full-matrix-result-review.md):
  all raw outcomes and the third-pair restart limitation.
- [Original four-way component block](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-export/full1000-result-review.md)
  and [source-level work attribution](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-export/mechanism-result-review.md):
  do not equate recorded large-LP races with all solves or GPU-removable wall.
- [Formal4.9component result](../../../artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9/full-populations/proofnet-result-review.md):
  complete ProofNet; the older miniF2Fcomponent matrix remains incomplete.
- [Complete SHRED/Kimina miniF2F comparison](../../../artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/full-pair-result-review.md)
  and [ProofNet comparison](../../../artifacts/linarith-oracle-2026-10-17/shred-closing/proofnet-full-result-review.md):
  as-integrated existing-method controls, with changed native outcomes.
- [GPU portfolio execution](../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-cpu-gpu-portfolio/result-review.md):
  actual5090execution and costs, with no demonstrated extra whole-flow benefit.
- [Public-file phase replay](../../../docs/reproduce-checkpoint.md#earlier-arithmetic-phase-analysis-from-public-files):
  recompute archived diagnostics without Lean/GPU; own capture denominator only.

All current implementation, execution and review are root-thread work.
Reviews are self-review, not independent audit. Established warm services,
snapshots, LP search and certificate checking are not individual novelty claims.

## Historical entrypoints

The former389-line guide is preserved [byte-for-byte as gzip](../../../artifacts/linarith-oracle-2026-10-17/arithmetic-entrypoints-through-20261019.md.gz).
Its relative links were authored for this original bench directory; a
[readable pinned copy](https://github.com/yunwei37/gpu-smt/blob/782f026/bench/lean-native/linarith-oracle/README.md)
preserves their original location. It describes dated build-stages/run-batch/run-matrix, formal-prefix,
GPU-support and diagnostic variants, including closed and interrupted routes.
Their source scripts and raw data remain in place. This archive records what
ran; it does not supersede current resource requirements or authorize a
restart. Use the corresponding dated plan/source/terminal records to interpret
a historical result. Do not overwrite an active library or output directory.
