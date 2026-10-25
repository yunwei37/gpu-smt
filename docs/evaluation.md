# Evaluation: current evidence and open work

Updated2026-10-25UTC. This thread alone implements, runs, analyzes and writes.
All reviews are self-review, not independent audit. The original
[Initial Narrative/fourRQs](idea-story.md) and ambitious systems goal remain
open; tests, setup and a compiled paper do not establish OSDI contribution.

## Current decision: frozen oracle and three continuing directions

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

All own capture trees share48GiB aggregate sampledRSS, at most2actual live
verification REPLs including startup/cache/retirement,24GiBAS each,CPU8–11.
The independent parent samples every1s and kills the largest owned REPL on
excess, preserving source/PID/birth/resource_failure. This is a sampled
response, not a kernel RSS quota. No otherWorkspace/quota/permission changes.
[Implementation and actual fault/positive qualification](../artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/README.md).

| Workload | Retained input/version | Current scope |
|---|---|---|
|miniF2F|244tasks×32=7,808,Lean4.9rc1|Completed native/GPU pair; failure profile and first-success work|
|GoedelWorkbook|29,750original Lean4.27files|Completed three-pair frozen CPU baseline; not32siblings/task|
|ProofNet|186tasks×32=5,952,Lean4.9rc1|Earlier complete controls retained without expansion|
|Lean code verification|Pinned Verina/miniCodeProps/CLEVER/lean-mlir sources|Native environments and profiler implementation prepared; reference timing pending|
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
zero overhead. The failedC++ABI diagnostic remains. Full480rankings/result
review remain pending until actual terminal collection; the output/launch
receipt owns runtime identity. Preserve a healthy owner without restarting.

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
and cleanup enter the complete consumer clock. Actual qualification/full
measurement remain pending while the sole480profile finishes.

## Lean code-verification workloads

[Pinned official sources and primary-source review](tmp/bootstrap/step-0011-20261023T195335-0700/literature-20261025-code-verification/report.md)
and [prepared environments](../artifacts/lean-code-verification-2026-10-25/sdk-preparation-review.md)
retain exact commits, licenses, toolchains and incomplete/reference boundaries.
Verina has189taskfiles,46without explicit admission tokens; all189will be
retained. Its4.18SDK/Mathlibaa936c36 cache6471/6471are ready. The original
native/profile runner is implemented but not yet executed. Its published
synchronous120s native limit is a separate resource/protocol point from
miniF2F300s, not a new research deadline or a pooled speed comparison.

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
