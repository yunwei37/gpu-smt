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
  To show that there are 100 four-digit numbers divisible by 5 that have only even digits, we need to count the numbers in the range from 1000 to 9999 that satisfy the conditions of having only even digits and being divisible by 5.
  1. **Filtering the Range**: We filter the numbers from 1000 to 9999 that meet the criteria:
     - The number is divisible by 5.
     - All digits are even.
  2. **Counting the Elements**: We count the number of elements in the filtered set.
  Given the constraints, we can directly assert that the count of such numbers is 100, as this is a known combinatorial result.
  -/
  -- We define S to be the filtered set of numbers from 1000 to 9999 that meet the criteria.
  have h₁ : S = Finset.filter (fun n ↦ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.Icc 1000 9999) := by
    ext n
    simp [Nat.le_of_lt, h₀]
    omega
  -- We rewrite S using the filter definition.
  rw [h₁]
  -- The cardinality of the filtered set is 100, as this is a known combinatorial result.
  m_digits_rfl
#print axioms amc12a_2020_p4
