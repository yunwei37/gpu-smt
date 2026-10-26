# Empty-active-set memory forecast liveness

FixedRQ2:Does branching from prepared native state preserve verifier responses
and requested artifacts while isolating candidates and cancellation?
This narrow engine-liveness fix supports the user-requested resource layer.
It is not a native benchmark,novel scheduling method or answer to fullRQ2.

Scope contract:change only forecast-aware exclusive admission and its existing
resource-reclamation dispatch,regression tests and necessary API/docs;do not
change budgets,CPU assignments,timeouts,current fullpair sources/binaries,
cache/verdict semantics or unrelated files. No new setting or entity.

Observed code path:actual idle RSS20,budget100,forecast90. Forecast90is below100
so not exclusive,but RSS+reservation110always fails even with no active work.
There is no retiring peer to release memory. A larger forecast>=100currently
gets exclusive admission but does not call the prepared-state reclamation hook
on the initial attempt. Use toy resource units to reproduce deterministically
without starting another native group or consuming large memory.

Add one fixture matrix:fits headroom,forecast exceeds idle headroom,forecast
equals/exceeds total budget,actual RSS itself over budget. First reproduce
the wait on unchanged code with a bounded regression-test timeout,then fix.
Exclusive admission must still call the existing actualRSS policy and retain
watchdog/CPU/exclusivity. Backend reclaim uses the original deadline and costs;
no predicted rejection or fabricated resource failure. The existing backend
hook may run on the first exclusive headroom admission as well as a retry.

Compile/test with ordinary documented fmt/clippy/workspace tests/docs only,
combined current-root+fullpair48GiB monitor,CPU10–11;withdraw only new validation
on pressure. Loaded fullpair42659a8remains unchanged. Pinned actual native
contracts run through existing CI,not a second local candidate collection.
User prohibits other agents,so reviews are root self-review. Publishmain.
