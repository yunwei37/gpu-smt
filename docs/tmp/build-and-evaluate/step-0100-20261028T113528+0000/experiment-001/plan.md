# Retain a timely native reply while charging physical retirement

The complete retry-frontier24 point is now retired and preserved. Source
inspection identifies an inconsistency: fresh NativeRepl selects a native reply
within its request budget, then always waits/charges cleanup; PreparedRepl
selects over both reply and retirement and can discard an already completed
native result at the deadline.

Use a real owned child and Unix protocol fixture to delay retirement after an
early reply. Run the same test first on the existing implementation, preserving
an observed failure, then fix only this reply/retirement boundary. Preserve the
original deadline: a late reply stays Timeout; cancellation and malformed
retirement must not become acceptance. Await/reap before unregistering and
returning; complete cleanup time remains in attempt and whole-run latency.
The fixture is not Lean and cannot prove the cause of 2507/7230.

Run focused controls, workspace tests/clippy/fmt and native CI. No independent
agent, observer, new runtime knob or timeout extension. All work is root-only
under 48GiB combined own-tree budget/CPU8–11, with no second native cohort.
