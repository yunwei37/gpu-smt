/-
Copyright (c) 2026 GPU-SMT contributors.
Released under Apache 2.0 license as described in the file LICENSE.

Opt-in experiment: interleave interval construction with one pruning stage.
This is not a native-equivalence guarantee or an early-rejection detector.
-/
import IntervalContinuation

open Lean Meta Elab Tactic
open Mathlib.Tactic.IntervalCases

namespace GpuSmt.IntervalMap

/-- Construct one interval's leaves on demand, run the supplied tactic on each,
and collect its surviving goals in traversal order. Surviving goals are allowed.
Construction interleaves with tactic execution, unlike native eager staging;
metavariable, recovery, diagnostic and resource behavior need differential tests. -/
def mapInterval (original : MVarId) (term : Syntax)
    (continuation : TSyntax `tacticSeq) : TacticM (Array MVarId) :=
  original.withContext do
    let expression ← Tactic.elabTerm term none
    let (subst, xs, goal) ←
      original.generalizeHyp #[{ expr := expression }] (← getFVarIdsAt original)
    goal.withContext do
      let x := xs[0]!
      let expression := subst.apply expression
      let mut lower := #[]
      let mut upper := #[]
      for declaration in ← getLCtx do
        try
          let (lo, hi, _) ← parseBound declaration.type
          if ← withNewMCtxDepth <| withReducible <| isDefEq (.fvar x) lo then
            upper := upper.push (.fvar declaration.fvarId)
          else if ← withNewMCtxDepth <| withReducible <| isDefEq (.fvar x) hi then
            lower := lower.push (.fvar declaration.fvarId)
        catch _ => pure ()
      let survivors ← IO.mkRef (#[] : Array MVarId)
      GpuSmt.IntervalContinuation.split goal (.fvar x) expression lower upper fun leaf => do
        let (equation, leaf) ← leaf.intro1
        let (_, leaf) ← substCore leaf equation (fvarSubst := subst)
        setGoals [leaf]
        -- Use native all_goals recovery/logging rather than silently swallowing
        -- an exception or treating a failed speculative leaf as a rejection.
        evalTactic (← `(tactic| all_goals $continuation:tacticSeq))
        let pending ← getUnsolvedGoals
        survivors.modify (· ++ pending.toArray)
      survivors.get

/-- Map an explicit continuation over on-demand interval leaves.
Later tactics run on the collected survivors; original interval_cases is untouched.
Errors restore this tactic's entry state before propagation. -/
syntax "interval_cases_map " term " => " tacticSeq : tactic

elab_rules : tactic
  | `(tactic| interval_cases_map $term => $continuation) => do
    let saved ← saveState
    try
      let remaining := (← getGoals).tail!
      let survivors ← mapInterval (← getMainGoal) term continuation
      setGoals (survivors.toList ++ remaining)
    catch error =>
      saved.restore
      throw error

end GpuSmt.IntervalMap
