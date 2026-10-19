# Explicit48GiB aggregate experiment point

[User-requested plan](plan.md), [root plan self-review](plan-review.md),
[stopped exact process tree](interrupted-processes.json),
[retirement receipt](stop-receipt.json) and
[preserved prior partial bytes](interrupted-partial-archive.json).

The former48GiB-per-worker two-client point is stopped, not a complete method.
The new requested point is at most two live native workers, each24GiB,
with a whole-owned-tree48GiB RSS watchdog sampling once per second. This
directory preserves the completed qualification and actual kill-branch evidence.
[Result self-review](result-review.md) and [recomputable analysis](analyze-budget.py)
show both24-source arms return17complete/4rejected/3resource failures;
root RSS peaks46.384/46.173GiB, at most2native workers. The safe real fault
injection kills the largest two owned workers with exact source attribution.
The [complete native7808cell](native-cell-result-review.md) now returns
3015complete/4675rejected/71timeout/47resource failures. SHRED is still
acquiring; no paired speed result is claimed.

## Implementation checkpoint

The [implementation self-review](implementation-review.md) records the actual
completed two-candidate real fault injection, including largest-victim choice,
source attribution and resource_failure responses. Normal24-source paired
qualification is closed; its actual records admit the single fresh full run.
The user-approved point uses [public watchdog](../../../../bench/lean-native/linarith-oracle/memory_budget.py)
and the [declared retained-dependency patch](kimina-aggregate-budget.patch).
Executed source snapshots preserve what the running driver actually loaded.

The [streaming native-cell analysis](analyze-native-cell.py) emits [all-source latencies](native-full-source-latencies.csv) and [closed-cell accounting](native-full-analysis.json).
