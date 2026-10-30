import Lean

/-- Counterexample to the auxiliary i≤40 assertion in minif2f-4997,
not a counterexample to the theorem's final i+m+o≤671 conclusion. -/
theorem auxiliary_bound_counterexample :
    (667 : Nat) ≠ 3 ∧ (3 : Nat) ≠ 1 ∧ (1 : Nat) ≠ 667 ∧
    (667 : Nat) * 3 * 1 = 2001 ∧ ¬(667 : Nat) ≤ 40 ∧
    (667 : Nat) + 3 + 1 = 671 := by decide

#print axioms auxiliary_bound_counterexample
