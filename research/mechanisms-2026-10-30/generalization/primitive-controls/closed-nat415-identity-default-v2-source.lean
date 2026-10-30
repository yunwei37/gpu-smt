import ClosedNatFacts
set_option maxHeartbeats 200000
theorem odd_identity : Finset.prod (Finset.filter (fun k : Nat => ¬Even k) (Finset.range 10000)) id =
 Nat.factorial 10000 / ((2 : Nat)^5000 * Nat.factorial 5000) := by
 rw [MClosedNat.odd_10000, MClosedNat.fac_10000, MClosedNat.fac_5000, MClosedNat.pow_2_5000] <;> decide
#print axioms odd_identity
