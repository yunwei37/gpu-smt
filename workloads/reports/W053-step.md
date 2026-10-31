# W053: cancel W queue and yield priority to M/O

## EXPERIMENT — requested operational correction
At06:28:45UTC, actual PID/birth/command38309/748045910 was verified waiting
without capture-start, then SIGTERM removed it from the kernel wait queue.
Active37246 is untouched. Before cancellation /proc/locks showed holder37246,
M waiter11027 and W waiter38309; after it showed37246/11027 only.
Final inspection at2026-10-31T06:36:48.498892+00:00 confirms cancelled wrapper stateabsent, no native
capture and no38309waiter. All original launch/source/raw records retained.

Future W launcher checks arrow-marked device/inode-matching waiters, tries
LOCK_EX|LOCK_NB, and rechecks before executing taskset0–7. Busy/waiting returns75
without enqueue or retry. Six controls passed on E cores, including a real
owned fixture holder. Real shared-lock inspection acquired nothing and returned
M waiter11027. No performance or fairness guarantee for other writers claimed.

## WRITE
W current state now explicitly holds every new W timing until M/O completion,
not merely until the wait queue happens to empty. Added small evidence, usage,
control source and scope. Historical W052 queued record remains unchanged.
During the hold, prepared six unchanged conditional draw inputs:2385uncached
jobs/19,920,109source bytes; no native launch and no new cost coverage.

## REVIEW — self-review
Exact cancellation scope checked; no current capture, M/O process, host setting
or other-lane file modified. Earlier W requeueing could starve M because flock
is not FIFO; the fix prevents W queueing and does not substitute a new scheduler.
M/O completion is never inferred from empty /proc/locks. Existing617-job capture
remains bounded/frozen. Root paper and global confidence claims unchanged.

A later read-only identity check found additional waiter42521 running the
startup-replay/repair-v3/repair-replay.py command, outside W's workload point.
It was not signaled or modified. Both W prepared next points now carry an
additive NEXT-RUN.md warning against replaying the historical blocking command.
