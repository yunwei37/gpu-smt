# Complete parsed prefix sharing and request-clock costs

This analysis uses both completed original-population captures, not another
experiment or a new whole-service claim. [Reproduce](../../../bench/lean-native/linarith-oracle/analyze-prefix-sharing.py)
using the retained native-parser records and input order. Native units define
edges; roots are exact header/statement pairs and reuse stays within original
32-candidate blocks. No declaration-name/semantic normalization is invented.

| Population | Sources / original32blocks | Parsed eligible | Exact potential edge reuse | Unit-text potential edge reuse |
|---|---:|---:|---:|---:|
| miniF2F-lineage |7808 /244|7672|8/29669=0.02696%|3987/29669=13.4383%|
| ProofNet-lineage |5952 /186|5717|45/21530=0.2090%|3957/21530=18.3790%|

miniF2F has2605sources with at least one shared unit-text prefix; ProofNet3029.
These are **parsed tactic-edge counts**, not CPU or time saved. All eligible
miniF2F blocks have one exact statement root. ProofNet's median isone, p90two,
maxfour (some blocks no eligible parser result). The input adapter retains
index/header/code but no explicit taskID; do not assert every original32block
is a single semantically identical task merely from grouping.

## Actual request costs explain why hits did not help this executor

All retained client intervals were separately validated sequential/nonoverlapping.
Unit-prefix ProofNet spends790.341696231seconds in successful prefix-step
request intervals and600.037638796seconds in failed prefix-step intervals.
It then spends908.574567120successful+5.748413482failed seconds in source
fallback batches. Preparation/other commands, parsing and cleanup add cost.
5581fallbacks out of5952sources mean prefix execution usually precedes a source
attempt anyway. The costs are request/waiting wall, not native/internal CPU,
and do not imply every prefix hit avoids the same amount of computation.

Unit-prefix miniF2F spends5387.233990681successful+7417.547359687failed seconds
in prefix-step intervals, followed by6228.165280695successful+
20817.783129969failed source-fallback-batch seconds. Failures and native
retirements remain part of the real workload, not removed as outliers.

As a generous **fixed-path sensitivity**, erase every prefix-step interval,
including all proof work, waiting and failures, while retaining recorded
fallbacks and all other durations. Modeled remaining unit time is28138.987819311s
miniF2F and1088.655366518s ProofNet: native-batch/model ratios1.01898x/1.03548x.
Exact-text sensitivities are1.01267x/1.05048x. This is not a valid measured
speedup, a scheduler/representation-independent upper bound or an upper bound
on full upstream SHRED. It shows that improving cache hits or only accelerating
prefix steps cannot rescue the **current fixed fallback executor**.

Decision: retain this implementation's negative end-to-end observations and
do not run another unit/text-cache parameter grid. A different failure policy,
baseline/service implementation or scheduling/proof representation would need
a separate causal mechanism and real matched preflight. The four paper RQs and
GPU/oracle main research remain open; this result does not stop the hourly task.

[miniF2F counts/costs](minif2f/sharing-and-request-costs.json),
[ProofNet counts/costs](proofnet/sharing-and-request-costs.json).
All operational differences, native kernel receipts, censored CPU, original
raw data and method scope remain in their individual result reviews.
Root self-review only; no OMP/subagents/independent reviewer.
