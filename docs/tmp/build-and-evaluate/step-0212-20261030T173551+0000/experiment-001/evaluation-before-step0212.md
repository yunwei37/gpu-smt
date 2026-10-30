# Evaluation: current evidence and open work

Updated 2026-10-30 UTC. Root owns paper/evidence integration; all root reviews
are **self-review (自审)**. All four frozen RQs remain open.
The [verbatim prior frontier](tmp/build-and-evaluate/step-0204-20261030T150458+0000/archived-evaluation-before-step0204.md) retains every result, failure,
partial run and historical statement. Its relative links were written from
docs/evaluation.md; [the historical Git view](https://github.com/yunwei37/proofserve/blob/09a60a246b917b99d91d5d51aacee854e1fd36aa/docs/evaluation.md)
preserves their original navigation. No raw or other owner's file is removed.

<a id="current-decision-frozen-oracle-and-three-continuing-directions"></a>
## Authority and scope

Existing W/M/O forks own workload/mechanism/open-source paths; root integrates
evidence and paper. Mainline selection awaits their results and user decision.
The four continuing directions and Lean/SMT/OSDI objective remain; no switch
to a cache-only thesis, short negative paper or self-imposed deadline.
CPU oracle is frozen; E038/narrow GPU routes stay closed. Prepared state,
ordinary scheduling, reflection and generic caching are not novelty claims.
Authority: [verbatim user words](user-instruction.md),
[initial narrative/evolution](idea-story.md), [author decisions](questions-for-author.md).

| RQ | Frozen question | Current status |
|---|---|---|
| RQ1 | How much expensive native preparation can real verification candidate streams share across independent jobs? | unanswered:complete preparation-cost/context coverage remains missing |
| RQ2 | Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation? | unanswered:full native artifacts,history,cancellation and supported scopes remain incomplete |
| RQ3 | How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse? | unanswered:one full warm-resource pair is complete with limits;scaling/repetition promises remain open |
| RQ4 | After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path? | unanswered:no useful extra full-flow GPU gain has been demonstrated |

<a id="resource-point-and-workloads"></a>
<a id="resource-point"></a>
## Resource and measurement boundaries

Same gpu-smt-dev Workspace/phobos-vt/128GiB PVC; user allocation40GiB total:
W16/M16/O4/root4, each at most8cores. Root small analyses/builds use CPUs0–1.
Captures/binaries remain on the existing PVC outside Git. Own signal controls
return errno13; no functioning external signal watchdog is claimed.
Owners use explicit finite/natural-exit points and charge retained processes.
One-second RSS sampling can overshoot and is not a hard kernel quota.
Historical lab48GiB/CPU8–11/four-worker, older two-worker24GiB-AS and G10
points retain their own denominators, hardware, retries and incomplete data.

<a id="resource-layer-diagnosis-and-missing-warm-comparison"></a>
<a id="complete-nativemathlib-derived-pair"></a>
## Strong warm-service result and failure behavior

The [complete7,808pair](../artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md)
takes warm25,176.4873s / engine20,323.0076s:1.238817×,19.2778%less elapsed.
All7,808status aliases /3,014accepted IDs agree. Raw responses differ:
7,682payloads; stripping env/empty ast still leaves23rejected-source
diagnostic/optional-field differences. Retry order,affinity,warm-first order
and shared support work preclude COW-only,steady-state or general gain claims.
Own fresh/prepared1.24028× is not this baseline. Old21,693.76s two-worker
warm point has six state differences and is not a matched four-worker point.

The fixed [42solo recheck](../artifacts/engine-resource-profile-2026-10-25/solo42-native-library-20261029/README.md)
is complete:41resource-watchdog failures/1timeout/0restored acceptances.
Do not restart it or the retired FIFO/policy queues.
[Resource reanalysis](tmp/build-and-evaluate/step-0183-20261030T112405+0000/step-report.md)
finds11of52warm concurrent resource failures become timeouts in exclusive
retry at the same total cap. Global cap+goal+tactic is not a per-call failure
certificate; peak subtraction and simulated retries are not measured COW gains.

[480profiles](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md)
contain83timeouts/355ordinary errors/42resource failures. Timeout-thread CPU
55.19%interval_cases/28.21%simp_all is not all-candidate wall share.
The71source prototypes establish no reliable early-failure rule.
[Full scheduling](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md)
uses21,746.81s all /15,385.39s first-original /15,112.12s first-short,
same142solved tasks at the old two-worker point. This is pass@k,not per-candidate
RL rewards or scheduling novelty. Held-out source-cost ordering did not improve
FIFO and is not rerun. Selected32-source feedback is not full-population gain.

## Current workload evidence

[Library audit and native table](paper/main.tex) use OpenAI/math4eaee875,
Lean4.34.1/Mathlibd13f23b7. Static163,097files/1,354,379decide+kernel tokens
are not executions,cache misses,costs or transitive axiom closure.
The original53target frame and major typed repeated-goal probes remain incomplete.

| Separate native point | Calls | Compile | HB/wall stops | Uninvoked | Compiler-wall sum(s) |
|---|---:|---:|---:|---:|---:|
| Seven baseline |7|7|0/0|0|44.002841|
| Same seven,profiled |7|7|0/0|0|44.498820|
| Expanded50kHB |82|81|1/0|46|218.436127|
| Incremental100kHB |47|47|0/0|0|102.648630|
| Wider,j1 |109|108|0/1|62|724.588552|
| Grid profile/stats,j1 |1|0|0/1|0|300.100281|
| Grid unprofiled,j8 |1|1|0/0|0|634.280070|
| After Grid bounded group,j8 |14|12|0/2|48|1399.355128|
| Amplitudes longer bound,j8 |1|1|0/0|0|180.275578|
| New strata,j8,100k |109|106|2/1|2984|1399.655781|
| Two authored-option modules,j8 |2|2|0/0|0|41.811451|
| Authored probability point,j8 |189|187|0/1|incomplete closure|1399.505203|

Points have different budgets,workers,warm prerequisites and collection clocks;
never sum them as a fresh homogeneous library build. M8192 is cooperative
memory checking,not a kernel hard quota. Combined sampled peaks include the
retained EPFL process. Seven-source profile difference1.13%is one fixed-order
observation,not general instrumentation overhead. The300sGrid profile has491
completed events/176.426s reported type-check durations plus unfinished work;
overlap/incompleteness prevent an exclusive wall partition or root-cause claim.
Grid worker/wall limits change jointly; no isolated worker speedup follows.
[Step0202](tmp/build-and-evaluate/step-0202-20261030T144255+0000/step-report.md) checks the14/62group:10dependency-blocked+38not-started.
Last KernelValues10 receives only41.935s remainder,not120s. Unchanged Amplitudes
later compiles with1200s self-wall opportunity; its prior120.115s censor stays.
Compilation is not full-service acceptance or an imported-axiom audit.
[Expanded cohort audit](tmp/build-and-evaluate/step-0205-20261030T152520+0000/step-report.md) checks3114closure/3093fresh:
109calls,106compile/2HB/1residual-wall;217dependency-blocked+2767not-started.
The final call gets8.030s,not300s. Two original sources later compile with
CLI-heartbeat override removed and600s selfwall;not a same-budget gain.
Native wall1399.655781/41.811451s,capture1407.564239/50.057644s,
combinedsample12.40/11.99GiB. Acrosspoints365objects/18of53endpoints exist.


[Original-options sample audit](tmp/build-and-evaluate/step-0210-20261030T170436+0000/step-report.md) checkscompleteboundedledger236:
189actualnativeinvocations/187compile/1missingRellichKondrachov/1selfwall,
47recordedblockeddependents. NoCLIHBoverride,sourceexact189copies,
autoImplicit=false,j8/M8192/CPUs0–7,600sconfiguredchild/1400sgroup.
FinalWaveExpDatahas11.734364sremainder,not600s.16cachedtargetsremeasured
to privateobjects+171newdependencies;retired189actualPID/birthidentities.
Nativewall1399.505203/CPU2539.433437s,capture1407.576181s,
combinedsample13415440384B includesoldEPFL. .oleanonlynotfullLakeoutputs.
19/42matchedprobabilitycosts,6/21completecells,23unmeasuredendpoints;
nofullCPUestimate/95%CIorzero-costmissingcell,purposeful100krowsnotpooled.

[Native type-group audit](tmp/build-and-evaluate/step-0205-20261030T152520+0000/step-report.md) contrasts the135object pilot
(1799theorems/743auxiliary names/45distinct decision-shaped types) with a
completed363object read:89268theorems,47989auxiliary names,44528Exprkeys,
44532level-private groups. Its45661decision-shaped declarations have distinct
global names,in90modules,42610typegroups;933repeat/919crossmodules.
3051extra declarations=1497within-module extras+1554extra module/key pairs.
These are real native type matches,not merely repeated tactic text or
duplicate import enumeration. Actual export/cache mode,hiddendependencies,
runtime misses/CPUcost and fullaxioms remain unobserved. No saved-time or
full-population cache-eligibility claim. Metadata native1.762153s,capture
2.003251s,combinedsample6.24GiB includes retained EPFL;not proof rechecking.
The original repeated-text endpoint remains uncompiled;earlier45distinct
pilot result stays valid within its smaller scope. No key-IDcross-run join.
[Source/native unit reconciliation](tmp/build-and-evaluate/step-0210-20261030T170436+0000/step-report.md) rechecks363exactsourcefiles
andoriginalnativecensus:42886lexicalkernel-sitesvs45661retainedshapehelpers,
42610globalExprgroups/44164summedpermodulegroups. Jet50:944sites/3938helpers
alldistincttypes;Canonical240:114/600,alldistinct. Sourceinterval_cases/<;>/
nestedfin_casessyntaxobserved,notcausalper-eventinstrumentation.
AuxiliaryGram:0explicitkernel-sites/1matchinghelper,predicateisnotexact
syntaxattribution. Thesearecountsafterelaboration/cacheactivity,notraw
cachemisses,originalkernelcallcounts,replaykeysorweightedruntimebenefit.

[Same-point module exposure](tmp/build-and-evaluate/step-0206-20261030T155146+0000/step-report.md) maps52
global cross-type-bearing modules;48occur in the109-call new-strata point.
Those48successful calls use454.207083/1399.655781s=32.45%of own native-wall sum.
Other58successful calls903.310661s;3interrupted/untyped calls42.138037s.
Whole-module imports/elaboration/otherproofs are included:neither duplicate-
checking CPU nor saved time is identified. Unnamed491completed Gridprofile
events have no declaration identity and come from another point;no guessed
order-based join or cross-run phase rescaling. The2984uninvoked modules have
unknown contents/cost. No corpus/warm-service/GPU Amdahl bound or cacheenablement.


[Modern native certificate contrast](tmp/build-and-evaluate/step-0208-20261030T164526+0000/step-report.md) audits pinned M af6e66d:
seven distinct Int/list row goals from one module in the earlier45typepilot.
14whole-source calls allaccepted,14correctedobservers allaccepted;292new
theorem/auxiliary checks(14original+278certificate). Whole-source wall
13.317706/23.936857s and CPU13.108858/24.262333s original/certificate;
allsevenpairs slower. Extra-check intervals2.327609/5.757960s are additional
checks in a populated environment,not exclusive CPU/initialproofchecking;
definitions/abbrevs omitted there but included in plain sourcecost.
Same final proposition text/importonlyRowCompute,finalAXpropext/Quot.sound.
Corrupted scalar rejected. Native4.34.1/j1/M8192/source200k/depth10000/
CPUs8–15/self35s;45nativeidentities retired;samplepeak4980285440B,
nohardRSSquota. One modeobservation perrow,counterbalancednotrandomized.

MatchedSDKaddDeclCore defaultsdoChecktrue;getMaxHeartbeats multiplies1000,
so200koption→200000000raw. Threeinitialcertificate observers fail artificial
raw1m limit;excludednotoriginalprooffailures. Initial45typeprobe128budget
diagnostics retained. Corrected45typeprobe has49completedchecks,
16complete3repstypes/1partial1rep/28unreached,wall60.180691s/selfalarm-14,
nofinalcompletemarker. Parentgroupcompletion doesnotcomplete thiscensus.
Selectedsevennegative contrastsdonot negate algorithmicdigit/gridcompression,
provegeneralcertificatebenefit,measurewarmserviceoridentifyfullkernelcost.
No newrootnativecalls,cacheorproductionmode.


EPFL [136returned-prefix audit](tmp/build-and-evaluate/step-0185-20261030T113532+0000/step-report.md)
has53compile/71ordinary/12budget,623.799202s;budget25.60%of returned-prefix
cost,not full144frame/natural arrivals. Later seven-source10k/M6144/15s point:
1compile/1ordinary/3HB/2wall. Two j2revisits reachHBerrors13.689/13.734s
rather than j1wall-outs;no pass,isolated cause or shared denominator.
[APRIL39pairs](tmp/build-and-evaluate/step-0188-20261030T115336+0000/step-report.md)
have78returns:35reference passes/4HB;23mutation errors/16budget.
Unweighted mutation budget-cost50.53% vs inverse-inclusion11.05%for the
released1,835test rows only; no confidence interval or natural-arrival inference.
Exact original Mathlib unknown; release-version reconstructions are explicit.

[Training construction and12replays](tmp/build-and-evaluate/step-0202-20261030T144255+0000/step-report.md) are a separate distribution:
publisher4,836,380rows includes250,000synthetic and8457contract exclusions;
37primary counters checked. Stage filters are not disjoint global failure rates.
Twelve selected candidates yield3compile/3ordinary/6HB;budget16.178800/
29.392530s=55.04%selected cost. Four per stratum oversamples budget text.
Publisher-valid2compile/2HB;invalid1compile/3ordinary/4HB,not label-bug proof.
[Six label controls](tmp/build-and-evaluate/step-0204-20261030T150458+0000/step-report.md) use the same invalid-labelled program:
original0HB,annotation0HB,800kHB compile;recursion128 fails,256/512 compile.
Pinned SDK default512 verified. Calls1.861–2.095s,sum11.550774s,group12.015700s;
combined sample8.61GiB includes old EPFL. Heartbeat cap/comment presence do
not explain fresh success here; producer's exact original cause remains unknown.

[AutoVerus](tmp/build-and-evaluate/step-0179-20261030T095708+0000/step-report.md)
nonzero-exit candidates consume~95%of each complete3,566pass's process time,
but top1.6%consume only3.3–3.4%. JSON and exit disagree; generation unmeasured.
Failure frequency and heavy-tail concentration are different. The
[public kernel checker](tmp/build-and-evaluate/step-0184-20261030T113046+0000/step-report.md)
has90fixtures/250inputs/986static wrapper obligations,not native candidate
timing; FAIL/refutation/undecided/process failure and trust scopes stay separate.

## Mechanism and semantic frontier

[Full200/600matrix](tmp/build-and-evaluate/step-0186-20261030T114011+0000/step-report.md):
six cells/200IDs each retire;error flags/diagnostics/InfoTrees match,but rawHB
differs63off/62on. BodyCPU838.669501s,eqRefl781.383626s. Fixed indivisible-
leaf work/span ceiling1.031701× is conditional,not full DAG/service/GPU bound.
The group exceeded1800s;720sleaf crosses old300sservice cutoff. Keep invalid
protocol/runtime and exploratory scope; do not transplant its denominator.
[Original-budget50source/150returns](tmp/build-and-evaluate/step-0193-20261030T123624+0000/step-report.md):
all noerrors,19previous budget-clipped passes restored;rawHBdiffers29/30.
Eighteen allGoals forks/seven sources give body2/4/8core models
1.184675/1.275923/1.340367×;own full-clock models1.098627/1.142253/1.171287×.
These omit unmeasured snapshot/merge/HB costs,not actual parallel speedup.
PC samples/RC/alloc classifications are residence,not removable costs.
Existing negative typeclass/dependency caches are prior mechanisms; generic
failure/poststate/hidden-dependency/heartbeat/diagnostic replay is unqualified.

[Complete certificate pipeline](tmp/build-and-evaluate/step-0201-20261030T141554+0000/step-report.md)
proves original grid proposition via2004rows/16chunks,covering4,016,016logical
cells,not4million kernel cell evaluations. Full Ccompile+scan+emission+Lean+
capture2.290783s includes extra final recheck;initial chunks.790054s are not
pure rechecking. All24extra recheck groups/384checks retained,actual overlapping
call lifetimes1/2/4/8;median ratios1/1.775/3.102/5.002. Already-established
declarations,fresh names,discarded environments and per-task budgets do not
implement first-check merging,global heartbeat parity or service acceleration.
New theorem/algorithm is not validation of a false submitted prefix.

[Complete two-family native audit](tmp/build-and-evaluate/step-0207-20261030T161637+0000/step-report.md) supersedes the v5partial frontier:
pinned562a80e/88edb9d,all64family sources/128native calls,49pair98units plus15pair30.
Router scans7808source strings by theorem-header structure/literals,not names:
63routes(32digits/31grid);literalNone7206unsupported. No outside-family route
in this catalog;not a general misclassification or typed-acceptance estimate.

At the declared phobos/CPU8–11/j1/200k-sourceHB/-T50000000/M8192/16s-self point,
original0accepted/13errors/51budget,879.431413s invocation-wall sum;
repair31accepted/29errors/4budget,285.778088s. Flow31budget→accepted,
16budget→ordinaryerror,4staybudget,13ordinaryerrorsstayerrors.
All31final AXclosures subsetpropext/Quot.sound/Classical.choice,no sorryAx;
16digits/15grid. Exact source/compiled-module bytes,all128native PID/birth
retirements and fouradversarial controls checked by root. Original imports
remain original;certificate mode adds its checked module. Builds23.009619/
2.571431s outsidecandidate clocks;not free. Both finitegroupscomplete and
alternate firstmode. Source-budget settings are configured values,not a
globally reconciled heartbeat policy. Censored times are not uncensored speedup.

Twoactual-target/false-prefix controls preserve mapped diagnostics;no universal
fallback proof. v5stopped23/49,sorry leakage,panic and v8–v11 failures remain
preserved in oldreports/raw,not final recovery data. Ordinary failures do not
prove false assertions;known-false3689 inextra15 remainsrejected.
No original-mode passes in this cohort means no test of previouslypassing
candidate preservation. Two goal families absent from historical142solvedtasks
now have verifiednewproofs;not a measured full7808newsolve/throughput result.
This is opt-in specialized proof repair with changed acceptance,not result-
preserving verification,a generic compiler or established systems novelty.
No production mode enabled. Remaining37staticopportunities/11bridges and
rough engineering estimates are not implemented coverage or time savings.

[Remaining-limit native audit](tmp/build-and-evaluate/step-0211-20261030T172449+0000/step-report.md) checks M8412ff4 from raw C events,
not its narrative alone. Four byte-identical repaired sources preserve prior
operational categories, normalized full stdout and exact stderr; a positive
control also matches. Original lean_profileit delegation and matching
Lean/AddDecl.lean establish the declaration-check category; no profiler trace
option or proof-code changes in this primary comparison. Twelve actual native
PID/birth identities (4primary+1positive+7interventions) are retired.

3683: all observed tactics finish, max enclosing interval0.962999s, while
declaration checking remains open at16.247170s wall interruption.
3703: original rfl/eqRefl fallback remains open at16.245790s after failed
bridge attempt. 3698: prefix simp recursion-depth error at3.222368s;
M README's heartbeat-exhaustion attribution is contradicted by raw stdout.
3710: bridge recursion-depth error plus earlier omega error,3.675107s.
Raw heartbeat counts/observer overhead and exact kernel reduction node remain
unknown. Nested/incomplete frames do not partition whole-source wall.

Seven changed-source interventions retained with exact diffs. Removing
cardinality expansions or a bad prefix can replace a budget outcome with
ordinary proof errors; these are not semantics-preserving successful ablations.
Removing norm_num alone still reaches the bound. Direct whole-body theorem
application passes0.967882s, added theorem check0.000296484thread-CPU seconds;
prechecked imported lemma/different imports/body,not first certificate check
or another recovered candidate. No new accepted inventory ID or speedup claim.
Four-command C wrapper relink wall0.966679s is separate setup.
Other lane source/results are untouched; root corrects only canonical evidence
and paper attribution. Current33newproof/145task inventory stays unchanged.

[Third-family and corpus-inventory audit](tmp/build-and-evaluate/step-0209-20261030T165602+0000/step-report.md) adds a separate complete
32source/64native power-familypoint,pinned8412ff4collector/transform and
actualsources/receipts. Exactbounded128assignment lemma plus provedbounds
handles cube/fourth equation hypotheses;positivecontrolaccepted/exponent2
controlfallbackrejected. Both modulebuilds actualexit0/retired3.573104/
4.123672s,outsidecandidatephase. Rootchecks68actualretiredPID/birthidentities.

Original20ordinary/12budget/0accepted;certificate29ordinary/1budget/2accepted.
Flow20ordinary→ordinary,9budget→ordinary,1budget→budget,2budget→accepted.
Only7551of8historicalselectedtimeoutsrecovers;7545isalsoacceptedbutoutside8.
22of7808source stringsactuallychanged,powerfamily32tested,sameroutecatalog;
nohistoricalacceptedIDchanged. Candidatewall336.372899/208.961074s,
group545.592001s,ownsamplepeak4194463744B. Keep200ksourceHB/CLI-T5e7/
M8192/j1/CPU8–11/self16settingsnotglobalHBpolicyorwarmservice.
No sourcecost ratio inferredfromcensoredoriginaltimers.

Cross-experiment inventoryrecomputedfromrawhistorical7808input/outcomes,
prior31nativeproofs+2newproofs,notMsummaryalone. 244tasks×32sources,
3014historicalacceptances+33newcheckedrepairs=3047;142→145solvedtasks,
58.196721→59.426230%,+1.229508percentagepoints. All33newAXclosures reread,
standardthree/noadmissions. 3014historicalfullAXclosurefreshrechecknotdone.
Alloldacceptancesretainedbyunionconstruction,notmeasurednonregression.
Complete7808CSVacceptanceoverlaymatchesrecomputedsets;no7808newnative
run,nosamehardwareE2Eratio,notunchangedsourcevalidation.
Two-family144-taskintermediateinventoryretained;this145inventorysupersedes
onlyitscurrentcount. Shapecoverage57/126isnot57validrecoveredproofs;
only32of126opportunitysourcesnowhavecheckedrepairs(33rdoutside126).
Noengineproductionmodeornewpaperthesis;Mimplementationandfailuresunchanged.

<a id="public-lean-code-verification"></a>
## Earlier code/GPU evidence and interrupted captures

Verina189reference files include46no-explicit-admission successes/139stubs/
4missing-API errors;observed simp slices are not exclusive CPU. LNSym static
counts and publisher tooling are not native full-cost evidence.
[Lean-mlir](../artifacts/lean-code-verification-2026-10-25/leanmlir-native-20261027T025426Z/README.md)
whole module40.47/40.21s file/stdin,94.04sprofiled. Overlapping LRAT traces
do not partition original wall;existing streamed/LRAT methods limit novelty.
[Final arithmetic screening](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md)
preserves statuses/3014accepted IDs but is8.86%slower. Old25/0.2%coverage used
invalid wrapper data;final34refuted intermediate goals/29ordinary-error
candidates remove no timeout. No route expansion.
The interrupted8031state/cost capture retains2640archived returns,one
reconstructable panic with elapsed unknown and≥1273unrecovered observations.
Missing data are not failures/zero hits; old queues/hardware are not resumed.

## Next evidence and verification

Complete selected native workload coverage,source-preserving recovery with
matched operational controls,full requested artifacts/history/cancellation
and repeated equal-resource service measurements remain unresolved.
No new thesis,production cache/adapter or parallel engine is enabled.
Paper compilation,CI and self-review support build/evidence health only,
not novelty or venue acceptance. [Current paper](paper/).
Historical anchor aliases below retain incoming navigation.

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
