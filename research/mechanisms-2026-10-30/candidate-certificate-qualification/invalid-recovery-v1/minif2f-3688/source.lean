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
  To determine how many $4$-digit positive integers (numbers between $1000$ and $9999$, inclusive) have only even digits and are divisible by $5$, we can use the properties of finite sets and modular arithmetic.
  1. **Define the Set**: Let \( S \) be the set of all \( 4 \)-digit numbers that meet the criteria:
     - The number must be between $1000$ and $9999$.
     - All digits of the number must be even.
     - The number must be divisible by $5$.
  2. **Modular Arithmetic**: Since the number must be divisible by $5$, it must end in $0$ or $5$. Given that the digits are even, the possible end digits are $0$ and $2$.
  3. **Counting the Numbers**: We can count the numbers that meet the criteria by considering the properties of the numbers and the constraints on the digits.
  -/
  -- We need to show that the cardinality of S is 100.
  have h₁ : S = Finset.filter (fun n ↦ 5 ∣ n) (Finset.filter (fun n ↦ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 1000 ≤ n ∧ n ≤ 9999) (Finset.range 10000)) := by
    ext n
    simp [h₀, Nat.mod_eq_of_lt]
    omega
  rw [h₁]
  -- Simplify the expression to count the number of elements in S.
  simp only [Finset.card, Finset.filter_eq', Finset.mem_filter, Finset.mem_range, Finset.card_range]
  -- The result is 100, as derived from the properties of the numbers and the constraints.
  m_digits_rfl
#print axioms amc12a_2020_p4
