/-
Experimental fused LRAT action conversion/checking.
Based on the pinned Std checker, Copyright Amazon.com, Inc. or its affiliates,
and Copyright (c)2024 Lean FRO,LLC. Apache-2.0.
The stock RUP/RAT formula operations and checker truth are unchanged.
-/
import Std.Tactic.BVDecide.LRAT.Checker
import Std.Tactic.BVDecide.Reflect

open Std.Sat Std.Tactic.BVDecide
open Std.Tactic.BVDecide.LRAT.Internal

namespace GpuSmt.FusedLRAT

/-- Exactly the native conversion/filter,including skipped malformed actions. -/
def prepare (n : Nat) (input : LRAT.IntAction) : Option (DefaultClauseAction n) :=
  match intActionToDefaultClauseAction n input with
  | none => none
  | some (.addEmpty id hints) => some (.addEmpty id hints)
  | some (.addRup id clause hints) => some (.addRup id clause hints)
  | some (.del ids) => some (.del ids)
  | some (.addRat id clause pivot rup rat) =>
    if pivot ∈ Clause.toList clause then some (.addRat id clause pivot rup rat)
    else none

/-- Convert only the next action required by the unchanged sequential checker. -/
def run {n : Nat} (formula : DefaultFormula n) : List LRAT.IntAction → Result
  | [] => .outOfProof
  | action :: rest =>
    match prepare n action with
    | none => run formula rest
    | some (.addEmpty _ hints) =>
      let (_, success) := Formula.performRupAdd formula Clause.empty hints
      if success then .success else .rupFailure
    | some (.addRup _ clause hints) =>
      let (formula, success) := Formula.performRupAdd formula clause hints
      if success then run formula rest else .rupFailure
    | some (.addRat _ clause pivot rup rat) =>
      let (formula, success) := Formula.performRatAdd formula clause pivot rup rat
      if success then run formula rest else .rupFailure
    | some (.del ids) => run (Formula.delete formula ids) rest

theorem run_eq_native {n : Nat} (formula : DefaultFormula n)
    (actions : List LRAT.IntAction) :
    run formula actions = lratChecker formula (actions.filterMap (prepare n)) := by
  induction actions generalizing formula with
  | nil => rfl
  | cons action rest ih =>
    cases converted : prepare n action with
    | none => simpa [run, converted] using ih formula
    | some output =>
      cases output with
      | addEmpty id hints => simp [run, converted, lratChecker]
      | addRup id clause hints =>
        simp only [run, converted, List.filterMap_cons, lratChecker]
        split <;> simp_all
      | addRat id clause pivot rup rat =>
        simp only [run, converted, List.filterMap_cons, lratChecker]
        split <;> simp_all
      | del ids => simpa [run, converted, lratChecker] using ih (Formula.delete formula ids)

/-- The parsed input and CNF conversion are stock;only intermediate lists fuse. -/
def check (actions : Array LRAT.IntAction) (cnf : CNF Nat) : Bool :=
  run (CNF.convertLRAT cnf) actions.toList = .success

theorem check_eq_native (actions : Array LRAT.IntAction) (cnf : CNF Nat) :
    check actions cnf = LRAT.check actions cnf := by
  unfold check LRAT.check
  rw [run_eq_native]
  simp only [List.filterMap_map, Function.comp_def]
  congr 3
  apply congrArg (fun convert => List.filterMap convert actions.toList)
  funext action
  cases converted : intActionToDefaultClauseAction (cnf.numLiterals + 1) action with
  | none => simp [prepare, converted]
  | some output => cases output <;> simp [prepare, converted]

def verifyBVExpr (bv : BVLogicalExpr) (certificate : String) : Bool :=
  let cnf := AIG.toCNF bv.bitblast.relabelNat
  match LRAT.parseLRATProof certificate.toUTF8 with
  | .ok actions => check actions cnf
  | .error _ => false

theorem verifyBVExpr_eq_native (bv : BVLogicalExpr) (certificate : String) :
    verifyBVExpr bv certificate = Reflect.verifyBVExpr bv certificate := by
  unfold verifyBVExpr Reflect.verifyBVExpr Reflect.verifyCert
  split <;> simp_all [check_eq_native]

theorem unsat_of_checked (bv : BVLogicalExpr) (certificate : String)
    (checked : verifyBVExpr bv certificate = true) : bv.Unsat := by
  apply Reflect.unsat_of_verifyBVExpr_eq_true bv certificate
  rw [← verifyBVExpr_eq_native]
  exact checked

end GpuSmt.FusedLRAT
