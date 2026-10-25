/-
Copyright (c) 2026 gpu-smt contributors.
Released under Apache 2.0 license as described in LICENSE.
Diagnostic bound inspection uses the pinned Mathlib interval_cases Methods.
-/
import Mathlib.Tactic.IntervalCases
open Lean Meta Elab Tactic Mathlib.Tactic.IntervalCases
namespace GpuSmt.IntervalProfile

/-- Inspect native bounds in a restored state, without constructing leaves.
A large cardinality is not a timeout proof. Missing bounds remain unknown. -/
private def inspect (term : Syntax) : TacticM Json := withMainContext do
  let original ← getMainGoal
  let expression ← Tactic.elabTerm term none
  let (subst, xs, goal) ←
    original.generalizeHyp #[{ expr := expression }] (← getFVarIdsAt original)
  goal.withContext do
    let x := xs[0]!
    let expression := subst.apply expression
    let type ← whnfR (← inferType (.fvar x))
    let methods ←
      if type.isConstOf `Nat then pure natMethods
      else if type.isConstOf `Int then pure intMethods
      else throwError "interval profile: unsupported type"
    let mut lower ← try? (methods.initLB (.fvar x))
    let mut upper ← try? (methods.initUB (.fvar x))
    let mut boundHypotheses : Array Json := #[]
    for declaration in ← getLCtx do
      try
        let (lo, hi, _) ← parseBound declaration.type
        let lower? ← withNewMCtxDepth <| withReducible <| isDefEq (.fvar x) hi
        let upper? ← withNewMCtxDepth <| withReducible <| isDefEq (.fvar x) lo
        if lower? then
          if let some bound ← try? (methods.getBound (.fvar x) (.fvar declaration.fvarId) true) then
            boundHypotheses := boundHypotheses.push <| Json.mkObj [
              ("name", toJson declaration.userName.toString), ("direction", toJson ("lower" : String)),
              ("inclusive_value", toJson (toString bound.1.asLower))]
            if lower.all (·.1.asLower < bound.1.asLower) then lower := some bound
        else if upper? then
          if let some bound ← try? (methods.getBound (.fvar x) (.fvar declaration.fvarId) false) then
            boundHypotheses := boundHypotheses.push <| Json.mkObj [
              ("name", toJson declaration.userName.toString), ("direction", toJson ("upper" : String)),
              ("inclusive_value", toJson (toString bound.1.asUpper))]
            if upper.all (·.1.asUpper > bound.1.asUpper) then upper := some bound
      catch _ => pure ()
    let cardinality := match lower, upper with
      | some lo, some hi => some ((hi.1.asUpper - lo.1.asLower + 1).toNat)
      | _, _ => none
    return Json.mkObj [
      ("term", toJson (expression.getAppFn.constName?.map toString)),
      ("native_type", toJson (type.getAppFn.constName?.map toString)),
      ("lower", toJson (lower.map fun lo => toString lo.1.asLower)),
      ("upper", toJson (upper.map fun hi => toString hi.1.asUpper)),
      ("cardinality", toJson cardinality),
      ("bound_hypotheses", toJson boundHypotheses),
      ("leaves_constructed_by_inspector", toJson (0 : Nat)),
      ("certified_failure", toJson false), ("certified_timeout", toJson false)]

syntax (name := gpuSmtProfileInterval) "profile_interval_cases " tactic:2 : tactic
elab_rules : tactic
  | `(tactic| profile_interval_cases $inner:tactic) => do
    let saved ← saveState
    let invocation := inner.raw.getPos?.map (·.byteIdx)
    let started ← IO.monoNanosNow
    let detail ← try
      match inner with
      | `(tactic| interval_cases $term:term) => inspect term
      | _ => pure <| Json.mkObj [("unsupported_syntax", toJson true)]
    catch error =>
      pure <| Json.mkObj [("inspection_error", toJson (← error.toMessageData.toString))]
    saved.restore
    IO.eprintln <| "[gpu-smt-interval-stage] " ++ (Json.mkObj [
      ("event", toJson ("before-native-expansion" : String)),
      ("invocation_byte", toJson invocation), ("detail", detail),
      ("inspection_ns", toJson ((← IO.monoNanosNow) - started))]).compress
    let nativeStart ← IO.monoNanosNow
    try
      evalTactic inner
    finally
      IO.eprintln <| "[gpu-smt-interval-stage] " ++ (Json.mkObj [
        ("event", toJson ("native-return-or-unwind" : String)),
        ("invocation_byte", toJson invocation),
        ("elapsed_ns", toJson ((← IO.monoNanosNow) - nativeStart))]).compress
end GpuSmt.IntervalProfile
