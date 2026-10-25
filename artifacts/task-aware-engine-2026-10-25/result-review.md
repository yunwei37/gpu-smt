# Task-aware engine result — root self-review

This is a workload-policy implementation and retrospective opportunity model,
not a native performance result or a new contribution claim.

## Fixed HTTP-span model only

| Hypothetical workers | Flat first-success finish | Interleaved finish | Conditional solved-task p50, flat/interleaved |
|---|---:|---:|---:|
|2|14926.20s|14803.18s|4644.36/663.00s|
|4|7617.02s|7429.95s|2338.79/304.54s|

All7808/244task records remain;142have an observed valid candidate and102do
not. The latency quantiles condition on the142known-solvable tasks. The other
102have no finite accepted-decision time, not zero latency. All simulated
policies preserve the same142solved IDs by construction from known labels.

Whole-model finish changes little; work in groups without observed success remains. Only17of83
observed timeouts belong to solvable groups. Interleaving mainly changes when
successful tasks become internally available and avoids some simultaneous
sibling work; it cannot remove the other unresolved/time-out work.

Each request retains its old observed HTTP span as a fixed service cost. No
memory admission, warm-state change, packing, prediction, cancellation/cleanup
or contention cost is modeled. Four workers is a hypothetical model using
those same observations, not a measured4core/48GiB resource point. Internal
events are not client streaming; current batch HTTP/CLI replies return after
the batch. No runtime gain or Amdahl bound follows from these figures.

## Actual implementation evidence

SchedulingPolicy now has a default batch_priorities method. Existing policies
need no new implementation. TaskInterleave<P> wraps source ranking and RSS
prediction, interleaves first-success tasks and leaves all-mode unchanged.
No concurrency cap, native verdict, shorter timeout or prefix/certificate reuse
is introduced. The CLI exposes --policy task-interleave. Continuous-arrival
fairness and cross-batch task coordination are not implemented by this batch
policy; ordinary RR remains prior technique.

The actual Rust policy consumes the unchanged full7808JSONinput in both modes.
All-mode order matches the original array; first-success order exactly matches
the reference interleaving across all244task IDs, including literalNone rows.
The ordering-only example starts no verifier or resource worker.

Measurement reports conditional internal first-acceptance observation times,
unsolved task IDs and explicit returned-row throughput. Cancelled/cache/shared
rows cannot be called fresh native checks. These metadata do not add client
streaming. Native raw JSON and accepted-set comparisons stay intact.

Actual unit/interface/native CI outcomes are appended at the validated boundary.
Only the existing original native group is active locally. CPU oracle remains
frozen and four directions continue, without a new deadline/closure rule.
This review is by the root thread, not an independent audit.

The102groups without observed success are not declared mathematically unsolvable. The42old resource failures remain unresolved under a different resource point; isolated reruns can change observed solved groups. Original labels/results remain archived before this clarification. All7808slots reconcile as completed, queued-cancelled or active-cancelled model work.

## Local validated implementation boundary

Formatting, Clippy,33ordinary tests, API docs and CLI help pass:
artifacts/rust-engine-2026-10-25/validation-20261025T112606/validation.json. Two native tests remain explicitly ignored
locally while the sole original collection is active. The actual native CI test
now exercises task interleaving with same-proposition sibling groups and
admitted/rejected-only task exhaustion against fresh raw native responses;
its exact-head result is still pending the forward push. The ordering-only
Rust example agrees on every one of7808IDs in both modes with the reference
original/interleaved order.43relative core-document target paths exist;
external URL and anchor validity were not re-audited here.
