import Mathlib
import SimpAllProfile

example (p q : Prop) (hp : p) (hpq : p → q) : q := by
  simp_all
