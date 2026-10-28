/-
Pinned Lean4.27 BV frontend adaptation.
Upstream Copyright (c)2024 Lean FRO,LLC;Apache-2.0.
Explicit opt-in;stock frontend and kernel/compiler trust remain unchanged.
-/
import FusedLRAT
import Lean.Elab.Tactic.BVDecide

open Lean Meta Elab Tactic
open Lean.Parser.Tactic
open Lean.Elab.Tactic.BVDecide
open Lean.Elab.Tactic.BVDecide.Frontend
open Std.Sat Std.Tactic.BVDecide

namespace GpuSmt.FusedFrontend

private def addClosed (name : Name) (value type : Expr) : CoreM Unit :=
  addAndCompile <| .defnDecl {
    name, levelParams := [], type, value, hints := .abbrev, safety := .safe
  }

def reflectionProof (certificate : LratCert) (ctx : TacticContext)
    (reflection : ReflectionResult) : MetaM Expr := do
  addClosed ctx.exprDef reflection.expr (mkConst ``BVLogicalExpr)
  addClosed ctx.certDef (toExpr certificate) (mkConst ``String)
  addClosed ctx.reflectionDef
    (mkApp2 (mkConst ``GpuSmt.FusedLRAT.verifyBVExpr)
      (mkConst ctx.exprDef) (mkConst ctx.certDef)) (mkConst ``Bool)
  let auxType ← mkEq (mkConst ctx.reflectionDef) (toExpr true)
  let auxProof := mkApp3 (mkConst ``Lean.ofReduceBool)
    (mkConst ctx.reflectionDef) (toExpr true) (← mkEqRefl (toExpr true))
  let auxLemma ← withOptions (Elab.async.set · false) do
    withTraceNode `Meta.Tactic.sat (fun _ => return "Verifying fused LRAT certificate") do
      mkAuxLemma [] auxType auxProof
  return mkApp3 (mkConst ``GpuSmt.FusedLRAT.unsat_of_checked)
    (mkConst ctx.exprDef) (mkConst ctx.certDef) (mkConst auxLemma)

def fusedBitblaster (goal : MVarId) (ctx : TacticContext)
    (reflection : ReflectionResult)
    (atoms : Std.HashMap Nat (Nat × Expr × Bool)) :
    MetaM (Except CounterExample UnsatProver.Result) := do
  let entry ← IO.lazyPure (fun _ => reflection.bvExpr.bitblast)
  if ctx.config.graphviz then
    IO.FS.writeFile ("." / "aig.gv") (AIG.toGraphviz entry)
  let (cnf, mapping) ← IO.lazyPure (fun _ =>
    let (entry, mapping) := entry.relabelNat'
    (AIG.toCNF entry, mapping))
  match ← runExternal cnf ctx.solver ctx.lratPath ctx.config.trimProofs
      ctx.config.timeout ctx.config.binaryProofs with
  | .ok certificate =>
    let proof ← reflectionProof certificate ctx reflection
    return .ok { proof, lratCert := certificate }
  | .error assignment =>
    let equations := reconstructCounterExample mapping assignment entry.aig.decls.size atoms
    return .error { goal, unusedHypotheses := reflection.unusedHypotheses, equations }

def runFused (goal : MVarId) (ctx : TacticContext) : MetaM Unit := do
  let some goal ← Normalize.bvNormalize goal ctx.config | return ()
  match ← closeWithBVReflection goal (fun goal reflection atoms =>
      fusedBitblaster goal ctx reflection atoms) with
  | .ok _ => pure ()
  | .error counterExample =>
    counterExample.goal.withContext do
      throwError (← addMessageContextFull (← explainCounterExampleQuality counterExample))

syntax (name := fusedTactic) "bv_decide_fused" optConfig : tactic

@[tactic fusedTactic]
def evalFused : Tactic := fun
  | `(tactic| bv_decide_fused $cfg:optConfig) => do
    let config ← elabBVDecideConfig cfg
    IO.FS.withTempFile fun _ lratFile => do
      let context ← TacticContext.new lratFile config
      liftMetaFinishingTactic fun goal => runFused goal context
  | _ => throwUnsupportedSyntax

end GpuSmt.FusedFrontend
