# Step007 — native timing qualification and work/span measurement

M branch,2026-10-30UTC; self-review. Experiment in progress, not a result.

## EXPERIMENT entry and plan
RQ3/RQ4 supporting uncertainty: whether independently executable tactic work
can materially reduce the observed verification tail while preserving native
outcomes. Prior trace.profiler changes7/200 diagnostic error flags; its timed
DAG cannot support this inference. Retain that failed comparison.

Dynamic lean_profileit interposition produced0 callbacks. Reuse the existing
version-matched SDK archives and tiny original shell main; link-time
--wrap=lean_profileit redirects calls without recompiling Lean/Mathlib.
Installed archives:libLean119,617,182B,libInit7,956,708B,libleancpp5,891,138B,
libleanrt664,150B. Estimated link cost below2GiB RSS, two cores, a few minutes;
measure actual owned-tree RSS/CPU/wall. Products stay outside checkout.
This is not a whole-project build. No security/PMU/host changes.

Qualification requires real callback entry/exit evidence, original callback
delegation, and differential error flags/diagnostics/InfoTrees against stock
Lean. Raw heartbeat counts are also reported. Cold first-use caches are a
confound: the inactive hook's first source pair already had13000/12316 raw
heartbeats, so warm-order equality is not presumed. Use fresh process controls
where required; do not relabel absent instrumentation as a pass.

After qualification, retain the fixed200-source sample. Partition into
bounded serial captures using the prior control costs only to balance run
length, not to select favorable candidates. Every source remains included.
Each native capture stays below30min, one Lean process, <=8cores and16GiB M.
Report raw failures/budget stops separately. Full spans require an explicit
dependency/timing join; unsupported parts remain unknown.

## WRITE / REVIEW entry
The paper contract/RQs stay unchanged; only M evidence is edited.
Generic proof futures, reflection and compilation are prior work.
No complete DAG, production parity,1.3 gain or native speedup is claimed.
Daily reflection: repair the measurement that consumes the budget before
drawing an algorithmic conclusion; callback presence and full observed
responses matter more than a successful process exit.

## EXPERIMENT result — qualification only
The link succeeded using the existing SDK archives, same version4.9.0-rc1 and
githash be6c4894e0a6c542d56a6f4bb1238087267d21a0. Failed attempts are retained:
the SDK compiler lacks system stdio headers; using the host C compiler exposed
a newer-glibc strtol symbol. Only the measurement constructor's bounded decimal
argument parsing was changed to remove that dependency. Stock Lean objects
and verification code were not rebuilt or edited.

Final v5 keeps the name scratch buffer thread-local to avoid2KiB of extra
native stack per nested callback; it records raw EIO result tags with scalar
checks. Link phase wall0.47s; cumulative per-child kernel RSS high-water
443,830,272bytes. Subsecond aggregate RSS peaks can be missed by1s sampling;
that scalar is not a hard or simultaneous-tree quota.

Three independent fresh processes ran the same four controls with stock SDK,
linked/timing-off and linked/timing-on. All8 stock/comparator pairs have exactly
equal error flags, diagnostic strings, InfoTrees and raw heartbeat deltas
(13000,23351,4461,114090). Timed cell has1050 entries/1050 exits,526 tag0 and
524 tag1 results. Raw data remain in external captures/c-cold-v5-*; small result
is c-fresh-differential.json. This qualifies the hook on these controls only.

## WRITE
Source, build commands/failures, cold controls and resource limitations are
retained. No proof of generic transparency, full200 parity or speedup follows
from four examples. The failed trace.profiler data remain a separate point.

## REVIEW — self-review
Actual callbacks, fresh-order controls and raw counters checked. The first
within-process cache difference disappears in fresh matched processes.
For full captures the resource sampler now follows PID+birth descendants of
the declared finite controller, rather than counting only the direct Lean.
No external signal-based watchdog is claimed. No other line/main path changed.

Next: full200 stock/linked-off/linked-on matrix, disjoint input shards with
identical per-shard order across cells. Use past observed costs only to balance
collection lengths. Preserve failures and inspect complete observed parity
before interpreting a work/span model.

Dependency export now separates all reachable references from conservative
reachable unassigned expression/universe variables, following existing
assignments. This prevents already assigned meta references from automatically
being labeled mutable conflicts. Full local contexts are still overapproximated;
hidden state and nonmonotone metaprograms are not proven independent.
The final two fresh controls with that export have equal stock/timed errors,
diagnostics,full InfoTrees and all four raw heartbeat deltas.
