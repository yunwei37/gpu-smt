import CnfBridge
import Lean
open Std.Sat
open Std.Tactic.BVDecide
open GpuSmt.CnfBridge

def contradiction : CNF Nat := [[(0, true)], [(0, false)]]
def validCert : String := "3 0 1 2 0\n"

#guard Reflect.verifyCert contradiction validCert
#guard !(Reflect.verifyCert ([] : CNF Nat) validCert)
#guard !(Reflect.verifyCert contradiction "")
#guard !(Reflect.verifyCert contradiction "not an LRAT certificate")
#guard !(Reflect.verifyCert ([[(0, true)]] : CNF Nat) validCert)

theorem checkedContradiction : contradiction.Unsat :=
  Reflect.verifyCert_correct contradiction validCert (by native_decide)

-- Generic correspondence and native check transfer: no trusted host formula.
example (bv : BVLogicalExpr) (cnf : CNF Nat) (cert : String)
    (same : cnf = cnfOf bv)
    (checked : Reflect.verifyCert cnf cert = true) : bv.Unsat :=
  unsat_of_checked_cnf bv cnf cert same checked

#print axioms GpuSmt.CnfBridge.unsat_of_checked_cnf
#print axioms checkedContradiction
