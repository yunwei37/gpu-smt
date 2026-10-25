# Continue interval branch construction only when its leaf is needed

RQ3 implementation hypothesis under the user's continuing failure-aware
direction: for a chain of interval splits followed by a closing per-goal tactic,
constructing every branch before trying the first leaf can waste work on
candidates whose first leaf already fails. The completed profile attributes
48dominant timeout sources in7tasks to interval_cases. This does not prove
branch-construction is removable or establish a speedup fraction.

Pinned Mathlib4.9 source allocates all equality-goal metavariables, then builds
the bisect proof tree, then returns substituted goals to following tactics.
Prototype a separate opt-in continuation interface that constructs the same
numeric bisection in depth-first order, invokes a closing continuation at each
leaf, and stops on its native failure rather than allocating all later leaves.
Keep native proof terms and checking. Use existing Methods for numeric bounds
and proof construction. Do not modify or hook the original interval_cases,
rewrite original candidates, shorten timeouts, reject by range size, or claim
false arithmetic goals from tactic failure.

This stage only compiles the library against the exact retained API, without
executing any original candidate or adding another capture. Compiler and old
group RSS are summed each second; pressure aborts only this new preparation.
One CPU11,no AS cap,48GiB combined sampled response; old group remains frozen.

Next runtime qualification after the sole group retires must test solved/failed
leaves,integer/natural and inconsistent bounds,nested splits,rollback/fallback,
shared metavariables,diagnostics and resource outcomes before any population
integration. Closing-continuation semantics is narrower than arbitrary
all_goals/first/try/goal-order-dependent tactic programs; unsupported forms stay
original. A compile is not a working reliable failure detector, semantic
equivalence,CPU/GPU performance or novelty claim. Lazy traversal itself is a
standard implementation technique; any contribution remains unproven.
