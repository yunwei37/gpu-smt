# Step0148 — dynamic public backends and suspended failure replay

BUILD_AND_EVALUATE,root only. Latest user says remain onG10,continue Rust
work,12GiB serial/PVC for any future capture,and stop on API/unavailable<6GiB.
No native capture or placement/security change. Engineering dependency only.

## EXPERIMENT_GATE
E148.1:The existing engine uses trait objects;test the proposed failure cache
as an external public consumer with dyn backend. First compile fails on
implicit Sized,not native semantics. Relax only three bounds with ?Sized.
[Plan](experiment-001/plan.md),[result](experiment-001/result-review.md).

E148.2:Three public asynchronous integration fixtures prove supported dynamic
usage and meaningful in-flight effects:clear with two suspended consumers,
post-lookup generation change,and cancellation isolation. Native state can be
Send/notSync;typed exceptions preserve original failure semantics in fixtures.
8priorunits pass;fmt/clippy/example/rustdoc pass. Pure Rust validation
max344,473,600B sampled;no observed hostMemAvailable<6GiB. No proof/run benefit.

## WRITE_GATE
API/architecture docs describe dynamic associated types,exclusive state and
in-flight ownership without claiming native replay. No paper result/claim,
RQ,baseline or frozen native observer change. G10 guard qualification and
state/cost population evidence stay open;12GiB is not a hard kernel quota.

## REVIEW_GATE — same-thread self-review
Public consumer red result prevents a superficial trait-only extension claim.
Check no concrete-backend dependence,no metadata lock held across replay,
record lifetime at clear,cancellation/state freshness and correct HB costs.
No fixture is labelled native differential or independent review. Existing
native/default paths remain unchanged;only Sized relaxes. Full CI is pending
after publication. Commit/push this complete local implementation boundary,
then verify full CI. Continue G10 work without another lab request or unsafe
collection;only actual complete matched data can decide native cache benefit.
