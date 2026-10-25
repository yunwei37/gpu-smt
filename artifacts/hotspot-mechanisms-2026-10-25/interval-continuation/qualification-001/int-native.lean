import Mathlib
import IntervalContinuation

example (z : Int) (lo : -2 ≤ z) (hi : z < 2) : z ≤ 1 := by
  interval_cases z <;> omega
