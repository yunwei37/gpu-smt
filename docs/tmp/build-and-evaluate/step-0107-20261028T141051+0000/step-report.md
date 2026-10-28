# Step0107 — remove resource queue broadcast wakeups

2026-10-28; BUILD_AND_EVALUATE;root only. Previous turn is progress:
actual35-test source CI archived and attribution limitations pushed9ad1d50.
The priority remains the sole frozen full Kimina/resource pair,then original42.

## EXPERIMENT_GATE

### Node E107.1 — source defect and implementation

[Plan](experiment-001/plan.md) folds resource maintenance into RQ3. It is not a
new paper experiment. The complete current queue source shows that every
pending acquire future waits on one broadcast Notify. Watchdog ticks,lease
retirement and ticket removal notify every pending request,although only the
first ordered key is eligible. No profiler or claimed measured CPU fraction
is needed to identify this concrete wake path.

The ordered queue now maps the exact same ticket keys to per-ticket Notify.
Each acquire waits on its ticket;ordinary resource transitions notify only
the head. On ticket cancellation/removal the next head is notified. A stored
notify_one permit covers a transition before polling. Shutdown and both fatal
monitor paths wake all queued futures;active native cancellation and retirement
remain on their existing registry/lifecycle paths. The global Notify remains
for shutdown's active-retirement wait. No API,policy,forecast,budget,timeout,
native code,logging field or active binary changes.

### Node E107.2 — deterministic actual acquire-future controls

Two new unit controls manually poll the real private acquire futures with
counting Wakers. The7808queue control registers every waiter before invoking
the real watchdog,then requires exactly one head wake and no tail wakes.
It admits a lease,checks that retirement hands the available CPU to the
successor,then requires all remaining futures to return shutdown errors.
The second control cancels the head and injects an actual ResourceMonitor
error,requiring successor progress and all remaining waiters to finish.

These are synthetic resource/lifecycle controls,not7808real Lean executions.
Existing queue/forecast/retry/cancellation/shutdown/native contract tests remain
required. Rustfmt and git diff --check pass. Compilation,clippy,unit/native CI
are pending after publication;no pass is inferred. The existing CI executes
validation without local compilation or another Workspace native cohort.
No full-performance or RQ-answer claim is made.

## WRITE_GATE

Targeted architecture text documents targeted waking,all-waiter fault exit,
one extra notification per pending request,and the frozen-full-source boundary.
No paper result,title,abstract,scientific contract or RQ changes. Four RQs
remain unanswered. The currently running13d4606collection is not upgraded
mid-run and cannot measure this later source change. No new schedule,Agent,
provider,log framework or experimental matrix is introduced.

## REVIEW_GATE — root self-review,CI pending

The executing root checks wake coverage against every old broadcast site:
ticket drop,lease drop,periodic watchdog,monitor failure,engine-only RSS fatal,
and shutdown. Terminal publication/completion notifications are unchanged.
Queue ordering and exclusive retry admission are retained. The new controls
also check absence of stranded shutdown/error waiters,not just reduced wake
counts. No independent audit is available under the explicit user prohibition.

Direction remains equal-resource native throughput with exact behavior/
resource evidence. Efficiency removes a source-visible whole-queue wake path;
it does not assign a native CPU fraction or throughput value. Maintenance adds
no API knob and keeps existing CI/contracts. Final full native data,source CI,
complete accepted-set/resource parity,novelty and independent auditing remain
open. The next native boundary is still the actual full serial pair terminal;
no second local acquisition or scientific promotion is authorized by this test.
