import Mathlib
import ClosedTail

example (n : Nat) (h : n = n) : n = n := by
  try (omega; exact h)
  exact h
