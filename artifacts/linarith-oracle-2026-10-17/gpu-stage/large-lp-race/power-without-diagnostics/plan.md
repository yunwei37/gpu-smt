# E1080 — remove Lean diagnostic cost from the matched arithmetic comparison

## Admission
RQ4 unchanged. Source inspection finds eager diagnostic JSON/LP row/product-flag
construction and thread clocks in the supposedly normal-output Cost path.
A sink that discards output does not avoid constructing its arguments.
Therefore the existing629.48/350.68 result and E1077 repetitions are valid only
for that common instrumented build; they are not zero-instrumentation production
results. Retain every observation. This protocol repair can change whether the
user's1.5x criterion survives ordinary execution cost, so it has decisive value.
It is not another solver, kernel, allocator, thread or cache tuning grid.

## Change and controls
Private same-algorithm Lean build: replace diagnostic CostTelemetry.emit
statements and emitFast call arguments with pure Unit; stage timed combinator
becomes its original action; product tagging used only by telemetry becomes
no-op; direct certificate proof/check remains. Keep numeric Power/HiGHS/exact
binaries frozen from E1074 using links, same native omega and fallback.
RPC source/call correlation and remaining non-stage clocks are still charged.
Do not call this completely zero-instrumentation: candidate timestamps/RPC
correlation and backend records remain.

Both retained and reduced-diagnostic builds run the unchanged original first64
sources in native Fast/hybrid and Power modes, same8queues/fourCPU8--11/48GiB.
This2x2 is one necessary measurement-overhead control, not independent new
baselines. Disable the optional process-tree resource observer in all4cells via
the documented --sample-seconds0 qualification option; keep original raw
candidate responses/timestamps/native checks/backend logs. Thus no new memory
claim and no comparison of these clocks directly with E1077's observed clocks.
Normal quit/setup/fallback/teardown remain inside every boundary.

## Qualification and full correction
Real qualification completes all64 in each condition, actual native lib chosen,
original source/native response parity and fixed numerical binaries.
Then complete the original1000 native/Power pair with the reduced-diagnostic
build and the same no-observer protocol. This is the actual same-algorithm
comparison repair, not selecting a new winning configuration from a grid.
A loss/ratio below1.5 is retained and narrows the claim; no instant GPU closure.
No final ratio from partial cells. Initial Narrative/all4RQs/Lean+SMT/GPU target
remain; all review is root self-review, no independent audit.

Command: pinned Kimina venv Python driver.py. Raw under qualification/ and
full1000/; private build under /tmp/gpu-smt-linarith-oracle-20261017/
power-without-diagnostics. Compiled source/build attempts preserved here.
