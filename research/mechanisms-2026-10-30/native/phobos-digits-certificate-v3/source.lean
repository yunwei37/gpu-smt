import Mathlib.Data.Nat.Digits
import Mathlib.Data.Finset.Card
import Lean.Elab.Tactic.Omega
set_option maxHeartbeats 200000
set_option maxRecDepth 4000
namespace MechanismCertificate

/-- Decimal extraction by bounded structural recursion. -/
def digitsFuel : Nat → Nat → List Nat
  | 0, _ => []
  | k + 1, n => if n = 0 then [] else n % 10 :: digitsFuel k (n / 10)

theorem digitsFuel_eq (k n : Nat) (h : n < 10 ^ k) :
    digitsFuel k n = Nat.digits 10 n := by
  induction k generalizing n with
  | zero =>
    have hn : n = 0 := by simpa using h
    subst n
    simp [digitsFuel]
  | succ k ih =>
    by_cases hn : n = 0
    · subst n; simp [digitsFuel]
    · rw [digitsFuel, if_neg hn,
        Nat.digits_of_two_le_of_pos (by decide) (Nat.pos_of_ne_zero hn)]
      congr 1
      apply ih
      apply (Nat.div_lt_iff_lt_mul (by decide)).2
      simpa [Nat.pow_succ, Nat.mul_comm] using h

def eligible (n : Nat) : Bool :=
  decide (1000 ≤ n) && decide (n ≤ 9999) &&
    (digitsFuel 4 n).all (fun d => d % 2 == 0) && (n % 5 == 0)

theorem eligible_iff (n : Nat) (hn : n < 10000) :
    eligible n = true ↔
      1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n := by
  unfold eligible
  rw [digitsFuel_eq 4 n hn]
  simp [List.all_eq_true, Nat.even_iff, Nat.dvd_iff_mod_eq_zero, and_assoc]

def countFast : Nat → Nat
  | 0 => 0
  | n + 1 => countFast n + if eligible n then 1 else 0

theorem countFast_eq_card (n : Nat) :
    countFast n = ((Finset.range n).filter (fun k => eligible k = true)).card := by
  induction n with
  | zero => simp [countFast]
  | succ n ih =>
    by_cases h : eligible n = true
    · simp [countFast, Finset.range_succ, Finset.filter_insert, h, ih]
    · simp [countFast, Finset.range_succ, Finset.filter_insert, h, ih]

/-- Each block has at most 100 recursive layers during kernel reduction. -/
def countBlock (start : Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => countBlock start n + if eligible (start + n) then 1 else 0

theorem countFast_add (start n : Nat) :
    countFast (start + n) = countFast start + countBlock start n := by
  induction n with
  | zero => simp [countBlock]
  | succ n ih => simp [countFast, countBlock, ih, Nat.add_assoc]

def blockSum : Nat → Nat
  | 0 => 0
  | n + 1 => blockSum n + countBlock (100 * n) 100

theorem blockSum_eq (n : Nat) : blockSum n = countFast (100 * n) := by
  induction n with
  | zero => simp [blockSum, countFast]
  | succ n ih =>
    simp only [blockSum, ih, Nat.mul_succ]
    exact (countFast_add (100 * n) 100).symm

/-- Ordinary kernel reduction, with no native_decide or new axiom. -/
theorem computed_count : blockSum 100 = 100 := by decide

theorem amc12a_2020_p4_certificate (S : Finset Nat)
    (h : ∀ n, n ∈ S ↔
      1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d ∈ Nat.digits 10 n, Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have hs : S = (Finset.range 10000).filter (fun k => eligible k = true) := by
    ext n
    rw [h, Finset.mem_filter, Finset.mem_range]
    constructor
    · intro hn
      have bound : n < 10000 := by omega
      exact ⟨bound, (eligible_iff n bound).2 hn⟩
    · rintro ⟨bound, hn⟩
      exact (eligible_iff n bound).1 hn
  rw [hs, ← countFast_eq_card, ← blockSum_eq 100]
  exact computed_count

open Lean Elab Command in
elab "recheck_count_kernel" : command => do
  let env ← getEnv
  let some (.thmInfo value) := env.find? ``computed_count
    | throwError "computed_count theorem missing"
  let start ← IO.monoNanosNow
  let result := env.addDeclCore 100000000
    (.thmDecl { value with
      name := `M_count_kernel_recheck
      all := [`M_count_kernel_recheck] })
  match result with
  | .error error => throwError "kernel recheck failed: {error}"
  | .ok _ =>
    let stop ← IO.monoNanosNow
    logInfo m!"M_KERNEL_RECHECK_NS={stop - start}"
recheck_count_kernel
#print axioms digitsFuel_eq
#print axioms computed_count
#print axioms amc12a_2020_p4_certificate
end MechanismCertificate
