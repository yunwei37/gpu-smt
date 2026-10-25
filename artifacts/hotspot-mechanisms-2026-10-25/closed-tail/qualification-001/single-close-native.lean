import Mathlib
import ClosedTail

example (n : Nat) (h : n = n) : n = n := by
  omega; exact h
