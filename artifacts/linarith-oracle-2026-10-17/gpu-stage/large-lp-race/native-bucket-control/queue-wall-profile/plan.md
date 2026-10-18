# RQ4 opportunity attribution for the stronger native queue baseline

This continues the user's requested Amdahl measurement. It does not propose
another LP algorithm, parameter grid, runtime constructor or full GPU variant.

The upstream eight-queue native interface completes the original 1,000 sources
in 685.730742286 seconds, with identical full native response JSON to the
earlier 1,237.37-second eight-item-wave reference. Thus the old wave-only
paired profile and 1.600x answer-aware control cannot settle opportunity
against this stronger common CPU interface.

Use the already-qualified pooled native all-call profiler without rebuilding
or changing native algorithms. The only protocol delta is the same upstream
eight sequential queues and private telemetry-only candidate-timing REPL.
Keep original source order, maximum eight tasks, four eligible CPUs, 48 GiB,
native heartbeat behavior and whole preparation/EOF/retirement accounting.
No artificial array-wide deadline is added. Record all native source JSON,
candidate intervals, numerical worker receipts, LP shapes, failed branches
and the four observed regions. These regions overlap, so report interval
unions and CPU work separately instead of a fabricated disjoint partition.

First run the actual original24-source native/CPU diagnostic on CPUs8–11,
compare verdict/non-message fields to the corresponding completed primary
qualification, and verify source/shape/worker metadata is complete. This is
instrumentation qualification, not a performance improvement condition.

Only after the active full common CPU pair on CPUs0–3 actually ends, run
one full native/oracle diagnostic pair through that same queue protocol on
CPUs0–3. The profiler already passed the all-call contract in the wave
protocol; only its changed submission interface needs qualification.
Any zero-cost calculation uses the new diagnostic's own native/oracle clocks.
Do not divide old phase sums, CPU sums or fixed-answer timings into685.73s.
Retain failures and any telemetry defects explicitly. Profile data may bound
a claim only within its actual workload/protocol assumptions; it is not
achieved GPU speedup. Negative route closure still requires applicable
opportunity evidence under the user's >1.5x decision, not a slow kernel.

This experiment can change the decision to continue a heterogeneous
mechanism versus preserve a negative result. It strengthens the existing
baseline family and attribution; it does not supply systems novelty itself.
All work and review stay in this root thread. The original four RQs and
paper target remain unchanged. No independent audit is claimed.
