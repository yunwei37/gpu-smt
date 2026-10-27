import SharedCNF
example (x : BitVec 4) : x * x = x := by
  bv_decide
