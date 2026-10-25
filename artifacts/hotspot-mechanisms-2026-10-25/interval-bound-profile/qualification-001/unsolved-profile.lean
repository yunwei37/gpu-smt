import Mathlib
import IntervalProfile

example (n : Nat) (h : n < 3) : n ≤ 2 := by
  profile_interval_cases interval_cases n <;> skip
