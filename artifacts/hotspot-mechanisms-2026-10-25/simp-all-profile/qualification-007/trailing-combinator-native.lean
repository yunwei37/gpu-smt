import Mathlib
import SimpAllProfile

example (n : Nat) (h : n = 0) : n = 0 := by
  simp_all <;> rfl
