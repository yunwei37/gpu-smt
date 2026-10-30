import ClosedNatMethods
set_option maxHeartbeats 200000
theorem negative : Nat.factorial 942 % (15^234) = 0 := by m_closed_nat_rfl
#print axioms negative
