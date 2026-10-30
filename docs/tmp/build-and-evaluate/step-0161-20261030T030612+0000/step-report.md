# Step0161 — native differential evidence in the paper and completed CI

BUILD_AND_EVALUATE; same-thread self-review, with no new Lean execution on G10.

## EXPERIMENT_GATE
E161.1: Source7ab0e40 engine40995303698 and benchmark-smoke40995303783
both actually completed successfully. Rust executes the explicit workspace
doctest command:2passed, plus its existing all-target suite. The separate
native job runs6stock-REPL comparisons and the Lean4.9 finite transition controls,
then all10whole-candidate cases across5modes. Benchmark smoke retains81Python
test passes. Full raw job logs and terminal metadata are archived here.

E161.2: The native job actually uploaded artifact12950654651. Downloaded the
76849-byte ZIP and inspected219file entries:complete50-cell result,6forced hits,
raw sources/stdout/stderr/JSON, and zero olean files. The ZIP and manifest remain
in experiment-001. This is actual fixture evidence retention,not a promise based
on workflow syntax. The first fetch attempt failed because the renamed repository
API returned301then302;the fixed reader handles API redirects while keeping
Authorization only on api.github.com. No source/native outcome was affected.

E161.3: Recomputed paper reference counts from retained local matrix JSON:
3accepted,5rejected,1incomplete/sorry,1heartbeat-limit. The five modes match
the complete ordered diagnostics,exit,status and authored theorem audit.
No inference of population hit rate or exact resource-bound response parity.

## WRITE_GATE
Paper RQ2 behavior section now gives the authored same-retained-input controls
and their limits,separate from the service comparisons. API documentation links
the same boundary. Tectonic builds the complete manuscript successfully with
raw output retained;observed layout warnings remain,with no attribution to an
unrebuilt baseline and no claim of publication-ready layout. The G10 paper build
samples peak197390336bytes in its compiler tree and minimum node available
19860606976bytes;sampling is not hard enforcement. It launches no Lean.

## REVIEW_GATE — self-review
Checked terminal head SHA,complete CI job logs and downloaded artifact contents;
source7ab0e40 is the qualified code boundary. This later commit changes evidence
and documentation only. The ordinary-failure adapter remains default-off and
stock native/CLI/HTTP backends do not enable it. Short authored same-entry hits
do not qualify arbitrary IO/opaque effects,cross-candidate semantic rebasing,
full-workload accepted-set equality,timeout parity,hit opportunity or speedup.
Formal8031-unit population measurement remains incomplete;the AppArmor signal
limitation still rules out formal/long G10 collection. No signal/security repair,
resource/scheduling mutation,CronJob operation,other agent or duplicate capture.
Four directions remain active and CPU oracle/narrow-GPU/interval-elasticity
closures remain in force.

Raw-evidence note: unfiltered git diff --check reports whitespace only in retained
verbatim logs. Source/documentation check passes;raw logs are not normalized.
