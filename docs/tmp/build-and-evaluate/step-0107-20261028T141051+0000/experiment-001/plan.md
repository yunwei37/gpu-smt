# E107 — resource queue wakeup repair, not a second native experiment

RQ3; BUILD_AND_EVALUATE. Root executes and self-reviews; no independent Agent.
Previous turn changed public interpretation, archived actual source CI and
pushed9ad1d50:progress,not a verified full native result.

Actual source inspection:acquire waits on Inner.notify for every physical
request. Watchdog,lease retirement and ticket removal broadcast notify_waiters;
only the first ordered ticket can sample/admit. A complete7808queue can
therefore wake all waiters for a one-head eligibility transition.

Keep the exact ordered ticket keys,retry epoch/frontier,resource forecasts,
CPU/RSS budget and native semantics. Store a private notification with each
existing ticket;ordinary resource transitions wake the current head only.
Shutdown/fatal monitoring wakes all pending tickets. Ticket removal wakes its
successor. Per-ticket notify_one retains a permit if a wake precedes polling.

Validation:manually poll7808real private acquire futures with counting Wakers,
hold CPU eligibility until they are all pending,then drive the real watchdog,
lease retirement and shutdown. Require one eligible-head wake,no tail wakes,
sequential lease admission and every remaining future finishing on shutdown.
Also retain existing delayed forecast,large wait queue,preemption/retry-frontier,
subscriber cancellation and shutdown-race controls. Normal existing CI builds
and tests this code;no local compiler/native cohort competes with the running
frozen13d4606 full native pair. Add no runtime logger/flag/provider.
A unit wake count is not measured native CPU cost or whole-workload speedup.
Whole native performance remains pending and cannot be attributed to this edit.
