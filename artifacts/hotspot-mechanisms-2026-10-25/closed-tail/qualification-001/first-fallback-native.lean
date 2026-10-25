import Mathlib
import ClosedTail

example (n : Nat) (h : n = n) : n = n := by
  first | (omega; exact h) | exact h
