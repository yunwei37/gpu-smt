import Mathlib
import SimpAllProfile

example (n : Nat) (h : n = 3) : n + 1 = 4 := by
  simp_all
