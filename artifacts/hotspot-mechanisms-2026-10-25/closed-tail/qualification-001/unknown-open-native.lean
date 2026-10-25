import Mathlib
import ClosedTail

example (p : Prop) (hp : p) : p := by
  skip; exact hp
