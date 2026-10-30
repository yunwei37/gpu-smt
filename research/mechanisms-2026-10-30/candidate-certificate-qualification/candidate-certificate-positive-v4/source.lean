import CertificateMethods
import Mathlib
set_option maxHeartbeats 200000
example : ([] : List Nat) = [] := by m_digits_rfl
example : ((Finset.range 10000).filter (fun n : Nat =>
    1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n)).card = 100 := by
  m_digits_rfl
example (m n : Nat) (hm : 1 < m) (hn : 1 < n) (hprod : m*n=2005) :
    m+n=406 := by m_interval_cases m
