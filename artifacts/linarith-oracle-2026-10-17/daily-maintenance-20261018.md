# Daily repository maintenance and research reflection — 2026-10-18 local

## Repository maintenance

Source, benchmarks, raw artifacts and docs/paper retain their existing homes.
README and evaluation distinguish current primary performance, paired
diagnostics and answer-aware controls. The complete LP figure has its CSV,
source and unchanged gate provenance. New collector options use the existing
native API and existing finite GPU lifecycle. Historical failures and other
authors' work remain preserved.

Ten closed runtime logs are losslessly compressed after checking that no
process has them open. Their retained gzip contents are compared with the
original bytes. This recovers 1,471,750,144 bytes, bringing the project volume's
free space to about 4.10 GB at that observation. Published raw archives and
active collectors are preserved. The compression receipt names both paths.

Paper source compiles with no overfull boxes; the latest result additions are rendered and checked. The earlier version was 22 pages with no overfull boxes. Rendered pages 15–16
are visually inspected for the four-region table, LP distribution figure and
known-answer result. This is targeted validation, not completion of full
writing refinement or a paper acceptance review.

No new Workspace, scheduler, persistent GPU server, model, credential or
storage setting is introduced. The one hourly task remains active. All work
is by this root thread; reviews are self-review.

## How to make substantive progress

The central uncertainty is why numerical search has substantial removable
cost but current GPU execution changes whole verification time very little.
The full answer-aware control now takes 767.62 seconds versus fresh native
1,228.00 seconds: 1.600x with Lean checking retained. It cannot count as valid
acceleration, but it prevents a premature below-1.5x impossibility claim.
An actual solver has little remaining room for search, transfer and scheduling.

More batching alone is insufficient. The original joint-model GPU run cancels
311 of 384 batches. Independent cancellation removes that coupling, yet the
24-source GPU qualifier remains slightly slower than CPU oracle. The next
causal question is precise: source 37 waits 22.548 seconds for a second GPU
request and never gets submitted. That source is absent from the first
24-source qualification. Test the already-frozen native slowest ten with
immediate independent admission and fresh matching CPU/native references.
A negative result rejects this integration without pretending to prove all
GPU designs impossible. Do not replace this question with a solver flag grid.

The common baseline also matters. Native eight-queue submission is already
upstream; it is not our contribution. Its real CPU qualification improves
27.22 to 23.48 seconds. A full matched native/CPU run through that interface is
now needed before any new representative GPU claim. Generic batching, caches,
ordinary native compilation and an external arithmetic oracle do not by
themselves establish new systems novelty.

## Actions implementing this reflection

The complete own-clock profile and full known-answer control are in main.
The eight-queue GPU qualifier and independent-cancellation qualifier are
complete with raw native responses, task spans, job cancellation/retirement
and cold lifecycle receipts. Both GPU Jobs are deleted with lab Ready and the
other Workspace Running.

The full 1,000-source native/CPU queue comparison starts at 07:59:10 UTC on
CPUs 0–3. The frozen ten-source tail native/CPU comparison completes with
206.68 and 173.26 seconds. Its matching immediate-admission GPU qualification
completes in 170.26 warm seconds after its 08:11:32 UTC start on CPUs 8–11. Its complete cold lifecycle is 191.47 seconds; all ten native verdicts match, all six single-LP jobs retire, and the Job is deleted. RPC peak is one, so no actual cross-candidate batching is claimed for that tail capture. The original prefix
capture is preserved on its own CPUs. These are real experiments rather than
repeated health polling. Full RQ coverage, a supported systems contribution
and the paper's complete research process remain unfinished.

The full source-native queue reference has now closed at 685.73 seconds with exact complete native JSON parity, versus the older 1,237.37-second wave reference. The matched CPU oracle completes in537.31seconds(1.27622x),with the same992complete/eightrejected outcomes and88warning-only changes. This stronger baseline invalidates transferring the earlier wave-only opportunity denominator; any subsequent attribution must use the queue protocol and its own clocks. Published source commit cde662a also passes benchmark-smoke CI: https://github.com/yunwei37/gpu-smt/actions/runs/39110354163 .


The first queue-profile qualification is explicitly invalid: the root omitted
the existing row11 environment parameter and numerical panics were masked by
Lean fallback. Raw failure data are preserved. Required-input validation and
the corrected launch remove the fault:24native/24oracle results match primary
verdicts,231/125calls have complete metadata,all4/5workers have complete EOF
and wait4receipts,and no numerical error or stderr remains. The new full
own-clock queue profile starts08:28:53UTC on CPUs0–3 after actual primary
pair completion. It is a diagnostic for the user's Amdahl question,not another
GPU variant or an achieved speedup. The invalid clocks are not published as
an instrumentation-overhead conclusion.


## Follow-through after the completed queue profile
The full matched queue attribution completes at691.20native/545.05oracle
seconds with exact primary response parity and complete all-call/worker
receipts. Its LP interval union75.53%cannotbe substituted for causal saving.
An optimistic union-deletion model5.18x remains above the user's threshold,
so negative GPU closure remains unsupported.

The trace-driven Nat/Int coverage hypothesis is implemented and tested,
rather than left as a proposal. It eliminates unsupported-type errors and
passes alltennative outcomes,but158.02seconds is worse than143.75seconds.
The full source and negative records remain reproducible; it doesnot replace
the default and no full matrix opens. Successful-branch LPsearch is small
beside observed Lean checking,so type support alone is not the bottleneck fix.

The next GPU admission should target the actualhard numerical work:518.39CPU
seconds in1,888FP-failed moderate LPs,not the whole-verification Nat tails.
The exact-stage median is82rows/230columns and different-source searches
overlap for221.40seconds. A solver/formulation suited to finding a feasible
basic support,with exact CPU repair and the same Lean check,has more decision
value than another thread/cache/precision grid. A strong CPU numerical
baseline must accompany it; simply choosing a different established solver
willnotbe claimed as systems novelty.


Follow-through:the complete own-clock profile and Nat/Int negative attempt are
pushed728952c. Exact-LP-head10 finds a stronger CPUHiGHS control18.13s vs74.44s
native;fresh full1000three-cell capture runs automatically,not idle waiting.
Barrier encounters reproduced async allocation failure under48GiB;two failed
finite loader repairs are retained and not applied as services. A substantive
legacy-allocation device-batched phase-I solver is compiled/run on5090:five
actual2/3-source CUDA launches,independent model cancellation,one exact checked
GPUcertificate,all launchesretired. Its37.98sselectedpreflight trails18.13sHiGHS,
so no full unprofitable candidate matrix is started. The observed numerical
weakness is degeneracy/scaling (up to16745pivots),notmissingbatching alone.
The next single numerical repair is row/column equilibration plus reduced-cost
pricing on the same10;no parameter grid/new cohort. Full CPU results,not another
report,will decide whether the stronger published numerical baseline clears1.5x.
The remaining mainline gap is a real system contribution surviving strongest
native/HiGHS and completedGPU comparisons;these controls do not create novelty.


Nextactualstepcompleted:the fullCPUtriple closes691.10/529.17/462.50s,ratio1.49425x.
Itsremainingnegativeexactraces177.756sleadstoimplementedtwo-sidedcertificates.
Afteronefailedreconstructionrepair,110negativecertificatesvalidateonreal10,
newCPU28.60vsoldoracle40.85s(nativematches28.58). GPUnegativevariantreallyruns
18negative+2positivecertwinsbut42.58s,slowerthantheCPUdualcontrol. Newfull1000
CPUtriple193488nowexecutes;no polling-onlygoalturns ornewunprofitableGPUmatrix.
Remainingpaperdecisionisfullgain/noveltyafterthisstrongerbaseline,notmoreLP
kernelflags. Allreviewisself-review andallfouroriginalRQspreserved.

Furtherfollow-throughwhilemaincaptureishealthy:primarysourceworkconfirms
dualLPcertificationandone-block-per-LPbatchingareexistingwork,nowexplicitly
citedinpaper/canonicalmap. Oneequal-four-CPU32queue64sourceprobeactuallyruns:
CPU39.66s/GPU45.02s,allnativeoutcomesmatch,10real2-4sourcegroupsretire.
No continuedcapacitygridorfullunprofitableGPUrun. Existingtracesalsoexpose
exactnumericalqueryreuse,whichmustbeconsideredasCPUcompetition,notnovelty.
Remaininghighest-valueactionisclosedfullCPUdualevidencefollowedbyreal
system/servicecomparison;morelabelsorordinarykernelvariantsdonotfillthatgap.
