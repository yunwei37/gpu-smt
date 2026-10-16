-- SPDX-License-Identifier: Apache-2.0
import Lean

/- Native Meta integration for batched, read-only argument comparisons.
   Source-native order, assignments, instance synthesis and unknown cases stay
   in Lean. The frontier is implementation input, not GPU engagement evidence. -/
namespace GPUMetaBatch
open Lean Meta

private def readOnly (e : Expr) : Bool :=
  !e.hasExprMVar && !e.hasLevelMVar && !e.hasFVar && !e.hasLooseBVars

/-- Sufficiently independent argument pairs at this native application.
    Equal terms are skipped because stock quick equality already handles them.
    The provider must support actual reduction; no result is guessed here. -/
@[export gpu_meta_batch_collect]
def collect (t s : Expr) : Array (Expr × Expr) := Id.run do
  if !t.isApp || !s.isApp || t.getAppFn != s.getAppFn then
    return #[]
  let left := t.getAppArgs
  let right := s.getAppArgs
  if left.size != right.size then return #[]
  let mut pairs := #[]
  for i in [:left.size] do
    let a := left[i]!
    let b := right[i]!
    if a != b && readOnly a && readOnly b then
      pairs := pairs.push (a, b)
  return pairs

/-- This supplies the real compiled MetaM result ABI. It is used only after
    a provider has positively established the supported equality. -/
@[export gpu_meta_batch_return_true]
def returnTrue (_t _s : Expr) : MetaM Bool :=
  return true

end GPUMetaBatch
