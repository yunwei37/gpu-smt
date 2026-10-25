import Mathlib
import IntervalContinuation

example (n : Nat) (h : n < 3) : False := by
  interval_cases n <;> omega
