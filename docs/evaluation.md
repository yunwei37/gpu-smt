# Evaluation: current evidence and open work

Updated 2026-10-30 UTC. Root owns paper/evidence integration; all root reviews
are **self-review (自审)**. The four frozen RQs remain open.
The current paper is [docs/paper](paper/).

The [verbatim previous frontier](tmp/build-and-evaluate/step-0212-20261030T173551+0000/experiment-001/evaluation-before-step0212.md) preserves all prior statements,
numbers and links. Its links retain the original docs/evaluation.md base;
the [historical Git view](https://github.com/yunwei37/proofserve/blob/b7a77f868b9ea844c6554fcc7b04e115d104f7e1/docs/evaluation.md)
preserves their navigation. Earlier archives and raw failures are unchanged.

<a id="current-decision-frozen-oracle-and-three-continuing-directions"></a>

## Authority and scientific scope

W/M/O retain their own workload/mechanism/open-source paths; root integrates
their evidence. The mainline awaits W/M results and user decision. Keep the
four continuing directions and Lean/SMT/OSDI objective, without a new deadline
or replacement cache-only/negative-paper thesis. CPU oracle remains frozen;
E038/narrow GPU routes stay closed. Preparation, ordinary scheduling, generic
caching and reflection alone are not new-contribution claims.
Authority: [user words](user-instruction.md), [initial narrative](idea-story.md),
[author decisions](questions-for-author.md).

| RQ | Frozen question | Current status |
|---|---|---|
| RQ1 | How much expensive native preparation can real verification candidate streams share across independent jobs? | unanswered:complete preparation-cost/context coverage remains missing |
| RQ2 | Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation? | unanswered:full native artifacts,history,cancellation and supported scopes remain incomplete |
| RQ3 | How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse? | unanswered:one full warm-resource pair is complete with limits;scaling/repetition promises remain open |
| RQ4 | After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path? | unanswered:no useful extra full-flow GPU gain has been demonstrated |

<a id="resource-point-and-workloads"></a>
<a id="resource-point"></a>

## Resources and comparisons

Same gpu-smt-dev/phobos-vt/PVC. User shares:40GiB total, W16/M16/O4/root4,
each at most8cores. Root uses CPUs0–1 for small analysis/builds. Captures,
datasets and binaries remain on the existing PVC outside Git. Own signal
controls return errno13; no working external-signal watchdog is claimed.
Finite self-exit points charge retained processes. One-second RSS sampling
may overshoot and is not a hard quota. Historical lab48GiB/four-worker,
older two-worker24GiB-AS and G10 points keep their own resources and clocks.

<a id="resource-layer-diagnosis-and-missing-warm-comparison"></a>
<a id="complete-nativemathlib-derived-pair"></a>

## Strong warm-service and failed-candidate evidence

The [complete7808pair](../artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md)
takes warm25176.4873s/engine20323.0076s:1.238817×,19.2778%less elapsed,
with7808status aliases/3014accepted IDs equal. There are7682raw payload
differences and23rejected-source differences after env/empty-AST removal.
One ordered shared-host pair,affinity,retries and support work do not isolate
COW or prove a general gain. Old21693.76s two-worker and own-fresh1.24028×
are separate comparisons; the former also has six state differences.

[Fixed42solo](../artifacts/engine-resource-profile-2026-10-25/solo42-native-library-20261029/README.md):
41watchdog failures/1timeout/0restored accepts,complete;do not restart old queues.
[Resource reanalysis](tmp/build-and-evaluate/step-0183-20261030T112405+0000/step-report.md):
11of52concurrent resource failures become timeouts in solo retry. Global cap,
goal and tactic do not form a stable per-call failure certificate.
[480profiles](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md):
83timeouts/355ordinary/42resource;timeout-thread CPU55.19%interval_cases/
28.21%simp_all is not full-candidate wall.71prototypes establish no reliable
early-failure rule.
[Scheduling](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md):
21746.81s all/15385.39s first-original/15112.12s first-short,same142tasks,
old two-worker point. This is pass@k,not every-candidate RL rewards or novelty.
Held-out source-cost ordering did not beat FIFO; no repeat.

## Workload characterization

OpenAI/math4eaee875,Lean4.34.1/Mathlibd13f23b7:163097source files and
1354379lexical decide+kernel sites are not executions,cache misses or costs.
The [paper's native table](paper/main.tex) retains each separate point:
7baseline/7profile;82expanded50k;47incremental100k;109wider;Grid300sprofile/
634.280s unprofiled;14after-Grid;180.276s Amplitudes;109new-strata;two
authored-options sources;189original-options sample calls;11remaining calls.
Different budgets,prerequisites,workers and clocks are never pooled as a
homogeneous full build.491completed Grid-profile events plus unfinished work do not
partition wall; the intervals overlap. Seven-source1.13%profile difference is a single fixed-order
observation. Compilation is not full-service acceptance or full-axiom audit.

[Step0205](tmp/build-and-evaluate/step-0205-20261030T152520+0000/step-report.md):
new-strata109calls/106compile/2HB/1remainderwall,2984uninvoked.
Final call has8.030s,not300s;two unchanged sources later compile after removing
the100kCLIoverride,7.934/33.878s,not a same-budget gain.
[Step0210](tmp/build-and-evaluate/step-0210-20261030T170436+0000/step-report.md):
189calls/187compile/1missingRellich/1remainderwall,47blocked dependents;
1399.505203wall/2539.433437CPU s.16cached targets freshly remeasured,
171new dependencies. Last call11.734s,not600s.19of42probability endpoints
and6of21complete cells;23costs missing. .olean-only,not full Lake artifacts.

[Latest remaining23 audit](tmp/build-and-evaluate/step-0212-20261030T173551+0000/step-report.md):
11calls/7compile/2memory diagnostics/2selfalarms;8blocked/10724never-started,
no new endpoint cost. Exact source,authored HB,j8/M8192,CPUs0–7.
Native wall1399.897144/CPU1894.702852s,capture1406.532695s.
Memory exceptions156.589663s/full600.120081s censor/remainder106.116280s
sum862.826024s,61.63%of this selected dependency-heavy point only.
Interpreter-tag memory exceptions exit-11;the tag is a check site,not tactic
CPU or an intrinsic invalid-goal claim. Same19/42costs,23missing. No easy
replacement draws,missing-as-zero,successful-subset whole-library estimate
or finite population95%CI. Combined sample12.49GiB includes retained EPFL.

[Native363metadata](tmp/build-and-evaluate/step-0205-20261030T152520+0000/step-report.md):
89268theorems/47989auxiliaries/44528Exprkeys/44532level-private groups.
45661decision-shaped helper names in90modules form42610types;
933repeat/919cross-module.3051extras split1497within-module+1554cross-module
module/key extras. Actual hidden/export/cache state,misses,cost and full
axioms remain unknown.135-object45distinct pilot is not generalized.
[Source/native units](tmp/build-and-evaluate/step-0210-20261030T170436+0000/step-report.md):
42886source sites vs45661retained helpers;Jet50944/3938 and
Canonical240114/600,each helper type distinct. Branch syntax is observed,
event attribution is not. AuxiliaryGram0sites/1helper limits the predicate.
[Module exposure](tmp/build-and-evaluate/step-0206-20261030T155146+0000/step-report.md):
48of109calls containing cross-module types use454.207083/1399.655781s
(32.45%),including all module work;this is not duplicate-check CPU/time saved.

[Modern certificate pairs](tmp/build-and-evaluate/step-0208-20261030T164526+0000/step-report.md):
seven Int/list goals,all original/cert sources accepted,all pairs slower:
13.317706→23.936857s whole-source wall;extra theorem checks2.327609→5.757960s,
292checks,not exclusive CPU/first checking/warm service.
Wrong-raw-HB observers excluded;matched45typeprobe only16complete/1partial/
28unreached,60.181s selfalarm,not a completed census.

[EPFL prefix](tmp/build-and-evaluate/step-0185-20261030T113532+0000/step-report.md):
136returns53compile/71ordinary/12budget,623.799s;25.60%budget cost is prefix-only.
Later10k/j1/j2 points remain separate;original stuck source is censored.
[APRIL39pairs](tmp/build-and-evaluate/step-0188-20261030T115336+0000/step-report.md):
35reference passes/4HB;23mutation errors/16budget. Selected50.53%budget cost
vs11.05%inverse-inclusion ratio for released1835rows,not natural arrivals/CI.
[Training construction](tmp/build-and-evaluate/step-0202-20261030T144255+0000/step-report.md):
4836380publisher rows include250k synthetic/8457contract exclusions;stage
filters are not disjoint failure rates.12selected replays3compile/3ordinary/
6HB,55.04%selected budget cost. Six recursion controls in
[step0204](tmp/build-and-evaluate/step-0204-20261030T150458+0000/step-report.md)
do not identify the producer's original invalid-label cause.

## Mechanism evidence and semantic limits

[Retained200source diagnostic matrix](tmp/build-and-evaluate/step-0186-20261030T114011+0000/step-report.md):
flags/diagnostics/InfoTrees equal,rawHB differs63off/62on;838.670bodyCPU/
781.384eqRefl. Conditional indivisible-leaf1.0317× is not a full-flow bound.
[Original-budget50source/150returns](tmp/build-and-evaluate/step-0193-20261030T123624+0000/step-report.md):
19prior-clipped passes restored;rawHBdiff29/30.18forks/seven sources:
2/4/8core body models1.1847/1.2759/1.3404×,own-full-clock models
1.0986/1.1423/1.1713×;snapshot/merge/HB costs unmeasured,no actual parallel gain.

[Complete grid pipeline](tmp/build-and-evaluate/step-0201-20261030T141554+0000/step-report.md):
2004rows/16chunks represent4016016logical cells;2.290783s full collection
includes C compilation/emission/Lean/extra recheck.384additional checks show
overlapping1/2/4/8task lifetimes,median ratios1/1.775/3.102/5.002.
Pre-established declarations/fresh names/discarded environments and per-task
budgets do not implement first-check merging or globalHB parity.

[Complete64source repairs](tmp/build-and-evaluate/step-0207-20261030T161637+0000/step-report.md):
128native calls;original0accepted/13errors/51budget,repaired31/29/4.
Invocation-wall879.431413/285.778088s;separate builds23.010/2.571s.
[Third-family32source point](tmp/build-and-evaluate/step-0209-20261030T165602+0000/step-report.md):
original20errors/12budget,repair2accepted/29errors/1budget;
336.372899/208.961074s native wall,separate3.573/4.124s builds.
One of8historical opportunity sources recovers,not eight.
All33new proofs have standard-three axiom closures/no admissions.
Historical3014+33=3047IDs and142→145/244tasks,58.1967→59.4262%,
is a cross-experiment inventory,not a new7808run or unchanged-source verdict
parity. Old passes retained by union construction,not measured nonregression.

[Remaining four](tmp/build-and-evaluate/step-0211-20261030T172449+0000/step-report.md):
3683tactics return0.963s then an open declaration check at16s;
3703open eqRefl fallback at16s;3698prefix simp recursion (not HB);
3710bridge recursion plus prior omega error. Primary source/diagnostic parity
covers these four plus positive only. Seven changed-source interventions
identify sensitive paths,not equivalent successful acceleration.0.296ms
direct theorem application excludes first imported proof checking;no new
candidate recovery or exact reduction-node diagnosis.33/145inventory unchanged.

<a id="public-lean-code-verification"></a>

## Other retained results

[AutoVerus](tmp/build-and-evaluate/step-0179-20261030T095708+0000/step-report.md):
nonzero exits use~95%process time,top1.6%only3.3–3.4%;JSON/exit disagree,
generation unmeasured. Failure frequency is not heavy-tail concentration.
Verina189:46no-explicit-admission successes/139stubs/4missing-API errors;
simp elapsed slices are not exclusive CPU. LNSym/source checker counts are
not native timings. [Lean-mlir](../artifacts/lean-code-verification-2026-10-25/leanmlir-native-20261027T025426Z/README.md)
40.47/40.21s file/stdin vs94.04s profiled;overlapping LRAT traces do not
partition wall,prior LRAT work limits novelty.

[Final arithmetic screening](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md):
same3014accepted IDs,8.86%slower;34refuted intermediate goals/29ordinary-error
candidates,no timeout removed. Old25/0.2%used invalid wrappers,not final data.
Interrupted8031state/cost capture preserves2640archived returns/one derived
panic with elapsed unknown/at least1273unrecovered observations. Missing
records are not failures,zero hits or a complete run;old queues do not resume.

## Open evidence

Complete requested native workload/context coverage,artifact/history/cancellation
semantics,equal-resource scaling/repetition and useful extra heterogeneous
full-flow gain remain unresolved. No production failure cache,parallel verifier
or generic proof-repair mode is qualified by these selected points.
Paper builds,CI and self-review establish evidence/build health,not novelty
or venue acceptance. Mainline and user decision remain unchanged.

## Historical navigation aliases

<a id="own-load-aware-methods"></a>
<a id="frozen-evidence-and-full-history"></a>
<a id="complete-retry-tail-engagement-2026-10-29"></a>
<a id="elastic-branches-and-complete-state-tactic-caching-initial-opportunity"></a>
<a id="native-input-matching-and-completed-error-cost-actual-measurement"></a>
<a id="actual-population-interruption-2026-10-29"></a>
<a id="current-recovery-status-after-the-storage-eviction"></a>
<a id="g10-continuation-user-directed-separate-hardware-point"></a>
<a id="shared-node-guard-implementation-step0150"></a>
<a id="2026-10-30-resource-tail-and-exact-first-success-opportunity"></a>
<a id="latest-correction-runtime-only-and-cross-proof-call-granularity"></a>
<a id="2026-10-30-root-paper-integration-after-authorized-parallelization"></a>
<a id="2026-10-30-root-audit-of-completed-m1149a59-evidence"></a>
<a id="2026-10-30-root-cross-check-of-w002-and-native-reuse-baseline"></a>
<a id="2026-10-30-integrate-w003-and-m003-without-selecting-a-new-thesis"></a>
<a id="2026-10-30-retained-grid-checks-and-fixed-trace-memory-envelopes-step0178"></a>
<a id="2026-10-30-failure-frequency-versus-tail-concentration-step0179"></a>
<a id="2026-10-30-profiler-changes-diagnostic-execution-step0180"></a>
<a id="2026-10-30-first-released-module-native-costs-and-engaged-timing-hook-step0181"></a>
<a id="2026-10-30-native-failuredependency-cache-precedents-step0182"></a>
<a id="2026-10-30-full-coverage-memory-retries-and-native-outcome-transitions-step0183"></a>
<a id="2026-10-30-released-kernel-checker-fixture-units-step0184"></a>
<a id="2026-10-30-completed-prefixes-do-not-qualify-a-full-native-comparison-step0185"></a>
<a id="2026-10-30-complete200-native-diagnostic-differential-step0186"></a>
