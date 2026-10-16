import Std.Sync.Mutex
import Mathlib.Tactic.Linarith.Frontend
import Farkas.Native

open Lean Elab Parser Tactic Meta Syntax
open Mathlib.Tactic.Linarith

namespace Farkas427
initialize sink : Std.Mutex Unit ← Std.Mutex.new ()
initialize sequence : IO.Ref Nat ← IO.mkRef 0

private def emit (fields : List (String × String)) : IO Unit :=
  sink.atomically do
    if let some path ← IO.getEnv "FARKAS_CORPUS_FILE" then
      let h ← IO.FS.Handle.mk path .append
      h.putStrLn (Farkas.Telemetry.row fields)
      h.flush

private def loggedOracle (id : Nat) (inner : CertificateOracle) : CertificateOracle where
  produceCertificate hyps maxVar := do
    let input := s!"\{\"maxVar\":{maxVar},\"hyps\":[{",".intercalate (hyps.map Farkas.Telemetry.compJson)}]}"
    let start ← IO.monoNanosNow
    try
      let result ← inner.produceCertificate hyps maxVar
      let stop ← IO.monoNanosNow
      let cert := result.toList.map fun (i,c) => s!"[{i},{c}]"
      emit [("call",toString id),("start_ns",toString start),("elapsed_ns",toString (stop-start)),
        ("ok","true"),("lp",input),("cert",s!"[{",".intercalate cert}]")]
      return result
    catch e =>
      let stop ← IO.monoNanosNow
      emit [("call",toString id),("start_ns",toString start),("elapsed_ns",toString (stop-start)),
        ("ok","false"),("lp",input),("error",Farkas.Telemetry.jstrEsc (← e.toMessageData.toString))]
      throw e

private def run (onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  let id ← sequence.modifyGet fun n => (n+1,n+1)
  let saved ← saveState
  let native := { cfg with oracle := loggedOracle id Farkas.native }
  try
    commitIfNoEx do liftMetaFinishingTactic <| Mathlib.Tactic.Linarith.linarith onlyOn args native
    emit [("call",toString id),("route","\"native\"")]
  catch _ =>
    saved.restore
    emit [("call",toString id),("route","\"stock-fallback\"")]
    commitIfNoEx do liftMetaFinishingTactic <| Mathlib.Tactic.Linarith.linarith onlyOn args cfg

elab_rules : tactic
  | `(tactic| linarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    if ((cfg.raw.reprint.getD "").splitOn "oracle").length > 1 then
      throwUnsupportedSyntax
    let args ← ((args.map (TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `linarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run o.isSome args.toList cfg

elab_rules : tactic
  | `(tactic| nlinarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    if ((cfg.raw.reprint.getD "").splitOn "oracle").length > 1 then
      throwUnsupportedSyntax
    let args ← ((args.map (TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `nlinarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    let cfg := { cfg with preprocessors := cfg.preprocessors.concat nlinarithExtras }
    run o.isSome args.toList cfg
end Farkas427
