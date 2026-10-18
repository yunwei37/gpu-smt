# Completed first full GPU variant: slower and eight operational failures
All1000 original candidates were attempted under the frozen phase-I PDLP/crossover implementation and48GiB cap. Whole wall3374.147306631 seconds,984 complete/8 rejected/8 operational. This is a completed finite run, not a successful verification-parity result. The new HiGHS/native controls continue automatically under the same driver; their matched comparison is pending.

Against historical same-cohort native primary3 (2325.931717792 seconds), the descriptive ratio is0.689339x (GPU45.07% longer). This is context only, not the pending matched-order estimate. The original three-pair CPU oracle result remains1.346679850013x. No CPU-only closure or final best(CPU,GPU) claim.

1854 support requests formed1835 actual GPU batches:1816 singleton and19 pairs. Thus only38/1854requests (2.05%) participated in multirequest batches; no claim of effective large native batching. Sum unique batch solver time1129.332seconds, maximum443.788seconds. Returned states1795 optimal/40 primal-feasible; current frozen client requires optimal before exposing hints, so some finite nonoptimal points are discarded and fall back. Individual solver times are not pure GPU kernel time and cannot be added to overlapping CPU phases as disjoint wall.

[Raw cell and numeric records](.), [recomputable summary](gpu-cell-analysis.json), [expired-owner PDLP trace](../cuopt-target/live-pdlp-result-review.md), [actual finite cleanup](../cuopt-target/full1000-cleanup-receipt.json). All eight operational responses differ from historical native outcomes (indices332--335,756--759). Two source task-end records are absent,335 and759; the other six task spans do not recover responses discarded when the four-source wave expired. Top1%/10% observed job rankings are explicitly censored; do not call them complete-cohort tails. Same final native comparison remains pending.

The upstream Job was deleted after GPU host-proxy retirement; the other GPU Workspace remains Running and lab Ready. All source, raw/failed results and other experiments remain. A direct-feasibility and per-client cancellation repair is justified by the measured444-second convergence/stale ownership defect, not by a speculative GPU kernel grid. It must pass real difficult-LP and native preflight before any new full run. Root self-review only. Goal/hourly remain active.

## Solver-tail concentration
Of1835GPUbatches,21(over10s;1.14%) consume930.020/1129.332solverseconds(82.35%). The slowest job alone443.788s(39.30%); top10jobs785.851s(69.59%). This is numerical-batch ranking, not candidate-wall ranking or removable end-to-end time. [All tail/shape summaries](gpu-solver-tail-analysis.json). Requests entering robustGPUfallback have median82rows/230cols/1538nnz, p99=323/741/6967, max730/2628/17569. These are selected robust-fallback calls, not the median10x20 of the entire native LP stream. The actual444s trace attributes one heavy job to PDLP convergence. No inference that every batch is a large efficient GPU workload or that all tails are due to transport.

## Import-graph qualification and precise stale-owner binding
Native environment inspection subsequently finds that this measured version
loads both legacy/new arithmetic elaborators. Failed attempts can continue into
earlier handlers. Its results stay version-scoped and do not establish the
leanest-reference or corrected-oracle performance. See the
[real corrected-header qualification](../header-correction-preflight24/result-review.md).
No completed or partial value is erased or relabelled.

The slowest completed backend record is call1452, a singleton26x96/500nnz request
before phase-I slack. Its actual clientarrival lies uniquely in wave756,
and its response ends296.092205409seconds after that wave expires.
[Raw-clock binding](slowest-LP-arrival-wave-binding.json) strengthens the earlier
server-submission-only association, without inventing an individual source ID.
The independent PDLP convergence cost remains real; header correction alone
does not explain it.

## Same-plan full controls closed, 2026-10-18T02:06Z
All three frozen stacked-header cells are now terminal. The paired native
reference is 2331.394867909s, 992 complete/8 rejected/0 operational; robust CPU
HiGHS is 2363.001837636s with the same outcomes (0.986624x). GPU is
3374.147306631s, 984/8/8 (0.690958x, 44.73% longer), with eight outcome changes.
These are the actual same-plan denominators; the earlier historical-primary
ratio above remains descriptive history. All cells use48GiB. The method's
stacked arithmetic import graph remains a protocol defect; no corrected-family
claim or universal GPU impossibility follows from this closed comparison.
The single pidfd collector fired on actual driver exit; no goal-minute wait
was used to receive it. [Raw and recomputable full pair](paired-analysis.json).

Baseline-selected candidate tails, not LP-call rankings:

| Baseline-selected sources | Native task interval sum (s) | HiGHS task interval sum (s) | GPU task interval sum (s) |
|---|---:|---:|---:|
| Slowest10 |713.667|1135.543|1092.635|
| Slowest100 |2023.488|1801.023|1862.124 (99 observed)|

Task sums overlap across concurrent commands; they are not whole elapsed
savings. GPU source335 is censored in the top100; the top10 has complete spans.
Joining those exact IDs to the separate earlier diagnostic gives top10 native
LP38.895 CPU seconds, preprocess/linearize171.250, product proof53.523 and
certificate79.453. Top100 gives354.916/242.384/121.140/121.944 respectively.
Four source-unlabelled numeric calls can add up to1.664LP CPU seconds to
the top100; they do not intersect the top10. The diagnostic predates family-only
headers. These are workload-composition counters, not measured primary
critical-path fractions or same-run GPU savings.

## Heavy convergence is not exclusively no-certificate work
All21 batches above10solver-seconds return PDLP_OPTIMAL. Their reported
phase-I objectives range from-6.66e-16 to4.09e-6; the444-second batch reports
3.53e-12. These floating values do not prove original feasibility, but the
measured tail cannot simply be described as solving only no-certificate
instances. [Actual tail objectives/shapes](solver-heavy-tail-floating-objectives.json).
The physical work is the measured convergence/queueing of small sparse
systems, not a demonstrated large-device throughput advantage. No new
numeric parameter search follows from this additional attribution.
