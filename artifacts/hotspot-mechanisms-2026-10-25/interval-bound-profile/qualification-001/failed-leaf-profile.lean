import Mathlib
import IntervalProfile

example (n : Nat) (h : n < 3) : False := by
  profile_interval_cases interval_cases n <;> omega
