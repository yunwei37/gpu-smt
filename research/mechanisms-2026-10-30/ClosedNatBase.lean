import Mathlib
set_option maxHeartbeats 200000
set_option maxRecDepth 10000
open scoped BigOperators
namespace MClosedNat
def block (f : Nat → Nat) (start : Nat) : Nat → Nat
 | 0 => 1
 | n+1 => block f start n * f (start+n)
theorem block_eq (f : Nat → Nat) (a n : Nat) :
 block f a n = ∏ k ∈ Finset.range n, f (a+k) := by
 induction n with
 | zero => simp [block]
 | succ n ih => simp [block, Finset.prod_range_succ, ih]
theorem prod_step (f : Nat → Nat) (a b v w : Nat)
 (hp : (∏ k ∈ Finset.range a, f k) = v) (hb : block f a b = w) :
 (∏ k ∈ Finset.range (a+b), f k) = v*w := by
 rw [Finset.prod_range_add, ← block_eq, hp, hb]
theorem factorial_step (a b v w : Nat)
 (hp : a.factorial = v) (hb : (a+1).ascFactorial b = w) :
 (a+b).factorial = v*w := by
 rw [← Nat.factorial_mul_ascFactorial, hp, hb]
theorem power_step (a b c v w : Nat)
 (hp : a^b = v) (hb : a^c = w) : a^(b+c)=v*w := by
 rw [pow_add, hp, hb]
def oddTerm (k : Nat) : Nat := if ¬Even k then k else 1
theorem odd_filter (n : Nat) :
 Finset.prod (Finset.filter (fun k : Nat => ¬Even k) (Finset.range n)) id =
 ∏ k ∈ Finset.range n, oddTerm k := by
 simp only [Finset.prod_filter, oddTerm, id_eq]
end MClosedNat
