import Mathlib
import IntervalContinuation

example (z : Int) : z = z := by
  first | (interval_cases_then z => rfl) | rfl
