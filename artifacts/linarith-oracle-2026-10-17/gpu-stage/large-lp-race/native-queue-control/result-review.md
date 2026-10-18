# E1063 — completed native scheduling preflight

Root thread implementation/execution/self-review, 2026-10-18T12:57:37.911161+00:00.
The original first64 candidates, same new native binary, four CPUs4–7,
eight workers and48GiB, unchanged source order/imports/body/checker:

| Policy | Whole pipeline seconds | Complete/rejected/operational |
|---|---:|---:|
| Native fixed contiguous queues | 54.811967251 |63/1/0|
| Native FIFO workers | 58.321468348 |63/1/0|

Static/dynamic = 0.939824884x: dynamic costs 6.403% MORE elapsed time in
this preflight. Every source ID, verdict and full native JSON response agrees.
Both have64 uniquely matched candidate spans, maximum8 active candidates,
zero memory-observer read errors and no operational failures.

**Disposition:** Functional control passes, performance admission fails. Per
the written plan, do not launch its1,000-source component matrix, retune worker
counts, select a friendlier cohort, or claim a scheduling contribution.
Keep original full29,750 and prefix acquisitions running unchanged. This small
preflight does not prove static scheduling globally optimal or erase the real
full1,000 lane imbalance. It establishes that this implemented FIFO alternative
has not earned promotion. The modeled10.7% gain is expressly NOT an observed
speedup. No GPU impossibility or whole-project negative closure follows.

All raw inputs are the already-published first64 file; all closed output,
candidate intervals, event/resource streams, errors and startup/teardown are
retained here losslessly. Native compiler failures and repaired build commands
are retained separately. Review is self-review, not independent audit.
