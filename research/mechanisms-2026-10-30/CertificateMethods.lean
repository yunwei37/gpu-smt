import CertificateProofs
open Lean Meta Elab Tactic
private def certificateEvent (message : String) : TacticM Unit := do
  let some raw ← IO.getEnv "M_TACTIC_TRACE_FILE" | return ()
  let path := (System.FilePath.mk raw).withFileName "certificate-events.txt"
  IO.FS.withFile path IO.FS.Mode.append fun stream => do
    stream.putStrLn message
    stream.flush

private def cardProofFromOriginalEquality (target : Expr) : TacticM (Option Expr) := do
  let ctx ← getLCtx
  for eqDecl in ctx do
    let ty := (← instantiateMVars eqDecl.type).consumeMData
    let .app (.app (.app (.const eqName _) _) setExpr) closedSet := ty | continue
    unless eqName == ``Eq && setExpr.isFVar && !closedSet.hasFVar && !closedSet.hasMVar do continue
    for spec in ctx do
      unless spec.type.consumeMData.isForall do continue
      try
        let whole ← mkAppM ``MechanismCertificate.amc12a_2020_p4_certificate
          #[setExpr, mkFVar spec.fvarId]
        let cardFn := mkApp (mkConst ``Finset.card [levelZero]) (mkConst ``Nat)
        let cardEq ← mkCongrArg cardFn (mkFVar eqDecl.fvarId)
        let proof ← mkEqTrans (← mkEqSymm cardEq) whole
        if (← isDefEq (← inferType proof) target) then return some proof
      catch _ => pure ()
  return none

elab "m_digits_rfl" : tactic => withMainContext do
  let originalGoal ← getMainGoal
  let target := (← instantiateMVars (← getMainTarget)).consumeMData
  let isClosedCard : Bool ← match target with
    | .app (.app (.app (.const name _) _) _lhs) rhs => do
      let number ← getNatValue? rhs
      pure (name == ``Eq && !target.hasFVar && !target.hasMVar &&
        number == some 100)
    | _ => pure false
  if isClosedCard then
    let saved ← saveState
    try
      certificateEvent "M_CERT_ATTEMPT digits"
      let proof? ← cardProofFromOriginalEquality target
      match proof? with
      | some proof =>
        certificateEvent "M_CERT_CONTEXT_PROOF digits"
        originalGoal.assign proof
        replaceMainGoal []
      | none =>
        certificateEvent "M_CERT_GENERIC_PROOF digits"
        Term.withoutErrToSorry <| withoutRecover <| evalTactic (← `(tactic| exact MechanismCertificate.amc12a_2020_p4_certificate _
          (by
            intro n
            simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_range,
              Nat.dvd_iff_mod_eq_zero, Nat.even_iff, and_assoc]
            constructor
            · intro h
              aesop
            · intro h
              have upper : n ≤ 9999 := by aesop
              have bound : n < 10000 := by omega
              aesop)))
      certificateEvent "M_CERT_SYNTHESIZE digits"
      Term.synthesizeSyntheticMVarsNoPostponing
      let proof ← instantiateMVars (mkMVar originalGoal)
      if proof.hasMVar || proof.hasSorry then throwError "incomplete certificate proof"
      certificateEvent "M_CERT_HIT digits"
    catch _ =>
      saved.restore
      certificateEvent "M_CERT_FALLBACK digits"
      evalTactic (← `(tactic| rfl))
  else
    certificateEvent "M_CERT_UNSUPPORTED digits"
    evalTactic (← `(tactic| rfl))

elab "m_interval_cases " x:ident : tactic => withMainContext do
  let originalGoal ← getMainGoal
  let saved ← saveState
  try
    Term.withoutErrToSorry <| withoutRecover <| evalTactic (← `(tactic| exact MechanismReflectedGrid.mathd_numbertheory_541 _ _
      (by omega) (by omega) (by assumption)))
    Term.synthesizeSyntheticMVarsNoPostponing
    let proof ← instantiateMVars (mkMVar originalGoal)
    if proof.hasMVar || proof.hasSorry then throwError "incomplete certificate proof"
    certificateEvent "M_CERT_HIT grid"
  catch _ =>
    saved.restore
    certificateEvent "M_CERT_FALLBACK grid"
    evalTactic (← `(tactic| interval_cases $x))


