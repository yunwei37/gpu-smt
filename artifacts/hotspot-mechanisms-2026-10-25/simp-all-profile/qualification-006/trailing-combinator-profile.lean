import Mathlib
import SimpAllProfile

example (n : Nat) (h : n = 0) : n = 0 := by
  profile_simp_all simp_all <;> rfl
