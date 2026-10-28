# Step0112 — independent RSS sampling and native resource interruption

2026-10-28UTC;BUILD_AND_EVALUATE;root only. Previous goal turn completed the
historical exclusive-headroom calculation and pushedf454e84. That result is
supporting interpretation,not native warm parity. FourRQs remain open.

## EXPERIMENT_GATE

### E112.1 — source repair of the requested resource contract

[Plan](experiment-001/plan.md) selects RQ3supporting resource enforcement.
The exact source has Tokio-spawned interval sampling inside Engine::new.
That sampler shares request execution;blocking all Tokio workers prevents its
progress. This is a source-level execution dependency,not a measured cause of
the old full-run performance gap. The CLI already binds its parent before
creating its configured runtime;no extra CPU range is introduced.

Current user-instruction/questions snapshots are unchanged from the complete
gate-entry read in step0111;actual git diff of both and the scientific/paper
files is empty. Root-only work/resource parity/one native cohort/preserved
healthy collector remain. Owning research skills still apply;no idea refinement
or separate Agent is invoked.

Engine now owns one standard thread for the existing nominal1s sampler.
The original monitor,aggregate budget,largest-active selection,ownership,
preemption and retry paths are unchanged. A condition variable wakes stop;
sampling time is charged against the next interval. Slow monitor/syscall/lock/
OS scheduling may still delay a sample:it is not a realtime or hard RSS bound.
The thread holds only Weak<Inner>while asleep. Shutdown awaits native/backend
retirement then stops and joins it. Last-owner drop wakes it too;destruction
on the sampler's own thread does not self-join. Constructor spawn failure
returns an error rather than an unwatched engine.

### E112.2 — regression contracts and source-CI handoff

Two new Rust controls:occupy the only Tokio request executor with a bounded
synchronous wait and require the actual sampler to cancel the overbudget fake
owned attempt,with retained preempted→exclusive history;drop the final cloned
Engine without explicit shutdown and require monitor retirement.
These fake-resource fixtures are software contracts,not native proof or
performance evidence. Syntax/rustfmt succeeds. [Result review](experiment-001/result-review.md)
is pending actual source CI. Existing engine workflow supplies compilation,
fmt/clippy/workspace/rustdoc plus pinned4.18native protocol controls;no local
build is run alongside the real4.9Mathlib capture. Source publication is the
CI trigger,not a claim that tests already passed.

Current copied full-pair script/private13d4606binary and active controller are
untouched. No active default switch,new native cohort,watcher,service,schedule,
policy layer or competing checkout is created. The source sampler stays in
its existing parent process and inherits its CPU mask.

## WRITE_GATE

Update the existing architecture resource paragraph with independent execution,
cadence/lifecycle and delay limits. The existing daily file records the actual
fault and next verification. No RQ,claim,narrative,acceptance semantics or paper
number changes. Paper source/authority diff is empty;the prior unchanged-source
compile remains the only compilation receipt,no fresh LaTeX build is claimed.
Full writing and milestone review are skipped by phase/missing-evidence
conditions. No resource primitive is promoted to novelty.

## REVIEW_GATE — root self-review,CI pending

[Outer self-audit](outer-audit.md) covers ownership,lifetimes,stop/join ordering,
same-thread drop and unchanged budgets/process counts. Independent review
is absent under the user's no-other-agent requirement. The sampler releases its
temporary strong owner before waiting;stop/join holds no engine state or
monitor lock. Existing native cleanup completes before shutdown stops sampling.

Direction:repair the resource contract without layering failure/policy gains.
Efficiency:one actual source change with two discriminating regressions,no
new logging tool or invented performance result. Maintenance uses existing
architecture/daily owners. Seven-step native-evidence warning is not solved by
this code;all throughput/RQ claims await complete actual native evidence.

Next:collect actual source CI and repair any code/test failures;then record its
precise scope. Preserve the sole full native pair until its existing exit
event,root-review complete results,and proceed to the prepared42solo point.
No new workload experiment or automatic queue is started. Goal remains active.


### E112.3 — preserve and repair first real CI failure
Source80c271dRust job122952278167fails E0063because the pre-existing private
shutdown/admission race fixture manually constructs Inner without its new
field. Root missed that initializer. Add the default unstarted guard only;
no fixture sampling thread is started and its paused-sample semantics stay.
Native contract job122952277663passes5explicit controls(4.63s,not a performance
measurement). Failed log/run metadata remain;do not call this source qualified.
A forward source commit retriggers the same existing workflow.


Corrected-sourcef15197fCI40727967801passes fmt/clippy,all8engine unit controls,
all26engine integration controls(including both new regressions),all8Lean unit/
8process controls and5explicit pinned-native contracts. It then fails existing
CLI structured_resource_logs_do_not_corrupt_jsonl_results:an empty short request
exits before the new delayed first sample. Root had changed the old immediate
interval phase. Restore an immediate first sample with Duration::ZERO,then
retain the same nominal1s period. Do not weaken the existing log assertion,
insert fixture sleeps or call the partial workspace pass complete.
Failed job122956253072and successful native job122956253593full logs are retained.


## EXPERIMENT_GATE re-entry — E112.4,physical interruption

Actual source4966491CI40729814255passes all72workspace controls,fmt/clippy/
rustdoc,all5explicit native contracts,and38Python controls. Full job logs
and exact-source counts are retained. This qualifies that source's independent
sampling/notification,not physical stop under a blocked executor.

The root then found the remaining dependency:Native backends physically kill
from their async cancellation paths. The sampler can request a token while
the executor remains blocked. Add VerificationBackend's source-compatible
provided synchronous request_resource_preemption hook. The engine snapshots
owned roots before cancellation and calls the hook outside engine locks.
Allfour local native provider forms and the existing journal wrapper forward
the existing birth-matched group signal. Other backends' default remains
cooperative;no generic hard-interruption guarantee is invented.

The strengthened blocked-executor fixture now requires both token and hook.
A real OS-process unit control covers stale birth/correct group/unrequested
sentinel for allfour providers without a Tokio runtime. A new sixth pinned
native control verifies actual prepared-child PPID/no prior fallback,stops it
while the only executor is held,and then resumes awaited reaping. Possible
cancelled-transport errors remain operational,never proof rejection.
These controls must pass actual source CI before the expanded repair qualifies.

No active collector/private binary changes. The fixed4.9Mathlib full pair
still runs at its own point. Kernel scheduling,monitor/syscall/engine-lock
latency,signal latency and between-sample growth remain;physical interruption
does not turn the1s sampler into a hard RSS quota. Changed scheduling can alter
operational preemptions/statuses,so future real paired acceptance/status sets
remain required. This is resource engineering,not a workload novelty result.

## WRITE_GATE re-entry

The architecture/API Rustdoc now distinguishes synchronous signalling from
awaited retirement and documents default cooperative-only plugins. Existing
daily thought records the dependency. Paper/scientific contract remain
unchanged. The source/CI predecessor remains separately attributed;no proxy
notification test is presented as a native independent-kill test.

## REVIEW_GATE re-entry — pending expanded-source CI,self-review

Audit callback execution outside locks,owned-root capture before token wake,
birth verification in the unchanged native group guard,and wrapper forwarding.
The new test rejects fresh fallback as prepared engagement before interruption;
post-cancel fallback diagnostics alone do not falsify the earlier actual PPID
witness. Target and sentinel fixtures own/reap their children on both pass and
assertion failure. Actual native retirement is awaited before checking the
blocked-executor observation. No other agent or independent-audit claim.

Route to the same existing CI for the expanded source. Prior72/5/38passes
cannot qualify these later code bytes. Complete native population/warm parity
and all RQs remain open;keep the one live cohort and full goal unchanged.


Before expanded-source qualification,the native control is tightened to require
a live pre-stop child with matching kernel birth as well as PPID. Merely seeing
a parent-related PID that had already exited would not establish intervention.
This changes the new control only,not resource implementation. Preserve all
source-CI revisions separately;final qualification must cover this exact control.
