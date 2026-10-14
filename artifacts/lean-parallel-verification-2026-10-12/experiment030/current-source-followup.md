# Current source follow-up — 2026-10-14

Purpose: check current-source novelty and strongest-baseline coverage while E030
runs on its retained version-aligned candidate stream. This is a source follow-up,
not a completed new literature loop or a current-toolchain benchmark.

The [official release](https://github.com/leanprover/lean4/releases/tag/v4.35.0)
and [release notes](https://lean-lang.org/doc/reference/latest/releases/v4.35.0/)
identify v4.35.0, published2026-10-12. Earlier4.32references describe an inspected
historical version; they are no longer the latest stable release. E030's pinned
4.9.0-rc1/Mathlib candidate outputs remain a same-version experiment, not measured
superiority over current Lean.

[Current REPL source](https://raw.githubusercontent.com/leanprover-community/repl/master/REPL/Lean/InfoTree.lean)
retains whole-Syntax string predicates for explicit sorry tactics/terms. Its term
collector additionally stops beneath sorry tactic nodes, unlike the retained4.9
collector. E030 preserves the retained traversal and original positive predicates;
it is not a drop-in claim about the complete current REPL implementation.

[Lean PR15531](https://github.com/leanprover/lean4/pull/15531) remains open/unmerged
at observation, head5b76244dd0a3a58c5090de56edfc48c182808420. It addresses repeated
module mapping inside a process and remains a concrete competing preparation
mechanism. Its author measurements are prior-work evidence, not this project's
measured result. No extra rerun of the closed shared-process candidate is admitted
from this status alone.

Implication: current native snapshots/services/mapper mechanisms remain required
strong baseline coverage. Routine AST matching is not a systems novelty claim.
All four RQs and full Lean/SMT/GPU evaluation remain open.
Raw primary responses/URL/time receipts: current-source/.
