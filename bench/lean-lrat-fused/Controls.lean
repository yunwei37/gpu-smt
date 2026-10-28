import FusedFrontend
set_option trace.Meta.Tactic.sat true

open Std.Sat Std.Tactic.BVDecide
open GpuSmt.FusedLRAT

def contradictory : CNF Nat := [[(0,true)],[(0,false)]]

example : check #[LRAT.Action.addEmpty 3 #[1,2]] contradictory = true := by
  native_decide
example : check #[] contradictory = false := by native_decide
example : check #[LRAT.Action.addEmpty 3 #[99]] contradictory = false := by
  native_decide
example : check #[LRAT.Action.addRup 3 #[0] #[],
    LRAT.Action.del #[], LRAT.Action.addEmpty 4 #[1,2]] contradictory = true := by
  native_decide
example : check #[LRAT.Action.addRat 3 #[1] (1,false) #[] #[],
    LRAT.Action.addEmpty 4 #[1,2]] contradictory = true := by native_decide
example : check #[LRAT.Action.del #[1],
    LRAT.Action.addEmpty 3 #[1,2]] contradictory = false := by native_decide
example : check #[LRAT.Action.addEmpty 3 #[1,2],
    LRAT.Action.addEmpty 4 #[99]] contradictory = true := by native_decide

theorem fused_multiply (x y : BitVec 4) : x * (y + 1) = x * y + x := by
  bv_decide_fused
theorem native_multiply (x y : BitVec 4) : x * (y + 1) = x * y + x := by
  bv_decide
theorem configured (x y : BitVec 4) : x * (y + 1) = x * y + x := by
  bv_decide_fused +acNf +shortCircuit

#print axioms GpuSmt.FusedLRAT.check_eq_native
#print axioms GpuSmt.FusedLRAT.verifyBVExpr_eq_native
#print axioms fused_multiply
#print axioms native_multiply
