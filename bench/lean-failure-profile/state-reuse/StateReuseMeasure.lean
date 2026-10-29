/- Native original-source parsing/front-end execution. No proof-result reuse. -/
import StateReuseProfile
import Lean.Elab.Import
import Lean.Parser.Module
import Lean.Elab.Frontend

open Lean Elab

private def expensive (k : Name) : Bool :=
  k == `nlinarith || k == `Mathlib.Tactic.intervalCases ||
  k == `Lean.Parser.Tactic.simpAll || k == `Mathlib.Tactic.normNum

/-- Wrap only the outer native tactic sequence units; never recurse inside a unit.
Preserve native source positions/text and all syntax children. No old extractor
offsets and no textual proof parsing authorize insertion. -/
private partial def wrapSequence (stx : Syntax) : Syntax × Nat := Id.run do
  let k := stx.getKind
  if k == `Lean.Parser.Term.byTactic then
    let (child, count) := wrapSequence stx[1]
    return (stx.setArg 1 child, count)
  if k == `Lean.Parser.Tactic.tacticSeq ||
     k == `Lean.Parser.Tactic.tacticSeq1Indented then
    let (child, count) := wrapSequence stx[0]
    return (stx.setArg 0 child, count)
  if k == nullKind then
    let mut args := stx.getArgs
    let mut count := 0
    for i in [:args.size] do
      if expensive args[i]!.getKind then
        args := args.set! i (mkNode `GpuSmt.StateReuseProfile.observeState
          #[mkAtom "observe_state", args[i]!])
        count := count + 1
    match stx with
    | .node info kind _ => return (.node info kind args, count)
    | _ => return (stx, 0)
  return (stx, 0)

private partial def observe (stx : Syntax) : Syntax × Nat := Id.run do
  if stx.getKind == `Lean.Parser.Term.byTactic then return wrapSequence stx
  let mut count := 0
  let mut args := stx.getArgs
  for i in [:args.size] do
    let (child, n) := observe args[i]!
    args := args.set! i child
    count := count + n
  match stx with
  | .node info kind _ => return (.node info kind args, count)
  | _ => return (stx, count)

private def emit (value : Json) : IO Unit := do
  let out ← IO.getStdout
  out.putStrLn value.compress
  out.flush

unsafe def main (args : List String) : IO Unit := do
  let (input, synchronized) ← match args with
    | [input] => pure (input, false)
    | [input, "ack"] => pure (input, true)
    | _ => throw (IO.userError "usage: StateReuseMeasure INPUT [ack]")
  let stdin ← IO.getStdin
  initSearchPath (← findSysroot)
  enableInitializersExecution
  if let some library ← IO.getEnv "LEAN_SERVER_NATIVE_DYNLIB" then
    Lean.loadDynlib library
  let rows ← IO.ofExcept (Json.parse (← IO.FS.readFile input) >>= fromJson? (α := Array Json))
  let mut headers : Array (String × Environment) := #[]
  for row in rows do
    if synchronized then
      if (← stdin.getLine) != "next\n" then
        throw (IO.userError "native request admission acknowledgement missing")
    let id ← IO.ofExcept (row.getObjValAs? String "id")
    let source ← IO.ofExcept (row.getObjValAs? String "code")
    let mode ← IO.ofExcept (row.getObjValAs? String "mode")
    emit <| Json.mkObj [("event", toJson ("candidate_begin" : String)),
                        ("id", toJson id), ("mode", toJson mode)]
    let context := Parser.mkInputContext source "<input>"
    let (_, initial, messages) ← Parser.parseHeader context
    let rawHeader := context.input.extract 0 initial.pos
    let setup := rawHeader ++ (if mode == "original" then "" else "\nimport StateReuseProfile\n")
    let mut env? := none
    for (text, env) in headers do
      if text == setup then env? := some env
    let env ← match env? with
      | some env => pure env
      | none => do
        let setupContext := Parser.mkInputContext setup "<native-imports>"
        let (header, _, setupMessages) ← Parser.parseHeader setupContext
        let (env, setupMessages) ← Elab.processHeader header {} setupMessages setupContext
        if setupMessages.hasErrors then throw (IO.userError "native setup import error")
        headers := headers.push (setup, env)
        pure env
    let mut parserState := initial
    let mut commandState := Command.mkState env messages {}
    -- Match the retained REPL Frontend.processCommandsWithInfoTrees.
    commandState := { commandState with infoState.enabled := true }
    let mut commands : Array Syntax := #[]
    let mut wrapped := 0
    let start ← IO.monoNanosNow
    repeat
      let scope := commandState.scopes.head!
      let pmctx : Parser.ParserModuleContext := {
        env := commandState.env, options := scope.opts,
        currNamespace := scope.currNamespace, openDecls := scope.openDecls }
      -- Follow the pinned native Frontend.processCommand order exactly:
      -- command start precedes parse;messages enter command state;EOI elaborates.
      let commandStart := parserState.pos
      let (stx, next, msgs) := Parser.parseCommand context pmctx parserState commandState.messages
      parserState := next
      commandState := { commandState with messages := msgs }
      commands := commands.push stx
      let terminal := Parser.isTerminalCommand stx
      let (stx, n) := if mode == "observe" then observe stx else (stx, 0)
      wrapped := wrapped + n
      let (_, front) ← (Frontend.elabCommandAtFrontend stx |>.run { inputCtx := context }).run {
        commandState := commandState, parserState := parserState,
        cmdPos := commandStart, commands := commands }
      commandState := front.commandState
      if terminal then break
    let mut diagnostics := #[]
    for message in commandState.messages.toList do
      diagnostics := diagnostics.push <| Json.mkObj [
        ("severity", toJson (match message.severity with | .error => "error" | .warning => "warning" | .information => "information")),
        ("text", toJson (← message.toString))]
    emit <| Json.mkObj [("event", toJson ("candidate_end" : String)),
      ("id", toJson id), ("mode", toJson mode),
      ("native_error", toJson commandState.messages.hasErrors),
      ("wrapped_outer_units", toJson wrapped), ("elapsed_ns", toJson ((← IO.monoNanosNow) - start)),
      ("diagnostics", Json.arr diagnostics), ("proof_result_reused", toJson false)]
