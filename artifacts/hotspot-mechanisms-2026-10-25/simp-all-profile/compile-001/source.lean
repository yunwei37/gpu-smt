/-
Copyright (c) 2021 Microsoft Corporation. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Leonardo de Moura
-/
import Lean.Meta.Tactic.Clear
import Lean.Meta.Tactic.Util
import Lean.Elab.Tactic.Simp

namespace GpuSmt.SimpAllProfile
open Lean Meta

open Simp (Stats SimprocsArray)

namespace SimpAll

structure Entry where
  fvarId   : FVarId -- original fvarId
  userName : Name
  id       : Origin -- id of the theorem at `SimpTheorems`
  origType : Expr
  type     : Expr
  proof    : Expr
  deriving Inhabited

structure State where
  profileRound : Nat := 0
  hypothesisUpdates : Nat := 0
  modified     : Bool := false
  mvarId       : MVarId
  entries      : Array Entry := #[]
  ctx          : Simp.Context
  simprocs     : SimprocsArray
  usedTheorems : Simp.UsedSimps := {}
  diag         : Simp.Diagnostics := {}

abbrev M := StateRefT State MetaM

/-- Diagnostic wrapper only: no rejection, caching or rewrite change.
Hashes below are hints for investigation, never equality/cycle witnesses. -/
private def timed (phase : String) (slot : Nat) (action : M α) : M α := do
  let start ← IO.monoNanosNow
  try
    action
  finally
    let elapsed := (← IO.monoNanosNow) - start
    let state ← get
    IO.eprintln <| "[gpu-smt-simp-stage] " ++ (Json.mkObj [
      ("phase", toJson phase), ("round", toJson state.profileRound),
      ("slot", toJson slot), ("elapsed_ns", toJson elapsed.toNat),
      ("entries", toJson state.entries.size),
      ("hypothesis_updates", toJson state.hypothesisUpdates),
      ("entry_type_hashes", toJson (state.entries.map fun e => (hash e.type).toNat))
    ]).compress

private def initEntries : M Unit := do
  let hs ←  (← get).mvarId.withContext do getPropHyps
  let hsNonDeps ← (← get).mvarId.getNondepPropHyps
  let mut simpThms := (← get).ctx.simpTheorems
  for h in hs do
    unless simpThms.isErased (.fvar h) do
      let localDecl ← h.getDecl
      let proof  := localDecl.toExpr
      simpThms ← simpThms.addTheorem (.fvar h) proof
      modify fun s => { s with ctx.simpTheorems := simpThms }
      if hsNonDeps.contains h then
        -- We only simplify nondependent hypotheses
        let type ← instantiateMVars localDecl.type
        let entry : Entry := { fvarId := h, userName := localDecl.userName, id := .fvar h, origType := type, type, proof }
        modify fun s => { s with entries := s.entries.push entry }

private abbrev getSimpTheorems : M SimpTheoremsArray :=
  return (← get).ctx.simpTheorems

private partial def loop : M Bool := do
  modify fun s => { s with modified := false, profileRound := s.profileRound + 1 }
  let simprocs := (← get).simprocs
  -- simplify entries
  for i in [:(← get).entries.size] do
    let entry := (← get).entries[i]!
    let ctx := (← get).ctx
    -- We disable the current entry to prevent it to be simplified to `True`
    let simpThmsWithoutEntry := (← getSimpTheorems).eraseTheorem entry.id
    let ctx := { ctx with simpTheorems := simpThmsWithoutEntry }
    let (r, stats) ← timed "hypothesis" i do
      simpStep (← get).mvarId entry.proof entry.type ctx simprocs (stats := { (← get) with })
    modify fun s => { s with usedTheorems := stats.usedTheorems, diag := stats.diag }
    match r with
    | none => return true -- closed the goal
    | some (proofNew, typeNew) =>
      unless typeNew == entry.type do
        /- We must erase the `id` for the simplified theorem. Otherwise,
           the previous versions can be used to self-simplify the new version. For example, suppose we have
           ```
            x : Nat
            h : x ≠ 0
            ⊢ Unit
           ```
           In the first round, `h : x ≠ 0` is simplified to `h : ¬ x = 0`.

           It is also important for avoiding identical hypotheses to simplify each other to `True`.
           Example
           ```
           ...
           h₁ : p a
           h₂ : p a
           ⊢ q a
           ```
           `h₁` is first simplified to `True`. If we don't remove `h₁` from the set of simp theorems, it will
           be used to simplify `h₂` to `True` and information is lost.

           We must use `mkExpectedTypeHint` because `inferType proofNew` may not be equal to `typeNew` when
           we have theorems marked with `rfl`.
        -/
        trace[Meta.Tactic.simp.all] "entry.id: {← ppOrigin entry.id}, {entry.type} => {typeNew}"
        let mut simpThmsNew := (← getSimpTheorems).eraseTheorem (.fvar entry.fvarId)
        let idNew ← mkFreshId
        simpThmsNew ← simpThmsNew.addTheorem (.other idNew) (← mkExpectedTypeHint proofNew typeNew)
        modify fun s => { s with
          modified         := true
          hypothesisUpdates := s.hypothesisUpdates + 1
          ctx.simpTheorems := simpThmsNew
          entries[i]       := { entry with type := typeNew, proof := proofNew, id := .other idNew }
        }
  -- simplify target
  let mvarId := (← get).mvarId
  let (r, stats) ← timed "target" 0 do
    simpTarget mvarId (← get).ctx simprocs (stats := { (← get) with })
  modify fun s => { s with usedTheorems := stats.usedTheorems, diag := stats.diag }
  match r with
  | none => return true
  | some mvarIdNew =>
    unless mvarId == mvarIdNew do
      modify fun s => { s with
        modified := true
        mvarId   := mvarIdNew
      }
  if (← get).modified then
    loop
  else
    return false

def main : M (Option MVarId) := do
  timed "initialize" 0 initEntries
  if (← loop) then
    return none -- close the goal
  else
    let mvarId := (← get).mvarId
    -- Prior to #2334, the logic here was to re-assert all hypotheses and call `tryClearMany` on them all.
    -- This had the effect that the order of hypotheses was sometimes modified, whether or not any where simplified.
    -- Now we only re-assert the first modified hypothesis,
    -- along with all subsequent hypotheses, so as to preserve the order of hypotheses.
    let mut toAssert := #[]
    let mut toClear := #[]
    let mut modified := false
    for e in (← get).entries do
      if e.type.isTrue then
        -- Do not assert `True` hypotheses
        toClear := toClear.push e.fvarId
      else if modified || e.type != e.origType then
        toClear := toClear.push e.fvarId
        toAssert := toAssert.push { userName := e.userName, type := e.type, value := e.proof }
        modified := true
    let (_, mvarId) ← mvarId.assertHypotheses toAssert
    mvarId.tryClearMany toClear

end SimpAll

def simpAll (mvarId : MVarId) (ctx : Simp.Context) (simprocs : SimprocsArray := #[]) (stats : Stats := {}) : MetaM (Option MVarId × Stats) := do
  mvarId.withContext do
    let (r, s) ← SimpAll.main.run { stats with mvarId, ctx, simprocs }
    if let .some mvarIdNew := r then
      if ctx.config.failIfUnchanged && mvarId == mvarIdNew then
        throwError "simp_all made no progress"
    return (r, { s with })

builtin_initialize
  registerTraceClass `Meta.Tactic.simp.all

end GpuSmt.SimpAllProfile


open Lean Meta Elab Tactic

/-- Opt-in profiling of the pinned native simp_all algorithm.
It observes phase costs; it never declares a cycle or returns early. -/
syntax "profile_simp_all " tactic : tactic

elab_rules : tactic
  | `(tactic| profile_simp_all $inner:tactic) => withMainContext do
    unless inner.raw.isOfKind ``Lean.Parser.Tactic.simpAll do
      throwError "profile_simp_all expects one simp_all invocation"
    withSimpDiagnostics do
      let { ctx, simprocs, .. } ← mkSimpContext inner (eraseLocal := true)
        (kind := .simpAll) (ignoreStarArg := true)
      let (result?, stats) ← GpuSmt.SimpAllProfile.simpAll (← getMainGoal) ctx
        (simprocs := simprocs)
      match result? with
      | none => replaceMainGoal []
      | some goal => replaceMainGoal [goal]
      if tactic.simp.trace.get (← getOptions) then
        traceSimpCall inner stats.usedTheorems
      return stats.diag
