import ClosedNatMethods
set_option maxHeartbeats 200000
theorem positive : Nat.factorial 942 % (15^233) = 0 := by m_closed_nat_rfl
#print axioms positive
