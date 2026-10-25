# Step0028 — actual native simp_all phase instrumentation

## EXPERIMENT_GATE
Resume source-grounded simp hypothesis at its missing diagnostic implementation.
Plan/self-review in experiment-001. Compile original phase algorithm in opt-in
namespace;execute actual native/profile development controls. Original group
still owns the only full collection. Do not replace original source or infer
cycle/failure from hash/keyword. Four directions continue.

## WRITE_GATE
Targeted instrumentation documentation,not full paper rewrite or scientific
contract change. Original RQs/Initial Narrative and result slots unchanged.

## REVIEW_GATE
Root self-review below and outer record;no independent audit or delegation.

# simp_all native-phase prototype — root self-review

The opt-in module preserves the pinned native Lean4.9 simplification loop and
adds begin/end events around initialization,each hypothesis,and target
simplification. A final unmatched begin in a later killed request can identify
the interrupted stage; no event means the request has not entered that hook.
Round count,entry count,hypothesis-update count and type hashes are diagnostic
hints. They do not include complete context/proof/cache/mvar/config state and
are NEVER used to return failure. No builtin replacement.

First compile fails on Nat.toNat and unconstrained helper universe; raw source
and errors retained. Second compile succeeds. Adding a begin event before each
phase fixes the important limitation that end-only logging cannot locate a
phase killed by timeout;third compile succeeds. First end-only12controls stay
as version-specific evidence. Final12controls(6native/profile pairs) all agree:
4accepted pairs,1rejected,1incomplete. All16begin events match
16end events in these controls;phase records are actually emitted,
not merely mocked. Native proofs execute/check. Fallback/admission retained.

Final control lifecycle36.072264s,combined original-owner/test-tree
1s sampled peak43,020,148,736bytes
(40.07GiB),no48GiB pressure or monitor
errors;no fixed AS cap,CPU11 shares the retained full capture. Test clocks
include startup,logging and completion polling;no speedup estimate. Phase
nanoseconds are control-only,instrumented and not the original23sources'
wall-time shares.

Reliable request-level early rejection is still unresolved. A future cycle
criterion must establish a full deterministic repeating state and preserve
enclosing first/try behavior. Native simp already skips unchanged expression
rewrites. Repeated expression hashes,large expressions,commutative lemmas and
source keywords do not prove failure. For interval_cases,the separate closing
continuation controls show local status agreement only;range size is not a
request timeout proof. Original48/23sources remain unmodified and await the sole
population slot. No frozen CPU oracle or comparison reproduction.
Root self-review,not independent audit.

## Targeted paper update and retained acquisition

# Targeted paper/evidence update — self-review

Update only facts justified by Steps0026–0028: actual six full-Mathlib
fresh/child control pairs, two simultaneously connected children, nine interval
status pairs, six final simp_all phase pairs. Preserve source-level semantic
limits, diagnostics differences and missing original48/23/full-population
evidence. No claim of general safe fork, early request rejection, speedup or
novelty. Four RQs and Initial Narrative unchanged; no full writing loop.

Tectonic compiles the current paper to PDF with exit0; layout warnings retained,
no visual/publication acceptance asserted. Generated PDF stays in /tmp.
Existing shared-owner full scheduling collection still runs first-original.
At15:37UTC its ledger has2422actual returns(139valid,2230lean_error,34timeout,
19server_error transport labels)and4157cancelled-before-start records;these
are a nonterminal progress snapshot,not complete paired throughput or corrected
native resource labels. first-short not started. Do not freeze incomplete logs
as a completed experiment or interrupt the owner. All-cell7808complete evidence
already committed;no duplicate full workload starts.

Daily maintenance/reflection updated in its existing canonical record.
CI receipts identify source SHA and actual workflow status; no engine/native
CI is triggered by bench/docs-only paths. Root-only self-review,not independent
audit. Exact original lean-mlir dependencies complete but full-module execution,
42isolated resource retries,dynamic throughput and original48/23hook coverage
remain real runtime work after the sole full collection retires.
