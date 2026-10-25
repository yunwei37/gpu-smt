import Mathlib
import ClosedTail

example (n : Nat) (h : n = n) : n = n := by
  try (early_fail_tail { omega; exact h })
  exact h
