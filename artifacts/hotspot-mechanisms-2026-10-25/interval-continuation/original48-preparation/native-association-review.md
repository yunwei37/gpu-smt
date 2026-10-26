# Native stage ordering — source-grounded root self-review

Pinned SDK4.9.0-rc1 Init/Tactics.lean lines347–355 defines <;> as a focus of
the left tactic followed by all_goals of the right tactic. The retained original
Syntax shows left-associated nested nodes for all48 cohort chains. Thus
interval_cases m <;> interval_cases n <;> norm_num <;> omega is not parsed as a
right-nested per-leaf closing continuation.

Lean/Elab/Tactic/BuiltinTactic.lean lines244onward reads the current goals,
evaluates the continuation on each, appends resulting unsolved goals, then sets
the resulting complete goal list. Its recover mode can log an exception and
retain the goal. The existing opt-in continuation instead traverses a leaf,
runs its whole closing continuation and restores saved state on thrown failure.
That is a material semantic/protocol difference, not a cosmetic source rewrite.

Retained original [Mathlib interval source](../../official-source/Mathlib-IntervalCases.lean.gz)
already documents eager goal construction; the additional exact SDK source
archives here retain parser macro and all_goals implementation. This is official
language/source grounding, not reproduction of a competitor verifier system.

Disposition: preserve the on-demand variant as an experiment; reject the claim
that its failed leaves alone authorize early request rejection. Final-chain
syntax permits a well-defined cohort variant but does not prove all shared
metavariable/fresh-name/name-dependent effects or finite-resource acceptance
equivalence. Require actual raw native and variant results with costs/fallback,
and a sufficient witness before any active service rejection. A large potential
Cartesian count also is not a wall-time or actual-RSS proof.
