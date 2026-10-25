import Mathlib
import IntervalProfile

example (n : Nat) (lo : 5 ≤ n) (hi : n < 4) : False := by
  profile_interval_cases interval_cases n
