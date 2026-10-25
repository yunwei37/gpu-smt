import Mathlib
import IntervalProfile

example (z : Int) : z = z := by
  first | (profile_interval_cases interval_cases z <;> rfl) | rfl
