import Mathlib
import ClosedTail

open Lean Elab Tactic
@[tactic Lean.Parser.Tactic.omega] def testOmegaNoop : Tactic := fun _ => pure ()
example (p : Prop) (hp : p) : p := by
  early_fail_tail { omega; exact hp }
