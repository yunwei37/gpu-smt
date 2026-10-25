/-
Copyright (c) 2019 Scott Morrison. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Scott Morrison, Mario Carneiro

Experimental continuation traversal derived from Mathlib/Tactic/IntervalCases.
Only the traversal is changed; Methods supplies the native bound/proof routines.
This opt-in prototype does not replace the original interval_cases elaborator.
-/
import Mathlib.Tactic.IntervalCases

open Lean Meta Elab Tactic
open Mathlib.Tactic.IntervalCases

namespace GpuSmt.IntervalContinuation

/-- Build interval leaves only as their closing continuation is requested.
This is a prototype API, not a native-behavior or performance guarantee. -/
partial def visit (m : Methods) (g : MVarId) (count : Nat)
    (z1 z2 : Bound) (e1 e2 p1 p2 e : Expr) (tag : Name)
    (finish : MVarId → TacticM Unit) : TacticM Unit := g.withContext do
  if count > 1 then
    let target ← g.getType
    let mid := count / 2
    let z3 := z1.asLower + mid
    let e3 ← m.mkNumeral z3
    let le ← mkAppM ``LE.le #[e3, e]
    let left ← mkFreshExprMVar (← mkArrow (mkNot le) target) .syntheticOpaque
    let right ← mkFreshExprMVar (← mkArrow le target) .syntheticOpaque
    g.assign (← mkAppM ``dite #[le, right, left])
    let (hleft, left) ← left.mvarId!.intro1
    visit m left mid z1 (.lt z3) e1 e3 p1 (.fvar hleft) e tag finish
    let (hright, right) ← right.mvarId!.intro1
    visit m right (count - mid) (.le z3) z2 e3 e2 (.fvar hright) p2 e tag finish
  else if count == 1 then
    let rhs ← m.mkNumeral z1.asLower
    let target ← g.getType
    let leaf ← mkFreshExprMVar (← mkArrow (← mkEq e rhs) target)
      .syntheticOpaque (appendTag tag (.mkSimple (toString z1.asLower)))
    let lower ← match z1 with
      | .le _ => pure p1
      | .lt _ => m.roundUp e1 e rhs p1
    let upper ← match z2 with
      | .le _ => pure p2
      | .lt _ => m.roundDown e e2 rhs p2
    g.assign (.app leaf (← mkAppM ``le_antisymm #[upper, lower]))
    finish leaf.mvarId!
  else
    throwError "interval continuation: empty non-contradictory interval"

/-- Native bound selection with on-demand leaf construction.
A continuation failure propagates; callers own rollback/remaining goals. -/
def split (g : MVarId) (e e' : Expr) (lbs ubs : Array Expr)
    (finish : MVarId → TacticM Unit) : TacticM Unit := g.withContext do
  let type ← whnfR (← inferType e)
  let m ←
    if type.isConstOf ``Nat then pure natMethods
    else if type.isConstOf ``Int then pure intMethods
    else throwError "interval continuation: unsupported type {type}"
  let mut lower ← try? (m.initLB e)
  for proof in lbs do
    if let some bound ← try? (m.getBound e proof true) then
      if lower.all (·.1.asLower < bound.1.asLower) then lower := some bound
  let mut upper ← try? (m.initUB e)
  for proof in ubs do
    if let some bound ← try? (m.getBound e proof false) then
      if upper.all (·.1.asUpper > bound.1.asUpper) then upper := some bound
  match lower, upper with
  | some (z1, e1, p1), some (z2, e2, p2) =>
    if z1.asLower > z2.asUpper then
      (← g.exfalso).assign (← m.inconsistentBounds z1 z2 e1 e2 p1 p2 e)
    else
      visit m g (z2.asUpper - z1.asLower + 1).toNat z1 z2 e1 e2 p1 p2 e (← g.getTag) finish
  | none, _ => throwError "interval continuation: no lower bound on {e'}"
  | _, none => throwError "interval continuation: no upper bound on {e'}"

/-- Experimental syntax: every continuation must close its single leaf.
The original interval_cases syntax and implementation remain untouched. -/
syntax "interval_cases_then " term " => " tacticSeq : tactic

elab_rules : tactic
  | `(tactic| interval_cases_then $term => $continuation) => do
    let saved ← saveState
    try
      let remaining := (← getGoals).tail!
      let original ← getMainGoal
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
          split goal (.fvar x) expression lower upper fun leaf => do
            let (equation, leaf) ← leaf.intro1
            let (_, leaf) ← substCore leaf equation (fvarSubst := subst)
            setGoals [leaf]
            evalTactic continuation
            if !(← getUnsolvedGoals).isEmpty then
              throwError "interval continuation: continuation left unsolved goals"
      setGoals remaining
    catch error =>
      saved.restore
      throw error

end GpuSmt.IntervalContinuation
