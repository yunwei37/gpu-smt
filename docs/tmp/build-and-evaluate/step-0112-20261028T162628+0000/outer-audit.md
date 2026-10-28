# Step0112 outer audit — root self-review,final source qualified

Executing root only;this is not independent audit. Inputs:exact source diff,
two new Rust controls,architecture paragraph,plan/result review and unchanged
authority/paper snapshot. No subagent,OMP or native AI session is used.

The inspected defect is dependency on the request executor,not an observed
benchmark sampling failure. An independent parent-process thread can progress
when Tokio is blocked;it still depends on OS scheduling,monitor latency and
engine locks. No stronger1s/hardquota claim is accepted.

Lifecycle review:the worker has a Weak engine reference while waiting;its
condition variable owns no native processes. Constructor records the join
handle before returning. Shutdown retires backend/native work first,then
wakes and joins the sampler. Final-owner drop wakes it;the same-thread
destruction branch drops its own join handle rather than joining itself.
The sampler drops a temporary owner before the next wait. No lease/
ownership lock is held across join. NewEngine spawn failure returns error.

New tests must actually run in CI;rustfmt alone is not qualification.
The blocked single-thread Tokio control is expected to distinguish the old
co-scheduled sampler from the independent one. Final-clone drop checks lifetime.
Native protocol controls remain pinned4.18and cannot establish4.9Mathlib gain,
population status equality or the full project's acceptance.

No budget,core/native-worker count,admission forecast,operational cache,
deadline or verdict rule changes. The live full pair stays on frozen13d4606;
these source changes are not retroactively attributed to it. No second local
native collection or compilation is launched.

Disposition:publish the source boundary to trigger the existing CI,explicitly
pending;close validation only after actual job results. Full native outcomes,
warm parity,original42solo,methods/novelty and complete paper evidence remain.


Re-entry finding:source4966491passes72workspace/5native/38Python controls,but
its blocked-executor test proves cancellation notification,not independent
physical stop. The root accepts this distinction and extends the same repair
with a synchronous backend hook plus actual owned-group/native-COW controls.
The hook is outside engine locks and retirement remains awaited. Local
backends signal existing PID/birth guards;unimplemented plugin hooks remain
cooperative only. These later bytes are pending fresh CI,not covered by the
earlier green source. No change to native4.9active acquisition or proof policy.


## Final audit of actual evidence
Read exact final08d6bccengine/smoke terminals and allthree completed job logs:
73workspace controls,6explicit pinned-native controls,38Python controls,
fmt/clippy/rustdoc success. Real OS-group hook unit and blocked-executor
hook dispatch pass. The strict native control proves pre-stop liveness,birth,
PPID and no prior fallback;stop is observed before async repoll,and native
retirement is awaited afterward. Composed controls are not described as one
native48GiBpressure/blocked-executor experiment.

The earlier compile/CLI failures are preserved and corrected forward-only.
Code byte-diff against the qualified source is empty at evidence closure.
No source/native settings or private running binaries are edited after testing.
No whole-candidate throughput,accepted-set equality,hard quota,novelty or
OSDIacceptance is claimed. This is root self-audit,not independent review.
The final source boundary is complete;the existing full research run is not.
