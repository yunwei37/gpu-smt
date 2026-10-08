# Experiment003: normal Mathlib source component costs

Status: supporting BOOTSTRAP experiment admitted by root; source-qualified and independently approved in round1; actual preflight and full36cell matrix completed, independently result-reviewed and root-audited. See result-review.md and actual raw artifacts for bounded interpretation. Experiment002 remains pending on the already submitted RTX5090 Job; its exact protocol and consumed reviews/preflight count are preserved. This CPU experiment neither replaces real generated candidate traffic nor closes any RQ.

## Research question

RQ4: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

Specific supporting uncertainty: on complete real Mathlib source modules with ordinary checking, is expensive instrumented residual work mainly in native declaration checking, or in tactics/other frontend work? This selects where deeper dynamic profiling/GPU or CPU algorithm work is justified. Previous disabled-kernel Mathlib profile and resident metadata pass cannot settle it. This is a component profile of official source verification, not an accelerated method comparison or final answer about strongestCPU/device performance.

## Paper-value admission

Role: supporting. Largest credible story unlocked: a measured normal-check account of costly native boundaries that can justify or falsify targeting kernel work after imports. Strongest reject argument addressed: the GPU checker route profiles only metadata or disabled-kernel frontend work, so no expensive actual checked boundary is established. Independent evidence: newly executed normal-check complete public module sources across six declared domains with stock native profiler and paired unprofiled overhead controls. No published result or retained raw data establishes these version/workload costs. A large kernel category motivates deeper conversion/dependence/fastCPU investigation; tactic/frontend-dominated costs direct acceleration there and limit the local kernel route. Mixed or highly perturbed profiles leave the route unresolved rather than claimingGPU benefit.

Best alternative now is authentic generated-attempt capture (experiment002), but its required normally assigned5090 Job is Pending/Insufficient GPU. Single-thread/fork fixtures would only demonstrate implementation readiness; another disabled profile repeats a known defect. This finite normal-check source study adds consequential scope while that independent external dependency remains open. It does not weaken the user’s Lean/SMT/real-stream/service/GPU goal. Contradiction bounds only this version/module/profile boundary, not all heterogeneous checking or the central service thesis.

## Primary precedent and assets

Reuse official Lean CLI `--profile`, full public Mathlib sources, normal frontend/addDecl path and GNUtime resources. Exact profiling implementation and limits are source-verified in [E7](../literature-20261007T225255+0000/lean-profiler-boundary.md). Profiler measures exclusive instrumented elapsed scope time within a thread, cumulative globally by category; worker/parent scopes may overlap. The default100ms threshold suppresses individual prints only, not totals. Keep it to limit avoidable observer output. Printed category values have three significant digits, with ms/s units. No trace-profiler/Firefox data is mixed into this experiment.

Exact restored Lean4.9rc1 be6c4894e0a6c542d56a6f4bb1238087267d21a0 and Mathlib2f65ba7f1a9144b20c8e7358513548e317d26de1, exact archived dependencies/vendor packaging adaptations as in native-setup. Six complete source modules selected purposively by domain before any cost inspection:

1. Mathlib/Algebra/Group/Basic.lean
2. Mathlib/Algebra/Polynomial/Basic.lean
3. Mathlib/Data/Nat/Prime.lean
4. Mathlib/LinearAlgebra/FiniteDimensional.lean
5. Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean
6. Mathlib/MeasureTheory/Integral/IntervalIntegral.lean

Actual pinned paths checked; guessed newer split-directory paths were absent and corrected before admission or execution. This is one library/version and six purposive files, not a random full-library sample, candidate stream or two independent corpora. Transitive compiled dependencies load normally; their proofs are not all rechecked. Complete current file source/new declarations are elaborated and ordinarily kernel checked; no skipKernelTC, sorry insertion or parse-only mode. Ordinary Lean may admit actual sorry/axioms; full source/diagnostics remain evidence, not a semantic equivalence proof.

## Comparison and metrics

The profiled ordinary native path is the measured method. Same-module unprofiled native CLI is an observer-overhead control, not a competing accelerated backend or a weak cold-service baseline. StrongestCPU/kernel alternatives remain required by the fullRQ4 promise before any superiority claim; a numerical rerun of them is not needed to interpret this coarse profile boundary.

Primary metrics: stock cumulative per-category elapsed times and each paired unprofiled/profiled complete invocation wall time, including lake/env setup, imports, normal frontend/checking and process completion. Report type checking, import, tactics, residual elaboration and every extra native category without renaming residual elaboration as shareable theorem preparation. Descriptive category shares use the sum of observed categories (or explicitly non-import categories) only, never called wall-clock/CPU fractions, critical paths or Amdahl bounds. Do not sum printed per-scope entries, which are thresholded. No operation count, GPU-ready width, memory-latency or bandwidth claim.

Paired ratio profile/normal wall diagnoses instrumentation plus system variability; all three paired values per module remain visible, medians/ranges are descriptive, no reliable p99/load confidence from three repeats. GNUtime CPU and maximumRSS are diagnostics; maximumRSS is neither fleetPSS nor a matched service memory frontier. Actual affinity/environment/load and all outcomes retained; affinity is not isolation. No interpretation assumes quiet host or equal competing load.

Correctness: every native exit/system failure and complete CLI JSON diagnostic retained. Compare normal/profile diagnostics for the same source, including warnings/admissions/positions; neither profiling success nor accepted exit counts alone establishes proof completeness. Unknown/malformed stdout/duplicate totals/absence of terminal record remains explicit. No failures filtered or interpreted as acceleration. Native profile alone does not certify no-sorry/dependency/theorem identity; source and requested original ordinary checking boundary remain fixed.

## Planned matrix and execution

| Group | Role | Inputs | Paths | Repeats |
|---|---|---|---|---:|
| Native real preflight | Dependency | First complete public group module | Normal and stock-profiled native CLI, same analysis | 1 |
| Full component matrix | Supporting | All six original modules | Normal/profiled | 3 |

36 full cells,18 pairs. For each repeat, finish both paths for each module in declared source order; normal/profile, profile/normal, normal/profile across repeats. Preflight is separate and not substituted for a final repeat. Every planned cell must reach terminal status; partial prefixes are incomplete. No imposed experiment deadline or artificial stop budget. Preserve actual failures/interruption and repair only systematic execution defects on the same fixed metric/oracle, with affected cells rerun distinctly.

From repository root, export exact releasebin PATH, LEAN_NUM_THREADS=1 and retainedcache XDG_CACHE_HOME. Thin capture command `taskset -c 0 python3 bench/lean_profile_modules.py --workspace /workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/mathlib4 --lake /workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux/bin/lake --lean /workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux/bin/lean --out artifacts/lean-module-profile-2026-10-08/full --repeats 3`. Add `--preflight` with distinct preflight output for one module/pair. It invokes stock `/usr/bin/time` around lake/env/lean, with native `-j1 --json`, adds only `--profile` on the profiled path and emits no olean/ilean/C outputs. Capture sets child affinity0 before launch; outer taskset startup is outside the individual invocation clock. Driver invocation wall includes launch, event writing and up to20ms completion polling, then excludes raw fsync/result serialization/source hashing; corpus makespan includes capture lifecycle. Analysis `python3 tools/analyze_lean_module_profile.py --input <capture-dir> --out <new-analysis-dir>`; preserve the executed analyzer bytes alongside capture sources.

Raw stdout/stderr/time metadata/source files/commands/events/provenance retained under artifacts/lean-module-profile-2026-10-08. Native capture code and profile analysis must exist and be reviewed before real preflight. Source hashes/config/analysis meaning frozen before final matrix; future changes retain actual executed version. GNUtime1.9-0.2 restored from Debian official package, not a custom stage timer. Existing exact source build is terminal; no build/inference/GPU concurrency is added to this CPU study.

## Interpretation and output

One descriptive module-component table plus profile-overhead pairs, honest source/compiler/import/trust/thread/rounding limits and all failures. Supporting valid costs choose a future dynamic CPU/kernel profile or frontend/preparation experiment; small kernel share bounds only the observed accumulated scope distribution. No fullGPU checker, fastestCPU comparison, semantic equivalence, real serving speedup, locality or finalRQ4 answer is asserted. Full run requires a fresh result review with no desired verdict. Report valid/invalid/incomplete, supported/contradicted/inconclusive, supporting/dependency-only value and precise local paper impact separately.
