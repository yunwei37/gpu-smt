import Mathlib
import Aesop
import Lean.Elab.Frontend
set_option maxHeartbeats 200000
set_option maxRecDepth 4000
open Lean Elab Command
@[extern "m_cpu_ns"] opaque mCpuNS : IO UInt64
namespace MechanismDAG

partial def levelDeps (l : Level) : List String :=
  match l with
  | .mvar id => ["u:" ++ id.name.toString]
  | .succ l => levelDeps l
  | .max a b | .imax a b => levelDeps a ++ levelDeps b
  | _ => []

partial def exprDeps (e : Expr) : List String :=
  match e with
  | .mvar id => ["e:" ++ id.name.toString]
  | .sort l => levelDeps l
  | .const _ ls => ls.bind levelDeps
  | .app a b => exprDeps a ++ exprDeps b
  | .lam _ t b _ | .forallE _ t b _ => exprDeps t ++ exprDeps b
  | .letE _ t v b _ => exprDeps t ++ exprDeps v ++ exprDeps b
  | .mdata _ e | .proj _ _ e => exprDeps e
  | _ => []

partial def exprMVars (e : Expr) : List MVarId :=
  match e with
  | .mvar id => [id]
  | .app a b => exprMVars a ++ exprMVars b
  | .lam _ t b _ | .forallE _ t b _ => exprMVars t ++ exprMVars b
  | .letE _ t v b _ => exprMVars t ++ exprMVars v ++ exprMVars b
  | .mdata _ e | .proj _ _ e => exprMVars e
  | _ => []

/-- Conservative closure over all local declarations, not a dynamic read set. -/
partial def goalDeps (ctx : MetavarContext) (todo : List MVarId)
    (seen : List MVarId := []) (deps : List String := []) : List String :=
  match todo with
  | [] => deps.eraseDups
  | g :: gs =>
    if seen.contains g then goalDeps ctx gs seen deps else
    let decl := ctx.decls.find? g
    let expressions := match decl with
      | none => []
      | some d => d.type :: d.lctx.foldl
          (fun es ld => ld.type :: (ld.value?.toList ++ es)) []
    let expressions := (ctx.eAssignment.find? g).toList ++ expressions
    let more := expressions.bind exprDeps
    let goals := expressions.bind exprMVars
    let pending := (ctx.dAssignment.find? g).toList.map (·.mvarIdPending)
    goalDeps ctx (goals ++ pending ++ gs) (g :: seen)
      (("e:" ++ g.name.toString) :: more ++ deps)

def goalJson (ctx : MetavarContext) (gs : List MVarId) : Json :=
  toJson (gs.map fun g => (g.name.toString, goalDeps ctx [g]))

partial def infoJson : InfoTree → Json
  | .context _ t => infoJson t
  | .hole id => Json.mkObj [("hole", toJson id.name.toString)]
  | .node info children =>
    let fields := match info with
      | .ofTacticInfo i =>
        [("kind", toJson i.stx.getKind.toString),
         ("startByte", toJson (i.stx.getPos?.map (·.byteIdx))),
         ("stopByte", toJson (i.stx.getTailPos?.map (·.byteIdx))),
         ("before", goalJson i.mctxBefore i.goalsBefore),
         ("after", goalJson i.mctxAfter i.goalsAfter)]
      | _ => []
    Json.mkObj (fields ++ [("children", toJson (children.toArray.map infoJson))])

partial def traceJson : MessageData → Array Json
  | .withContext _ m | .withNamingContext _ m | .nest _ m | .group m
      | .tagged _ m | .ofWidget _ m => traceJson m
  | .compose a b => traceJson a ++ traceJson b
  | .trace d _ children =>
    let cs := children.foldl (fun acc child => acc ++ traceJson child) #[]
    if d.cls == `Elab.step then
      #[Json.mkObj [("kind", toJson d.tag),("startSeconds",toJson (toString d.startTime)),
        ("stopSeconds",toJson (toString d.stopTime)),("children",toJson cs)]]
    else cs
  | _ => #[]

elab "measure_dag " path:str : command => do
  let env ← getEnv
  let content ← IO.FS.readFile path.getString
  let json ← match Json.parse content with
    | .ok j => pure j
    | .error e => throwError "{e}"
  let cases ← match json.getArr? with
    | .ok a => pure a
    | .error e => throwError "{e}"
  for c in cases do
    let id := (c.getObjValAs? String "id").toOption.getD "unknown"
    let code := (c.getObjValAs? String "code").toOption.getD ""
    let mode := (c.getObjValAs? String "mode").toOption.getD "observe"
    let opts := ({} : Options) |>.setNat `maxHeartbeats 3000
      |>.setBool `trace.profiler (mode == "observe") |>.setNat `trace.profiler.threshold 0
    let cpuStart ← mCpuNS
    let start ← IO.monoNanosNow
    let state ← IO.processCommands (Parser.mkInputContext code id)
      {} (Command.mkState env {} opts)
    let stop ← IO.monoNanosNow
    let cpuStop ← mCpuNS
    let mut traces := #[]
    for message in state.commandState.messages.toList do
      traces := traces ++ traceJson message.data
    let mut errors : Array String := #[]
    for m in state.commandState.messages.toList do
      if m.severity == .error then
        errors := errors.push (← m.data.toString)
    let obj := Json.mkObj [("mode",toJson mode),("errors",toJson errors),("id",toJson id),("wallNanoseconds",toJson (stop-start)),("cpuNanoseconds",toJson (cpuStop-cpuStart).toNat),
      ("hasErrors",toJson state.commandState.messages.hasErrors),
      ("infos",toJson (state.commandState.infoState.trees.toArray.map infoJson)),
      ("traces",toJson traces)]
    IO.println ("M_DAG " ++ obj.compress)
    (← IO.getStdout).flush
end MechanismDAG

measure_dag "/workspaces/repository/research/mechanisms-2026-10-30/dag200-input.json"
