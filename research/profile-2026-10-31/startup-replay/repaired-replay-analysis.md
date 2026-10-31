# Repaired native kernel replay results
Generated 2026-10-31T07:08:10Z; review: self-review.
This supersedes the failed v2 module-enumeration attempt, whose data remain intact.
Raw data: /workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3. Version: Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release).
Terminal: {'status': 'finished_bounded_matrix', 'rows': 21, 'target_rows': 15, 'target_success': 15, 'scope_rows': 5, 'elapsed_s': 673.5147476298735}.

## Repair qualification
Every one of the 28 prior targets and 13 prior empty controls failed lookup,
not kernel checking. The symlink realpath escaped the checker search roots.
Ordinary hardlinks inside a correctly named artifact tree repair enumeration.
The separate unmeasured E-core functional control exited0, announced the exact
NearPinDeletion target and printed no stderr. Formal timing then rechecked that
same target under the shared P-core lock; the batch could start only on success.
These are stock 4.34.1 leanchecker runs, with matching LEAN_SYSROOT and no custom
kernel or patched checker. --fresh was not used as a path fix.

## Import-relative replay versus construction
Returned 15/15 requested target records; 15 uncensored exit-zero
replays. All numeric ratios below use only qualified successes.
Of thirteen short modules with prior 3-repeat build medians, 13 succeeded.
Their checker process wall median is 3.5103127267211676 seconds; median
checker/full-build ratio is 1.2805046357990424.
This process duration includes CLI module discovery, dependency import, target
kernel replay and cleanup. It is **not exclusive kernel CPU**. The thirteen build
denominators come from the earlier P-core paired startup matrix and include its
observer cost; they are not contemporaneous randomized build/replay pairs.
Read observer-calibration.csv and startup-analysis.md before generalizing.
Grid and Amplitudes ratios use their separately retained historical standard
build durations. They are explicitly labelled in the CSV and are not substituted
into the thirteen-module matched-build median.
- OAI.MeasureTheory.Falconer.Estimates.NearPinDeletion: success=True, wall=2.555695s, peak RSS=1.930GiB, replay/build=2.21954454544492, stop=none.
- OAI.Analysis.Cotype.FiniteRankWalsh: success=True, wall=3.930133s, peak RSS=6.004GiB, replay/build=0.9267021710830023, stop=none.
- OAI.Analysis.Laughlin.FiniteFlux.ComputeRow1115Batch17: success=True, wall=3.675953s, peak RSS=1.279GiB, replay/build=1.5640116027635051, stop=none.
- OAI.Analysis.Laughlin.FiniteFlux.Row0705207: success=True, wall=2.576674s, peak RSS=2.010GiB, replay/build=2.1727444309048156, stop=none.
- OAI.NumberTheory.PadicHodge.IntegralComparison.OrderedCech.ReindexSingle: success=True, wall=2.817109s, peak RSS=2.756GiB, replay/build=1.2805046357990424, stop=none.
- OAI.Analysis.MutuallyUnbiased.MixedSemantics.Zeros30: success=True, wall=3.885028s, peak RSS=6.019GiB, replay/build=1.1513706306495677, stop=none.
- OAI.GroupTheory.PolycyclicRecognition.Analysis.TranslationCovering: success=True, wall=2.600623s, peak RSS=1.919GiB, replay/build=1.8250262545818783, stop=none.
- OAI.Geometry.CylinderCovering.Radial.Assembly: success=True, wall=3.983339s, peak RSS=6.015GiB, replay/build=0.8509680609000353, stop=none.
- OAI.NumberTheory.Catalan.Analysis.ManuscriptNormLogPGroup006: success=True, wall=3.053982s, peak RSS=2.713GiB, replay/build=1.3384695968513174, stop=none.
- OAI.Analysis.CircleDomains.Rigidity.MaskedCircleEnergy: success=True, wall=3.895815s, peak RSS=6.019GiB, replay/build=1.0624986421111173, stop=none.
- OAI.Analysis.MutuallyUnbiased.GramAssembly.Block0Data: success=True, wall=3.918764s, peak RSS=6.010GiB, replay/build=0.8435991548824964, stop=none.
- OAI.Analysis.PlanarPacking.Certificate.WUCert48: success=True, wall=3.291775s, peak RSS=3.443GiB, replay/build=1.4039494938218244, stop=none.
- OAI.NumberTheory.Catalan.Determinants.FixedCompactRow48: success=True, wall=3.510313s, peak RSS=2.617GiB, replay/build=1.1572988127369372, stop=none.
- OAI.Analysis.PlanarPacking.Grid: success=True, wall=253.438516s, peak RSS=2.378GiB, replay/build=0.39956878413583924, stop=none.
- OAI.Analysis.PlanarPacking.Certificate.Amplitudes: success=True, wall=113.617746s, peak RSS=3.245GiB, replay/build=0.630244803827891, stop=none.

## --fresh scope samples
Default replay trusts imported declarations and rechecks target-module constants.
--fresh loads the target, then replays its entire loaded constant map into an
empty kernel environment: it can be much more expensive and is not comparable
to reconstructing only one source module. Both modes skip unsafe and partial
declarations in upstream Kernel.Environment.replay and reuse the stock kernel;
neither is an independently implemented checker. Fresh mode does not mean cold
OS page cache. All samples are separate bounded process invocations.
- Init.Data.Nat.Basic: default=2.026039s; fresh success=True, observed=2.428217s, bound=180.000s, stop=none, ratio=1.1985042406126558.
- Mathlib.Data.Nat.Basic: default=2.194992s; fresh success=True, observed=73.134445s, bound=180.000s, stop=none, ratio=33.318772538739076.
- OAI.MeasureTheory.Falconer.Estimates.NearPinDeletion: default=2.555695s; fresh success=False, observed=180.111180s, bound=180.000s, stop=wall_budget, ratio=.

Censored fresh runs are only observed resource/time limits; no successful replay
duration or exact build ratio is imputed for them. A timeout's observed wall is
not a successful fresh-check cost. Full stdout/stderr and RSS samples are on PVC.

## Measurement and limitations
The submission observed W holder37246 and existing M waiter11027; O joined after
M. Actual kernel lock state at acquisition is in launch.json. The whole measured
matrix holds one existing P-core lock, with affinity0-7, eight runtime workers,
a 1,700s internal block deadline and per-cell bounds. Actual RSS sampling reserves
128MiB for its parent inside the12GiB allocation. Child user/system CPU, wait4
maximum RSS, sampled tree RSS and observer CPU remain distinct columns.
No host settings, other pods, old captures or other lines' paths were changed.
