import Mathlib
import SimpAllProfile

example (n : Nat) : n = n := by
  first | simp_all only | rfl
