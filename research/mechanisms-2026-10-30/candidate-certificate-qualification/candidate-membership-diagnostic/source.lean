import CertificateMethods
import Mathlib
set_option maxHeartbeats 200000
example (n : Nat) :
    n ∈ ((Finset.range 10000).filter (fun n : Nat =>
      1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n)) ↔
      1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n := by
  simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_Icc,
    Nat.dvd_iff_mod_eq_zero, Nat.even_iff]
  trace_state
  omega
