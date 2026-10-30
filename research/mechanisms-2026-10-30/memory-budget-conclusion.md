# Memory/core feasibility: complete coverage matters

M branch;2026-10-30UTC;self-review. Offline simulation and retained native
evidence,not another paired run. Four cores; totals8/16/32/48GiB.

|GiB/core|Fit/excluded|Fixed-pool stress seconds*|Kill-and-drop seconds / lost|Kill,then solo retry seconds**|Peak admission seconds|
|---:|---:|---:|---:|---:|---:|
|2|7718/90|6410.77|5797.69 /10|8681.98|7194.06|
|4|7766/42|10062.13|6438.16 /49|21156.68|18543.67|
|8|7766/42|10062.13|7494.06 /38|18423.31|11498.37|
|12|7808/0|13449.45|9759.43 /48|24832.48|23163.71|

*The fixed-pool stress schedule exceeds the selected aggregate budget. It is
not a valid same-budget Kimina runtime baseline. **Zero cleanup sensitivity;
all initially preempted jobs restart alone after ordinary work drains. New
schedules change which jobs are active,so victim counts need not equal the
kill-and-drop model. Explicit1s/5s serialized cleanup sensitivities are stored
in retained-analysis/memory-full-coverage-retry.json. They are assumptions,
not measured cancellation latency. In particular48GiB kill-and-drop9759s
turns into24832s with full subset coverage even in this optimistic flat-peak
model. Dropping difficult verification results cannot be called acceleration.

These models reserve recorded peaks for each job's full recorded physical
attempt work (including historical retries). They exclude consumer queue
latency and do not invent within-job memory growth. The new retry model
preserves every fit-subset frozen label by assumption,not a Lean differential.
Timeout/resource peaks are censored; new-budget excluded rows remain unknown.
All3014 originally accepted rows fit each subset,but that does not prove new
resource policies preserve semantic or operational outcomes.

## What the native data actually establish

Same historical48GiB point: the warm pool has52 concurrent resource failures
followed by exclusive retries.41 remain resource failures;11 become timeouts.
The engine has42 preemptions followed by exclusive retries:41 resource
exhaustions and1 timeout. There are no recovered acceptances in these retry
sets. Thus co-load changes the operational failure classification even at
one total budget. A resource failure is not a proof that the target is false;
it cannot be safely memoized from goal,strategy,total budget alone.

The first retained snapshot with four warm native REPLs each above3GiB has
REPL RSS3478355968,3452882944,3452137472,3454156800bytes; total own-tree RSS
15131496448bytes (~14.09GiB). Therefore an8GiB total point cannot simply keep
this four-warm-process initial footprint. At16GiB it leaves only~1.91GiB
headroom at that snapshot. This is a measured snapshot,not a global minimum
load requirement or a new warm startup benchmark.

Prepared native wait4 leader RSS excludes descendants and shared parent.
Registry attempt peak can include the parent while preparing the first
candidate. At source13d4606,the engine computes registry peaks from currently
registered process roots and combines wait4 leader high-water observations.
Consequently substituting leader peaks for whole-tree peaks,or subtracting
independent maxima to claim COW savings,would be invalid. Parent baseline
~3.61GB and observed residual quantiles are separately retained in
retained-analysis/parent-rss-scope.json; no COW discount appears in the table.

## Direction assessment

Supports aggregate memory accounting,backfill and honest full-coverage retry
engineering; does not establish a new mechanism or a calibrated COW speedup.
The admission model beats the full-coverage retry model at all four points,
but hindsight flat peaks and unknown trajectories prevent a native performance
claim. A three-way real throughput result at new budgets remains unmeasured.
The existing48GiB full native warm/engine pair remains the actual runtime
evidence; these proxies must not replace its denominators.
