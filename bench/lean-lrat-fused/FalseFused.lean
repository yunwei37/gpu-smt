import FusedFrontend
example (x : BitVec 4) : x * x = x := by bv_decide_fused
