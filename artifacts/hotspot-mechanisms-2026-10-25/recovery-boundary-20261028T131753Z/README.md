# Recovery semantics: reused native controls and original71 source structure

Root self-review,2026-10-28. This reuses completed2026-10-26 Lean4.9 native
outputs; it executes zero new candidate proofs and claims no speedup.

## Recomputed actual native result

| Native development control | Original | Recovery-disabled wrapper |
|---|---|---|
| Explicitly recovery-sensitive custom tactic | accepted,exit0 | rejected,exit1 |
| Ordinary first/backtracking | accepted,exit0 | accepted,exit0 |
| Failed inner have followed by True proof | rejected,exit1 | rejected,exit1 |

Raw original/modified sources and native responses:
[completed6control cell](../original71-native-20261026T125951Z/failfast-controls6/).
The first source explicitly reads its native recovery context; wrapped error
is requires recovery context. This is a deliberately constructed correctness
counterexample,not an observed natural-workload regression rate. There was
no separate import-only cell for these6 controls. Inspection of the opt-in
NativeFailFast source shows only imports,new syntax and the two native context
wrappers,not a global builtin replacement. Definition compilation alone did
not establish transparency. No generic recovery-disabled rejection path is
enabled in the Rust engine.

Recompute from exact saved inputs/results and parser outputs:

    python3 artifacts/hotspot-mechanisms-2026-10-25/recovery-boundary-20261028T131753Z/analyze.py

## Source-native boundary,not a new rejection predicate

The completed parser table covers exactly the same71original IDs,without
elaborating their proof bodies. All71 parse without errors and have one final
theorem declaration after set_option/open setup. A hook only after the final
theorem command cannot skip later proof declarations in this group. This is
not a measured0/71failure-coverage result,nor a claim about possible setup
errors,other workloads or earlier internal tactic events.

[Original parser output](../native-sites/compile-005/sites.json) and
[original71source/reference](../original71-native-20261026T125951Z/native71/)
are unchanged. analysis.json lists all71 command shapes and exact control
outcomes;analyze.py is offline result analysis,not a runtime observer/checker.

## Official source interpretation and decision

Pinned Lean [Tactic.Basic](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Elab/Tactic/Basic.lean)
makes recovery part of TacticM context;its exception handling can restore
saved state including messages,and alternatives already use withoutRecover.
[all_goals](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Elab/Tactic/BuiltinTactic.lean)
can log one branch error and continue under recovery.
[Top-level command elaboration](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Elab/Command.lean)
saves earlier command messages and appends current messages after elaboration.
These three local SDK source files matched the pinned upstream bytes when
inspected. This is an algorithm/source argument,not a new runtime equivalence
theorem or a general promise for arbitrary unsafe metaprograms.

Keep native recovery settings. A local error or branch failure is insufficient
unless a witness also excludes enclosing recovery/backtracking and later
acceptance. Do not rerun the already-settled generic transparency control or
deploy the unqualified23wrapper as a speedup. The four continuing directions
remain;this evidence excludes one unsafe constructor rather than closing
early-failure research. The sole current full7808 resource pair remains frozen
13d4606;fixed42 follows its actual completion/review. CPU oracle stays frozen.
