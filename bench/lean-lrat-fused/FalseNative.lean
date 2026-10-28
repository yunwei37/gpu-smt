import Lean.Elab.Tactic.BVDecide
example (x : BitVec 4) : x * x = x := by bv_decide
