import Mathlib
import IntervalProfile

example (n : Nat) (h : n < 4) : n ≤ 3 := by
  profile_interval_cases interval_cases n <;> omega
