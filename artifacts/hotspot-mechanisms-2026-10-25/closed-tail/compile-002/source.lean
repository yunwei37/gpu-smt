/- Runtime-guarded, opt-in local proof-program failure shortcut.
No builtin is overridden. A witness throws a normal tactic exception; enclosing
first/try still decides the complete request. This is not mathematical falsity.
-/
import Mathlib

open Lean Elab Tactic

namespace GpuSmt.ClosedTail

private def andThenKind : Name := .str `Lean.Parser.Tactic "tactic_<;>_"

/-- Exact pinned4.9 handlers; any changed dispatch falls back to native. -/
private def expected : List (Name × List String × List String) := [
  (``Lean.Parser.Tactic.omega, ["Lean.Elab.Tactic.Omega.evalOmega"], []),
  (``Lean.Parser.Tactic.exact, ["Lean.Elab.Tactic.evalExact"], []),
  (``Mathlib.Tactic.intervalCases, ["Mathlib.Tactic._aux_Mathlib_Tactic_IntervalCases___elabRules_Mathlib_Tactic_intervalCases_1"], []),
  (andThenKind, [], ["Lean.Parser.Tactic.«_aux_Init_Tactics___macroRules_Lean_Parser_Tactic_tactic_<;>__1»"]),
  (``Lean.Parser.Tactic.focus, ["Lean.Elab.Tactic.evalFocus"], []),
  (``Lean.Parser.Tactic.allGoals, ["Lean.Elab.Tactic.evalAllGoals"], [])]

private def stockDispatch : TacticM Bool := do
  let env ← getEnv
  return expected.all fun (kind, elaborators, macros) =>
    (tacticElabAttribute.getEntries env kind).map (·.declName.toString) == elaborators &&
    (macroAttribute.getEntries env kind).map (·.declName.toString) == macros

private partial def leafTokens (stx : Syntax) : Array (Bool × String) := Id.run do
  if stx.isAtom then return #[(false, stx.getAtomVal)]
  if stx.isIdent then return #[(true, stx.getId.toString)]
  let mut result := #[]
  for child in stx.getArgs do result := result ++ leafTokens child
  return result

private def plainInterval (stx : Syntax) : Bool :=
  stx.isOfKind ``Mathlib.Tactic.intervalCases &&
  match leafTokens stx with
  | #[(false, "interval_cases"), (true, _)] => true
  | _ => false

private partial def intervalTree (stx : Syntax) : Bool :=
  plainInterval stx ||
  (stx.getKind == andThenKind && stx.getNumArgs == 3 &&
    intervalTree stx[0] && intervalTree stx[2])

/-- Only the pure interval tree followed by the native default omega finisher.
No arbitrary preceding tactic or configurable expression is admitted. -/
private def closesOrErrors (stx : Syntax) : Bool :=
  (stx.isOfKind ``Lean.Parser.Tactic.omega && leafTokens stx == #[(false, "omega")]) ||
  (stx.getKind == andThenKind && stx.getNumArgs == 3 &&
    intervalTree stx[0] && stx[2].isOfKind ``Lean.Parser.Tactic.omega &&
    leafTokens stx[2] == #[(false, "omega")])

private def exactIdentifier (stx : Syntax) : Bool :=
  stx.isOfKind ``Lean.Parser.Tactic.exact &&
  match leafTokens stx with
  | #[(false, "exact"), (true, _)] => true
  | _ => false

/-- Inspect only the final adjacent pair; leave prefix evaluation native. -/
syntax (name := earlyFailTail) "early_fail_tail " tacticSeqBracketed : tactic

elab_rules : tactic
  | `(tactic| early_fail_tail $program:tacticSeqBracketed) => do
    -- Do not invoke bracket closure/admission: these braces carry a script
    -- whose original separator evaluator must preserve multiple-goal behavior.
    let sequence := program.raw[1]
    let args := sequence.getArgs
    if args.size < 3 || args.size % 2 != 1 then
      evalSepTactics sequence
    else
      let close := args[args.size - 3]!
      let tail := args[args.size - 1]!
      if !closesOrErrors close || !exactIdentifier tail then
        evalSepTactics sequence
      else
        let split := args.size - 3
        evalSepTactics (mkNullNode args[:split])
        let goals ← getGoals
        if goals.length == 1 && !(← goals.head!.isAssigned) && (← stockDispatch) then
          IO.eprintln <| "[gpu-smt-closed-tail] " ++ (Json.mkObj [
            ("rule", toJson ("native-finisher-then-exact" : String)),
            ("active_goals", toJson (1 : Nat)),
            ("close_byte", toJson (close.getPos?.map (·.byteIdx))),
            ("tail_byte", toJson (tail.getPos?.map (·.byteIdx))),
            ("scope", toJson ("local tactic suffix; enclosing fallback remains native" : String))
          ]).compress
          throwError "closed-tail witness: native finisher closes the only goal or fails; following exact cannot accept"
        else
          evalSepTactics (mkNullNode args[split:])

end GpuSmt.ClosedTail
