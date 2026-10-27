import SharedCNF
set_option trace.Meta.Tactic.sat true

-- Direct core: fallback cannot hide failure or bypass engagement.
theorem sharedDistrib (x y z : BitVec 4) :
    x * (y + z) = x * y + x * z := by
  bv_decide_shared_core

-- Public opt-in form with preserved native config parser.
theorem publicDistrib (x y z : BitVec 4) :
    x * (y + z) = x * y + x * z := by
  bv_decide_shared (timeout := 10)

-- Restore after native proof construction and deliberately fail this branch.
theorem backtrackDistrib (x y z : BitVec 4) :
    x * (y + z) = x * y + x * z := by
  first
  | bv_decide_shared_core
    fail "deliberate backtracking control"
  | bv_decide

#print axioms sharedDistrib
#print axioms publicDistrib
#print axioms backtrackDistrib
