import CertificateMethods
import Mathlib
import Aesop

set_option maxHeartbeats 200000

open BigOperators Real Nat Topology Rat

/-- How many $4$-digit positive integers (that is, integers between $1000$ and $9999$, inclusive) having only even digits are divisible by $5?$

$\textbf{(A) } 80 \qquad \textbf{(B) } 100 \qquad \textbf{(C) } 125 \qquad \textbf{(D) } 200 \qquad \textbf{(E) } 500$ Show that it is \textbf{(B) } 100.-/
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  /-
  To determine the number of 4-digit positive integers with only even digits that are divisible by 5, we need to count the integers in the range from 1000 to 9999 that satisfy the conditions:
  1. Each digit is even.
  2. The number is divisible by 5.
  Given that each digit of a number must be even, the only even digits are 0, 2, 4, 6, and 8. Since the number must be divisible by 5, the last digit must be 0 or 5. However, since the number must have only even digits, the last digit must be 0.
  Thus, the number must be of the form \( \overline{abcd} \) where \( a, b, c, d \) are digits, \( d \) is even, and \( d = 0 \). The first digit \( a \) can be any digit from 1 to 9 (9 choices), the second digit \( b \) can be any digit from 0 to 9 (10 choices), the third digit \( c \) can be any digit from 0 to 9 (10 choices), and the fourth digit \( d \) can be 0 (1 choice). Therefore, the total number of such numbers is \( 9 \times 10 \times 10 \times 1 = 900 \).
  -/
  have h₁ : S = Finset.filter (fun n ↦ 5 ∣ n) (Finset.filter (fun n ↦ ∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) (Finset.Icc 1000 9999)) := by
    ext n
    simp [h₀]
    refine' ⟨_, fun h => ⟨_, _, _, h⟩⟩
    · rintro ⟨h₁, _, h₃, h₄⟩
      exact (Nat.mod_eq_of_lt (Nat.mod_lt _ (zero_lt_succ _))).symm
    · rcases h with (rfl | rfl | rfl | rfl) <;> norm_num
  rw [h₁]
  simp only [Finset.card_filter, Nat.card_Icc, Nat.add_sub_cancel, Finset.card_range, Finset.card_product]
  norm_num
  m_digits_rfl
#print axioms amc12a_2020_p4
