import Lean.Elab.Tactic.Omega
import Lean

set_option maxHeartbeats 200000
set_option maxRecDepth 8000
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
theorem full_rows : block 2 2004 = true := by
  change block 2 (128 + 1876) = true
  rw [block_append, chunk0]
  change block 130 1876 = true
  change block 130 (128 + 1748) = true
  rw [block_append, chunk1]
  change block 258 1748 = true
  change block 258 (128 + 1620) = true
  rw [block_append, chunk2]
  change block 386 1620 = true
  change block 386 (128 + 1492) = true
  rw [block_append, chunk3]
  change block 514 1492 = true
  change block 514 (128 + 1364) = true
  rw [block_append, chunk4]
  change block 642 1364 = true
  change block 642 (128 + 1236) = true
  rw [block_append, chunk5]
  change block 770 1236 = true
  change block 770 (128 + 1108) = true
  rw [block_append, chunk6]
  change block 898 1108 = true
  change block 898 (128 + 980) = true
  rw [block_append, chunk7]
  change block 1026 980 = true
  change block 1026 (128 + 852) = true
  rw [block_append, chunk8]
  change block 1154 852 = true
  change block 1154 (128 + 724) = true
  rw [block_append, chunk9]
  change block 1282 724 = true
  change block 1282 (128 + 596) = true
  rw [block_append, chunk10]
  change block 1410 596 = true
  change block 1410 (128 + 468) = true
  rw [block_append, chunk11]
  change block 1538 468 = true
  change block 1538 (128 + 340) = true
  rw [block_append, chunk12]
  change block 1666 340 = true
  change block 1666 (128 + 212) = true
  rw [block_append, chunk13]
  change block 1794 212 = true
  change block 1794 (128 + 84) = true
  rw [block_append, chunk14]
  change block 1922 84 = true
  exact chunk15

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

#print axioms row_sound
#print axioms full_rows
#print axioms mathd_numbertheory_541
end MechanismReflectedGrid
