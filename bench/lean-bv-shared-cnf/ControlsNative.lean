import SharedCNF
theorem nativeDistrib (x y z : BitVec 4) :
    x * (y + z) = x * y + x * z := by
  bv_decide
#print axioms nativeDistrib
