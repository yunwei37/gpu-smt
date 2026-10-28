# E112 — independent parent-process RSS sampling

RQ3supporting resource-contract repair,not a new performance experiment.
The current Rust watchdog is a Tokio task sharing the request executor.
Synchronous request processing can occupy that executor and delay sampling.
The user requires a nominal1s aggregate sampler independent of native work.

Replace only that execution mechanism with one owned parent-process thread,
same1s cadence,existing monitor/ownership/budget/cancellation/requeue logic.
No native worker,CPU mask,AS cap,timeout,collector,service or schedule is added.
Preserve the currently running full pair's copied source/private13d4606binary.

The sampler must not retain a strong engine owner while waiting. Shutdown
wakes and joins it;last-owner retirement also wakes it. A last owner held by
the sampler itself must not join itself. Charge sampling work to the interval,
without trying to claim realtime enforcement or a hard RSS quota.

Two contract regressions:occupy the only Tokio executor while a fake owned
attempt exceeds the fake budget,and require actual cancellation/preempted→solo
history;drop the final engine clone without shutdown and require monitor
retirement. These are software controls,not Lean/profiling/throughput runs.
Use existing source CI for compilation/workspace tests/native protocol controls;
do not compile locally alongside the real native collection. Pending CI is
not qualification,and pinned4.18controls cannot prove4.9Mathlib performance.
