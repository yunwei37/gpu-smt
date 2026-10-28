# Step0094 — defer resource retries behind registered ordinary work

BUILD_AND_EVALUATE,root only;the original fourRQs and Lean/SMT/OSDI goal remain.

## EXPERIMENT_GATE

[Plan](experiment-001/plan.md) and [actual self-review](experiment-001/result-review.md).
Implement queue-frontier resource retries,not speculative sharing of full-budget
memory. Stable ordinary order and finite arrival frontiers avoid both mid-batch
drains and indefinite retry starvation by later arrivals. Exclusive retirement,
48GiB sampled accounting and full attempt costs stay.
Old-source negative control fails;fixed progress,late-arrival ordering and
shutdown controls pass,as do workspace targets/doctest/fmt/clippy/docs.
Resource/fixture failures and ignorednative tests remain explicit.
Current frozen native qualification is not modified or used as this fix's result.

## WRITE_GATE

README,architecture and implementation describe frontier ordering and limitations.
No throughput number or paper contribution is invented. The current paper's
resource superiority question remains open;this source repair is pending native
evaluation,not a full writing or milestone event.

## REVIEW_GATE

[Outer self-audit](outer-audit.md). Rootself-review,not independent auditing.
Current warm side exits0 and retires all workers;engine side sequentially
starts. Collect the closed warm raw boundary separately,then root-review the
complete matched pair before new throughput/policy/failure/LRAT measurements.
No sampling/diagnostic tooling or service layer is added to the engine.

## Next

Commit/push source and regression evidence;follow the existing engine CI.
Preserve warm terminal/raw inputs and wait for actual engine terminal through
its existing owner event. Do not overwrite its binary or run another cohort.
