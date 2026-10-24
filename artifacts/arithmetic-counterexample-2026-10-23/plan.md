# GPU arithmetic counterexample screening — RQ4

User-directed own-method experiment. Stop extending external SHRED/Kimina/
Farkas comparisons; retain their existing evidence. The existing native
request boundary is reused only to run our method off/on on identical
original candidates, not to integrate another competitor.

Hypothesis: a consequential fraction of failed arithmetic attempts reach a
genuinely false supported goal whose exact counterexample can avoid expensive
native search. Existing failed request time alone does not establish this.

First characterize the full retained miniF2F native outcomes/time and
arithmetic failure messages. Build a native Lean goal/context extractor at
actual tactic entry. Record supported typed arithmetic AST and complete
propositional context; unsupported/metavariable/dependent terms fall back.
Do not use unconstrained linarith atoms as semantic variables or infer false
from numeric solver failure. Candidate failure is distinct from false goal.

For a counterexample, every supported assumption must be true and the goal
false under exact rational/integer evaluation with correct native type/domain
constraints and local definitions. GPU float evaluation only proposes points.
CPU exact verification authorizes early arithmetic-tactic failure, never proof
acceptance. Preserve enclosing first/try/repeat alternative behavior, rather
than kill an entire candidate because one branch has a false goal.

Measure observed supported/falsified goals by final candidate outcome and
historical own request cost, preserving unknown/no-witness/unsupported classes.
If the real opportunity survives this measurement, prototype a batched
point-evaluation kernel on RTX5090 and compare off/on at the same candidate/
resource point. Report complete costs, accepted/rejected/incomplete/resource/
timeout outcomes, failed-source and timeout distributions separately. No
assumed accepted-set invariance or whole-wall speedup from overlapping sums.

All work root-only, main/existingWorkspace. Max2actualREPL24GiBeach,
48GiBaggregate sampled ownRSS includes any GPUprovider. One fullgroup only.
Original workloads/failures/raw remain. No third-party reproduction or solver/
kernel tuning grid. Real qualification precedes any full end-to-end pair.


## Executable complete comparison after native qualification

Reuse the existing finite device lifecycle, Phase lean24 first, then
lean-full after root reviews actual device/outcome/cleanup results. The
complete pair uses all7808originals, same order, original300stimeouts,
same4CPU/max2REPLs/2×24GiB/48GiBaggregate including the point provider.
Off uses untouched original Lean sources. On pays own parser preparation,
imports/wrappers, export, point proposals, upload/compute/download, exact
checks, fallback, queueing and retirement. It does not reuse an instrumented
observation clock as the native denominator.

The existing runner's --full switch executes off then on serially, one full
group only. No full acquisition is launched before the actual current
observation closes and native24 is reviewed. This is a fixed-order first pair,
so a final effect claim needs uncertainty/repetition appropriate to its size.

Use analyze-screening.py with --off/--on closed cells, --lifecycle and
--preparation summary. Report statuses/acceptance changes, baseline-failed
and baseline-timeout cost distributions, and identical IDs ranked by baseline
HTTP time for slowest1%/10%. Keep all resource failures and incomplete results.
HTTP/body sums overlap and never substitute for whole elapsed.

Warm whole-group/native complete lifecycle clocks and cold provider creation/
retirement are reported separately. The combined controller clock includes
both cells. Its residual after subtracting the native off lifecycle includes
on preparation, execution and controller/retirement overhead, an explicit
accounting convention rather than an isolated on measurement. Do not call
offline474batch/device qualification a complete proof result.

## Native-facing worker transport qualification, 2026-10-24UTC

Fold one missing interface check into the existing point qualification, not
a separate research experiment. The earlier actualGPU qualification supplied
one prepacked474entry request and did not execute the persistent worker's
individual screen RPC, exact host recheck or CPUclosed dispatch. Reuse the
same actual474entry input and expected exact witnesses through two persistent
worker processes, current worker source, existing finite5090provider and
existing joint48GiB watchdog including the active original census.
No new REPL or secondfullcapture; record the short coexecution window rather
than treat observer times as an isolated performance baseline.

Command: existing device-lifecycle.ps1 -Phase points -WorkerStream, with a new
result directory. Compare actual source/entry ownership, expected exact
witnesses, invalid points/provider errors, worker exits, actual GPU batch
membership and complete provider/Job retirement. This is dependency-only
evidence. Success returns to the already-planned native24/fullpair after
actual observation completion; failure repairs only this online interface.
No new numerical competitor, parameter search or RQ result is admitted.
