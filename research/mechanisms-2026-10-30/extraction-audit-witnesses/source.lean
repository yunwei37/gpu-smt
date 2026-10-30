import Mathlib.Data.Nat.Digits
set_option maxHeartbeats 200000
set_option maxRecDepth 2000
namespace ExtractionAuditWitnesses
theorem missing_five : Nat.digits 10 2002 = [2,0,0,2] ∧ 2002 % 5 ≠ 0 := by decide
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
end ExtractionAuditWitnesses
