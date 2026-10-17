import Mathlib.Tactic.Linarith.Frontend
import Farkas.Fast
import Farkas427.Products
open Lean Meta Elab Tactic Mathlib.Tactic.Linarith
namespace GpuArithmetic.Baseline
def run (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  if (← IO.getEnv "GPU_ARITHMETIC_BASELINE").isNone then throwUnsupportedSyntax
  let saved ← saveState
  let original := if nlin then {cfg with preprocessors := cfg.preprocessors.concat nlinarithExtras} else cfg
  let cfg := if nlin then {cfg with preprocessors := cfg.preprocessors.concat Farkas427.Products.extras} else cfg
  let cfg := {cfg with oracle := Farkas.native}
  if (← Farkas.Fast.tryFast nlin onlyOn args cfg 0) then return
  saved.restore
  try
    commitIfNoEx do liftMetaFinishingTactic <| Mathlib.Tactic.Linarith.linarith onlyOn args cfg
  catch _ =>
    saved.restore
    commitIfNoEx do liftMetaFinishingTactic <| Mathlib.Tactic.Linarith.linarith onlyOn args original
elab_rules : tactic
  | `(tactic| linarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    if !(Lean.Parser.Tactic.getConfigItems cfg.raw).isEmpty then throwUnsupportedSyntax
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `linarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run false o.isSome args.toList cfg
elab_rules : tactic
  | `(tactic| nlinarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    if !(Lean.Parser.Tactic.getConfigItems cfg.raw).isEmpty then throwUnsupportedSyntax
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `nlinarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run true o.isSome args.toList cfg
end GpuArithmetic.Baseline
