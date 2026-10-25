import Mathlib
import ClosedTail

example (n : Nat) (h : n < 3) (hp : True) : n ≤ 2 ∧ True := by
  early_fail_tail { constructor; interval_cases n <;> omega; exact hp }
