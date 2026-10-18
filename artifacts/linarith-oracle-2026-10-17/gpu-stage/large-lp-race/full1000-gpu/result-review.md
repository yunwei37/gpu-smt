# Complete large-LP CPU/GPU race, true multi-candidate batches — root self-review

## RQ and fixed protocol
RQ4 heterogeneous execution. The same original1,000arithmetic-heavy sources, corrected family-only headers, width8, upstream48GiB, CPUs0–3 and original source order are used for pooled native, CPU AST oracle and GPU race. Methods run sequentially. The GPU server and every numerical client/child share the same four permitted CPUs; the existing shared RTX5090 is additional hardware, not an added CPU budget. The native reference is the qualified independent-daemon pool using original CPU hybrid, not the slower serial-native control.

This frozen implementation races eligible row≥11LPs before any FP search. Each CPU/GPU numerical child returns either an exactly verified coefficient certificate or failure. GPU floating output is only a support hint; CPU exact repair and Lean checking remain mandatory. Small direct FP misses fall back. A numerical child that loses is killed and waited; withdrawal cancels the joint GPU batch and surviving requests are requeued while their CPU shadows continue. MinimumGPUbatch is two live requests.

## Complete matched outcomes and clocks
| Method | Whole seconds | Native / method | Complete / rejected / operational |
|---|---:|---:|---|
| Pooled native | 1237.370439599 | 1 | 992 / 8 / 0 |
| CPU AST oracle | 1037.849203905 | 1.192244919 | 992 / 8 / 0 |
| GPU race, warm upstream server | 1020.121393778 | 1.212963915 | 992 / 8 / 0 |
| GPU full cold lifecycle | 1036.252508600 | 1.194081973 | Same GPU verification cell |

All1,000source verdicts and non-message native JSON fields agree. CPU has88warning-only response changes relative to native; GPU has98. Native task spans cover every source. Warm whole includes the0.087549870s proxy setup/retirement overhead. The full lifecycle includes5.8002015s from creation toPodReady,1022.1180082s client wrapper,8.3305059s collection/retirement/restoration. CUDA/API readiness is also inside the client wrapper; PodReady is not called numeric warmup. No pre-cell numeric warmup was run. The finiteJob is deleted, labReady=True and the otherWorkspace remainsRunning; exact UID/lifecycle receipts and server logs/affinity live in ../../cuopt-target/.

The observed warm GPU/CPU ratio is1.017378138x; adding its full lifecycle gives1.001540836x versus CPU. This is one full observation, not replicated evidence of a stable GPU advantage. It is below the more-than1.5x overall target and does not meet the continuation result standard. It does NOT establish a GPU impossibility bound or authorize negative project closure.

## Real batches, cancellation and numerical outcomes
There are384submitted GPU jobs:358pairs,20triples,4quads and2five-request batches. Every submitted batch has the same number of distinct source labels as requests: these are real cross-candidate batches.73jobs return results;311are cancelled after a member withdrawal; all384have client-retirement receipts and dispatcher pending_jobs=0. The all-submitted counts include cancelled work, rather than counting only returned jobs as GPU engagement.

4,656labelled LP races end in3,352CPU certificates,1,214CPU-no-certificate results and90GPU repaired certificates. Summed retirement costs are4.619732779s; summed decision intervals are541.042309826s. They overlap and are not disjoint fractions of whole verification wall.

The proxy records2,433numerical requests and1,320error replies. These are numerical cancellations/failures charged to the CPU fallback path, not1,320native operational failures. Native operational count is zero. Exact errors and source/call IDs remain in raw requests. The server reports18.399solver seconds for jobs that return; cancelled-job device compute is unknown, not zero. Summed client batch/retirement intervals83.903565945s includeRPC and cancellation, not a GPU-kernel stopwatch. No unsupported Amdahl input is derived from them.

## Heavy tail
Select identities using the native reference, then compare the same sources. For the slowest1% (10sources), summed command-service spans are505.9692s native,389.9932s CPUoracle and391.7585s GPU. GPU does not improve the CPU oracle on this group. For the slowest10% (100sources), sums are1266.4538s,948.4037s and927.6876s; their occupancy unions are1060.8097s,844.6244s and837.6370s. The sums overlap and are not cohort elapsed; see paired-analysis.json for exact source identities, per-method-selected tails, all spans and quantiles. GPU maximum on the native-selected tails is79.6602s vsCPU80.7477s and native79.4477s.

Historical stacked-header phase costs are no longer attached automatically by analyze-batch.py. Explicit legacy attachment requires --historical-phase-profile and is not current pooled-cell attribution. The default analysis here has no cross-epoch phase join.

## Limits and next decisive work
The original CPU/native resource samplers have zero read errors; GPU sampling has203proc-read errors while transient race processes exit. GPU sampled peakPSS9.789GB/RSS10.464GB is a sampled lower bound with incomplete reads, and excludes the separate cuOptPod. Collector/waited-childCPU is not complete serviceCPU or device compute. No resource-superiority claim is made.

The separate width4 own-clock profile's conditional1.93412x opportunity does not transfer to the faster pooled baseline. Its new width8 pooled-family profile passed real24source parity/telemetry qualification and starts only after this actual GPU lifecycle retired. It will supply its own native/oracle phase clocks, allLP+numeric product attribution and1%/10% source tails. GPU closure remains open until applicable opportunity evidence supports the user criterion.

Cancellation affects311/384=80.99%of submitted jobs. Together with the completed native trace's4393cheap FP-only eligible calls versus1636exact-fallback calls, this admits a private FP-first exact-fallback hardware qualification, not another full grid or an unmeasured performance claim. Its CPU24source parity qualification passes. The active original full cell is never hot-edited; every failure/partial/raw result is retained.

All implementation/execution/analysis/review is performed by this thread. This is self-review, not independent audit. No OMP, subagent or native research session is started. Hourly automation remains active; OSDI acceptance or a finished paper is not claimed.
