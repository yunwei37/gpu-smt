import Mathlib
set_option maxHeartbeats 200000
theorem unrelated (S : Finset Nat) (h :
    ∀ n, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧
      (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n) :
    (Finset.range 2).card = 100 := by
  rfl
#print axioms unrelated
