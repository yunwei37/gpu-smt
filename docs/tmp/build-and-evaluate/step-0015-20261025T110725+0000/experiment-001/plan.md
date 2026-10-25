# Task-aware policy dependency plan

Use unchanged validated original7808 record identities/statuses/HTTP intervals.
Compare flat vs task-interleaved first-success fixed-cost models at2/4workers,
including paid modeled in-flight work and internal task-first-success times.
Cancellation/setup/prediction/memory effects remain omitted assumptions.

Implement composable TaskInterleave<P> around existing SchedulingPolicy.
The default batch-priority method preserves existing implementers. The wrapper
uses only task identity and wrapped source ranking, delegates RSS forecasts,
and changes neither sources/timeouts nor all-mode behavior. Global admission
still enforces CPU/RSS, including exclusive resource retries. Interface tests
must prove actual execution order, cancellation/failed-task exhaustion and
policy failure handling without treating fixtures as native proof evidence.

Measurement reports separate internal accepted-decision availability, unsolved
tasks and returned consumer rows. Existing native tests/CI verify that the
default and resource backends preserve their declared contracts.
