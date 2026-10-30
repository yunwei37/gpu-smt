import Mathlib.Data.Nat.Digits
import Lean.Elab.Tactic.Omega
set_option maxHeartbeats 200000
set_option maxRecDepth 2000
namespace ExtractionAuditWitnesses
/-- Decimal extraction by bounded structural recursion. -/
def digitsFuel : Nat → Nat → List Nat
  | 0, _ => []
  | k + 1, n => if n = 0 then [] else n % 10 :: digitsFuel k (n / 10)

theorem digitsFuel_eq (k n : Nat) (h : n < 10 ^ k) :
    digitsFuel k n = Nat.digits 10 n := by
  induction k generalizing n with
  | zero =>
    have hn : n = 0 := by simpa using h
    subst n
    simp [digitsFuel]
  | succ k ih =>
    by_cases hn : n = 0
    · subst n; simp [digitsFuel]
    · rw [digitsFuel, if_neg hn,
        Nat.digits_of_two_le_of_pos (by decide) (Nat.pos_of_ne_zero hn)]
      congr 1
      apply ih
      apply (Nat.div_lt_iff_lt_mul (by decide)).2
      simpa [Nat.pow_succ, Nat.mul_comm] using h


theorem missing_five : Nat.digits 10 2002 = [2,0,0,2] ∧ 2002 % 5 ≠ 0 := by
  constructor
  · rw [← digitsFuel_eq 4 2002 (by decide)]
    decide
  · decide
-- N = product of factorials1!..9!, computed independently; next theorem checks that equality.
theorem factorial_product :
    (1 * 2 * 6 * 24 * 120 * 720 * 5040 * 40320 * 362880 : Nat) =
      1834933472251084800000 := by decide
theorem divisor_not_square :
    1834933472251084800000 % 65536 = 0 ∧
    1834933472251084800000 % (65536 * 65536) ≠ 0 := by decide
theorem square_divisor_outside_claimed_ranges :
    1834933472251084800000 % (4180377600 * 4180377600) = 0 ∧
    99999999 < (4180377600 : Nat) ∧ 362880 < (4180377600 : Nat) := by decide
#print axioms missing_five
#print axioms factorial_product
#print axioms divisor_not_square
#print axioms square_divisor_outside_claimed_ranges
theorem match_bound_counterexample :
    (16 : Nat) ^ (2 ^ 2) = 2 ^ 16 ∧ ¬ (16 ≤ 1 ∨ 2 ≤ 1) := by decide
theorem no_fibonacci_period_two (a : Nat → Nat) (h1 : a 1 = 1) (h2 : a 2 = 1)
    (step : ∀ n, a (n + 2) = a (n + 1) + a n) :
    ¬ (∀ n, a (n + 2) % 4 = a n % 4) := by
  have a3 : a 3 = 2 := by simpa [h1, h2] using step 1
  intro period
  have impossible := period 1
  simpa [a3, h1] using impossible
#print axioms match_bound_counterexample
#print axioms no_fibonacci_period_two
end ExtractionAuditWitnesses
