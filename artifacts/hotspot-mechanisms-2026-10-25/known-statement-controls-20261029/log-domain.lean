import Mathlib
import Aesop

/- Correctness control for a known miniF2F formalization defect.
   DSP+, arXiv:2506.11487v1, Appendix F. Not a new finding or engine policy.
   Pending execution against the retained Lean 4.9 environment. -/
namespace GpuSmtKnownStatementControls

theorem log_domain_counterexample :
    ¬ (∀ n : ℕ, 0 < n →
      Real.logb 2 (Real.logb 16 (n : ℝ)) =
        Real.logb 4 (Real.logb 4 (n : ℝ)) →
      (List.sum (Nat.digits 10 n)) = 13) := by
  intro claimed
  have bad := claimed 1 (by decide) (by simp)
  have different : (List.sum (Nat.digits 10 1)) ≠ 13 := by decide
  exact different bad

end GpuSmtKnownStatementControls
