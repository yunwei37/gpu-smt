import Mathlib.Tactic.IntervalCases
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

end MechanismCertificate

namespace MechanismReflectedGrid

/-- Untrusted batch evaluator's complete in-range solution payload. -/
def certificate : List (Nat × Nat) := [(5, 401), (401, 5)]

/-- Division proves that a nonzero row has at most one possible solution.
The payload must include it, and its claimed sum is independently checked. -/
def rowTest (m : Nat) : Bool :=
  decide (2005 % m = 0 → 2 ≤ 2005 / m → 2005 / m ≤ 2005 →
    (m, 2005 / m) ∈ certificate ∧ m + 2005 / m = 406)

theorem row_sound (m n : Nat) (hm : 0 < m) (hn : 2 ≤ n) (hn' : n ≤ 2005)
    (prod : m * n = 2005) (check : rowTest m = true) : m + n = 406 := by
  have q : 2005 / m = n := by rw [← prod]; exact Nat.mul_div_right n hm
  have rem : 2005 % m = 0 := by rw [← prod]; exact Nat.mul_mod_right m n
  have h := of_decide_eq_true check
  change (2005 % m = 0 → 2 ≤ 2005 / m → 2005 / m ≤ 2005 →
    (m, 2005 / m) ∈ certificate ∧ m + 2005 / m = 406) at h
  rw [q] at h
  exact (h rem hn hn').2

def block (first : Nat) : Nat → Bool
  | 0 => true
  | width + 1 => block first width && rowTest (first + width)

theorem block_sound (first width i : Nat) (hi : i < width)
    (check : block first width = true) : rowTest (first + i) = true := by
  induction width with
  | zero => omega
  | succ width ih =>
    simp only [block, Bool.and_eq_true] at check
    by_cases h : i < width
    · exact ih h check.1
    · have : i = width := by omega
      simpa [this] using check.2

theorem block_append (first a b : Nat) :
    block first (a + b) = (block first a && block (first + a) b) := by
  induction b with
  | zero => simp [block]
  | succ b ih => simp [block, ih, Nat.add_assoc, Bool.and_assoc]

theorem chunk0 : block 2 128 = true := by decide
theorem chunk1 : block 130 128 = true := by decide
theorem chunk2 : block 258 128 = true := by decide
theorem chunk3 : block 386 128 = true := by decide
theorem chunk4 : block 514 128 = true := by decide
theorem chunk5 : block 642 128 = true := by decide
theorem chunk6 : block 770 128 = true := by decide
theorem chunk7 : block 898 128 = true := by decide
theorem chunk8 : block 1026 128 = true := by decide
theorem chunk9 : block 1154 128 = true := by decide
theorem chunk10 : block 1282 128 = true := by decide
theorem chunk11 : block 1410 128 = true := by decide
theorem chunk12 : block 1538 128 = true := by decide
theorem chunk13 : block 1666 128 = true := by decide
theorem chunk14 : block 1794 128 = true := by decide
theorem chunk15 : block 1922 84 = true := by decide
theorem block_join (first a b : Nat) (ha : block first a = true)
    (hb : block (first + a) b = true) : block first (a + b) = true := by
  rw [block_append]
  rw [ha, hb]
  rfl

theorem full_rows : block 2 2004 = true :=
  (block_join 2 128 1876 chunk0 (block_join 130 128 1748 chunk1 (block_join 258 128 1620 chunk2 (block_join 386 128 1492 chunk3 (block_join 514 128 1364 chunk4 (block_join 642 128 1236 chunk5 (block_join 770 128 1108 chunk6 (block_join 898 128 980 chunk7 (block_join 1026 128 852 chunk8 (block_join 1154 128 724 chunk9 (block_join 1282 128 596 chunk10 (block_join 1410 128 468 chunk11 (block_join 1538 128 340 chunk12 (block_join 1666 128 212 chunk13 (block_join 1794 128 84 chunk14 chunk15)))))))))))))))

theorem mathd_numbertheory_541 (m n : Nat) (hm : 1 < m) (hn : 1 < n)
    (prod : m * n = 2005) : m + n = 406 := by
  have mn : m ≤ 2005 := by
    have h := Nat.mul_le_mul_left m (show 1 ≤ n by omega)
    simpa [prod] using h
  have nn : n ≤ 2005 := by
    have h := Nat.mul_le_mul_right n (show 1 ≤ m by omega)
    simpa [prod] using h
  have index : m - 2 < 2004 := by omega
  have checked := block_sound 2 2004 (m - 2) index full_rows
  have same : 2 + (m - 2) = m := by omega
  rw [same] at checked
  exact row_sound m n (by omega) (by omega) nn prod checked

end MechanismReflectedGrid

