/- Generic experimental proof contract. Actual qualification is linked from README.md.
   No physical sharing, tactic hook, GPU implementation or performance claim. -/
import Std.Tactic.BVDecide.Reflect

open Std.Sat
open Std.Tactic.BVDecide

namespace GpuSmt.CnfBridge

-- A closed generated definition of this expression could be consumed by both
-- the existing SAT frontend and the unchanged native certificate checker.
def cnfOf (bv : BVLogicalExpr) : CNF Nat :=
  AIG.toCNF bv.bitblast.relabelNat

-- Supplying a host-side CNF is insufficient: its correspondence to the exact
-- reflected expression and the original checked certificate are both required.
theorem unsat_of_checked_cnf
    (bv : BVLogicalExpr) (cnf : CNF Nat) (certificate : String)
    (cnf_eq : cnf = cnfOf bv)
    (checked : Reflect.verifyCert cnf certificate = true) : bv.Unsat := by
  apply Reflect.unsat_of_verifyBVExpr_eq_true bv certificate
  change Reflect.verifyCert (cnfOf bv) certificate = true
  rw [← cnf_eq]
  exact checked

end GpuSmt.CnfBridge
