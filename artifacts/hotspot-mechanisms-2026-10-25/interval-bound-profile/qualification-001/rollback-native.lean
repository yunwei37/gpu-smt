import Mathlib
import IntervalProfile

example (z : Int) : z = z := by
  first | (interval_cases z <;> rfl) | rfl
