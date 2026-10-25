import Mathlib
import IntervalProfile

example (z : Int) (lo : -2 ≤ z) (hi : z < 2) : z ≤ 1 := by
  profile_interval_cases interval_cases z <;> omega
