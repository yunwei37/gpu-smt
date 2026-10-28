# Step0109 — event-driven native parent retirement waiting

2026-10-28;BUILD_AND_EVALUATE;root only. Previous turn's actual6trace replay/
source evidence and push368a5bd are progress,not a new native speedup.
The current full resource pair/next42priority remains unchanged.

## EXPERIMENT_GATE

### Node E109.1 — resource implementation,not a separate paper experiment

[Plan](experiment-001/plan.md) selects a concrete prepared-host wait path.
Actual C source uses poll(...,100) to cover the child/stop signal arrival gap.
Simply deleting its timeout would risk indefinite waiting after a signal that
already ran its handler. The standard atomic signal-mask/ppoll interface
addresses that race without choosing another periodic wake interval.

The parent blocks lifecycle signals between reap/check and ppoll,which
temporarily enables them while waiting. It handles descriptor readiness,
stdin EOF,stop and child-reaping events through existing lifecycle paths.
Handler/mask setup errors prevent readiness and use the existing parent-fault
path. Audited native import initialization finishes before checked handlers
are reinstalled. Forked candidates reset handlers and restore the launcher's
original mask before native service initialization;there is no inherited
periodic-wait policy in their runtime.

The manual source at https://man7.org/linux/man-pages/man2/poll.2.html
documents atomic mask switching/wait and the null-timeout behavior. It is
protocol rationale,not timing evidence. No timer,thread,daemon,setting,
permission,baseline or new native logger is added. Child ownership,
waitid(WNOWAIT)/wait4,group killing,retirement receipts,deadlines,fallback
and aggregate RSS retain their previous definitions.

### Node E109.2 — actual-native contract validation completed in CI

The existing real pinned4.18native source vector now reads its own SigBlk field
from /proc/self/status. The raw fresh verifier must actually return that field,
and the prepared result must match its full raw response without fresh fallback.
This checks signal-mask inheritance through native execution,not a mock ready
handshake or fixed assumed zero mask. Existing concurrent-child,Timer/Promise,
isolation,error/sorry,timeout/fallback/shutdown checks remain required.

Actual source4283acbpasses engine40710734996and smoke40710735308.
Rustfmt/clippy/rustdoc,70workspace tests,5explicit pinned4.18native tests
and35Python controls succeed. The real import-parent differential executes
the added SigBlk case,requires an actual field and refuses fresh fallback.
[Result review](experiment-001/result-review.md) and complete raw logs retain
the precise scopes. No local compiler or native cohort competes with13d4606. No per-request wait
savings or full-throughput gain is estimated from the removed100msconstant.

## WRITE_GATE

The native adapter guide explains event waiting and child mask preservation.
It also replaces stale statements that all Mathlib child controls are pending:
the existing completed child controls and corrected full resource guide are
linked at their own evidence scope. Initial import-only observations stay
historical;they are not rewritten into branch execution.

The paper and four-RQ scientific contract are unchanged. This source maintenance
does not fill an endpoint result,enter a full writing loop or imply novelty.
Resource preparation/event handling is prior technique. No broad literature
survey or new research route is claimed.

## REVIEW_GATE — root self-review,source CI verified

Root checks every lifecycle signal has an enabled atomic-wait path,errors
cannot emit false readiness,child mask restoration precedes runtime work,and
normal wait/EOF/retirement ownership remains. The new native case must emit
the real field and cannot pass solely by falling back to fresh verification.
No timing-bound assertion is used. General arbitrary-FFI/fork safety remains
outside the declared audited context;this is not an isolation proof.

Direction and scope remain resource-layer matching before new workload gains.
Efficiency removes periodic polling rather than tuning its frequency.
Maintenance reuses standard kernel/libc operations and existing CI;no new
observer/framework/Agent. Review is self-review,not independent auditing.
Source/native contract CI is verified;full current population outcomes,
resources/accepted sets,novelty and independent audit remain open. No OSDI acceptance is claimed.


The15:02:44UTC exact-PID/birth check preserves the still-running warm/full
controller. The latest RSS point is one observation,not a hard-budget proof.
Neither full/warm terminal exists;engine has not started. This later source
repair cannot be credited to the frozen native pair. The paper source diff
against13d4606is empty;no fresh compile or whole-paper review is claimed.
