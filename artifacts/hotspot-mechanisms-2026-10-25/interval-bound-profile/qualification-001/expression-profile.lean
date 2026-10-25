import Mathlib
import IntervalProfile

example (n : Nat) (h : n + 1 < 4) : n + 1 ≤ 3 := by
  profile_interval_cases interval_cases (n + 1) <;> omega
