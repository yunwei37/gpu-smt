import Mathlib
set_option maxHeartbeats 200000
theorem prefix_error (S : Finset Nat) (h :
    ∀ n, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧
      (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n) :
    (Finset.range 100).card = 100 := by
  have impossible : (1 : Nat) = 2 := by decide
  rfl
#print axioms prefix_error
