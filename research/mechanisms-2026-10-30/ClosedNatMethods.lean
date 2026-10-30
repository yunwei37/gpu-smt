import ClosedNatFacts
open Lean Meta Elab Tactic
private def event (s : String) : TacticM Unit := do
 let some path ← IO.getEnv "M_CLOSED_EVENT" | return ()
 IO.FS.withFile path IO.FS.Mode.append fun f => do
  f.putStrLn s
  f.flush
elab "m_closed_nat_rfl" : tactic => withMainContext do
 let saved ← saveState
 let goal ← getMainGoal
 try
  event "M_CLOSED_ENTER"
  Term.synthesizeSyntheticMVarsNoPostponing
  let target ← instantiateMVars (← getMainTarget)
  if target.hasFVar || target.hasMVar then throwError "open numeric target"
  Term.withoutErrToSorry <| withoutRecover <| evalTactic (← `(tactic|
   (simp only [MClosedNat.fac_942,MClosedNat.fac_5000,MClosedNat.fac_10000,
     MClosedNat.odd_10000,MClosedNat.pow_2_5000,MClosedNat.pow_15_233,
     MClosedNat.pow_5_234] <;> decide)))
  Term.synthesizeSyntheticMVarsNoPostponing
  let value ← instantiateMVars (mkMVar goal)
  if value.hasMVar || value.hasSorry then throwError "incomplete closed numeric proof"
  event "M_CLOSED_HIT"
 catch _ =>
  saved.restore
  event "M_CLOSED_FALLBACK"
  evalTactic (← `(tactic| rfl))
