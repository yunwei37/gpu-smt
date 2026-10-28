# Completed real32FIFO/task-memory development pair

Root self-review,collected2026-10-28UTC;both cells actually completed2026-10-27.
Source8045cca release,pinned native Lean4.9rc1/Mathlib,exact32originals,
all/reusefalse/300s,48GiB actual sampledRSS,CPU8–11/fourone-core leases,noAS.
One sequential FIFO-then-task-memory group,each with cold policy history.
No prior outcomes/peaks are injected. [Original setup](README.md).
Selection uses old outcomes(two resource-heavy/two ordinary tasks,first8each):
development evidence,not an unbiased final population or strongest warm service.

|Metric|FIFO|Task-memory|
|---|---:|---:|
|Whole external CLI seconds|2832.462187|2169.738637|
|Closed archival seconds|0.020199|0.017950|
|Internal lifecycle seconds|2832.456717|2169.735294|
|Accepted / rejected / resource failure|16 /7 /9|16 /7 /9|
|Native attempts|41|37|
|Retries|9|5|
|Exclusive attempts,including forecast-solo initials|11|10|
|Watchdog-marked attempts,including solo failures|18|14|
|Sampled aggregate peakGiB|48.753387|48.558949|
|Recorded over-budget samples|18|14|

Whole external ratio1.305439346x;23.397437%less elapsed. Archival-inclusive
times2832.482385/2169.756587s remain separately available in analysis.json.
The complete controller5020.974704s includes both preflights,fullcells,archival
and compare;releasebuild12.010628s and environment preparation are separate.
No complete cold deployment or causal replicated gain is claimed. A short
CPU11existing-data analysis occurred during FIFO;possible contention is retained.

## Correctness and method engagement

Exact Candidate fields/order/task/timeout/reuse match;32uniqueIDs each,no
cache/coalescing. All32raw native outcomes are exactly equal,including errors,
messages/positions and accepted IDs. There are no timeouts/cancellations/backend
faults. Every9resource failure is an aggregate-watchdog solo failure,not
semantic rejection or a prediction used as outcome.

Sources3683,3685,3686,3687each change from a preempted nonexclusive attempt plus
solo retry to one actual forecast-exclusive native attempt. Allfour still hit
the actual watchdog limit. This shows the method engaged,not a predicted-failure
shortcut. Others retain their attempt counts. It does not isolate how much
of662.723550s observed whole difference comes from these four changes versus
changed overlap/reservations/native costs. Max-sibling peaks may overreserve
small siblings and censored peaks may underestimate;no prediction guarantee.

Both fullcells'78native attempt births plus2CLIbirths are retired(80identities);
the earlier four preflight native births and original controller also retired.
Zero live matching non-zombies. The1s sampled watchdog overshoots48GiB in both
conditions,so it is not a hard RSS quota or proof of never crossing the budget.
Sampled attempt HWM is not aggregatepeak;resource journals retain actual scope.

The existing comparison's slowest1%/10%cohorts contain1/4sources selected by
baseline accumulated attemptwall. Their overlapping sums and statuses remain
in comparison.json;these are not whole-clock tail speedups or significance.
No full7808extrapolation,novelty claim or RQclosure follows from this biased32.

## Provenance and next interpretation

Original temporary sources/captures/resources remain at the run path in
ingestion.json. Closed raw streams are copied byte-for-byte;all failures remain.
Run python3 analyze.py to reproduce source/output/resource/retirement analysis.
The earlier competing-release failure is unchanged;this uses the later qualified
copied8045cca release. Existing measure/compare/native backends only,no new
logger,scheduler,oracle or competitor reproduction.

Run status:complete planned development pair.
Tested hypothesis:supported for observed fewer retries and shorter whole time
on these selected originals,with exact raw outcome equality.
Value:supporting,not representative final or independent audit.
Next:measure the same policy on all7808originals atop the actual prepared
Mathlib backend,against its own same-version FIFO ablation. This tests load
feedback after established preparation reuse. Preserve old freshnative/COW
reference results;do not splice their clocks into a different-version policy
comparison. Allfour userdirections and fullpaper goals remain open.
