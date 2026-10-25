import Mathlib
import SimpAllProfile

example (n : Int) (h : n = 0) : n % 3 = 0 := by
  profile_simp_all simp_all
