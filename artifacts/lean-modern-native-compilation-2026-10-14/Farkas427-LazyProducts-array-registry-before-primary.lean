/-
Product preprocessing copied from Mathlib4 Mathlib/Tactic/Linarith/Preprocessing.lean
Copyright (c) 2020 Robert Y. Lewis; Apache 2.0.
Invocation-local resolved application reuse added by gpu-smt.
-/
import Mathlib.Tactic.Linarith.Frontend
import Farkas.Telemetry
import Farkas.Products
import Lean.Meta.CollectMVars

open Lean Meta Qq
open Mathlib.Tactic.Linarith
namespace Farkas427.LazyProducts

private structure Template where
  name : Name
  key : Array Expr
  fn : Expr
  args : Array Expr
  aSlot : Nat
  bSlot : Nat
  conclusion : Expr
private structure Pending where
  id : MVarId
  fn : Expr
  args : Array Expr
private structure Cache where
  templates : Array Template := #[]
  reused : Nat := 0
  built : Nat := 0
  defer : Bool := false
  pending : Array Pending := #[]
  inputMap : Array (Option Expr) := #[]
  realized : Nat := 0

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
      let state := { state with reused := state.reused + 1 }
      if state.defer && !args.any (fun e => e.hasMVar || e.hasLevelMVar) then
        let type := t.conclusion.instantiateRev args
        let hole ← mkFreshExprMVar type .syntheticOpaque
        let pending : Pending := { id := hole.mvarId!, fn := t.fn, args }
        ref.set { state with pending := state.pending.push pending }
        return hole
      ref.set state
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
        let mut conclusion ← inferType fn
        for _ in args do
          conclusion := conclusion.bindingBody!
        let template : Template := { name, key, fn, args, aSlot := ai, bSlot := bi, conclusion }
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

private def productProofs (ref : IO.Ref Cache) (ls : List Expr) : MetaM (List Expr) := do
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
    Farkas.Telemetry.emit <| Farkas.Telemetry.row
      [("ty", "\"product-application\""), ("reused", toString st.reused),
       ("built", toString st.built), ("templates", toString st.templates.size),
       ("input_facts", toString ls.length), ("products", toString products.reduceOption.length)]
  compWithZero.globalize.transform products.reduceOption

private def realize (ref : IO.Ref Cache) (id : MVarId) : MetaM Unit := do
  let st ← ref.get
  for p in st.pending do
    if p.id == id then
      unless (← id.isAssigned) do
        id.assign (mkAppN p.fn p.args)
        ref.modify fun s => { s with realized := s.realized + 1 }
      return

private def realizeAll (ref : IO.Ref Cache) : MetaM Unit := do
  for p in (← ref.get).pending do
    realize ref p.id

private def monoCarrier (ls : List Expr) : MetaM Bool := do
  let mut carrier : Option Expr := none
  for e in ls do
    try
      let ty ← typeOfIneqProof e
      if ty.hasMVar || ty.hasLevelMVar then return false
      match carrier with
      | none => carrier := some ty
      | some t => if t != ty then return false
    catch _ => return false
  return carrier.isSome

/-- Ordinary native preprocessor/oracle pair; private invocation-local holes are
assigned before the unchanged native verifier constructs its final proof. -/
def make : MetaM (GlobalPreprocessor × (CertificateOracle → CertificateOracle)) := do
  let ref ← IO.mkRef ({} : Cache)
  let extra : GlobalPreprocessor := {
    description := "nonlinear arithmetic extras"
    transform := fun ls => do
      let new_es ← squareProofs ls
      ref.set { defer := (← monoCarrier (new_es ++ ls)) }
      let products ← productProofs ref (new_es ++ ls)
      let es := new_es ++ ls ++ products
      let mut indices : Array (Option Expr) := #[none]
      let mut mapped := true
      for e in es do
        try
          let (ineq, _) ← parseCompAndExpr (← inferType e)
          if ineq == .eq then indices := indices.push (some e)
          indices := indices.push (some e)
        catch _ => mapped := false
      ref.modify fun s => { s with inputMap := if mapped then indices else #[] }
      return es }
  let wrap := fun (inner : CertificateOracle) => ({
    produceCertificate := fun hyps maxVar => do
      let cert ← inner.produceCertificate hyps maxVar
      let st ← ref.get
      if !st.pending.isEmpty then
        if st.inputMap.size != hyps.length then
          realizeAll ref
        else
          for (i, _) in cert.toList do
            if let some (some e) := st.inputMap[i]? then
              for id in (← getMVars e) do
                realize ref id
            else if i != 0 then
              realizeAll ref
      if (← IO.getEnv "FARKAS_CORPUS_FILE").isSome then
        let after ← ref.get
        Farkas.Telemetry.emit <| Farkas.Telemetry.row
          [("ty", "\"lazy-products\""), ("deferred", toString after.pending.size),
           ("materialized", toString after.realized),
           ("mapping_entries", toString after.inputMap.size),
           ("oracle_comparisons", toString hyps.length)]
      return cert } : CertificateOracle)
  return (extra, wrap)
end Farkas427.LazyProducts
