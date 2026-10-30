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
  To determine the number of 4-digit positive integers with only even digits that are divisible by 5, we need to count the integers \( n \) in the range from 1000 to 9999 that satisfy the following conditions:
  1. All digits of \( n \) are even.
  2. \( n \) is divisible by 5.
  Given that \( n \) must be divisible by 5, we know that \( n \) must end in 0 or 5. Since the digits must be even, the only possible last digit is 0 (as 5 would not have only even digits). Therefore, \( n \) must end in 0.
  The number of 4-digit integers ending in 0 is 900 (from 1000 to 9999). Since we need only those that have only even digits, we exclude the numbers that do not meet this criteria.
  Thus, the number of 4-digit integers with only even digits that are divisible by 5 is 100.
  -/
  have h₁ : S = Finset.filter (fun n : ℕ => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
      (Finset.Icc 1000 9999) := by
    ext n
    simp [Nat.lt_succ_iff, h₀]
    omega
  rw [h₁]
  simp [Finset.filter_eq, Finset.Icc]
  m_digits_rfl
#print axioms amc12a_2020_p4
