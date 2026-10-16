# Evaluation: current evidence and open questions

Current analyzed frontier: 2026-10-16T07:45:59.725269+00:00. Root implements, runs, analyzes and writes
in the retained gpu-smt Workspace on main. BOOTSTRAP remains unfrozen; all four
RQs and the full Lean-first/SMT/RTX5090/paper objective remain open.
Last published head is fe13c12; unfinished Step0010 is uncommitted/unpushed.
Root self-review is not independent audit. [Current step](tmp/bootstrap/step-0010-20261014T133154+0000/step-report.md).
[Previous frontier and detailed history](tmp/bootstrap/step-0010-20261014T133154+0000/evaluation-history-20261016T025154+0000.md) is archived verbatim,
including its original observation dates and superseded partial counts.
Its relative links were authored from docs/evaluation.md. Current result reviews
below own the evidence; a live handle must be checked rather than inferred here.

## Research questions and evidence still required

| RQ | Current evidence | Still required |
|---|---|---|
| RQ1: expensive preparation shared by real streams | Original candidate/header associations, competent native reuse and scoped CPU observations | Native preparation expense, actual service submissions, multiple projects/contexts and unrelated-work controls in both families |
| RQ2: native responses/artifacts and independent cancellation | Scoped full-source controls, retained differences and invalid earlier epochs | Final supported branch behavior/artifacts, incomplete proofs, history, cancellation and resource behavior |
| RQ3: equal-resource service frontier | Complete 30-cell ProofNet replay loses branch latency; complete SMT source experiment is negative | Complete final workload/load/concurrency/PSS/CPU/placement/lifecycle matrix and repetitions |
| RQ4: heterogeneous checking after strong CPU reuse | Complete negative ProofNet GPU version, completed and pending CPU comparisons | Strongest relevant CPU residual, useful expensive device work, full setup/transfers/fallback, formal coverage and uncertainty |

The [Initial Narrative and evaluation promise](idea-story.md) remain unchanged.
Complete acquisition, compiler availability and positive controls do not close
an RQ, establish system novelty or prove venue acceptance.

## Formal workloads and common boundaries

| Cohort | Population and producer | Scope |
|---|---|---|
| GoedelWorkbook4.27 | All 29,750 released sources; 3c2afe6b, Lean4.27/db93fe16, Mathliba3a10db0 | Published proof outputs/migration failures, not all model rollouts or an arrival trace |
| ProofNet attempts | 5,952 candidates, 186 tasks × 32; retained producer4.9 | Complete source-native GPU/service cohorts; versions/protocols remain separate |
| miniF2F attempts | 7,808 candidates, 244 tasks × 32; Lean4.9.0-rc1/be6c4894e0a6, original Mathlib/Aesop | Earlier unrestricted native epoch failed; default-GC CPU epoch is distinct |
| AutoVerus sources | 3,566 original Rust candidates; pinned Verus33269/Z34.12.5 | Native source/frontend/solver interactions; source-sort is not a historical arrival trace |

Current official-service CPU captures use upstream 12GiB/300s/default23pool/
unlimited-reuse settings and four HTTP requests in flight. The proposed custom
8GiB limit remains unapplied and [does not block the default route](questions-for-author.md).
Original bytes/order, producer options and every outcome remain. Whole clocks
charge input persistence, startup/import/library load, verification, transport,
capture/logging, replacement, shutdown and EOF; software build and final ZIP
are outside. Request durations overlap and are not CPU/makespan fractions.
Native payload comparison excludes only the proven adapter timer.
Affinity is shared eligibility, not isolation; separate blocks cannot supply
each other's denominators. Old ignored-gc/invalid-header epochs remain
[distinct and retained](../artifacts/lean-modern-native-compilation-2026-10-14/no-gc-baseline-supersession.md).

## Complete CPU observations and active formal acquisitions

Counts describe the latest analyzed complete conditions, not partial-prefix
performance. Each row uses its own matched resource/version/protocol block.

| Comparison | Complete analyzed evidence | Remaining declared scope |
|---|---|---|
| Original GC → native compilation, Goedel | 4/8 conditions; two pairs 32,945.979→15,835.679s and 38,443.590→18,306.126s, 51.93%/52.38% lower | Third pair and two profiles |
| Compiled Mathlib → native exact oracle, Goedel | 8/8; three primary results 4.73% slower, then 18.66%/1.40% lower; mixed signs | Acquisition/root review complete; no stable general gain |
| Tiered/hybrid/HiGHS, Goedel | 10/12; hybrid 10.61%/5.22%/23.43% slower; HiGHS 11.83% slower/11.45% lower/21.47% slower than tiered; tiered resource capture complete | Two separate hybrid/HiGHS resource profiles; no final global winner |
| Full/Fast × hybrid/HiGHS, Goedel | 9/16; two complete four-way blocks: Fast under hybrid 4.52% lower then 8.50% slower; under HiGHS 7.87%/6.12% slower | Third Full/HiGHS complete; its same-block counterparts and four resource profiles remain; no universal winner |
| Fast/hybrid → product reuse, Goedel | 8/8; primary reductions 9.82%/12.79%/15.39%, descriptive mean 12.67% | Acquisition/root review complete; no global CPU ranking |
| Original oracle → product reuse, Goedel | 6/8; all three primary pairs: 0.586% slower, then 5.110%/14.303% lower; descriptive mean 6.276% lower, mixed signs | Two separate resource profiles; no stable uniform gain |
| GC → selective native arithmetic, miniF2F | 7/8; all three primary pairs 7.61%/10.74%/16.96% lower, descriptive mean 11.77%; p99 worse in first two and lower in third | Original resource profile complete; compiled profile pending; no paired resource saving yet |

[Compilation review](../artifacts/lean-modern-native-compilation-2026-10-14/gc2-first-pair-result-review.md)
retains 25 first-pair differences and 33 second-pair basic transitions plus
one operational-to-operational diagnostic change. The second has no direct
complete/rejected flip; failures stay charged. Compilation is prior art.
[Native exact complete review](tmp/bootstrap/step-0010-20261014T133154+0000/native-oracle-complete-matrix-result-review.md)
retains all operational/native changes and reference drift; its single
sampled PSS comparison 6,561,664→7,478,115KiB supplies no memory saving.
[Product complete review](../artifacts/lean-modern-native-compilation-2026-10-14/product-application-first-pair-result-review.md)
retains 10/11/6 primary native changes and seven profile transitions.
Sampled PSS is 7,674,160→6,961,995KiB with 33/7,051 and 34/6,198 incomplete
non-atomic samples: no exact or replicated memory advantage.
[Original-oracle product review](../artifacts/lean-modern-native-compilation-2026-10-14/stock-products-first-pair-result-review.md)
keeps both timing signs. [MiniF2F review](../artifacts/lean-native-compilation-2026-10-14/gc49/first-pair-result-review.md)
keeps all failures and the mixed tail-latency behavior despite lower whole elapsed.

[HiGHS trio review](../artifacts/lean-modern-native-compilation-2026-10-14/highs-native-cpu-first-trio-result-review.md)
and [Full/Fast review](../artifacts/lean-modern-native-compilation-2026-10-14/farkas-fast427-first-fourway-result-review.md)
retain source19124 complete→rejected recursion-depth errors and other native
differences. No source/depth adjustment or selected retry repairs the result.
The [paired CPU plot and source](paper/figures/plot-cpu-paired-whole-time.py)
show all three observations from two completed comparisons. Different references/
affinities prevent cross-row ranking. Separate profiles are not extra primary
repetitions; observed ranges are not confidence intervals. Shared-background
reference drift prevents an isolated causal explanation or global winner.
The getrusage-based counter is not validated exhaustive descendant CPU.

## Generator availability and batch consumer

All 13,760 candidates retain task/sample/source associations in four real RTX5090
serial-generator segments, plus 24 returned orphans/open/partial tails.
The clocks measure output availability, not verifier-request arrivals.
Official Goedel batches generation and then reads a completed file for batched
verification; synthetic offered load is not a replay of these output clocks.
Mini has one original header/zero duplicate non-None code occurrences; ProofNet
has 17 headers/121 duplicates. These do not measure preparation cost.
[Full source/consumer-boundary review](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-031/result-review.md).

## Actual warm-header engagement in the modern corpus

Two complete GC2 captures account for every original source once:
original executes 67 headers/29,683 started-REPL reuses, compiled executes
60/29,690. An every-request-import control would weaken this competent baseline.
Counts do not isolate preparation CPU, latency or memory.
[Source/log characterization](tmp/bootstrap/step-0010-20261014T133154+0000/native-warm-reuse-characterization-result-review.md).

## Complete native service-load cohort

E023 completes 30 ProofNet conditions/178,560 attempts. At the highest
synthetic rate 19.56/s, branch arrival p95 is 7.08–8.44× warm, with queue waiting
dominant. Basic outcomes match; single incomplete/non-atomic PSS profiles do
not establish a replicated memory frontier. Both E023 and E020 explicitly
warm LibrarySearch(True): E023 observes 6.69–6.93s wall, E020 9.26–10.03s
within initialization. These are modified preparation protocols, not untouched
official-service or request-derived preparation costs; no causal subtraction.
Mini calibration/offered-load scope remains missing: no complete 60-cell claim.
[Service review](../artifacts/lean-service-lifecycle-2026-10-13/experiment023/result-review.md),
[preparation qualification](tmp/bootstrap/step-0010-20261014T133154+0000/e023-preparation-scope-result-review.md).

## Complete repaired-registry SMT experiment

All 12 conditions return 3,566 sources each, 42,792 executions. Stock→branch
whole time rises 36.07%/37.91%/28.84% (mean 34.27%), with actual 2,316 parent
hits per condition. All 14,264 stock/branch comparisons including the profile
qualify native inputs/results/artifacts. Three logical-source stdin annotations
remain: all 12 acquired, ten strict-complete, not universal logical superiority.
Single sampled PSS is 224,644/783,477/791,914KiB for stock/branch/logical; no
stock-relative memory saving. Recorded getrusage CPU rises 23.57% on average,
not validated total-tree CPU. This tested constructor is closed.
[Full review and raw/source records](../artifacts/autoverus-native-2026-10-09/experiment025/full-registry-repaired1-result-review.md).
Old 31-status-change/hit-refusal/fallback epochs and the retained oversized
derivative/restore receipt remain in the archived history and current review.

## Closed optimization branches and retained failures

- Native6 scalar GPU loses 1.74%/3.64%/1.58% in complete ProofNet pairs.
  One CUDA thread plus synchronization returns 2,201 supported operations
  among about 2.38million observed calls (0.0925% count, not CPU coverage).
  No full miniF2F GPU result; its old unrestricted epoch failed with host OOM.
- E029 shared-process placement loses 22.64%/18.72%/15.13%; E023 per-candidate
  branching is closed for its measured workload/load/protocol.
- The complete SMT prefix constructor is closed. Plain FP64hybrid loses all
  three tiered comparisons; its whole-time acceleration hypothesis is unsupported.
  Mixed HiGHS remains a declared comparator; finish existing profiles without
  new mode-only tuning or transfer to differently composed CPU methods.
- Deferred product construction's three five-source pairs lose a mean10.97%;
  E027 projection is closed and E028 cache evidence unstable. E030 response
  extraction has a scoped three-pair mean1.63% lower elapsed, not system novelty.
[Disposition and reopening rationale](tmp/bootstrap/step-0010-20261014T133154+0000/negative-routes-disposition-20261015.md),
[GPU cost/source analysis](tmp/bootstrap/step-0010-20261014T133154+0000/gpu-cost-reanalysis.md).
Do not stitch versions/protocols, filter failures or revive these constructors
with metadata-only numbers. Old native4 approximately33% is historical; sharing
the GPU is not established as the cause of loss. Historical20.9× metadata and
14.6× warm-REPL values are not complete-verification speedups.

## Native costs and device selection

The original-route trace profiler returns all29,750sources, with29,689body
profiles and61operational sources without one. Linarith dominates recorded
leaf-wall traces, which overlap and are not CPU fractions.
[Complete trace/source review](../artifacts/lean-modern-native-compilation-2026-10-14/dynamic-profile-complete-result-review.md).
Finite cuOpt26.8 qualification uses nine saved LPs×three methods: forced GPU
repairs4/9 then falls back5; CPUdual/defaultconcurrent repair9/9. Default may
execute onCPU; these are engagement controls, not full Lean/GPU performance.
[Device scope](../artifacts/lean-modern-native-compilation-2026-10-14/cuopt-lp-qualification-observation.md).
Farkas/Fast/lp, native compilation, GC and product specialization are prior
mechanisms; generic process isolation/preloading also faces AXLE/snapshot prior
work. [Closest-work map](background-related-work.md). No systems novelty is established.

## Native CPU residual observation (E032, full capture complete)

All29,750sources return, with5,401,763userCPU samples/no reported loss and exact
exclusive-period reconciliation. Against recorded userCPUperiod, overlapping
Children displays are35.00%Meta equality,16.96%sparse simplex,10.81%typeclass
synthesis; importModules displays0.36%. Import weight is neither all preparation
nor cold-to-warm savings. These are not purekernel/wall/GPU fractions.
Reference decrement/small allocation total20.045619%native exclusive period,
not an exhaustive runtime category. Full5,665,548,374byte recording and95available
ELFs are retained outsideGit; one missing temporaryvDSO stays explicit.
[Complete sampling/source/error-retention review](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-032/result-review.md).
These costs belong to the compiled original route, not a selected fastest composition.

## Exact numeric-query screening on a separate Fast/hybrid profile

The full log has62,197parseable LPs/30,898ordered unique problems/31,299repeats;
29,908successful calls follow an earlier successful completed same problem.
Their intervals are19.333910%of summed logged-call wall, not savedCPU or makespan.
Actual coefficients reach106,285bits. All28malformed lines and the original
reader failure remain; source texts are not fully mapped to input attempts.
Existing Meta caches and these scope limits do not justify blind generic caching.
[Complete screening](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-032/reuse-screening-result-review.md).

## Complete supporting Meta operand/cost observation

E033 returns all29750original source bytes/order/indices, driver0. Existing
analysis qualifies345thread files with0parse/clock errors and no live observed
native process. Three terminated outer calls/84nested entries remain censored.
Of observed completed outer instrumented threadCPU,76.39%has expression or
universe metavariable flags at entry;18.01%has no variable/level-parameter flags.
These overlapping descriptors are not wholeCPU fractions, parallel readiness,
GPU eligibility or an Amdahl bound. Static-link/DSO/observer bias remains.
Existing full E032sampling places instantiate_mvars_fn::visit at1.93%Children;
metavariable prevalence does not establish a costly substitution hotspot.
[Full actual results, source and root decision](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-033/result-review.md)
retain counters, incomplete work, source qualification and reader-path repair.

## Next decision

Keep existing CPU/formal acquisitions running without another plain CPU tuning
matrix. Main work is a real Lean/GPU implementation: qualify independent native
normalization/comparison work and its state/representation boundary, then compare
complete device cost to the same-algorithm and competent compiled CPU routes.
The new full Meta observation is selection evidence, not an implemented mechanism.
Do not add another failed scalar/import/placement microvariant.
Complete actual preparation/service streams, equal-resource frontier,
native artifact/cancellation behavior, strong competitors in both families,
fullpaper/gates/independent audit and completed-step main publication remain.
The paper and twelve adapted root writing passes do not close these requirements.
