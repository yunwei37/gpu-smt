import Mathlib
import ClosedTail

example (n : Nat) (h : n < 3) : n ≤ 2 := by
  interval_cases n <;> omega; exact h
