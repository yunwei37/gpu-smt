# Step012 — ancestry-qualified branch model and sampling workload preparation

2026-10-30UTC;M;self-review. No second native M process.

## EXPERIMENT
The completed shard0 native/off/on cells each return100/100,exit0 and retire.
Both comparators preserve all100 error flags,diagnostic strings and InfoTrees.
Both differ from stock in33 raw allocation-heartbeat deltas. The full200
comparison is still pending; small-control exact heartbeat equality does not
generalize to all candidates. Source minif2f-4544 alone uses721.6184s body
CPU and one eqRefl leaf720.2499s in the on cell. Its original historical
service outcome is300s timeout; new diagnostic maxHeartbeats3000 does not
make this a wall-clock-comparable production workload. No borrowed denominator.

The branch analyzer now requires the entire ordered allGoals-ancestry
projection to be isomorphic between InfoTree and completed successful C calls.
This supports repeated/nested constructs while refusing unmatched forests;
it is not a naive global kind/order join. Branch count,goal identity/order
and live-expression/universe dependencies are checked. Model spans compose
bottom-up,so nested savings are not simply summed over overlapping intervals.
Shard0 has1 qualified multi-goal split,modeled0.015943s saved from742.650412s
body CPU. Full DAG remains unknown; names/messages/caches/merge semantics
remain unproved. This local model is not the full available parallelism.

An offline mutant introduces a shared live metavariable into the independent
native control: modeled saving drops to0. An incomplete C frame is refused.
Four symbol-family checks ensure heartbeat increments are not misclassified
as reference counting. Mutants are not new Lean executions.

Prepared a future31-unit software-sampling input:10 repetitions of the
median-CPU observed ordinary pass,error and budget-prefix sources within
completed shard0,plus one manual closed List.range4000 fold decide control.
Selection is fixed before looking at software PC samples; this is a small
median diagnostic sample,not a workload-weighted overall precompile estimate.
Raw input is outside Git on PVC; plan retains source provenance.
Native sampler qualification and these representatives wait for matrix
retirement. Per-cell60s/180s internal bounds,one M Lean,16GiB/8core allocation.

## WRITE / REVIEW
Shard0 check and model are explicitly partial outputs,not the full200 result.
Parser regressions pass; C capture sources/binaries/collector remain frozen.
Software sampling has no native qualification or workload fractions yet.
Full matrix completion,differential and local work/span assessment continue.
