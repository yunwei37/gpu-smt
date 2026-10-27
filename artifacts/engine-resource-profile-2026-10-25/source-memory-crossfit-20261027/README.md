# Source-only native memory prediction — whole-task-held-out result

Reuse the complete original7,808 uncapped native capture; no new Lean proofs
or change to the ongoing matched pair. The existing27 comment-stripped source
features and one log-RSS ridge model use L2penalty1,train-only standardization,
an unpenalized intercept and five folds of whole tasks. No parameter search,
test-task sibling leakage or outcome input at prediction.

7,807 sources have positive observed peaks. minif2f-4969 has no positive peak
and stays unknown; it is not treated as zero demand. The target is each
candidate's maximum reported actual attempt peak,including original preemptions
and retries. Resource/timeout observations are finite-resource lower bounds,
not uncensored intrinsic demand. All rows and statuses remain in predictions.

| Measured target subgroup | Sources | Ridge MAE GiB | Fold-training median MAE GiB | Ridge / median underpredict by more than2x |
|---|---:|---:|---:|---:|
|All known peaks|7,807|0.606624|0.352486|94 /100|
|Completed without preemption|7,677|0.303014|0.035456|0 /2|
|Timeout|87|6.870098|7.525021|53 /57|
|Resource failure|41|44.158729|44.504535|41 /41|
|Had a preempted attempt|44|42.467103|42.875429|44 /44|

The source model worsens overall/ordinary accuracy and still misses every
resource-failure and preemption case by more than a factor2. The limited
timeout improvement does not qualify it as a safe or useful admission policy.
Do not deploy this model or start a coefficient/feature parameter grid.
The median row is an offline training-fold predictive constant,not an exact
causal replay of the live engine's evolving median.

The44 actually preempted attempts accumulate5,537.329118 elapsed seconds,
within78,218.880094 seconds summed over all original attempts. These
overlapping sums are not whole-lifecycle savings or an Amdahl ceiling.
There is no admission simulation,changed accepted set or measured speedup here.

A useful different signal is task-local measured history:41resource failures
concentrate in four tasks (29 amc12a_2020_p4,9 mathd_numbertheory_483,
2 mathd_numbertheory_427,1 amc12a_2020_p10). A policy could learn from a real
completed sibling's observed memory instead of predicting demand from lexical
features. Availability and changed admission must be tested causally; using
all sibling outcomes in advance would be an oracle. This motivates a separate
opt-in resource-policy implementation,not a claimed result or novelty.
It never authorizes propagating rejection or proof/certificate reuse.

The existing support runner executes on CPU11 in4.005610s with one BLAS thread,
zero native candidates,6combined tree samples and peak25,585,016,832B,
without pressure abort or monitor error. This overlaps the current native
collection and is recorded as own CPU contention. The existing capture remains
on its frozen binary/resources. Source,fold models,all heldout predictions,
preempted attempts and raw execution receipt remain available. Root self-review,
not independent audit. Four research directions remain open.
