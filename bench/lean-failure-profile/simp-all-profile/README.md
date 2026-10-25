# Pinned native simp_all phase instrumentation

Opt-in profile_simp_all simp_all [...] keeps the Lean4.9 native simplification
algorithm and wraps initialization, each hypothesis and target phase with
monotonic timing and diagnostic JSON on stderr. Original copyright/license
retained. No global tactic replacement or active-source rewrite.

This is instrumentation to distinguish slow per-expression normalization from
repeated full-context passes in the 23 simp_all-dominant timeouts. Type hashes
are investigation hints only: they omit proof/cache/mvar/context/config state
and cannot establish a cycle. No early failure, timeout prediction, semantic
equivalence or speedup is claimed. The native simplifier already detects an
unchanged post-rewrite expression, so that existing behavior is not our method.
Measured timings include diagnostic overhead and keep their own denominator.

The future testable rejection condition would require a proven repeating
complete deterministic transition state and preserved enclosing fallback
behavior. Neither a keyword nor expression hash meets that condition.

Begin/end pairs expose the phase in progress if a request is later killed.
[Native qualification](../../../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/result-review.md)
now executes6native/profile pairs;all statuses match,including rejected and
incomplete controls. It does not run the23original timeouts or establish a
safe rejection predicate. Exact original-source profiling is the next runtime
node once the retained full acquisition releases the slot.
