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
  To determine how many 4-digit positive integers (i.e., integers between 1000 and 9999, inclusive) have only even digits and are divisible by 5, we need to consider the properties of such numbers.
  1. **Range of Numbers**: The numbers in question are between 1000 and 9999.
  2. **Digit Analysis**: Each digit in the number must be even. The digits of a number are given by the list of digits obtained by repeatedly dividing by 10 and recording the remainders.
  3. **Divisibility by 5**: The number must be divisible by 5. This implies that the last digit (remainder when divided by 10) must be 0 or 5.
  Given these conditions, we can deduce that the last digit must be 0 or 5. The remaining three digits can be any even digit (0, 2, 4, 6, 8). The first digit cannot be 0 (as it would not be a 4-digit number). Therefore, the first digit can be 2, 4, 6, or 8 (4 choices). The second and third digits can be any even digit (4 choices each). Thus, the total number of such numbers is calculated as follows:
  - There are 4 choices for the first digit (2, 4, 6, or 8).
  - There are 4 choices for the second digit (2, 4, 6, or 8).
  - There are 4 choices for the third digit (2, 4, 6, or 8).
  - There are 2 choices for the last digit (0 or 5).
  Multiplying these choices together, we get:
  \[ 4 \times 4 \times 4 \times 2 = 128 \]
  However, since the number must be divisible by 5, the last digit must be 0 or 5. This reduces the count by half (since there are 2 choices for the last digit). Therefore, the total count is:
  \[ 128 / 2 = 64 \]
  Thus, the number of 4-digit positive integers with only even digits and divisible by 5 is 64.
  -/
  -- We define a set S that contains the numbers that meet the criteria.
  have : S = Finset.filter (fun n ↦ n % 5 = 0 ∧ (∀ d ∈ Nat.digits 10 n, Even d)) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Nat.lt_succ_iff, Nat.le_add_left]
    -- We need to show that the set S is equivalent to the set of numbers that meet the criteria.
    -- This involves checking the conditions for membership in S.
    -- The filter function will select numbers that meet the criteria:
    -- 1. n % 5 = 0 (number is divisible by 5)
    -- 2. All digits of n are even
    -- 3. The number is between 1000 and 9999.
    omega
  -- We rewrite S using the above equivalence.
  rw [this]
  -- The cardinality of the set is 100.
  m_digits_rfl
#print axioms amc12a_2020_p4
