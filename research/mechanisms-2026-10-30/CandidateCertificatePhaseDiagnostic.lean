import CertificateMethods
import Mathlib
set_option maxHeartbeats 200000
#eval do
  let stream ← IO.getStderr
  stream.putStrLn "M_CONTROL_DECL 0"
  stream.flush
example : ([] : List Nat) = [] := by m_digits_rfl
#eval do
  let stream ← IO.getStderr
  stream.putStrLn "M_CONTROL_DECL 1"
  stream.flush
example : ((Finset.range 10000).filter (fun n : Nat =>
    1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n)).card = 100 := by
  m_digits_rfl
#eval do
  let stream ← IO.getStderr
  stream.putStrLn "M_CONTROL_DECL 2"
  stream.flush
example (m n : Nat) (hm : 1 < m) (hn : 1 < n) (hprod : m*n=2005) :
    m+n=406 := by m_interval_cases m
#eval do
  let stream ← IO.getStderr
  stream.putStrLn "M_CONTROL_DECL 3"
  stream.flush
example (S : Finset Nat) (h :
    ∀ n, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have eqSet : S = (Finset.Icc 1000 9999).filter (fun n =>
      (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n) := by
    ext n
    rw [h, Finset.mem_filter, Finset.mem_Icc]
    tauto
  rw [eqSet]
  m_digits_rfl
