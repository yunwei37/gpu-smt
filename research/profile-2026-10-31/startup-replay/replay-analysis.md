> Historical failed lookup attempt: see [corrected replay results](repaired-replay-analysis.md).

# Native kernel replay and finalized capture
Generated from actual retained records at 2026-10-31T05:52:40Z.
Review: self-review. Raw data: /workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay.
This report does not claim uninstrumented timings, a new checker, or acceleration.

## Terminal coverage
Startup: {'n': 39, 'success': 39}, imports:
{'n': 39, 'success': 39}, Mathlib: {'n': 3, 'success': 3}.
Target-module replay returned 28/28 records, 0 exit-zero uncensored.
Empty-module checker controls: 13/13 records.
Separate perf runs: 5 records;
96 reported hotspot rows. Missing or failed cells are not successes.
Calibration: 21/21 records; observer CPU sum
14.347585 seconds.
All native wall/stop/returncode fields are retained in the CSVs and PVC.

## Replay cost
For the 0 successful replay records, median total checker/historical-full-build
ratio is None. The entire checker process is measured, including
path search, imports, target replay and cleanup. Imported declarations remain
trusted; upstream skips unsafe/partial declarations. Thus this is not the cost
of checking the entire dependency closure from empty state.
Only 13 short modules have new matched full-build repetitions; their separate
ratios are in kernel-replay.csv. The remaining build denominators are historical
A/Grid/Amplitudes runs, not a current randomized paired comparison.
Do not interpret the ratio as removable end-to-end work or a guaranteed speedup.

## Controls and observer costs
checker-controls.csv compares each available small target with a zero-declaration
module with the same direct imports. Differences are between separate processes;
they are not exclusive kernel time and may be negative.
observer-calibration.csv compares the original all-proc descendant scan with
own-task child discovery on historical min/median/max-sized short modules plus
Mathlib. It is a sequential calibration, not a randomized causal estimate.
The original startup observer/preparation cost was about 54.045 CPU seconds;
that overhead is not subtracted from reported wall time. The original and
calibration captures remain separate, including all memory samples.

## Perf interpretation
perf-hotspots.csv lists native perf self-sample symbol percentages, separately
for each import-only profile. The first four are user-space cycles only;
perf-all-mathlib includes user and kernel. Percentages are sampling distributions,
not whole-build elapsed fractions. Profiled wall times are not used as ordinary
timing repetitions. perf.data, reports, stderr/lost-sample diagnostics and exact
commands remain on PVC. No host sysctl or kernel module was changed.

## Startup scale and scope
The complete instrumented first startup matrix is analyzed in startup-analysis.md:
13 short selected modules, import median 1.355 s, cohort import/build ratio about
0.68. Scaling 163,000 identical imports illustrates serial 32.23–144.68 hours,
median 61.34 hours, not a population estimate or parallel build prediction.
The main dataset is conditional on historical small successful modules, with warm
OS page cache and explicit compiler artifacts, not a cold fresh machine.

## Non-success replay rows
- OAI.MeasureTheory.Falconer.Estimates.NearPinDeletion: rc=1, stop=None, wall=2.413s.
- OAI.Analysis.Cotype.FiniteRankWalsh: rc=1, stop=None, wall=2.159s.
- OAI.Analysis.Laughlin.FiniteFlux.ComputeRow1115Batch17: rc=1, stop=None, wall=2.130s.
- OAI.Analysis.Laughlin.FiniteFlux.Row0705207: rc=1, stop=None, wall=2.596s.
- OAI.NumberTheory.PadicHodge.IntegralComparison.OrderedCech.ReindexSingle: rc=1, stop=None, wall=2.138s.
- OAI.Analysis.PDE.Weak.Elliptic.InteriorH1Derivative: rc=1, stop=None, wall=2.135s.
- OAI.Analysis.MutuallyUnbiased.MixedSemantics.Zeros30: rc=1, stop=None, wall=2.147s.
- OAI.GroupTheory.PolycyclicRecognition.Analysis.TranslationCovering: rc=1, stop=None, wall=2.132s.
- OAI.Geometry.CylinderCovering.Radial.Assembly: rc=1, stop=None, wall=2.593s.
- OAI.NumberTheory.Catalan.Analysis.ManuscriptNormLogPGroup006: rc=1, stop=None, wall=2.137s.
- OAI.Analysis.MutuallyUnbiased.TaoCertificate.Rows45: rc=1, stop=None, wall=2.153s.
- OAI.Analysis.CircleDomains.Rigidity.MaskedCircleEnergy: rc=1, stop=None, wall=2.598s.
- OAI.Analysis.MutuallyUnbiased.GramAssembly.Block0Data: rc=1, stop=None, wall=2.137s.
- OAI.Analysis.PlanarPacking.Certificate.WUCert48: rc=1, stop=None, wall=2.136s.
- OAI.Analysis.Conductivity.Variational.VariationalDN: rc=1, stop=None, wall=2.594s.
- OAI.NumberTheory.Catalan.Determinants.FixedCompactRow48: rc=1, stop=None, wall=2.586s.
- OAI.Analysis.MutuallyUnbiased.PairSemantics.Canonical240: rc=1, stop=None, wall=2.132s.
- OAI.Analysis.Triangular.Envelope.EnvelopePsiB: rc=1, stop=None, wall=2.145s.
- OAI.NumberTheory.DirichletL.Eisenstein.SourceProjection: rc=1, stop=None, wall=2.591s.
- OAI.NumberTheory.DirichletL.Cusp.ResiduesModThree: rc=1, stop=None, wall=2.139s.
- OAI.GameTheory.SnakyTwentyOne.Cards.Height12Part04: rc=1, stop=None, wall=2.617s.
- OAI.Computability.Logspace.EstimatorBounds: rc=1, stop=None, wall=2.601s.
- OAI.Probability.TraceReconstruction.Binomial: rc=1, stop=None, wall=2.131s.
- OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41: rc=1, stop=None, wall=2.155s.
- OAI.Analysis.PlanarPacking.Certificate.UMoments9: rc=1, stop=None, wall=2.548s.
- OAI.MathematicalPhysics.Transonic.Certificates.Barrier50: rc=1, stop=None, wall=2.600s.
- OAI.Analysis.PlanarPacking.Grid: rc=1, stop=None, wall=2.142s.
- OAI.Analysis.PlanarPacking.Certificate.Amplitudes: rc=1, stop=None, wall=2.131s.
