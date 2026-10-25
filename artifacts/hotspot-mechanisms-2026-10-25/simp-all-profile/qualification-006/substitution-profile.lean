import Mathlib
import SimpAllProfile

example (n : Nat) (h : n = 3) : n + 1 = 4 := by
  profile_simp_all simp_all
