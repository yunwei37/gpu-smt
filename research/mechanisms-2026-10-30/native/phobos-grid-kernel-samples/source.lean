import Lean
set_option maxHeartbeats 200000
set_option maxRecDepth 4000
namespace MechanismGrid
def cell (m n : Nat) : Bool := (m * n != 2005) || (m + n == 406)
def row (m first : Nat) : Nat → Bool
  | 0 => true
  | width + 1 => row m first width && cell m (first + width)
def rectangle (firstM firstN width : Nat) : Nat → Bool
  | 0 => true
  | height + 1 =>
    rectangle firstM firstN width height && row (firstM + height) firstN width
theorem block32 : rectangle 2 2 32 32 = true := by decide
theorem block64 : rectangle 2 2 64 64 = true := by decide
theorem block128 : rectangle 2 2 128 128 = true := by decide
/-- Include each actual solution within a nontrivial sampled block. -/
theorem solutionBlockLeft : rectangle 2 390 32 32 = true := by decide
theorem solutionBlockRight : rectangle 390 2 32 32 = true := by decide
open Lean Elab Command in
elab "recheck_grid " id:ident : command => do
  let env ← getEnv
  let name := Name.str `MechanismGrid id.getId.toString
  let some (.thmInfo value) := env.find? name
    | throwError "grid theorem missing"
  let checkName := Name.str `MechanismGrid ("recheck_" ++ id.getId.toString)
  let start ← IO.monoNanosNow
  let result := env.addDeclCore 100000000 (.thmDecl {
    value with
    name := checkName
    all := [checkName] })
  match result with
  | .error _ => throwError "grid kernel recheck failed"
  | .ok _ =>
    let stop ← IO.monoNanosNow
    logInfo m!"M_GRID_KERNEL_NS {id.getId} {stop - start}"
recheck_grid block32
recheck_grid block64
recheck_grid block128
recheck_grid solutionBlockLeft
recheck_grid solutionBlockRight
#print axioms block32
#print axioms block64
#print axioms block128
#print axioms solutionBlockLeft
#print axioms solutionBlockRight
end MechanismGrid
