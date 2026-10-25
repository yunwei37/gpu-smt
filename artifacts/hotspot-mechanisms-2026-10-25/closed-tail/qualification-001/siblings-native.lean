import Mathlib
import ClosedTail

example (n : Nat) (h : n < 3) (hp : True) : n ≤ 2 ∧ True := by
  constructor; interval_cases n <;> omega; exact hp
