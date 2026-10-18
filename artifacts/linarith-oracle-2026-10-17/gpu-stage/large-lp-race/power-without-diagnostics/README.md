# Arithmetic comparison with reduced Lean diagnostic cost

[Plan](plan.md), [source changes](source-changes.json), [build](build.py),
[actual native/numeric composition](runtime-composition.json),
[64-source qualification](qualification-result-review.md), [finite driver](driver.py).

The original instrumented timings remain intact. This same-algorithm correction
removes eager diagnostic rows, stage clocks and product tagging; it retains
native certificate checking, exact repair, numeric binaries and fallback.
It is not entirely instrumentation-free and not a new contribution.

All64 qualification verdicts/non-message fields agree across four cells.
The corrected original1000 native/direct pair is running; no full result yet.
Do not rebuild this private library while that capture is active.
