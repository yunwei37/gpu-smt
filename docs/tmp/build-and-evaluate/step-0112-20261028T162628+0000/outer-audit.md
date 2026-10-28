# Step0112 outer audit — root self-review,source CI pending

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
