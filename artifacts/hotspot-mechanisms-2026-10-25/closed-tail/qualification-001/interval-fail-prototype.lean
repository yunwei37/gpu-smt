import Mathlib
import ClosedTail

example (n : Nat) (h : n < 3) : False := by
  early_fail_tail { interval_cases n <;> omega; exact h }
