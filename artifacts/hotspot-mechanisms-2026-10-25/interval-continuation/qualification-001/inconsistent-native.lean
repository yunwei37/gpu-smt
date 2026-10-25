import Mathlib
import IntervalContinuation

example (n : Nat) (lo : 5 ≤ n) (hi : n < 4) : False := by
  interval_cases n
