import Mathlib.Tactic.Linarith.Frontend
import GpuArithmetic.CostFast
import GpuArithmetic.CostProducts
open Lean Meta Elab Tactic Mathlib.Tactic.Linarith
namespace GpuArithmetic.CostBaseline
def run (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  if (← IO.getEnv "GPU_ARITHMETIC_STRONG_PROFILE").isNone then throwUnsupportedSyntax
  let cost ← IO.mkRef ({} : GpuArithmetic.CostStages.Costs)
  let cpu0 ← GpuArithmetic.CostStages.threadCpuNs
  let wall0 ← IO.monoNanosNow
  try
    runInstrumented cost nlin onlyOn args cfg
  finally
    let dc := (← GpuArithmetic.CostStages.threadCpuNs).toNat - cpu0.toNat
    let dw := (← IO.monoNanosNow) - wall0
    let stats ← cost.get
    let source := (← getFileMap).source
    Farkas.Telemetry.emit (Farkas.Telemetry.row [
      ("ty",Farkas.Telemetry.jstrEsc "strong-arithmetic-stages"),
      ("source",Farkas.Telemetry.jstrEsc source),
      ("cpu_ns",toString dc),("wall_ns",toString dw),
      ("stages","{" ++ ",".intercalate (stats.toList.map fun (k,v) =>
        Farkas.Telemetry.jstrEsc k ++ ":[" ++ toString v.1 ++ "," ++ toString v.2 ++ "]") ++ "}")])
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
