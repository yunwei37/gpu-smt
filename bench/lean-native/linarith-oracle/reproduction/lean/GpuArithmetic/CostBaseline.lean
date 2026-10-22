/- gpu-smt reproduction snapshot; local Lean4.27 adaptation/reduced diagnostic implementation. See ../../PROVENANCE.md. -/
import GpuArithmetic.CostTelemetry
import Mathlib.Tactic.Linarith.Frontend
import GpuArithmetic.CostFast
import GpuArithmetic.CostProducts
open Lean Meta Elab Tactic Mathlib.Tactic.Linarith
namespace GpuArithmetic.CostBaseline
def run (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  if (← IO.getEnv "GPU_ARITHMETIC_STRONG_PROFILE").isNone then throwUnsupportedSyntax
  let enabled := (← IO.getEnv "GPU_ARITHMETIC_COST_TIMING") == some "1"
  let cost ← IO.mkRef ({ profile := enabled } : GpuArithmetic.CostStages.Costs)
  if !enabled then
    runInstrumented cost nlin onlyOn args cfg
  else
    let start ← IO.monoNanosNow
    let source := (← getFileMap).source
    let returned ← IO.mkRef false
    try
      runInstrumented cost nlin onlyOn args cfg
      returned.set true
    finally
      GpuArithmetic.CostStages.emitProfile cost source start (← IO.monoNanosNow)
        (if (← returned.get) then "returned" else "failed")

where
 runInstrumented (cost : IO.Ref GpuArithmetic.CostStages.Costs)
     (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
   let saved ← saveState
   let original := if nlin then {cfg with preprocessors := cfg.preprocessors.concat (GpuArithmetic.CostProducts.stockExtras cost)} else cfg
   let cfg := if nlin then {cfg with preprocessors := cfg.preprocessors.concat (GpuArithmetic.CostProducts.extras cost)} else cfg
   let cfg := {cfg with oracle := GpuArithmetic.CostNative.native}
   if (← GpuArithmetic.CostFast.tryFast cost nlin onlyOn args cfg 0) then return
   saved.restore
   try
     commitIfNoEx do liftMetaFinishingTactic <| GpuArithmetic.CostStages.linarith cost onlyOn args cfg
   catch _ =>
     saved.restore
     commitIfNoEx do liftMetaFinishingTactic <| GpuArithmetic.CostStages.linarith cost onlyOn args original
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
end GpuArithmetic.CostBaseline
