"""Build a private native REPL for real prefix execution, preserving all source/runtime state.
Applies SHRED's snapshot-context repair and adds ordinary kernel checking of closed roots.
"""
from pathlib import Path
import shutil, subprocess, os, json
R=Path('/workspaces/repository')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/prefix')
SRC=Path('/tmp/gpu-smt-native-repl-20261014')
DST=U/'repl-kernel'
if not DST.exists():
    shutil.copytree(SRC,DST,ignore=shutil.ignore_patterns('.git','.lake'))
p=DST/'REPL/Snapshots.lean'
s=(SRC/p.relative_to(DST)).read_text()
s=s.replace('  tacticContext : Tactic.Context','  tacticContext : Tactic.Context\n  initialGoals : List MVarId := []',1)
s=s.replace('Lean.Elab.Term.TermElabM.run (s := p.termState)','Lean.Elab.Term.TermElabM.run (ctx := p.termContext) (s := p.termState)',1)
s=s.replace('      termContext := {}','      termContext := { declName? := ctx.parentDecl? }',1)
s=s.replace('      tacticContext := { elaborator := .anonymous } }','      tacticContext := { elaborator := .anonymous }\n      initialGoals := goals }',1)
marker='/-- Pretty print the current goals in the `ProofSnapshot`. -/'
check='''/-- Verify each original closed root using the ordinary native kernel. -/
def kernelCheckClosed (p : ProofSnapshot) : IO Bool := do
  if !p.tacticState.goals.isEmpty || p.initialGoals.isEmpty then return false
  let (checked, _) ← p.runMetaM do
    for root in p.initialGoals do
      root.withContext do
        let value ← instantiateMVars (.mvar root)
        if value.hasMVar || value.hasLevelMVar then throwError "unresolved proof"
        let mut locals : Array Expr := #[]
        for decl in (← getLCtx) do
          locals := locals.push (.fvar decl.fvarId)
        let value ← Meta.mkLambdaFVars locals value
        let type ← Meta.mkForallFVars locals (← root.getType)
        let levels := ((collectLevelParams {} type).collect value).params.toList
        let name ← mkFreshUserName `gpuSmtCheckedPrefix
        let decl := Declaration.thmDecl {name,levelParams := levels,type,value}
        match (← getEnv).addDeclCore 0 decl with
        | .ok _ => pure ()
        | .error _ => throwError "native kernel rejected closed root"
    return true
  return checked

'''
assert marker in s
s=s.replace(marker,check+marker,1);p.write_text(s)
p=DST/'REPL/JSON.lean';s=(SRC/p.relative_to(DST)).read_text()
s=s.replace('  tactic : String\nderiving','  tactic : String\n  declName : Option String := none\nderiving',1)
s=s.replace('structure ProofStepResponse where\n','structure ProofStepResponse where\n  kernelChecked : Bool := false\n',1)
s=s.replace('[("proofState", r.proofState)]','[("proofState", r.proofState),("kernelChecked",toJson r.kernelChecked)]',1)
p.write_text(s)
p=DST/'REPL/Main.lean';s=(SRC/p.relative_to(DST)).read_text()
s=s.replace("let proofState' ← proofState.runString s.tactic","""let configuredProofState : ProofSnapshot := {
        proofState with
        coreContext := { proofState.coreContext with maxHeartbeats := 0 }
        termContext := { proofState.termContext with declName? := (s.declName.map String.toName).orElse (fun _ => proofState.termContext.declName?) }
      }
      let proofState' ← configuredProofState.runString s.tactic""",1)
s=s.replace('    proofState := id\n    goals :=','    proofState := id\n    kernelChecked := (← proofState.kernelCheckClosed)\n    goals :=',1)
p.write_text(s)
# Native warm batch and proof-step batch: same immutable input state per native task.
p=DST/'REPL/JSON.lean';s=p.read_text()
s += """
namespace REPL
structure NativeCommandBatch extends CommandOptions where
  env : Nat
  cmds : Array String
deriving FromJson
structure NativeProofBatch where
  proofSteps : Array ProofStep
deriving FromJson
structure ClearProofSnapshots where
  clearProofSnapshots : Bool
deriving FromJson
end REPL
"""
p.write_text(s)
p=DST/'REPL/Main.lean';s=p.read_text()
marker='/--\nRun a single tactic,'
# Native batch of unchanged full commands; state returned by each candidate is discarded.
code="""
def nativeCommandBatch (b : NativeCommandBatch) : M IO Json := do
  let initial ← get
  let tasks ← b.cmds.mapM fun cmd => IO.asTask do
    let (answer, _) ← (runCommand {
      toCommandOptions := b.toCommandOptions, env := some b.env, cmd := cmd, ast := some false, tactics := some false, premises := some false, commandAST := some false }).run initial
    return match answer with | .inl x => toJson x | .inr x => toJson x
  let answers := tasks.map fun t => match t.get with
    | .ok x => x
    | .error e => toJson (Error.mk e.toString)
  return Json.mkObj [("results",Json.arr answers)]

"""
assert marker in s
s=s.replace(marker,code+marker,1)
marker='\nend REPL\n'
code="""

def nativeProofBatch (b : NativeProofBatch) : M IO Json := do
  let initial ← get
  let tasks ← b.proofSteps.mapM fun step => IO.asTask <| (runProofStep step).run initial
  let mut answers : Array Json := #[]
  for t in tasks do
    match t.get with
    | .ok (.inl answer, state) =>
      let id := (← get).proofStates.size
      if let some snapshot := state.proofStates.back? then
        modify fun s => {s with proofStates := s.proofStates.push snapshot}
        answers := answers.push (toJson {answer with proofState := id})
      else answers := answers.push (toJson (Error.mk "missing proof snapshot"))
    | .ok (.inr e, _) => answers := answers.push (toJson e)
    | .error e => answers := answers.push (toJson (Error.mk e.toString))
  return Json.mkObj [("results",Json.arr answers)]
"""
assert marker in s;s=s.replace(marker,code+marker,1)
s=s.replace('| command : REPL.Command → Input','| command : REPL.Command → Input\n| nativeBatch : REPL.NativeCommandBatch → Input\n| nativeProofBatch : REPL.NativeProofBatch → Input\n| clearProofSnapshots : REPL.ClearProofSnapshots → Input',1)
marker='    | .ok (r : REPL.Command) => return .command r'
new='''    | .ok (r : REPL.NativeCommandBatch) => return .nativeBatch r
    | .error _ => match fromJson? j with
    | .ok (r : REPL.NativeProofBatch) => return .nativeProofBatch r
    | .error _ => match fromJson? j with
    | .ok (r : REPL.ClearProofSnapshots) => return .clearProofSnapshots r
    | .error _ => match fromJson? j with
'''+marker
assert marker in s;s=s.replace(marker,new,1)
marker='  | .command r => return toJson (← runCommand r)'
new=marker+'''
  | .nativeBatch r => nativeCommandBatch r
  | .nativeProofBatch r => nativeProofBatch r
  | .clearProofSnapshots _ => do
    modify fun s => {s with proofStates := #[]}
    pure <| Json.mkObj [("cleared",Json.bool true)]'''
assert marker in s;s=s.replace(marker,new,1)
s=s.replace('  if query = "" then', '  if (Json.parse query >>= fun j => j.getObjValAs? Bool "quit").toOption.getD false then\n    IO.println (Json.mkObj [("bye",toJson true)]).compress\n    printFlush "\\n"\n    return ()\n  if query = "" then',1)
p.write_text(s)

env=dict(os.environ)
env['PATH']='/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux/bin:'+env['PATH']
with (U/'repl-build.log').open('w') as out:
    code=subprocess.run(['lake','build','repl'],cwd=DST,env=env,stdout=out,stderr=subprocess.STDOUT).returncode
(U/'repl-build.json').write_text(json.dumps({'source':str(SRC),'private':str(DST),'exit_code':code,'changes':'SHRED snapshot context + captured initial goals + closed-root native kernel check'},indent=2)+'\n')
raise SystemExit(code)
