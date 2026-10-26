/-
Copyright (c) 2026 gpu-smt contributors.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Lean.Elab.Tactic.Basic
import Lean.Elab.Tactic.BuiltinTactic

open Lean Elab Tactic

/-- Experimental opt-in native error propagation, not a failure predictor.
No global elaborator, timeout, logging or proof-checking setting changes.
Native acceptance equivalence is pending differential qualification. -/
syntax (name := nativeFailFast) "failfast_native " tacticSeq : tactic

elab_rules : tactic
  | `(tactic| failfast_native $body:tacticSeq) =>
    Term.withoutErrToSorry <| withoutRecover <| evalTactic body
