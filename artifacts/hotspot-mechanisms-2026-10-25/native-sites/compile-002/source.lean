/- Native parser inspection only. No candidate command is elaborated. -/
import Lean.Elab.Import
import Lean.Parser.Module

open Lean

unsafe def sites (source : String) (stx : Syntax)
    (ancestors : Array String := #[]) : Array Json := Id.run do
  let mut result := #[]
  let kind := stx.getKind.toString
  if kind == "Lean.Parser.Tactic.simpAll" ||
     kind == "Mathlib.Tactic.intervalCases" then
    if let some start := stx.getPos? then
      if let some stop := stx.getTailPos? then
        result := result.push (Json.mkObj [
          ("kind", toJson kind), ("start_byte", toJson start.byteIdx),
          ("end_byte", toJson stop.byteIdx),
          ("text", toJson (source.extract start stop)),
          ("ancestors", toJson ancestors)])
  for child in stx.getArgs do
    result := result ++ sites source child (ancestors.push kind)
  return result

unsafe def main (args : List String) : IO Unit := do
  let [input, output] := args | throw (IO.userError "usage: HotspotSites INPUT OUTPUT")
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let preparation := Parser.mkInputContext "import Mathlib\nimport SimpAllProfile\n" "<setup>"
  let (header, _, messages) ← Parser.parseHeader preparation
  let (env, messages) ← Elab.processHeader header {} messages preparation
  if messages.hasErrors then throw (IO.userError "native setup import failed")
  let rows ← IO.ofExcept (Json.parse (← IO.FS.readFile input) >>= fromJson? (α := Array Json))
  let mut results := #[]
  for row in rows do
    let id ← IO.ofExcept (row.getObjValAs? String "id")
    let source ← IO.ofExcept (row.getObjValAs? String "code")
    -- Disable CRLF normalization: byte offsets always address retained bytes.
    let context := Parser.mkInputContext source id (normalizeLineEndings := false)
    let (_, initial, messages) ← Parser.parseHeader context
    let mut state := initial
    let mut messages := messages
    let mut found := #[]
    let mut commands := #[]
    repeat
      let (stx, next, msgs) := Parser.parseCommand context { env, options := {} } state messages
      state := next
      messages := msgs
      if Parser.isTerminalCommand stx then break
      commands := commands.push stx.getKind.toString
      found := found ++ sites source stx
    let mut errors := #[]
    for message in messages.toList do
      errors := errors.push (← message.toString)
    results := results.push (Json.mkObj [
      ("id", toJson id), ("sites", toJson found), ("command_kinds", toJson commands),
      ("parse_errors", toJson messages.hasErrors), ("messages", toJson errors),
      ("candidate_elaborated", toJson false)])
  IO.FS.writeFile output (Json.pretty (toJson results))
