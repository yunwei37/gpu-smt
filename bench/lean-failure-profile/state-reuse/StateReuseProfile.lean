/- Opt-in measurement only. Never substitutes a tactic result or rejects a goal. -/
import Lean
import Init.System.Mutex
import Init.Util

open Lean Meta Elab Tactic

namespace GpuSmt.StateReuseProfile

/-- Keep strong references: an address reused after collection cannot alias an old environment. -/
unsafe def sameEnvironmentImpl (a b : Environment) : Bool := ptrEq a b

@[implemented_by sameEnvironmentImpl]
opaque sameEnvironment (a b : Environment) : Bool := false

/-- This is an observed input key, not a complete replay-state certificate.
The environment identity includes opaque extension state within this process.
Expressions use structural equality (not Expr's alpha-equivalence instance).
No digest or pretty-printed goal establishes a match. -/
structure Key where
  environment : Nat
  options : Options
  metadata : String
  expressions : Array ExprStructEq
  deriving BEq, Inhabited

structure Registry where
  environments : Array Environment := #[]
  keys : Array Key := #[]
  nextCall : Nat := 0
  deriving Inhabited

initialize registry : IO.Mutex Registry ← IO.Mutex.new {}

/-- Only immutable keys/identities are registered under this lock.
No tactic, expression construction, output or native search executes under it. -/
private def environmentId (env : Environment) : IO Nat :=
  registry.atomically do
    let s ← get
    let mut i := 0
    for existing in s.environments do
      if sameEnvironment existing env then return i
      i := i + 1
    set { s with environments := s.environments.push env }
    return i

private def register (key : Option Key) : IO (Nat × Option Nat) :=
  registry.atomically do
    let mut s ← get
    let call := s.nextCall
    s := { s with nextCall := call + 1 }
    let mut found := none
    if let some key := key then
      for i in [:s.keys.size] do
        if s.keys[i]! == key then
          found := some i
          break
      if found.isNone then
        found := some s.keys.size
        s := { s with keys := s.keys.push key }
    set s
    return (call, found)

private partial def nameIdentity : Name → Json
  | .anonymous => Json.arr #[toJson ("anonymous" : String)]
  | .str parent value => Json.arr #[toJson ("str" : String), nameIdentity parent, toJson value]
  | .num parent value => Json.arr #[toJson ("num" : String), nameIdentity parent, toJson value]

private def openIdentity : OpenDecl → Json
  | .simple name except => Json.arr #[toJson ("simple" : String), nameIdentity name,
                                     toJson (except.map nameIdentity)]
  | .explicit name decl => Json.arr #[toJson ("explicit" : String), nameIdentity name,
                                      nameIdentity decl]

private def resolvedIdentity : Syntax.Preresolved → Json
  | .namespace name => Json.arr #[toJson ("namespace" : String), nameIdentity name]
  | .decl name fields => Json.arr #[toJson ("decl" : String), nameIdentity name, toJson fields]

private partial def syntaxIdentity : Syntax → Json
  | .missing => toJson ("missing" : String)
  | .node _ kind args => Json.arr #[toJson ("node" : String), nameIdentity kind,
                                    Json.arr (args.map syntaxIdentity)]
  | .atom _ value => Json.arr #[toJson ("atom" : String), toJson value]
  | .ident _ raw name resolved => Json.arr #[toJson ("ident" : String),
      toJson raw.toString, nameIdentity name, toJson (resolved.map resolvedIdentity)]

private def configIdentity (c : Meta.Config) : Json :=
  Json.arr #[toJson c.foApprox, toJson c.ctxApprox, toJson c.quasiPatternApprox,
    toJson c.constApprox, toJson c.isDefEqStuckEx, toJson c.unificationHints,
    toJson c.proofIrrelevance, toJson c.assignSyntheticOpaque, toJson c.offsetCnstrs,
    toJson (reprStr c.transparency), toJson c.trackZetaDelta,
    toJson (reprStr c.etaStruct), toJson c.univApprox]

/-- Canonicalize only free-variable identity. Preserve ordered declaration metadata,
let values, binder names/annotations, all goals, and local-instance order.
Unresolved expression/universe metavariables and out-of-context fvars are unsupported.
This does not certify that hidden elaborator state or resource budgets are replayable. -/
private def inputKey (stx : Syntax) : TacticM (Option Key × String) := do
  let envId ← environmentId (← getEnv)
  let mut metadata : Array Json := #[syntaxIdentity stx]
  let mut expressions : Array ExprStructEq := #[]
  let core ← readThe Core.Context
  let meta ← readThe Meta.Context
  let tactic ← readThe Tactic.Context
  metadata := metadata ++ #[nameIdentity core.currNamespace,
    toJson (core.openDecls.map openIdentity), configIdentity meta.config,
    toJson meta.synthPendingDepth, toJson meta.univApprox,
    toJson meta.inTypeClassResolution, toJson tactic.recover]
  if meta.canUnfold?.isSome || meta.defEqCtx?.isSome then
    return (none, "custom_unfold_or_defeq_context")
  for goal in (← getGoals) do
    let decl ← goal.getDecl
    let mut fvars : Array Expr := #[]
    let mut locals : Array Json := #[]
    for localDecl in decl.lctx do
      fvars := fvars.push (mkFVar localDecl.fvarId)
      let type ← instantiateMVars localDecl.type
      let type := type.abstract fvars
      if type.hasMVar || type.hasFVar then return (none, "unresolved_local_type")
      expressions := expressions.push ⟨type⟩
      if let .ldecl _ _ _ _ value _ _ := localDecl then
        let value := (← instantiateMVars value).abstract fvars
        if value.hasMVar || value.hasFVar then return (none, "unresolved_let_value")
        expressions := expressions.push ⟨value⟩
      let tag := match localDecl with
        | .cdecl _ _ name _ binder kind =>
          Json.arr #[toJson ("variable" : String), nameIdentity name,
                            toJson (reprStr binder), toJson (reprStr kind)]
        | .ldecl _ _ name _ _ nonDep kind =>
          Json.arr #[toJson ("let" : String), nameIdentity name,
                            toJson nonDep, toJson (reprStr kind)]
      locals := locals.push tag
    let target := (← instantiateMVars decl.type).abstract fvars
    if target.hasMVar || target.hasFVar then return (none, "unresolved_target")
    expressions := expressions.push ⟨target⟩
    let mut instances : Array Json := #[]
    for inst in decl.localInstances do
      let expression := (← instantiateMVars inst.fvar).abstract fvars
      if expression.hasMVar || expression.hasFVar then return (none, "unresolved_instance")
      expressions := expressions.push ⟨expression⟩
      instances := instances.push (nameIdentity inst.className)
    metadata := metadata.push <| Json.arr #[nameIdentity decl.userName,
      toJson decl.depth, toJson (reprStr decl.kind), toJson decl.numScopeArgs,
      Json.arr locals, Json.arr instances]
  return (some { environment := envId, options := ← getOptions,
                 metadata := (Json.arr metadata).compress, expressions }, "observed_input_only")

private def emit (fields : List (String × Json)) : IO Unit :=
  IO.eprintln <| "[gpu-smt-state-reuse] " ++ (Json.mkObj fields).compress

/-- Run the original tactic and rethrow its original exception unchanged.
A normal return need not close a goal; an internal exception is never cached.
Timestamps/heartbeats below are observations, not a replay implementation. -/
elab (name := observeState) "observe_state " inner:tactic : tactic => do
  let captureStart ← IO.monoNanosNow
  let (key, eligibility) ← inputKey inner.raw
  let (call, keyId) ← register key
  let captureNs := (← IO.monoNanosNow) - captureStart
  emit [("event", toJson ("begin" : String)), ("call", toJson call),
        ("key", toJson keyId), ("eligibility", toJson eligibility),
        ("source", toJson (← readThe Core.Context).fileName),
        ("byte", toJson (inner.raw.getPos?.map (·.byteIdx))),
        ("kind", toJson inner.raw.getKind.toString), ("capture_ns", toJson captureNs),
        ("replay_qualified", toJson false)]
  let errorsBefore := (← getThe Core.State).messages.toList.filter (fun m => m.severity == .error) |>.length
  let start ← IO.monoNanosNow
  let hb ← IO.getNumHeartbeats
  let failure ← tryCatchRuntimeEx
    (do evalTactic inner; pure (none : Option Exception))
    (fun ex => pure (some ex))
  let used := (← IO.getNumHeartbeats) - hb
  let elapsed := (← IO.monoNanosNow) - start
  let errorsAfter := (← getThe Core.State).messages.toList.filter (fun m => m.severity == .error) |>.length
  let outcome := match failure with
    | none => "returned"
    | some ex => if ex.isMaxHeartbeat then "heartbeat_limit"
      else if ex.isMaxRecDepth then "recursion_limit"
      else if ex.isInterrupt then "interrupted"
      else match ex with | .error .. => "native_error" | _ => "internal_exception"
  emit [("event", toJson ("end" : String)), ("call", toJson call),
        ("key", toJson keyId), ("outcome", toJson outcome),
        ("elapsed_ns", toJson elapsed), ("heartbeats", toJson used),
        ("remaining_goals", toJson (← getGoals).length),
        ("new_error_messages", toJson (errorsAfter - errorsBefore)),
        ("replay_qualified", toJson false)]
  if let some ex := failure then throw ex

end GpuSmt.StateReuseProfile
