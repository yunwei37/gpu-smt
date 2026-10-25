import Mathlib
import IntervalContinuation

example (n m : Nat) (hn : n < 3) (hm : m < 4) : n + m < 6 := by
  interval_cases n <;> interval_cases m <;> omega
