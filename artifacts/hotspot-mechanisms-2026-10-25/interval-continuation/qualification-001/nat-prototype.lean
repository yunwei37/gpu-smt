import Mathlib
import IntervalContinuation

example (n : Nat) (h : n < 4) : n ≤ 3 := by
  interval_cases_then n => omega
