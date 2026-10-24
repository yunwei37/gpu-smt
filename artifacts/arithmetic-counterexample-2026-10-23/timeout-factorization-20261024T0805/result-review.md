# True arithmetic obligations in three costly timeout requests

Root self-review,2026-10-24UTC. Supporting interpretation withinRQ4.
Reuses three already-returned requests of the ongoing own7808observation;
no new Lean/GPU execution, numerical solver, optimization or competitor.

## Actual source and timeout evidence

Sources minif2f-7200,7205and7210 belong to the same original task,
mathd_numbertheory_541: natural m,n>1 with m*n=2005 imply m+n=406.
Their proofs contain nested interval_cases after arithmetic facts bounding
m/n by2005,401or406. This is a source-level indication of potentially
expensive case enumeration, not a measured number of generated branches.

The unchanged native SDK classifies every selected response timeout_error;
each records a300.0s request timeout. ObservedHTTP envelopes are
300.009982802,300.021576618and303.564660984s. The900s of reported request
limits and903.596220404s of cumulativeHTTP are not whole elapsed or CPU work:
requests can overlap, and HTTP includes waiting/transport.

The frozen subset contains2,3and4actual arithmetic entries respectively.
After the final observation worker reply, the response intervals continue
for299.825561419,299.684912210and299.667673935s. These intervals can include
the last arithmetic tactic itself and later source commands. No dynamic
tactic-exit/phase profile is available, so do not attribute every remaining
second to interval_cases or any one solver operation.

## What can and cannot be refuted

All9captured ASTs are supported Nat arithmetic and explicitly retain all three
base assumptions m>1,n>1,m*n=2005. Their goals are the copied product equality,
positivity facts and upper bounds2005/401/406. They are different from the
wrong auxiliary equalities in the earlier cheap-positive subset.

For any original solution, positivity bounds m by2005. Enumerating integer
divisors2through2005 yields exactly two feasible assignments:
(m,n)=(5,401)and(401,5). The analysis checks the captured hypotheses and goal
exactly at both points for every entry. Each point satisfies every captured
context and every one of the9goals. Since these contexts retain the original
premises, their model set is contained in those two assignments. Thus none
of these captured obligations has a counterexample under its full context.

This is an exact finite-domain reasoning argument for these source/AST
records, not a generic Lean validity checker, generated Lean proof term or
new runtime oracle. It neither replaces original verification nor certifies
unobserved later obligations. The original source and exported-domain
interpretation remain explicit inputs, with root self-review only.

A sound counterexample screen therefore cannot fail early at these9hook
points, regardless of numeric point throughput or a better sampling recipe.
The expensive requests are not evidence of false arithmetic targets at
those entry points. This is a genuine applicability limitation for the
current method, not justification for more point-kernel tuning.

## Raw/reproduction and resource scope

[Snapshot](snapshot.json), [actual9goal entries](goals.jsonl.gz),
[three original sources](originals.jsonl.gz), [three nativeHTTPresponses](http.jsonl.gz),
[executed analysis](analyze-executed.py), [exact domain checks](goal-checks.jsonl.gz)
and [result](result.json) preserve the complete argument.
The script asserts the original premises are present, matches each goal
timestamp inside its actual returned request, and uses the native SDK
status rather than interpretingHTTP200 as success.
[Command/exit](command.json) and jointmonitor evidence are retained.

One jointRSSsample includes the exact original observation PID/birth and
observes24,264,556,544bytes/max2actualREPLs,0kills/errors. It is not a complete
peak or kernel hardRSS enforcement. The live original files remain unchanged;
only complete selected lines were copied into this immutable subset.

## Result review and disposition

Run status: valid supporting source/AST/returned-response analysis.
Scientific result: these3costly timeouts contain9captured true obligations,
so lack a refutable target for the current arithmetic hook.
Scope: three chosen examples from one task; not a random sample, fullfalsegoal
rate, general timeout characterization or globalGPU/Amdahl impossibility bound.
Research value: supporting mechanism applicability evidence. It changes the
interpretation of costly failure: search failure does not imply target falsity.

Do not promote this case analysis into a new factorization solver, new
baseline matrix or general-purpose certificate system. Do not close the
GPU/project/hourlytask from this subset. Preserve the running fullcensus;
its actual completion still precedes complete coverage/cost analysis and
the already-planned ownnative24and fullpairedmeasurement.
