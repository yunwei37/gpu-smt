import Mathlib
import ClosedTail

example (n : Nat) (h : n = n) : n = n := by
  early_fail_tail { interval_cases n <;> omega; exact h }
