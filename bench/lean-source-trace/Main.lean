import Lean

open Lean Elab

-- Elaborate the original file normally and retain parser-observed command
-- boundaries. This avoids guessing proof ends using a source-code regex.
unsafe def main (args : List String) : IO Unit := do
  let [path] := args | throw <| IO.userError "expected one source file"
  Lean.initSearchPath (← Lean.findSysroot)
  enableInitializersExecution
  let input ← IO.FS.readFile path
  let inputCtx := Parser.mkInputContext input path
  let (header, parserState, messages) ← Parser.parseHeader inputCtx
  let (env, messages) ← processHeader header {} messages inputCtx
  let state ← IO.processCommands inputCtx parserState (Command.mkState env messages {})
  let spans := state.commands.filterMap fun cmd => do
    let start ← cmd.getPos?
    let stop ← cmd.getTailPos?
    return Json.mkObj [("start", toJson start.byteIdx), ("stop", toJson stop.byteIdx),
                        ("kind", toJson cmd.getKind.toString)]
  let errors := state.commandState.messages.toList.filter (·.severity == .error)
  let messages ← errors.mapM fun m => m.data.toString
  IO.println <| (Json.mkObj [("commands", toJson spans), ("errors", toJson messages)]).compress
  if !errors.isEmpty then throw <| IO.userError "source elaboration failed"
