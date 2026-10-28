# Resource retry tail — implementation and root self-review plan

User requests root-only implementation while retained qualification runs.
Change only resource retry ordering: ordinary physical work registered before a retry
precedes it; preserve ordinary policy keys within that frontier and stable
retry registration order. Later arrivals cannot overtake the queued retry.
A retry still waits for active peers to retire, reclaims idle prepared state,
and executes under the same aggregate RSS/watchdog/CPU/deadline rules.

Hypothesis: avoid interleaved queue drains and prevent known-heavy retry
waiters from blocking already queued normal work. The existing86% singleton
exclusive share is not removable time: final full-budget failures remain
serial and finite batches still pay their complete retries. No prediction
guarantees spare memory. Every retry closes its existing ordinary frontier to later arrivals;
this prevents starvation by future arrivals without promising bounded native latency.

Regression must make normal candidates run while a surviving peer is held,
then assert the deferred resource attempt begins only after ordinary work
and native retirement. Include cancellation/shutdown cleanup and preserve
attempt provenance, no predicted verdict. Run the new regression against the
old source as an observed negative control, restore exact edited bytes, then
workspace tests, format/clippy and existing CI. Supporting compilation uses
CPU11 with combined current-owner RSS guard; no second Lean collection.
Do not replace the qualification binary or start performance tests until the
current warm/engine pair is terminal and reviewed. Code/tests are not gain.
