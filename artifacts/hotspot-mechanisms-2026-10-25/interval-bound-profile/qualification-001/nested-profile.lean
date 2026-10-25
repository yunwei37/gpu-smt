import Mathlib
import IntervalProfile

example (n m : Nat) (hn : n < 3) (hm : m < 4) : n + m < 6 := by
  profile_interval_cases interval_cases n <;> profile_interval_cases interval_cases m <;> omega
