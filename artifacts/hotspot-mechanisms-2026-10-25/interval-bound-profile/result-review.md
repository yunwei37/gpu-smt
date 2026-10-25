# Interval bounds before expansion — root self-review

Implement an opt-in source-native observer that inspects the numeric range
using the retained Mathlib Methods,then restores the saved elaborator state
before delegating the unchanged interval_cases tactic. It emits invocation
byte,explicit bound hypotheses,inclusive bounds,cardinality,inspection time
and native return/unwind time. The inspection itself constructs zero leaves.
It does not replace the existing on-demand traversal,implement an early reject,
certify a timeout or treat a missing range as failure.

Real controls:18native invocations,nine matched pairs,zero expected-label
mismatches,zero observer/watchdog error;combined sampled RSS peak is
18377146368bytes including the unchanged acquisition.
Nat/Int/nested/inconsistent/missing-bound/failure/fallback/admitted cases are
retained as raw data. Inconsistent bounds are NOT failed proof goals:the native
tactic may close them by contradiction. Nine control pairs are qualification,
not execution of the48original timeouts or an isolated performance result.

All48original sources and116calls receive exact byte-mapped prefixes;
native parser validates all116inner-kind associations with zero parse errors.
The generalized preparer reproduces all original/import/profile23simp batches
byte-for-byte unchanged. The first parser wrapper census used an unqualified
namespace and missed wrappers despite successful source parse;that attempt is
retained,its wrapper-count validation invalidated,and compile003 fixes it.
No malformed source was run as a candidate.

Pinned Mathlib intervalCases allocates one IntervalCasesSubgoal per value
before Methods.bisect;native all_goals accumulates resulting unsolved goals.
This supports investigating a necessary-memory bound,not an admitted resource
certificate:actual entry bounds,representation/liveness and nested-branch
dependence must be validated. Cardinality alone is no300second proof,product
of source ranges cannot be assumed when a branch can close/shrink,goal
falsehood is not inferred,and all certificate flags remain false.

Original48on-demand before-expansion falsification/inevitable-timeout fraction
is UNMEASURED,not0/48from absence of execution. Original23stage/lemma table is
also not completed here. Current full scheduler group remains sole acquisition.
Latest user order:collect/push its completed pairing,then four-worker dynamic
48GiB+Mathlib-derived population pair,then lean-mlir bv_decide. No new scheduler,
fixed AS limit,subagent,external system reproduction or frozen CPU-oracle work.
Root self-review only. Four continuing directions remain unchanged.
