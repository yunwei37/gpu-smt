import CnfBridge
open Std.Sat
open Std.Tactic.BVDecide
open GpuSmt.CnfBridge

-- Expected native failure: an unrelated formula cannot supply correspondence.
example (bv : BVLogicalExpr) (cnf : CNF Nat) (cert : String)
    (checked : Reflect.verifyCert cnf cert = true) : bv.Unsat :=
  unsat_of_checked_cnf bv cnf cert (by rfl) checked
