/- gpu-smt reproduction snapshot; local Lean4.27 adaptation/reduced diagnostic implementation. See ../../PROVENANCE.md. -/
import GpuArithmetic.CostTelemetry
/-
Product preprocessing copied from Mathlib4 Mathlib/Tactic/Linarith/Preprocessing.lean
Copyright (c) 2020 Robert Y. Lewis; Apache 2.0.
Invocation-local resolved application reuse added by gpu-smt.
-/
import Mathlib.Tactic.Linarith.Frontend
import Farkas.Telemetry
import GpuArithmetic.CostStages

open Lean Meta Qq
open Mathlib.Tactic.Linarith
namespace GpuArithmetic.CostProducts

private structure Template where
  name : Name
  key : Array Expr
  fn : Expr
  args : Array Expr
  aSlot : Nat
  bSlot : Nat
private structure Cache where
  templates : Array Template := #[]
  reused : Nat := 0
  built : Nat := 0

private def relationKey (tp : Expr) : Expr :=
  let fn := tp.getAppFn
  let args := tp.getAppArgs
  mkAppN fn (args.extract 0 (args.size - 2))

private def applyProduct (ref : IO.Ref Cache) (name : Name) (a b : Expr) : MetaM Expr := do
  let ta ← inferType a
  let tb ← inferType b
  let (_, _, ax, az) ← ta.ineq?
  let (_, _, bx, bz) ← tb.ineq?
  let key := #[relationKey ta, relationKey tb, az, bz]
  let state ← ref.get
  for t in state.templates do
    if t.name == name && t.key == key then
      let args := ((t.args.set! t.aSlot ax).set! t.bSlot bx)
      let args := (args.set! (args.size-2) a).set! (args.size-1) b
      ref.set { state with reused := state.reused + 1 }
      return mkAppN t.fn args
  let pf ← mkAppM name #[a, b]
  let fn := pf.getAppFn
  let args := pf.getAppArgs
  let mut ty := (← getConstInfo name).type
  let mut names : Array Name := #[]
  while ty.isForall do
    names := names.push ty.bindingName!
    ty := ty.bindingBody!
  let aSlot := names.findIdx? (· == `a)
  let bSlot := names.findIdx? (· == `b)
  let state ← ref.get
  let state := { state with built := state.built + 1 }
  if let some ai := aSlot then
    if let some bi := bSlot then
      if names.size == args.size && args.size ≥ 4 &&
          ai < args.size-2 && bi < args.size-2 &&
          args[ai]! == ax && args[bi]! == bx &&
          args[args.size-2]! == a && args[args.size-1]! == b &&
          !fn.hasLevelMVar && !args.any (fun e => e.hasMVar || e.hasLevelMVar) then
        let template : Template := { name, key, fn, args, aSlot := ai, bSlot := bi }
        ref.set { state with templates := state.templates.push template }
        return pf
  ref.set state
  return pf

private def squareProofs (ls : List Expr) : MetaM (List Expr) := do
  let s ← Mathlib.Tactic.AtomM.run .reducible do
    let si ← ls.foldrM (fun h s' => do findSquares s' (← instantiateMVars (← inferType h))) ∅
    si.toList.mapM fun (i, is_sq) => return ((← get).atoms[i]!, is_sq)
  let new_es ← s.filterMapM fun (e, is_sq) =>
    observing? <| mkAppM (if is_sq then ``sq_nonneg else ``mul_self_nonneg) #[e]
  compWithZero.globalize.transform new_es

private def productProofs (cost : IO.Ref GpuArithmetic.CostStages.Costs) (ls : List Expr) : MetaM (List Expr) := do
  let ref ← IO.mkRef ({} : Cache)
  let with_comps ← ls.mapM (fun e => do
    let tp ← inferType e
    try
      let ⟨ine, _⟩ ← parseCompAndExpr tp
      pure (ine, e)
    catch _ => pure (Mathlib.Ineq.lt, e))
  let products ← with_comps.mapDiagM fun (⟨posa, a⟩ : Mathlib.Ineq × Expr) ⟨posb, b⟩ =>
    try
      (some <$> match posa, posb with
        | .eq, _ => applyProduct ref ``zero_mul_eq a b
        | _, .eq => applyProduct ref ``mul_zero_eq a b
        | .lt, .lt => applyProduct ref ``mul_pos_of_neg_of_neg a b
        | .lt, .le => do
            let a ← mkAppM ``le_of_lt #[a]
            applyProduct ref ``mul_nonneg_of_nonpos_of_nonpos a b
        | .le, .lt => do
            let b ← mkAppM ``le_of_lt #[b]
            applyProduct ref ``mul_nonneg_of_nonpos_of_nonpos a b
        | .le, .le => applyProduct ref ``mul_nonneg_of_nonpos_of_nonpos a b)
    catch _ => pure none
  if (← IO.getEnv "FARKAS_CORPUS_FILE").isSome then
    let st ← ref.get
    pure ()
  let normalized ← compWithZero.globalize.transform products.reduceOption
  GpuArithmetic.CostStages.registerProducts cost normalized
  return normalized

def extras (cost : IO.Ref GpuArithmetic.CostStages.Costs) : GlobalPreprocessor where
  description := "nonlinear arithmetic extras"
  transform ls := do
    let new_es ← squareProofs ls
    let products ← productProofs cost (new_es ++ ls)
    return new_es ++ ls ++ products
private def stockProductProofs (cost : IO.Ref GpuArithmetic.CostStages.Costs) (ls : List Expr) : MetaM (List Expr) :=
  withTraceNode `linarith (return m!"{exceptEmoji ·} adding product terms") do
  let with_comps ← ls.mapM (fun e => do
    let tp ← inferType e
    try
      let ⟨ine, _⟩ ← parseCompAndExpr tp
      pure (ine, e)
    catch _ => pure (Mathlib.Ineq.lt, e))
  let products ← with_comps.mapDiagM fun (⟨posa, a⟩ : Mathlib.Ineq × Expr) ⟨posb, b⟩ =>
    try
      (some <$> match posa, posb with
        | Mathlib.Ineq.eq, _ => mkAppM ``zero_mul_eq #[a, b]
        | _, Mathlib.Ineq.eq => mkAppM ``mul_zero_eq #[a, b]
        | Mathlib.Ineq.lt, Mathlib.Ineq.lt => mkAppM ``mul_pos_of_neg_of_neg #[a, b]
        | Mathlib.Ineq.lt, Mathlib.Ineq.le => do
            let a ← mkAppM ``le_of_lt #[a]
            mkAppM ``mul_nonneg_of_nonpos_of_nonpos #[a, b]
        | Mathlib.Ineq.le, Mathlib.Ineq.lt => do
            let b ← mkAppM ``le_of_lt #[b]
            mkAppM ``mul_nonneg_of_nonpos_of_nonpos #[a, b]
        | Mathlib.Ineq.le, Mathlib.Ineq.le => mkAppM ``mul_nonneg_of_nonpos_of_nonpos #[a, b])
    catch _ => pure none
  let normalized ← compWithZero.globalize.transform products.reduceOption
  GpuArithmetic.CostStages.registerProducts cost normalized
  return normalized


def stockExtras (cost : IO.Ref GpuArithmetic.CostStages.Costs) : GlobalPreprocessor where
  description := "nonlinear arithmetic extras"
  transform ls := do
    let new_es ← squareProofs ls
    let products ← stockProductProofs cost (new_es ++ ls)
    GpuArithmetic.CostStages.registerProducts cost products
    return new_es ++ ls ++ products
end GpuArithmetic.CostProducts
