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
  To determine how many 4-digit positive integers have only even digits and are divisible by 5, we need to count the numbers in the range from 1000 to 9999 that satisfy the conditions of having only even digits and being divisible by 5.
  1. **Filtering the Range**: We filter the numbers from 1000 to 9999 that are divisible by 5 and have only even digits.
  2. **Counting the Numbers**: We count the numbers that satisfy the given conditions.
  Given the constraints:
  - Numbers must be between 1000 and 9999.
  - All digits of the number must be even.
  - The number must be divisible by 5.
  We can deduce that the numbers must end in 0 or 5, and since only 5 can be the last digit (as 0 would make the number not divisible by 5), we have only 5 numbers ending in 0.
  Each number from 1000 to 9999 that ends in 0 can be represented as \(1000 + 10k\) where \(k\) ranges from 0 to 899 (since \(1000 + 10 \times 899 = 9990\)).
  Thus, there are 900 numbers that meet the criteria. However, we need to verify the count given in the problem, which states that there are 100 such numbers. This discrepancy suggests a possible error in the initial conditions or a misinterpretation of the problem.
  -/
  have h₁ : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext
    simp [h₀, Nat.mod_eq_of_lt]
    omega
  rw [h₁]
  m_digits_rfl
#print axioms amc12a_2020_p4
