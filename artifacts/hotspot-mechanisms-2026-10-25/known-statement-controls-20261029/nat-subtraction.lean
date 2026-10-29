import Mathlib
import Aesop

/- Correctness control for the known imo_1982_p1 Nat-subtraction defect.
   Witness credited to miniF2F_v2 issue #2, not our method or novelty.
   Pending execution against the retained Lean 4.9 environment. -/
namespace GpuSmtKnownStatementControls

def bumpedThird (n : ℕ) : ℕ := if n = 1982 then 661 else n / 3

theorem bumpedThird_step (m n : ℕ) :
    bumpedThird (m + n) - bumpedThird m - bumpedThird n = 0 ∨
    bumpedThird (m + n) - bumpedThird m - bumpedThird n = 1 := by
  unfold bumpedThird
  split_ifs <;> omega

theorem nat_subtraction_counterexample :
    ¬ (∀ f : ℕ → ℕ,
      (∀ m n, 0 < m ∧ 0 < n →
        f (m + n) - f m - f n = 0 ∨ f (m + n) - f m - f n = 1) →
      f 2 = 0 → 0 < f 3 → f 9999 = 3333 → f 1982 = 660) := by
  intro claimed
  have bad := claimed bumpedThird
    (fun m n _ => bumpedThird_step m n)
    (by decide) (by decide) (by decide)
  have different : bumpedThird 1982 ≠ 660 := by decide
  exact different bad

end GpuSmtKnownStatementControls
