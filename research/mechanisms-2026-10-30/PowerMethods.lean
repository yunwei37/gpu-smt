import PowerCertificate
open Lean Meta Elab Tactic
private def powerEvent (text : String) : TacticM Unit := do
  let some raw ← IO.getEnv "M_TACTIC_TRACE_FILE" | return ()
  IO.FS.withFile ((System.FilePath.mk raw).withFileName "certificate-events.txt") IO.FS.Mode.append fun f => do
    f.putStrLn text
    f.flush
private def equationPower? (ty : Expr) (exponent : Nat) : MetaM (Option (Expr × Expr)) := do
  let .app (.app (.app (.const eq _) _) lhs) rhs := ty.consumeMData | return none
  unless eq == ``Eq do return none
  unless lhs.getAppFn.constName? == some ``HPow.hPow || lhs.getAppFn.constName? == some ``Nat.pow do return none
  let args := lhs.getAppArgs
  if args.size < 2 then return none
  if (← getNatValue? args[args.size-1]!) != some exponent then return none
  return some (args[args.size-2]!,rhs)
elab "m_power_cases " x:ident : tactic => withMainContext do
  let goal ← getMainGoal
  let outer ← saveState
  let ctx ← getLCtx
  let mut success := false
  for cube in ctx do
    if success then break
    let some (cx,cn) ← equationPower? (← instantiateMVars cube.type) 3 | continue
    for fourth in ctx do
      if success then break
      let some (ft,fn) ← equationPower? (← instantiateMVars fourth.type) 4 | continue
      unless ← isDefEq cn fn do continue
      let saved ← saveState
      try
        let proof := mkAppN (mkConst ``MechanismPowerCertificate.no_small) #[cn,cx,ft]
        let subgoals ← goal.apply proof
        replaceMainGoal subgoals
        Term.withoutErrToSorry <| withoutRecover <| evalTactic (← `(tactic| all_goals first | assumption | omega))
        Term.synthesizeSyntheticMVarsNoPostponing
        let value ← instantiateMVars (mkMVar goal)
        if value.hasMVar || value.hasSorry then throwError "incomplete power certificate"
        success := true
        powerEvent "M_CERT_HIT power"
      catch _ => saved.restore
  if !success then
    outer.restore
    powerEvent "M_CERT_FALLBACK power"
    evalTactic (← `(tactic| interval_cases $x))
