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

## Actual source CI and release followthrough

db8ecbf GitHub engine run40672462407 completes both Rust and native-repl-contract
jobs successfully. Actual native job122762431233 runs all5pinnedLean4.18
differential/lifecycle tests with0ignored/0failed. Rust job122762431683
includes the two new engine regression controls and actual owned-process
watchdog tests. Benchmark-smoke run40672462371 also succeeds.
Exact metadata and rawcompressedlogs/testlines are in actual-source-ci/.
This is boundednativecontract evidence,not native4.9throughput or fullMathlib
matching and not independent auditing.

A singleCPU11releasebuild completes27.034840s with48,069,668,864Bcombinedpeak,
no pressureabort/monitorerror. Copying the full bytes freezes a prospective
newretry-orderbinary and unchanged24inputs privately;pending-native-release.json
records the exact latercommand. No runner/autostart is installed and current
qualificationbinary/nativehost remain unchanged. Executeonlyafter complete
rootreview of that pair. Preparation is not a measuredperformance result.
