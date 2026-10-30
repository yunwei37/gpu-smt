import CertificateMethods
import Mathlib
set_option maxHeartbeats 200000
example : (Finset.range 2).card = 101 := by m_digits_rfl
example (m n : Nat) (hm : m = 5) (hn : n = 401) : m+n=407 := by
  m_interval_cases m
  subst n
  norm_num
