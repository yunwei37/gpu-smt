# Evaluation: current evidence and open work

Updated 2026-10-30 UTC. Root owns paper/evidence integration; reviews are
self-review, not independent audits. All four RQs remain open. The complete
historical frontier, failures, partial outputs and superseded statements are
preserved in [the archived evaluation](tmp/build-and-evaluate/step-0187-20261030T114731+0000/archived-evaluation-20261030T114731+0000.md), with original dates intact.
No raw result or other owner's file is removed.

<a id="current-decision-frozen-oracle-and-three-continuing-directions"></a>
## Current directions

The user assigns existing W/M/O forks workload, mechanism and open-source
paths; root integrates evidence and paper. Mainline selection awaits their
results and the user's decision. Do not silently turn the paper into a
cross-proof-cache thesis or a short negative-results closure.
The continuing directions are the layered Rust engine, reliable early failure,
multi-candidate inference, and public mathematical/code-verification loads.
CPU oracle is frozen. Closed E038/narrow GPU constructors stay closed;
generic resource/COW/cache/scheduling primitives are not contributions.
Authority: [verbatim user log](user-instruction.md), [initial narrative and
evolution](idea-story.md), [author decisions](questions-for-author.md).

| RQ | Frozen question | Current status |
|---|---|---|
| RQ1 | How much expensive native preparation can real verification candidate streams share across independent jobs? | unanswered:complete preparation-cost/context coverage remains missing |
| RQ2 | Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation? | unanswered:full native artifacts,history,cancellation and supported scopes remain incomplete |
| RQ3 | How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse? | unanswered:one full warm-resource pair is complete with limits;scaling/repetition promises remain open |
| RQ4 | After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path? | unanswered:no useful extra full-flow GPU gain has been demonstrated |

<a id="resource-point-and-workloads"></a>
<a id="resource-point"></a>
## Current resource point

The existing gpu-smt-dev Workspace is on phobos-vt with its 128 GiB PVC.
The user allocates 40 GiB total: W 16 / M 16 / O 4 / root 4, each at most eight cores.
Root uses CPUs 0–1 for small analysis and builds. Captures and build outputs
stay on the existing PVC outside Git. Self-owned signal controls return
errno 13; a working signal watchdog is not claimed. Owners retain explicit
bounded/natural-exit methods and account for retained native processes.

Historical lab 48 GiB / CPU 8–11 / four-worker and two-worker / 24 GiB-AS points retain
their own conditions; G10 and phobos-vt do not inherit those denominators.
One-second RSS sampling can overshoot and is not a kernel hard quota.

<a id="resource-layer-diagnosis-and-missing-warm-comparison"></a>
<a id="complete-nativemathlib-derived-pair"></a>
## Strong warm-service result

The [complete matched 7,808 pair](../artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md)
takes 25,176.4873 s warm and 20,323.0076 s engine: 1.238817×, 19.2778% less elapsed.
All 7,808 status aliases / 3,014 accepted IDs agree. Raw responses do not:
7,682 raw payloads differ; even removing env/empty ast leaves 23 rejected-source
diagnostic/optional-field differences. All 126 operational strings differ.
Retry order,affinity,single warm-first order and shared support work prevent
a COW-only,steady-state or universal strong-service gain claim.

The [own fresh/prepared pair](../artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/result-review.md)
is 28,391.98 / 22,891.51 s = 1.24028× with different native-library context; it is
not this warm-baseline result. The old 21,693.76 s two-worker warm point and its
six status differences are preserved,not mixed into the four-worker pair.

The corrected [fixed 42 solo recheck](../artifacts/engine-resource-profile-2026-10-25/solo42-native-library-20261029/README.md)
is complete: 41 watchdog resource failures / 1 timeout / 0 recovered acceptances.
It is not pending and must not be restarted from an old queue.
The old FIFO/policy controller remains retired/paused; unrun policies are not
silently treated as completed. Detailed singleton/retry/response-origin
diagnoses and earlier faulty points remain in the archive.

## Failure and scheduling

The [480 profile](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md)
has 83 timeouts / 355 ordinary errors / 42 resource failures. Timeout-thread CPU
shares 55.19% interval_cases / 28.21% simp_all are not all-candidate wall shares.
The original 71-source prototypes establish no reliable early-failure rule.
Recovery-sensitive controls disprove generic transparent recovery disabling.
No ordinary tactic exception is treated as proof that a target is false.

The [full scheduling comparison](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md)
at its old two-worker point takes 21,746.81 s all, 15,385.39 s first-original and
15,112.12 s first-short, with the same 142 solved tasks. This is pass@k behavior,
not per-candidate RL rewards or scheduling novelty. Held-out source-cost
prediction did not improve FIFO and is not rerun/deployed. Later 32-source
memory feedback is selected engineering evidence,not full-population gain.

The [resource-reuse/memory audit](tmp/build-and-evaluate/step-0183-20261030T112405+0000/step-report.md)
rechecks all 7,808 attempts. Eleven of 52 warm concurrent resource failures become
timeouts in exclusive retry at the same total 48 GiB. Goal+tactic+global cap
does not certify a deterministic per-call failure. Full-coverage retry models
retain frozen labels only by assumption; they are not new-budget native
throughput. Hindsight peak subtraction does not isolate physical COW savings.

The [native-cache source audit](tmp/build-and-evaluate/step-0182-20261030T111939+0000/step-report.md)
finds existing negative typeclass caches and approximate full-state heartbeat
charging. Separately pinned current Lean tracks dependencies and normalizes
eligible contexts. Generic negative/read-set caching is prior mechanism;
arbitrary tactic failure replay and useful incremental coverage remain open.

## Current workload evidence

The [released Mathlib native pilot](tmp/build-and-evaluate/step-0181-20261030T105443+0000/step-report.md)
uses Lean 4.34.1 / Mathlib d13f23b7. Seven modules/four of 53 targets yield 14 native
exits0. Baseline/profile-only wall 44.002841 / 44.498820 s; the 1.13% difference is
one fixed-order,warm-cache,shared-node observation. Peak compiler RSS 7.46 GiB
is distinct from 1 s sampled tree 7.43 GiB. Full-library costs remain unmeasured.
The [expanded closure point](tmp/build-and-evaluate/step-0190-20261030T121230+0000/step-report.md)
keeps 128 module states: 82 actual compiler invocations, 81 passes, one
heartbeat boundary and 46 dependency-blocked modules left uninvoked. Two
of three target endpoints compile. At its separate unprofiled 50,000-HB
point, native process-wall sum is 218.436 s; capture 225.245 s; combined
W-tree sampled peak 11.87 GiB includes the old EPFL process. Full 53-target
coverage, original unbounded costs and transitive axioms are not established.
A [separate incremental 100k point](tmp/build-and-evaluate/step-0192-20261030T122728+0000/step-report.md)
retains the 81 objects and compiles all other 47 modules: all 128 closure
objects / three target endpoints are now available across points. Fresh
47-call wall sum is 102.649 s, capture 110.118 s. The 50k states stay unchanged;
no homogeneous fresh total is invented. Including the earlier pilot gives
135 distinct objects, still not all 53 targets or an imported-axiom audit.

The [public checker audit](tmp/build-and-evaluate/step-0184-20261030T113046+0000/step-report.md)
verifies 90 released KIR fixtures / 250 concrete inputs and 986 static positive
wrapper obligations,not native executions or an LLM candidate stream.
Tool FAIL,Lean wrapper refutation,UNDECIDED and process failure are separate;
the exact 4.34.0 / native_decide trust boundary differs from decide+kernel.

The [completed-prefix audit](tmp/build-and-evaluate/step-0185-20261030T113532+0000/step-report.md)
rechecks 136 of 144 selected EPFL returns: 53 compiler passes / 71 errors / 12 budget
cases, 623.799202 s. Eight remain unreturned/right-censored in that record;
25.60% budget share is returned-prefix cost,not a population estimate.
Compiler success does not implement the publisher's full declaration judge.
A later separate 10k-HB/M6144/15s-self-bound point returns the other seven
selected sources except the retained stuck request: 1 compiler pass, 1 error,
3 HB and 2 self-wall interruptions. Actual SIGALRM exits are observed.
It does not complete or replace the original 200k-HB point's missing tail.
The [wider-module/runtime-configuration audit](tmp/build-and-evaluate/step-0197-20261030T130732+0000/step-report.md)
checks171closure states/109actual native invocations:108compile/1Grid120s
self-wall interruption/62uninvoked. Seven of nine original endpoints compile;
the extra unweighted repeated-text probe stays blocked. Native wall sum
724.588552s/capture732.836210s;raw1ssampled combinedpeak12.20GiB including
retained old EPFL. GridCPU151.397173s exceeds120.094289swall;requestedj1/env1
is not measured oneOSthread or phase attribution. Across priorpoints243
distinct compiled objects/14of53frame endpoints exist;no homogeneous total.
Two same-source EPFLj2/env2returns reachHBerrors13.689/13.734s vsj1/env1
15swall-outs with~2.1CPU s. No pass,isolatedflagcausality,rootcause or speedup.
Ordinary-error first-message categories cover71requests/303.183521s as
whole-request groups;they are not phase/tactic costs.

The [complete APRIL39 replay](tmp/build-and-evaluate/step-0188-20261030T115336+0000/step-report.md)
has all 78 native returns at Lean 4.22rc4 / reconstructed Mathlib 928758a /
50,000 HB / M6144 / one thread / 30 s self-bound. References: 35 compiler
passes / 4 HB interruptions; mutations: 23 errors / 16 budget interruptions.
Unweighted interrupted-mutation request cost share is 50.53%; the inverse-
probability ratio is 11.05% for the released 1,835 mutation-test rows only,
without a confidence interval. These are whole process costs, not tactic
phase time or natural arrivals. The 39 pairs share 32 reference strings.
Original Mathlib pin is unknown; no publisher acceptance reproduction or
false-goal claim follows. EPFL censoring remains separate.

[AutoVerus reaggregation](tmp/build-and-evaluate/step-0179-20261030T095708+0000/step-report.md)
finds about 95% of each complete 3,566-candidate pass on nonzero-exit candidates,
despite only 3.3–3.4% in its top 1.6% tail. Native JSON success and process exit
classes differ. Those retained clocks do not include publisher generation.

## Complete native diagnostic matrix

The [full 200/600 reanalysis](tmp/build-and-evaluate/step-0186-20261030T114011+0000/step-report.md)
checks six exited/retired cells,all expected IDs and both raw C event streams.
Both linked comparators preserve 200 error flags/diagnostics/InfoTrees,but raw
heartbeat deltas differ 63 off / 62 on. Strict resource semantics is unqualified.
Diagnostic classes 31/19/150 are not full production acceptance/sorry policy.

Timing-on body CPU 838.669501 s includes 781.383626 s exclusive eqRefl (93.17%).
Largest-leaf-per-source sum 812.899512 s gives a conditional fixed-work,
indivisible-leaf work/span ceiling 1.031701×. It is not a complete DAG or a
bound on new algorithms,inner-leaf splitting,early rejection or work removal.
A 720.250 s leaf passes the historical 300 s service cutoff; neither its share
nor that ceiling applies to the original 7,808 service denominator or closes GPU.
Body and whole-process clocks remain separate; sampled peak 8.06 GiB is not
a hard quota. Step0185's stale full-matrix-pending statement is explicitly
corrected forward in step0186 and is preserved with its contrary raw receipt.

The [original-budget and native-type reanalysis](tmp/build-and-evaluate/step-0193-20261030T123624+0000/step-report.md)
checks all 150 returns from 50 selected prior passes at their original
maxHeartbeats0. All error flags/diagnostics/InfoTrees match across three cells;
raw HB differs 29 off / 30 on. Earlier 19 budget-clipped passes now return
without errors. The earlier diagnostic 1.031701× ceiling cannot exclude this
different point's branch opportunity. Linked-on body CPU is 95.931585 s;
18 matched allGoals forks in seven sources give finite 2/4/8-core latency
models 1.184675/1.275923/1.340367×. These preserve work and omit unmeasured
snapshot/merge/hidden-state/diagnostic/HB/memory costs, not actual parallel
execution or 7,808 throughput. Three whole cells take 501.013149 s; 3.85 GiB
sampled peak; have-only 1.015819× overlaps and is not added.

The [complete-clock sensitivity](tmp/build-and-evaluate/step-0194-20261030T124220+0000/step-report.md)
keeps the same capture's 70.667284 s outside-body work unchanged and maps
each modeled CPU reduction through its own source body wall/CPU ratio.
The conditional full-process 2/4/8-core ratios are 1.098627/1.142253/1.171287×,
versus the body-only 1.184675/1.275923/1.340367×. No measured runtime benefit,
warm-service denominator or general Amdahl impossibility claim follows.
Three sources account for85.68%of modeled eight-core reduction; retrospective
concentration is not a predictor. Existing native rows are reanalyzed only.

Native metadata from 135 compiled objects yields 1,799 theorems, 743 auxiliary
names, 601 native Expr keys / 604 level-private groups, 45 cross-module groups.
The 45 decide-shaped auxiliaries have 45 distinct types: no exact-type
merge demonstrated for this pilot. Failed calls and major repeated-goal
clusters are absent; full imported axioms and cache/replay eligibility unknown.

The [software-sampling audit](tmp/build-and-evaluate/step-0189-20261030T120435+0000/step-report.md)
separates 14,118 outside-body samples from 2,531 body samples, and validates
a separately timed successful closed recheck (4,258 PCs). Named RC/alloc/table
residence is not total operation cost or a precompilation gain. An old timing
window included shutdown; the corrected timer and changed raw-HB scope remain
separate. M also reports the original six-cell group exceeded its 1,800 s
whole-group bound: native processes alone took 3,081.953 s. The captured
matrix remains exploratory evidence, not a conforming group/runtime claim.

The [Grid partial-profile audit and native-table consolidation](tmp/build-and-evaluate/step-0198-20261030T131856+0000/step-report.md)
checks own300.100281sSIGALRM record,491completed type-checking events/oneimport,
176.426sreported type-check sums plus unfinished trailing event. Partial,
possibly overlapping event durations do not partition300swall;--stats never
finishes. Native user/system176.164148/196.607446s,690504minor/0majorfaults,
24778976/127174voluntary/involuntaryswitches;no rootcause inferred.
Combinedsampledpeak10.89GiB includesoldEPFL. The120sunprofiled point and
seven-source1.13%profile observation are not borrowed denominators.
Paper now tabulates six distinct bounded points instead of narrating each
run,retaining statuses,clocks,metadata coverage and budget/axiom limitations.
Historical full wording remains in this step entry snapshot and priorGit.

The [completed Grid point audit](tmp/build-and-evaluate/step-0199-20261030T133110+0000/step-report.md)
checks the independent unprofiledj8/1200swall/100kHB/M8192 point:
compile_ok0/no sorry,native andcontroller retired,634.280070swall,
399.933766user/440.562612sys,12.24GiBsampledcombinedRSS. The84,076,976-byte
olean exists;these campaign points now yield244knownobjects,14frameendpoints.
Oldj1/120swall andprofiled300sinterruptions remain censored;worker andwall
bound changedjointly,so no isolatedworker speedup or originalj1long-bound
outcome is inferred. No next-target or native typed-probe completion follows.

The [historical-timeout-prefix reanalysis](tmp/build-and-evaluate/step-0196-20261030T125817+0000/step-report.md)
independently checks one original minif2f-4997 repeated10times in each cell:
30returns,all flags/diagnostics/InfoTrees/rawHB equal and native retired.
This 3000HB prefix differs from earlier historically passing budget median.
1,751body samples:149IR,185coldRC,156alloc/free,167namedtable,24unresolved;
57exact lean_inc/lean_dec samples supplement coldRC to242(13.82%).
It is not a full300s-timeout profile or precompilation gain. A separate
axiom-free native witness(667,3,1) refutes the local i<=40 bound but satisfies
the final sum<=671. It qualifies no general backtracking/recovery-safe
whole-request early abort and enables no closed GPU route. Root uses the
published9b67361decoder on raw snapshots,not uncommitted M code. One short
witness sample misses its524,357,632B native high-water peak.

The [full reflected-grid proof/recheck audit](tmp/build-and-evaluate/step-0200-20261030T134458+0000/step-report.md)
uses actual540cfc2source snapshot byte-equal to executedv4,not currentv5.
The original Nat proposition is proved via2004division rows/16chunks;
4,016,016cells are logically covered,not individually evaluated. Bridge/
assembly/final axioms onlypropext/Quot.sound. Whole6.929171s includes initial
sequential checking and320extra rechecks;no generatorcost measured.
Twenty1/2/4/8-task groups retain every startup repeat. Firsttwo8taskgroups
~.274s,lastthree~.085s;causeunestablished,no causal scaling/servicegain.
Same immutableenv,discarded newenvs,original sequential chunks used byfinal.
This is an alternateproof/algorithm,not unchanged-candidate parity;no generic
compiler or novelparallelmethod claimed. Oldfive-rectangle samples retained.

The [complete pipeline and overlap reanalysis](tmp/build-and-evaluate/step-0201-20261030T141554+0000/step-report.md)
checks frozenfd37172 source/raw capture,all24groups/384kernel checks and
per-group actual overlap1/2/4/8. Six-group medians .276177/.155573/.089030/
.055213s give observed recheck-phase ratios1/1.775/3.102/5.002;not initial
elaboration,mergedbudget orservice throughput. Earlier v4startupdata retained.
One fullv6Ccompile+scan+payload+Lean+capture pipeline takes2.290783s,
includingextra finalrecheck. Initialchunkwindow.790054s isnot purekernel
recheck;no5×rescaling. v5CPU/highwaterfields cumulative,not per-run;v6CPUdelta
2.145372s andsampled own-tree566886400B separately scoped. No originalsource
replacement or49recoveryclaim. Allsource andcontrollerretirements verified.

<a id="public-lean-code-verification"></a>
## Earlier program/GPU evidence

[Lean-mlir](../artifacts/lean-code-verification-2026-10-25/leanmlir-native-20261027T025426Z/README.md)
has one native module 40.47 / 40.21 s file/stdin, 94.04 s profiled. Overlapping LRAT
trace slices cannot partition the unprofiled wall denominator. Closed-CNF
and fused-checker work remain scoped prototype evidence,not general novelty.
[Final arithmetic screening](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md)
preserves statuses / 3,014 IDs but is 8.86% slower; 34 refuted intermediate goals in 29
ordinary-error candidates remove no timeout. The old 25 / 0.2% estimate used
invalid wrapper data and is not the final coverage. No route expansion.
The interrupted 8,031-unit state/cost capture retains 2,640 archived returns,
a reconstructable panic with unknown elapsed,and at least 1,273 unrecovered
ledger observations after eviction. Missing data are not failures or zero hits.
Full interruption,recovery,guard and default-disabled-cache history is archived.

## Next evidence and verification

Representative native workload coverage,matched-deadline opportunities,
full requested artifacts/history/cancellation and repeated service frontier
measurements remain unresolved. Use completed owner evidence and raw
terminals; running/incomplete/pending fields do not establish outcomes.
No new thesis,baseline family,production cache or parallel engine is enabled.

The current paper is [docs/paper](paper/);step0186's complete Tectonic build
and CI pass support build health,not scientific acceptance. All raw data,
failed attempts and earlier protocols remain linked from the archive.
The following historical anchor aliases retain incoming navigation.

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
See [the complete historical evaluation](tmp/build-and-evaluate/step-0187-20261030T114731+0000/archived-evaluation-20261030T114731+0000.md) for these superseded entries.
