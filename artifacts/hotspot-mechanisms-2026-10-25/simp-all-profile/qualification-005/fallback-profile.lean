import Mathlib
import SimpAllProfile

example (n : Nat) : n = n := by
  first | profile_simp_all simp_all only | rfl
