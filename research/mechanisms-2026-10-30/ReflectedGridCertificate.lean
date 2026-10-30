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

#eval IO.println "M_GRID_BEFORE_CHUNKS"
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
#eval IO.println "M_GRID_AFTER_CHUNKS"
theorem block_join (first a b : Nat) (ha : block first a = true)
    (hb : block (first + a) b = true) : block first (a + b) = true := by
  rw [block_append]
  rw [ha, hb]
  rfl

theorem full_rows : block 2 2004 = true :=
  (block_join 2 128 1876 chunk0 (block_join 130 128 1748 chunk1 (block_join 258 128 1620 chunk2 (block_join 386 128 1492 chunk3 (block_join 514 128 1364 chunk4 (block_join 642 128 1236 chunk5 (block_join 770 128 1108 chunk6 (block_join 898 128 980 chunk7 (block_join 1026 128 852 chunk8 (block_join 1154 128 724 chunk9 (block_join 1282 128 596 chunk10 (block_join 1410 128 468 chunk11 (block_join 1538 128 340 chunk12 (block_join 1666 128 212 chunk13 (block_join 1794 128 84 chunk14 chunk15)))))))))))))))

#eval IO.println "M_GRID_AFTER_ASSEMBLY"
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

open Lean Elab Command in
elab "measure_grid_chunks" : command => do
  let env ← getEnv
  let mut declarations := #[]
  for i in [:16] do
    let name := Name.str `MechanismReflectedGrid ("chunk" ++ toString i)
    let some (.thmInfo value) := env.find? name | throwError "missing chunk"
    declarations := declarations.push value
  for workers in [1, 2, 4, 8] do
    for repetition in [:5] do
      let start ← IO.monoNanosNow
      let mut tasks := #[]
      for worker in [:workers] do
        let job : IO Nat := do
          let mut total := 0
          for i in [:declarations.size] do
            if i % workers == worker then
              let value := declarations[i]!
              let checkName := Name.str `MechanismReflectedGrid
                ("checked_" ++ toString workers ++ "_" ++ toString repetition ++ "_" ++ toString i)
              let began ← IO.monoNanosNow
              match env.addDeclCore 1000000 (.thmDecl {value with name := checkName, all := [checkName]}) with
              | .error _ => throw (IO.userError "original kernel rejected chunk")
              | .ok _ => total := total + 1
              let ended ← IO.monoNanosNow
              IO.println s!"M_GRID_CHUNK {workers} {repetition} {i} {ended - began}"
          pure total
        let task ← IO.asTask job
        tasks := tasks.push task
      let mut count := 0
      for task in tasks do
        match task.get with
        | .error e => throwError "chunk task failed: {e}"
        | .ok n => count := count + n
      let stop ← IO.monoNanosNow
      unless count == 16 do throwError "incomplete checks"
      logInfo m!"M_GRID_GROUP {workers} {repetition} {stop - start} {count}"
measure_grid_chunks

end MechanismReflectedGrid
