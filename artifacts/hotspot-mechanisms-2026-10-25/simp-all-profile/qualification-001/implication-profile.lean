import Mathlib
import SimpAllProfile

example (p q : Prop) (hp : p) (hpq : p → q) : q := by
  profile_simp_all simp_all
