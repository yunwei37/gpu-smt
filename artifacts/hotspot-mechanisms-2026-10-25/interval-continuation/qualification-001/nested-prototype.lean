import Mathlib
import IntervalContinuation

example (n m : Nat) (hn : n < 3) (hm : m < 4) : n + m < 6 := by
  interval_cases_then n =>
    interval_cases_then m => omega
