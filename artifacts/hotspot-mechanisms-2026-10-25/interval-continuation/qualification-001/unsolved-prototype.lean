import Mathlib
import IntervalContinuation

example (n : Nat) (h : n < 3) : n ≤ 2 := by
  interval_cases_then n => skip
