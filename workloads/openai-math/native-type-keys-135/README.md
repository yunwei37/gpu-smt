# Native theorem-type census of 135 compiled OAI objects

Lean 4.34.1 readModuleData/readModuleDataParts reads the already compiled
objects directly. All 135 complete, with 1,799 serialized theorem declarations.
There are 743 auxiliary-name theorems, 601 distinct native Expr keys, or
604 groups when ordered universe parameters and private-name status are added.
45 of the latter groups occur in more than one module. These include ordinary
generated proofs; no time saving or expensive-tactic identity is inferred.

Five files contain all 45 source decide+kernel occurrences in this pilot.
The reader finds 45 auxiliary proofs directly headed by of_decide_eq_true;
their native Expr keys are all different. Per-file source/shape counts match:
ComputeRow1115Batch17 7, Row0705207 1, Row072 35, FourBody.Basic 1,
FourBody.Symmetry 1. Thus this small pilot does not demonstrate reduction of
these 45 calls by repeated goal types. This is not the full 1,354,379-call
corpus: repeated-goal PlanarPacking/Ramsey clusters are not represented here.

Native Expr equality uses Lean's Hashable/BEq instances, not source strings
or a textual pretty-printer. No definitional normalization is performed.
Auxiliary names/body heads are conservative producer indicators, not a complete
tactic execution trace. Private-name status is observed, not a recorded
producer env.isExporting flag; defeq/hidden state/replay options are not audited.
These groups are not production cache eligibility or failure-cache hit rates.
Only successfully serialized declarations appear; failed and unreachable
calls are absent. Source occurrence counts are lexical, not execution counts.
No global native goal-count estimate follows from this pilot.

Axiom closure, including transitive ofReduceBool dependence, remains UNMEASURED,
not zero. The full-environment helper failed compilation once, then timed out
at its 30s self boundary twice with no results. An initial object-reader type
error is also preserved. They are measurement setup failures, not dataset
proof failures. Native readModuleData succeeds without traversing all Mathlib.
v3 completes in 0.789s, CPU0.789s, native process peak1,876,248KiB; this is
metadata reading, not a verification acceleration result. The retained old
EPFL process is still charged. One-second sampling can miss this short reader;
per-child wait4 peak is separately retained, not a hard RSS guarantee.
All source/native object inputs, complete outputs and failed attempts remain
on PVC outside Git:
.../gpu-smt-captures/workloads/openai4341-olean-types-v3 and prior audit dirs.
