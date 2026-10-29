# Public failure-cache integration result — root self-review
The new public consumer first fails with E0277/E0599 because FailureCache's
implicit Sized bound rejects dyn FailureReplayBackend. Raw compiler output is
retained. Add only ?Sized to the struct and its two impls;no trait methods,
records,default activation or native adapter behavior changes.

Three public integration tests then pass with an explicit trait object and
exclusively owned Cell-based Send/notSync state. Two asynchronous replays
can both reach suspension before either completes. Clearing metadata prevents
new hits while both retain their opaque record;one record destructor runs
after the final reader. A generation change during suspension returns None
with untouched state/heartbeats. Cancelling one consumer leaves the other's
ordinary-exception transition and heartbeat debit intact.

Eight prior failure-cache units pass. All-target workspace clippy,fmt,
simulated public example and warning-free rustdoc pass. Peak nominal1s
owned development sample344,473,600B;host available memory never sampled below
6GiB. CPU6–7,one-job compact build caches/logs onPVC. No native process,
collection,global solve lock,dependency,service or permission change.

These tests establish the simulated public/API ownership boundary,not native
transition qualification,expensive-tactic coverage,speedup or novelty. Stock
Lean/Engine.verify/CLI/HTTP still do not construct this store. Native capture
remains stopped because required signal control failed. Full CI follows push;
the prior G10 lifecycle failures are not needlessly rerun/relaxed locally.
