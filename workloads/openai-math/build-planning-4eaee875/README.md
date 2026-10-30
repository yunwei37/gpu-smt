# Build planning before a native pilot

Pinned source: openai/math 4eaee87548250b2682affda7d05d947c05554bae.
These are conditional planning models, **not calibrated runtime/RSS predictions**.
Source size and import graphs cannot bound arbitrary kernel reduction.
No Lean build, toolchain installation or Mathlib cache download ran here.

## Work, span and hypothetical parallel schedules

All-source scope: 163,097 modules / 1,785,499,363 bytes.
Default Lake target OAI imports a smaller closure:
130,834 modules / 1,397,800,941 bytes. The source archive count is not
automatically the work performed by plain lake build. Other library globs
and preserved challenge sources require explicit targets.

Assume one CPU thread per module job, no memory stalls, external dependencies
already built, and a work-conserving scheduler prioritized by remaining
weighted path. Work is unchanged by worker count. Reported wall is a simulated
list schedule, not just division by cores.

| Assumed module cost, all-source scope | CPU-hours | 8-core wall h | 24-core wall h | Weighted critical path |
|---|---:|---:|---:|---:|
| 1 s / module | 45.30 | 5.66 | 1.89 | 451 s / 451 modules |
| 10 s / module | 453.05 | 56.63 | 18.88 | 4,510 s / 451 modules |
| 60 s / module | 2,718.28 | 339.80 | 113.27 | 27,060 s / 451 modules |
| 1 s startup + bytes at 64 KiB/s | 52.87 | 6.61 | 2.20 | 598.13 s / 449 modules |

The corresponding default-OAI closure byte scenario is 42.27 CPU-hours,
5.28 h at 8 cores or 1.76 h at 24 cores. Its 10 s/module scenario is
363.43 CPU-hours, 45.43 h / 15.15 h. The coefficients are assumptions, not
learned from this workload. Large decide computations can exceed every row.
No finite confidence interval for real total CPU time follows from these
static data. Cache acquisition, external package compilation, filesystem
contention, repeated native failures and Longhorn rebuild I/O are additional.

conditional-build-time.csv includes work/span lower bounds and scheduled
wall; default-root-build-time.csv keeps the two workload scopes separate.
model-critical-paths.csv records the exact paths under each assumed model.

## Memory and disk are separate, uncalibrated dimensions

At 1/2/4 GiB peak RSS per independent module job, eight jobs need roughly
8/16/32 GiB and 24 jobs need 24/48/96 GiB, before controller memory.
Thus eight available cores do not imply eight admissible workers under W's
16 GiB. Actual imported environments, kernel temporary data and largest
single-module RSS remain unknown. Source bytes alone cannot certify a fit.
W's eventual pilot retains one Lean process at a time, using no more than
8 cores; hypothetical 24/8-job full builds are projections, not W launches.

For all sources, source plus build artifacts at assumed artifact/source
ratios 2/10/40 need 4.99/18.29/68.18 GiB, excluding toolchain and package
caches. There is no measured artifact expansion ratio yet.
The pinned upstream README warns of vm.max_map_count problems for a full
library build and recommends compiling small portions. No sysctl, mmap,
allocator, Workspace or node configuration was changed by W.

## Stratified pilot and dependency closures

Stratify by source-size percentile 0–50 / 50–90 / 90–99 / 99–100,
import depth 1–10 / 11–100 / 101+, and decide+kernel presence.
21 nonempty cells, two modules each, seed20261030:42 probability targets.
Inclusion probabilities are saved in strata.csv. Retain expensive or
budget-exceeded samples; do not replace them with easier targets.
Only probability targets carry population weights. Dependency modules and
purposeful stresses are not extra random observations.

Eight project medians cover MutuallyUnbiased, Ramsey, PlanarPacking,
Transonic, SnakyTwentyOne, MatrixFields, SubexponentialSAT and Progressions.
project-closures.csv records complete project closures. Additional stresses
cover the largest source, most decide+kernel calls and deepest non-root.
phaseA-targets.csv names all53 targets.

The naive deepest-node stress was OAI itself:130,834-module closure,
nearly a full build. It is explicitly deferred, not silently dropped from
a population estimate. The replacement stress is
OAI.Combinatorics.Progressions.Main at depth450.

PhaseA union:12,785 internal modules /252,627,947 source bytes (0.235GiB),
146,375 decide+kernel occurrences and1,285 external import modules.
Full closure membership is saved. At10× /40× artifact/source expansion,
internal source+artifacts need2.59 /9.65GiB, before external caches/toolchain.
These are disk scenarios, not proof of a16GiB native memory fit.

## Native execution after expansion notification

1. Recheck writable capacity/free space, source ownership and native processes
   in the same Workspace/PVC. No setup before expansion is confirmed.
2. Prepare Lean4.34.1 and the pinned manifest with upstream compatibility
   patches; acquire locked Mathlib cache via lake exe cache get.
   Measure actual disk growth before more package setup.
3. Build dependency-first, one Lean process at a time, with finite heartbeats
   and natural termination. W aggregate RSS16GiB /8cores /under30min.
   Measure CPU, wall, RSS, diagnostics and budget interruptions.
4. Time each target after closure artifacts exist. Report setup/closure
   compilation separately; uncompleted targets are censored, not zero cost.
5. Fit per-stratum native costs and RSS, propagate uncertainty, then recompute
   8/24-core schedules with measured memory admission. Until then the full
   build rows are conditional scenarios, not calibrated predictions.

The pilot is a feasibility/coverage probe, not full project acceptance.
No syscall/node/Workspace/mmap/allocator configuration is changed.

## Reproduce static calculations

Run plan_build.py followed by refine_sample.py, both with
--inventory workloads/openai-math/static-4eaee875 and a persistent --out path.
The initial analysis took22.01s/385,152KiB peak: Python analysis, not Lean.
Naive sample and refined phaseA outputs are both retained.

Primary Lake glob semantics:
https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/lake/Lake/Config/LeanLibConfig.lean
