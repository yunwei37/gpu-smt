# Native scheduling qualification — root self-review

Eight real unmodified candidates: four from task 0 with actual accepted proofs,
four from task 2 with ordinary Lean errors. All-source replay returns 4 valid/4
lean_error. Both first-success modes return one actually checked valid proof and
four actual Lean errors; three pending siblings are cancelled against that
checked same-task winner. Both retain exactly solved task {0} and unsolved task
{2}. There are no status changes among actually executed sources.

Consumer complete lifecycles: all 6.212809683 s, first-original 6.203129127 s,
first-short 6.329753298 s. This tiny, startup-dominated qualification demonstrates
the real cancellation path, not a speedup or whole-population result.

Original transport slots encode pending cancellation using the SDK error field,
which its analyzer labels server_error. Those are not actual server failures:
consumer-results explicitly maps three slots to cancelled_after_success,
native_response_returned=false, time=null. Raw original transport slots and
their counts remain preserved. The next driver also publishes explicit consumer
and transport-slot counts in the terminal to avoid misleading aggregation.

All three native cells have max two live REPLs, peak sampled RSS below 8.11 GB,
zero watchdog kills/errors, 24 GiB AS per REPL, and no live descendants after
retirement. Only queued siblings were cancelled; same-task in-flight count is
one. In-flight sibling cancellation has not been implemented or measured.
CPU oracle/GPU screening remain disabled. Per-candidate rewards for RL are
unavailable under this consumer semantics. The executed source copies are kept.
Root self-review only; no independent audit or new scheduling novelty claimed.
