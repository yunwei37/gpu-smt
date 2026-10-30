# Runtime-only preemption/restart — root self-review

No source predictor is imported,trained or evaluated. Dispatch uses observed
attained service/current progress or unsuccessful-prefix length,stable queue
ties,and shared empirical runtime distributions from other heldout problems.
The index planner never sees code,tactic family,length,acceptance probability
or heldout outcome labels. Actual native labels/costs are read only by the
simulation completion generator and the hindsight control. Every observed-
unsolved task finishes all32candidates in every policy.

The empirical completion index minimizes expected truncated work divided by
completion probability conditional on survival beyond the observed age.
Lossless-resume control debits prior progress;restart-aware planning charges
the old prefix again and conditions on the longest failed uninterrupted prefix.
This is runtime-only empirical index scheduling,not a claim of the exact
M/G/1 Gittins theorem for finite proof groups/multiple workers. LAS controls use
attained service only;restart quantum doubles after each failed prefix.

## Full7808 current-point conditional CPU-slot model

|Policy|Consumed work seconds|Batch proxy seconds|Mean task finish seconds|
|---|---:|---:|---:|
|FIFO task-interleaved control|37164.887410|9913.302131|3986.809422|
|LAS lossless resume|38487.248192|10746.647743|1190.922669|
|Runtime-index lossless resume|38726.608345|11157.271265|1187.641427|
|LAS charged restart|96486.222253|26975.678217|2387.195069|
|Runtime-index charged restart|54747.316462|17063.831033|1596.579331|

All142observed-solved task IDs remain in these frozen-label models. Restarts
discard60349.000000s(LAS)or18569.881643s(index),with2904/5013actual restart
dispatches. Original native-budget eligibility is unknown for1032/3010distinct
restarted sources. Five completed sources newly exceed a300s aggregate-elapsed
proxy in each restarted model;no altered native verdict is fabricated from
that proxy. Composed-attempt/HTTP spans are not native heartbeat budgets.

The historical two-worker point is separate:runtime-index restart consumes
46217.152340s versus FIFO29613.524167s,and discards17025.416006s. Mean task
finish drops from6632.256677to3179.317054while batch proxy increases from
14847.509208to23838.111288. All other controls/raw per-source rows are retained.
This latency/work tradeoff must not be hidden by reporting only makespan.

## Ideal exact finite pass@k and physical limitations

Recomputed minimum frozen work is35838.016728s(current)and28923.681945s(old):
one fastest accepted source on each142observed-solved task,and all32on the102
others. All-candidate work52992.124106/43209.621347s gives conditional work ratios
1.478657/1.493918. Historical measured1.439031x is a different wall denominator,
not a new row or a factor multiplied into these work models.

All policies use one active process per task. Ready ties/continuations follow
the declared simulator,not a byte-for-byte replay of the old client semaphore.
The CPU-slot model omits RSS admission,exclusive retry serialization,checkpoint/
signal/retirement overhead,causal timing changes and unknown uncensored work.
In particular,the current CPU-slot times can be below the known exclusive-tail
resource-model lower bound;they are not physical equal-RSS service predictions.
Resume is an optimistic control;restarting copies the observed terminal labels
conditionally without resetting or certifying the original native budget.
No native process,signal,new runtime policy or production verdict cache executes.

The data reveal a possible mean-task-latency/work tradeoff,but do not justify
claiming useful equal-resource native throughput or exact bounded parity from
this runtime-only method. Compare existing strong consumer data as retained
evidence,not by retraining the frozen source model. Native continuation/resource
qualification remains a real open requirement,not a new project-ending gate.
