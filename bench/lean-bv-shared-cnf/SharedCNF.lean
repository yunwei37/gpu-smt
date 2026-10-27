/-
Experimental closed-CNF frontend based on pinned Lean4.27 BV frontend.
Original upstream frontend copyright (c)2024 Lean FRO,LLC;Apache-2.0.
No default replacement,performance or novelty claim.
-/
import CnfBridge
import Lean.Elab.Tactic.BVDecide

open Lean Meta Elab Tactic
open Lean.Parser.Tactic
open Lean.Elab.Tactic.BVDecide
open Lean.Elab.Tactic.BVDecide.Frontend
open Std.Sat Std.Tactic.BVDecide

namespace GpuSmt.SharedCNF

private def addClosed (name : Name) (value type : Expr) : CoreM Unit :=
  addAndCompile <| .defnDecl {
    name, levelParams := [], type, value,
    hints := .abbrev, safety := .safe
  }

unsafe def sharedBitblaster (goal : MVarId) (ctx : TacticContext)
    (reflection : ReflectionResult)
    (atoms : Std.HashMap Nat (Nat × Expr × Bool)) :
    MetaM (Except CounterExample UnsatProver.Result) := do
  let exprDef := ctx.exprDef.appendAfter "_shared"
  let cnfDef := ctx.exprDef.appendAfter "_cnf"
  let certDef := ctx.certDef.appendAfter "_shared"
  let reflectionDef := ctx.reflectionDef.appendAfter "_shared"
  addClosed exprDef reflection.expr (mkConst ``BVLogicalExpr)
  withTraceNode `Meta.Tactic.sat (fun _ => return "Compiling shared CNF declaration") do
    addClosed cnfDef
      (mkApp (mkConst ``GpuSmt.CnfBridge.cnfOf) (mkConst exprDef))
      (mkApp (mkConst ``CNF [.zero]) (mkConst ``Nat))
  let cnf ← withTraceNode `Meta.Tactic.sat (fun _ => return "Loading shared CNF for SAT") do
    evalConst (CNF Nat) cnfDef
  let result ← runExternal cnf ctx.solver ctx.lratPath
    ctx.config.trimProofs ctx.config.timeout ctx.config.binaryProofs
  match result with
  | .error assignment =>
    let entry ← IO.lazyPure (fun _ => reflection.bvExpr.bitblast)
    let (_, mapping) ← IO.lazyPure (fun _ => entry.relabelNat')
    let equations := reconstructCounterExample mapping assignment entry.aig.decls.size atoms
    return .error { goal, unusedHypotheses := reflection.unusedHypotheses, equations }
  | .ok cert =>
    addClosed certDef (toExpr cert) (mkConst ``String)
    addClosed reflectionDef
      (mkApp2 (mkConst ``Std.Tactic.BVDecide.Reflect.verifyCert)
        (mkConst cnfDef) (mkConst certDef))
      (mkConst ``Bool)
    let auxType ← mkEq (mkConst reflectionDef) (toExpr true)
    let auxProof := mkApp3 (mkConst ``Lean.ofReduceBool)
      (mkConst reflectionDef) (toExpr true) (← mkEqRefl (toExpr true))
    let auxLemma ← withOptions (Elab.async.set · false) do
      withTraceNode `Meta.Tactic.sat (fun _ => return "Verifying shared CNF certificate") do
        mkAuxLemma [] auxType auxProof
    let correspondence ← mkEqRefl (mkConst cnfDef)
    let proof := mkApp5 (mkConst ``GpuSmt.CnfBridge.unsat_of_checked_cnf)
      (mkConst exprDef) (mkConst cnfDef) (mkConst certDef)
      correspondence (mkConst auxLemma)
    return .ok { proof, lratCert := cert }

unsafe def runShared (goal : MVarId) (ctx : TacticContext) : MetaM Unit := do
  let some goal ← Normalize.bvNormalize goal ctx.config | return ()
  let prover : UnsatProver := fun goal reflection atoms =>
    sharedBitblaster goal ctx reflection atoms
  match ← closeWithBVReflection goal prover with
  | .ok _ => return ()
  | .error counterExample =>
    counterExample.goal.withContext do
      let message ← explainCounterExampleQuality counterExample
      throwError (← addMessageContextFull message)

syntax (name := sharedCore) "bv_decide_shared_core" optConfig : tactic

@[tactic sharedCore]
unsafe def evalShared : Tactic := fun
  | `(tactic| bv_decide_shared_core $cfg:optConfig) => do
    let config ← elabBVDecideConfig cfg
    IO.FS.withTempFile fun _ lratFile => do
      let context ← TacticContext.new lratFile config
      liftMetaFinishingTactic fun goal => runShared goal context
  | _ => throwUnsupportedSyntax

macro "bv_decide_shared" cfg:optConfig : tactic =>
  `(tactic| first | bv_decide_shared_core $cfg | bv_decide $cfg)

end GpuSmt.SharedCNF
