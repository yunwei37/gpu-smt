# Evaluation: current evidence and open work

Updated2026-10-26UTC. This thread alone implements, runs, analyzes and writes.
All reviews are self-review, not independent audit. The original
[Initial Narrative/fourRQs](idea-story.md) and ambitious systems goal remain
open; tests, setup and a compiled paper do not establish OSDI contribution.

<a id="current-decision-frozen-oracle-and-three-continuing-directions"></a>

## Current decision: frozen oracle and four continuing directions

The user prioritizes the [layered Rust engine](architecture.md): reusable crates,
public contracts, tests/CI/examples/docs first, then all three workload directions
on that foundation. Resource mechanisms are prior techniques, not novelty.
The next point has48GiB actual aggregate RSS, no fixed per-process AS cap,
measured CPU-aligned dynamic admission and1s watchdog/exclusive requeue.
The completed old7808group retains its historical settings. Its42resource
failures completed a separate exclusive rerun:41aggregate-budget failures and
one timeout,no accepted outcomes. [Rawresults and resource scope](../artifacts/engine-resource-profile-2026-10-25/isolated42-20261026T101138Z/README.md).
The sampled peak48.23GiB exceeded the48GiBbudget between watchdog responses.
The [new four-worker native cell](../artifacts/engine-resource-pair-2026-10-25/full7808-20261026T004621Z/README.md)
completed all7,808candidates, but its prepared cell failed with ENOSPC.
One historical acceptance becomes a timeout and sampled RSS peaks at48.79GiB;
neither transparent accepted-set parity nor a full-pair speedup is established.
[API/implementation scope](api.md).

[Original Verina full189 measurement](../artifacts/lean-code-verification-2026-10-25/verina-full189-20261025T0725/result-review.md) is complete: 46 no-explicit-admission native exits, 139 admitted stubs, four pinned-source API errors; every profiled status matches. No above-threshold SAT/LRAT tactic work appears in the completed subgroup. The real compiler bitvector workload remains in progress.

The completed [480-source profile](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md) preserves all selected statuses. Of observed timeout thread CPU, interval_cases accounts for 55.19% and simp_all 28.21%; these are sampled diagnostic fractions, not whole-workload wall fractions. Per-source timings, all 42 resource failures and censored streams are retained. No reliable early-rejection mechanism has yet been established.

The latest user decision removes the earlier1.3x admission condition,
2026-11-01 deadline and conditional short-paper closure. Goal stays active.
Continue all three directions; no new threshold, deadline or closure.
The external arithmetic CPU oracle is frozen: preserve implementation/data,
no optimization, extension or new oracle experiment, no contribution claim.

1. Reliable earlyfailure/timeout determination from actual failed-request
profiles. Preserve the complete accepted set. A small timeout, source-token
heuristic, large branch count or slow prefix is not proof of inevitable failure.
Account for tactic backtracking and native state before rejecting a request.
2. First-success scheduling for32candidates/task in pass@k or best-of-n.
A native checked success can cancel pending siblings; prediction changes
ordering only. This consumer does not produce every candidate reward for RL.
3. Real public Lean code-verification inputs/reference proofs, profiling
bv_decide/omega/simp/decide/grind and SAT/LRAT or large simplifier states
where those components actually execute.

Only one collection runs. While it runs, advance another direction's analysis,
implementation or data preparation. No subagents/OMP/nativeAI sessions or
external-system reproduction. Prefix/certificate reuse is not our method.
Exact latest user words remain in [user-instruction](user-instruction.md).

## Resource point and workloads

New capture trees share48GiB aggregate actual sampledRSS,CPU8–11,up to four
one-core workers under dynamic memory/CPU admission,no fixed per-process AS
limit. Every1s the watchdog preempts/reaps the largest owned attempt on excess
and requeues it for an exclusive retry under the same total budget. A retry
exceeding that budget remains an explicit resource failure. Sampling can
overshoot between observations and is not a kernel quota. OtherWorkspaces and
container quotas/permissions are unchanged.

Historical groups retain their own at-most2liveREPL/24GiBAS-per-process point.
Never pool their clocks with the new resource point.
[Historical implementation and actual fault/positive qualification](../artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/README.md).

| Workload | Retained input/version | Current scope |
|---|---|---|
|miniF2F|244tasks×32=7,808,Lean4.9rc1|Completed native/GPU pair; failure profile and first-success work|
|GoedelWorkbook|29,750original Lean4.27files|Completed three-pair frozen CPU baseline; not32siblings/task|
|ProofNet|186tasks×32=5,952,Lean4.9rc1|Earlier complete controls retained without expansion|
|Lean code verification|Pinned Verina/miniCodeProps/CLEVER/lean-mlir sources|Original Verina189 native/profile complete; real compiler SAT/LRAT timing still unmeasured|
|Verus/SMT|Version-aligned original traces|Prior negative/compatibility results retained; broader systems claims open|

Released candidates are replay inputs, not generator arrival traces.
Old unbudgeted/OOM/ENOSPC captures remain stopped partial records; do not pool
them with the current point. [ENOSPC preservation/repair](../artifacts/linarith-oracle-2026-10-17/enospc-recovery-20261020T0840/README.md).

## Completed GPU counterexample pair

[Complete corrected native/GPU pair](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md):
all7,808statuses and3,014accepted IDs exactly equal;4,669Leanerrors/
83timeouts/42resourcefailures on both sides. Native21693.761299439s versus
GPU23615.030439515s, **8.856321%slower**, plus23.989769s own preparation.
One fixed-order shared-host pair; no causal variance estimate.

All42sameIDs have std::bad_alloc under24GiBAS,42exit134records/side, zero
aggregatewatchdogkills/errors and no owned survivor. Failed bodytime0means
missing clock, not zero cost. SampledRSS46.87/47.38GiB,max2.
The complete cold-controller stopwatch is unavailable after observation
outage. Actual client/provider exit0 and ownedJob deletion are recorded;
8,345.949707s observer delay is not computational cleanup. Do not fabricate
a clock from another measurement.

34exact refutations occur in29ordinary-error candidates; no timeout removed.
Their cumulative nativeHTTP34.070886s/body28.410035s are not saved whole wall.
6,187deviceentries/6,186batches/onecross-source batch/1,528sources, no invalid
exact witness. The old25sources/78timeouts/984of1020numbers come from a
wrapper with109acceptance regressions and are not final coverage or a strict
0.2%bound. All old failed/partial data remain. No further expansion of this
screening pair; retain it as a small component.

## Current failure-hotspot diagnostic

[Plan](../artifacts/lean-failure-profile-2026-10-25/plan.md),
[real24qualification](../artifacts/lean-failure-profile-2026-10-25/preflight-result-review.md),
[full480 output](../artifacts/lean-failure-profile-2026-10-25/full480).
The fixed native-ranked slowest10%FAILED group has480of4,794sources:
83timeout/355Leanerror/42resourcefailure. Original83/old78mapping is retained.
It covers93.5659%of failed cumulativeHTTP, not that fraction of whole elapsed.

The C-only native runtime-boundary qualifier preserves4valid/18Leanerror/
1timeout/1resourcefailure, allsource attribution, no sampler/table/clockfaults
and complete retirement. Native/profile326.646616/326.839955s does not prove
zero overhead. The failed C++ ABI diagnostic remains. The completed
[full480 result and root self-review](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md)
retain all 480 outcomes, unchanged statuses, per-source rankings, 44.49 GiB
sampled peak RSS and zero watchdog kills/errors. All descendants retired.
Timeout endpoint attribution puts interval_cases at 55.19% and simp_all at
28.21% of observed timeout thread CPU. This is not a failure witness or speedup.

The earlier [primary memory join](../artifacts/source-memory-attribution-2026-10-25/result-review.md)
already observes477sources. A [body/full-read-window sensitivity check](../artifacts/lean-failure-profile-2026-10-25/body-memory-association-20261026/README.md)
retains435(310errors/all83timeouts/all42resourcefailures),33,039rows that are
a subset of the earlier34,130body rows. All125timeout/resource per-worker
sampled maxima are unchanged. This is the same old2worker/24GiB-AS observation,
not a new dataset,source-only demand,uncapped predictor or performance gain.


Profile counters distinguish child-subtracted threadCPU, nested wall spans,
sampled active tactics and unfinished timeout frames. Auxiliary offline
analysis/cache preparation shares the sampled budget; its actual intervals
remain as separate receipts and potential shared-host contention. Do not use
a partial distribution, missing failed-body clocks or nested/concurrent sums
as a removable whole-wall fraction. No new method is assumed to work from
a tactic's source spelling.

## First-success scheduling

[Complete existing-data opportunity](../artifacts/candidate-scheduling-2026-10-25/result-review.md)
joins all7,808native records with244task identities, retaining18literalNone
failures.142tasks have a valid sibling;102have no observed successful
candidate. Only17of83timeouts are in those142tasks;66remain in groups with
no observed success. This is not a claim that their theorem is false.

Two-worker fixed-HTTP-cost models give~1.45–1.48x for original/short-code
first-success policies and~1.50x for hindsight valid-fastest order. Zero
prediction/cancellation/setup cost and unchanged request spans are optimistic
assumptions, not measured speed or a physical Amdahl ceiling.

[Whole-task-held-out lexical predictor](../artifacts/candidate-scheduling-2026-10-25/crossfit/result-review.md)
does not improve: first-k1/2tasks92/105versus92/112original; modeled
15051.031831s versus14803.176432s original cancellation. Keep the negative
fit without adding a redundant long full cell or a parameter grid.
[Runtime implementation/plan](../artifacts/candidate-scheduling-2026-10-25/plan.md)
still compares native all-candidate, original first-success and short-code
first-success. Model/source sorting, queued cancellation, output handling
and cleanup enter the complete consumer clock.
[Real eight-candidate qualification](../artifacts/candidate-scheduling-2026-10-25/native-qualification-20261025T0715/result-review.md)
preserves the solved task and cancels three queued siblings only after a
checked winner. Its startup-dominated clocks do not establish a gain.
The original7808 scheduling matrix has completed at its frozen resource point;
[launch identity](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730.launch.json)
and actual terminal files own status. Do not restart a healthy capture.

The [completed all-candidate cell](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/all/result-review.md)
returns3014valid/4669errors/82timeouts/43resource failures with the exact same
accepted IDs as the historical native reference. minif2f-7231changes from
timeout to native bad_alloc; all43resource clocks remain unavailable rather
than zero. The [complete first-original cell](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/first-original/result-review.md)
takes15385.386818s versus21746.811714s:1.413471885x(29.252219%less elapsed).
Exactly142solved tasks match;3631sources execute and4177pending siblings are
cancelled against checked same-task winners. Executed labels/source bytes
match the paired all cell.65timeouts/35bad_alloc remain;body zeros areunknown.
Peak sampledRSS42,856,058,880bytes,max2REPLs,0watchdogkills/errors;cell retired.
The [complete three-cell matrix](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md)
includes first-short15112.118703443s:1.439031293x(30.508808%less).
It preserves142solvedtaskIDs,executes3724,cancels4084,with66timeouts/32bad_alloc.
7231changes all-cellbad_alloc to timeout;acceptedtasks unchanged.
Allgroup/cellprocesses retired,group exit0. First-shortpeakRSS43,824,566,272B,
0watchdogkills/errors. Raw failures/cancellations preserved. This single
shared-host old-point comparison is not isolated replication,new4worker
throughput,RL per-candidate rewards or a scheduling novelty claim. This is the frozen old point,
separate from the next uncapped dynamic-resource comparison.


## Lean code-verification workloads

[Pinned official sources and primary-source review](tmp/bootstrap/step-0011-20261023T195335-0700/literature-20261025-code-verification/report.md)
and [prepared environments](../artifacts/lean-code-verification-2026-10-25/sdk-preparation-review.md)
retain exact commits, licenses, toolchains and incomplete/reference boundaries.
The [complete original Verina189 measurement](../artifacts/lean-code-verification-2026-10-25/verina-full189-20261025T0725/result-review.md)
uses pinned4.18SDK/Mathlibaa936c36: 46 no-explicit-admission exits, 139 admitted
stubs and four API errors, exactly matched by the profiled run. Whole native
and diagnostic clocks are48.841915/53.948885s. The completed-reference subgroup
has8.909486s of nearest-simp trace wall slices, with no observed above-threshold
bv_decide/omega/decide/grind. Trace absence is not zero time. Its published
synchronous120s per-file limit remains a distinct protocol point from miniF2F300s.

miniCodeProps includes library/test material; CLEVER has many stubs.
FVAPPS gated contact-sharing terms are not accepted; accessible work continues.
Lean-mlir's exact nightlySDK/source are prepared; both public cache paths have
zero hits, so cache exit0 is not readiness. The real SLLVM proof file has89
source bv_decide mentions and a static58project/498external-module closure.
These are not executed calls, timing or GPU-ready coverage. Native source
build and profiling proceed after the current collection retires, without
substituting a different version or reproducing competitor prover systems.

## Frozen comparisons and limits

The external CPU oracle is a retained baseline, not novelty or future work.
[All29,750originals/threepairs](../artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/full-result-review.md)
give55,671.765767/50,323.789966s aggregate=1.106271x, with two native
rejections becoming checked completions in every pair, same40timeouts.
This is not transparent outcome equality or globally strongest-CPU proof.

[Matched selected1,000](../artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023/full-result-review.md):
native1376.236473s/CPU769.116831s/GPU762.439983s; GPU cold797.608028s is
3.7044%longer than CPU. No useful additional GPU gain established.
[Own-clock helper attribution](../artifacts/linarith-oracle-2026-10-17/native-stage-profile-20261022/reference-full-result-review.md)
finds39.935943s floatingLP and951.845679s exact fallback within its own
1380.322631s lifecycle; overlapping phase sums are not a strict GPU ceiling.

[Retained miniF2F existing-method control](../artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/full-pair-result-review.md)
is1.304587%slower, with five native success regressions and11incomplete
responses. [ProofNet control](../artifacts/linarith-oracle-2026-10-17/shred-closing/proofnet-full-result-review.md)
is4.73%slower with20reject-to-incomplete changes. Do not expand these
integrations. E038runtime/metadata/defeq/declaration/SMT-prefix constructors
stay closed; old20.9xresidentmetadata and14.6xwarmREPL proxies are not end-to-end.

## RQs, paper and provenance

The [InitialNarrative/fourRQs](idea-story.md) remain preserved and unanswered
at their full promised Lean/SMT/service scope. The latest user explicitly
directs three continuing routes above. Ordinary external certificate search,
native compilation, first-success scheduling, snapshot/prefix reuse and
counterexample testing alone are not new systems contributions.
[Current paper](paper/main.tex) follows verified results; a33page draft and
root self-review do not establish submission readiness or independent audit.

The previous389line evaluation is preserved byte-for-byte in
[dated gzip](tmp/bootstrap/step-0011-20261023T195335-0700/evaluation-history-through-20261025T0705.md.gz);
its relative paths were authored from docs/evaluation.md.
[A readable pinned copy](https://github.com/yunwei37/gpu-smt/blob/352b8ed/docs/evaluation.md)
keeps that location. Earlier archives and exact raw data remain linked there.
The [current step/self-audit](tmp/bootstrap/step-0011-20261023T195335-0700/step-report.md)
records transitions, root dispositions, failures and publication.


### Exact-source sharing in the original miniF2F population

The Rust engine supports exact result and in-flight sharing, but the original
7,808 sources contain 7,791 unique byte strings. Their only duplicate group is
18 literal None errors, leaving 17 repeated executions after the first.
Those repeated historical HTTP intervals sum to 13.337753652s out of
43,121.2401169s (0.03093% of cumulative intervals). This is not whole lifecycle
time, nor evidence of a new-resource speedup. No substantive proof candidate is
byte-identical here. Retain exact sharing as a component, not a novelty or major
performance claim. [Executed existing-data analysis](../artifacts/engine-resource-profile-2026-10-25/exact-duplicates/result-review.md).

Original lean-mlir code-workload prerequisites now [compile in the unchanged root package](../artifacts/lean-code-verification-2026-10-25/native-project-prerequisites2-20261025/result-review.md):60native targets/checks pass,with actual source/pins and combinedRSS retained. The bv_decide workload root remains unexecuted; no SAT/LRAT time or acceleration claim is available yet.

The optional Rust import backend now [evicts idle prepared state for an exclusive
resource retry](../artifacts/prepared-engine-2026-10-25/resource-retry/result-review.md),
then uses fresh native execution within the remaining deadline. Exact source
6e3d858passes four executed pinned-native differential/lifecycle tests and
ordinary RustCI. This is a resource-composition repair; fullMathlib/native
population and matched-throughput measurements remain outstanding.

The opt-in interval continuation has18executed native controls/nine matching
pairs,while [pre-expansion domain observation](../artifacts/hotspot-mechanisms-2026-10-25/interval-bound-profile/result-review.md)
has a separate nine-pair qualification and exact48source/116call preparation.
Original48runtime/demand-driven failure fractions remain unmeasured. Native
delegation/parse controls do not certify global failure,timeouts or novelty.
The [simp progress observer](../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/progress-repair-result-review.md)
retains actual native origins with seven matched control pairs;original23
phase/lemma attribution is still pending. Prior lazy-name placeholders and
sidecar-inflated source counts remain as explicitly invalid diagnostic attempts.
The closed-tail rule stays frozen at0/71original coverage.


The [new dynamic resource acquisition](../artifacts/engine-resource-pair-2026-10-25/full7808-20261026T004621Z.launch.json)
is now running under implementation42659a8:all7808originals,48GiBaggregateRSS,
CPU8–11,onecorelease,unlimitedAS,matched freshnative then Mathlib-derived.
[Real24qualification and transport repair](../artifacts/engine-resource-pair-2026-10-25/qualification24-20261026T003542Z/result-review.md)
preserve21accepted/3rejectedwith exactmatched sets;oneparentloads5545modules.
The firstbuffered-outputhang stays as an interruptedpartialrecord.
[Flushed native-attempt persistence](../artifacts/engine-resource-pair-2026-10-25/journal-control4-20261026T004354Z/result-review.md)
retains physicaloutcomes before finalCapture. These controls are notwholeflow
gains;the fullnewresourcepoint remains unfinished. Resourcepreparation is
priorart,not a strongestwarmbaseline ornovelty result.

The source backend now preserves declared compiler argv without changing default
flags or source bytes. [Step0041](tmp/build-and-evaluate/step-0041-20261026T011417+0000/step-report.md)
qualifies transport and compiles native differential coverage; original lean-mlir
file/stdin and profiler measurement still follows the sole dynamic full pair.


Original-file source checking now shares the Rust native lifecycle rather than
assuming stdin preserves filename/module context. [Step0042](tmp/build-and-evaluate/step-0042-20261026T013224+0000/step-report.md)
adds file/argv identity, pre-launch source-byte checks and local transport tests;
nightly whole-module file/stdin/profiler runs remain pending after full resource
pair. The retained SDK source exposes actual SAT/LRAT phase hooks; their presence
does not measure phase cost or executed bv_decide coverage.


The [original48 traversal inputs](../artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/original48-preparation/README.md)
now preserve48 complete original/import-control/experimental variants:
34 two-range,8 three-range,6 four-range chains,116 native sites. All generated
sources parse in pinned4.9 with exact variable/span/inverse checks. This is
syntax/preparation, not48 proved failures or a measured speedup. Native
left-associated stage accumulation differs from nested closing continuations;
the failed-leaf-to-global-failure claim is not admitted. Original48 runtime
failure/timeout proportions and23simp phase attribution remain unmeasured.

Complete per-attempt stderr capture is now an opt-in source-backend facility,
rather than relying on the64KiB response tail for diagnostic attribution.
[Step0044](tmp/build-and-evaluate/step-0044-20261026T021123+0000/step-report.md)
retains large-stream/error/retirement qualification; original23/48 runtime
measurements and full nightly code profiling remain pending. Transport-complete
EOF after interruption does not make the recorded native phase complete.


[Step0045](tmp/build-and-evaluate/step-0045-20261026T025106+0000/step-report.md)
adds optional completion-order delivery with unchanged verification semantics,
explicit terminal counts and subscriber-scoped disconnect handling. Tests prove
early body delivery with a gated peer, cancellation independent of reads, real
subprocess retirement and surviving shared RL demand; they do not measure native
stream latency or throughput. The frozen fullpair remains at42659a8.
The existing task-held-out lexical ranker remains a negative offline result;
no new model is trained from ambiguous old per-request RSS or incomplete new data.

## Interval first-stage mapping preparation

[Step0046 implementation evidence](../artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/first-stage-map/README.md)
adds opt-in leaf mapping with survivors,not a detector. All48original sources
(116sites) parse natively;19norm_num-first chains preserve later native suffixes,
17omega and12simp_all chains have no later suffix. Definition compilation and
22small control source parses execute zero candidate proofs. Exact inverse edits
and unchanged default-close source artifacts pass. Runtime parity,resource
savings,end-to-end speed and sufficient-failure coverage are unknown.
Existing0/71closed-tail result stays frozen. New construction/tactic interleaving
is still experimental; service rejection remains disabled. No RQ is closed.

## simp_all phase completeness dependency

[Step0047 source/diagnostic validation](../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/phase-completion-20261026/README.md)
labels native reassert/clear and per-hypothesis initialization previously hidden
by the observer. Actual retained4.9definitions compile;four analyzer tests keep
legacy native timings/origins unchanged while classifying legacy action outcomes
as unknown. This does not execute the23originals or establish failure/cycle
coverage. New observer parity/overhead remain pending;no detector is enabled.

## Idle-headroom liveness repair

[Reproduced and repaired boundary](../artifacts/rust-engine-2026-10-25/idle-headroom-20261026/README.md):
a forecast below total memory can exceed idle headroom and otherwise wait with
no active peer to retire. Initial exclusive admission now uses existing idle
preparation reclamation,still subject to actualRSS/watchdog/CPU policy.
A fixture regression fails on old code and passes after repair;49ordinary tests
pass. Pinned-native CI will exercise actual engine-to-parent eviction;not locally
executed alongside the fullpair. Current fullpair remains42659a8and no native
performance or original accepted-set conclusion follows from this fix.

## Dynamic-resource7808 native boundary and failed prepared cell

[Exact native/partial prepared record](../artifacts/engine-resource-pair-2026-10-25/full7808-20261026T004621Z/README.md):
native7808complete at3013accepted/4665rejected/87timeouts/41resource exhausted/
2backend faults,28466.132239s external cell. Historical accepted ID3086now
times out;no accepted-set equivalence or cross-point speedup is established.
85watchdog events;all-monitor peak48.788876GiB exceeds the sampled48GiB budget.
Prepared terminates ENOSPC with2408physical attempt rows,no completeCapture;
no pair ratio is available. Failed/raw data and lossless repair receipts remain.
Storage cache/core archival repaired writable space without changing quotas,
nativeflags or otherWorkspaces. Next native sequence is42exclusive reruns,
71timeout prototypes,then original lean-mlir. Completing the prepared comparison
remains open;partial physical rows cannot substitute for finalconsumer results.
