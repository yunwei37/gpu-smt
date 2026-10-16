/-
Copyright (c) 2023 Scott Morrison. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Scott Morrison
-/
import Lean.Elab.Frontend

open Lean Elab

namespace Lean.Elab.IO

/--
Wrapper for `IO.processCommands` that enables info states, and returns
* the new command state
* messages
* info trees
-/
def processCommandsWithInfoTrees
    (inputCtx : Parser.InputContext) (parserState : Parser.ModuleParserState)
    (commandState : Command.State) : IO (Command.State × List Message × List InfoTree) := do
  let commandState := { commandState with infoState.enabled := true }
  let profileStart ← IO.monoNanosNow
  let st ← IO.processCommandsIncrementally inputCtx parserState commandState none
  let traceStates := (Language.toSnapshotTree st.initialSnap).getAll.map (·.traces)
  let profile ← Firefox.Profile.export inputCtx.inputString (profileStart.toFloat / 1000000000) traceStates commandState.scopes.head!.opts
  let profileDirectory := (← IO.getEnv "LEAN_SERVER_PROFILE_DIRECTORY").getD "/tmp/lean-native-profiles"
  IO.FS.createDirAll profileDirectory
  let profilePath : System.FilePath := (System.FilePath.mk profileDirectory) / s!"{profileStart}.json"
  IO.FS.writeFile profilePath (Json.compress (toJson profile))
  let compressed ← IO.Process.output { cmd := "gzip", args := #["-f", profilePath.toString] }
  if compressed.exitCode != 0 then
    throw <| IO.userError s!"profile gzip failed: {compressed.stderr}"
  (← IO.getStderr).putStrLn ("LEAN_NATIVE_PROFILE " ++ profilePath.toString ++ ".gz")
  let s := st.commandState
  pure (s, s.messages.toList, s.infoState.trees.toList)

/--
Process some text input, with or without an existing command state.
If there is no existing environment, we parse the input for headers (e.g. import statements),
and create a new environment.
Otherwise, we add to the existing environment.

Returns the resulting command state, along with a list of messages and info trees.
-/
def processInput (input : String) (cmdState? : Option Command.State)
    (opts : Options := {}) (fileName : Option String := none) :
    IO (Command.State × List Message × List InfoTree) := unsafe do
  Lean.initSearchPath (← Lean.findSysroot)
  enableInitializersExecution
  let fileName   := fileName.getD "<input>"
  let inputCtx   := Parser.mkInputContext input fileName
  let (parserState, commandState) ← match cmdState? with
  | none => do
    let (header, parserState, messages) ← Parser.parseHeader inputCtx
    let (env, messages) ← processHeader header opts messages inputCtx
    pure (parserState, (Command.mkState env messages opts))
  | some cmdState => do
    pure ({ : Parser.ModuleParserState }, cmdState)
  processCommandsWithInfoTrees inputCtx parserState commandState

/-
  asTask but with a timeout
-/
def withTimeout {α : Type} (act : IO α) (timeoutMs : Nat) (prio := Task.Priority.default) : IO (Except IO.Error α) := do
  let task ← IO.asTask act prio
  let timeoutTask ← IO.asTask (do
      IO.sleep timeoutMs.toUInt32
      throw <| IO.userError s!"Operation timed out"
  )
  match ← IO.waitAny [task, timeoutTask] with
    | .ok a => do
      IO.cancel timeoutTask
      return .ok a
    | .error e =>
      IO.cancel task
      throw e
