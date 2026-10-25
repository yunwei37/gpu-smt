import Mathlib
import ClosedTail

example (p : Prop) (hp : p) : p := by
  early_fail_tail { skip; exact hp }
