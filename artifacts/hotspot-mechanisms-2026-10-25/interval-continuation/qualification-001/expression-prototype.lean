import Mathlib
import IntervalContinuation

example (n : Nat) (h : n + 1 < 4) : n + 1 ≤ 3 := by
  interval_cases_then (n + 1) => omega
