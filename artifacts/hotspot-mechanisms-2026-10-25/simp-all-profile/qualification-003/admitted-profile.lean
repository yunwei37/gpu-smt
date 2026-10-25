import Mathlib
import SimpAllProfile

example (p : Prop) : p := by
  try profile_simp_all simp_all
  sorry
