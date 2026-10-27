import CnfBridge
import Lean
open Std.Sat
open Std.Tactic.BVDecide

-- Expected native failure: no proof can be fabricated from the empty certificate.
example : CNF.Unsat ([[ (0, true) ]] : CNF Nat) :=
  Reflect.verifyCert_correct _ "" (by native_decide)
