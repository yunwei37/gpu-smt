import Mathlib
import ClosedTail

example (n : Nat) (h : n = n) : n = n := by
  interval_cases n <;> omega; exact h
