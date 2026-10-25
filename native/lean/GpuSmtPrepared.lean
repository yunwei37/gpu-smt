/- Engine-owned import preparation for a pinned stock REPL dependency.
   Imported FFI/initializers must be audited for the declared prepared context.
   Candidate commands run only in disposable OS children, never in the parent. -/
import REPL.Main

open Lean Lean.Elab

namespace GpuSmtPrepared

structure Root where
  imports : String
  env : Environment
  messages : MessageLog

@[export gpu_smt_prepared_create]
unsafe def create (encoded sysroot : String) : IO Root := do
  initSearchPath sysroot
  enableInitializersExecution
  let code ← IO.ofExcept (Json.parse encoded >>= fromJson? (α := String))
  let context := Parser.mkInputContext code "<input>"
  let (header, parser, messages) ← Parser.parseHeader context
  let (env, messages) ← processHeader header {} messages context
  if messages.hasErrors then
    throw <| IO.userError "native header import failed; use original frontend"
  return { imports := code.extract 0 parser.pos, env, messages }


@[export gpu_smt_prepared_stats]
def stats (root : Root) : String :=
  (Json.mkObj [
    ("imported_modules", toJson root.env.header.moduleNames.size),
    ("header_errors", toJson root.messages.hasErrors)]).compress

@[export gpu_smt_prepared_check]
unsafe def check (root : Root) (encoded : String) : IO String := do
  let code ← IO.ofExcept (Json.parse encoded >>= fromJson? (α := String))
  let context := Parser.mkInputContext code "<input>"
  let (_, parser, _) ← Parser.parseHeader context
  -- Different parsed import bytes use the original fresh-process backend.
  if code.extract 0 parser.pos != root.imports then
    return (Json.mkObj [("fallback", toJson true)]).compress
  let command := Command.mkState root.env root.messages {}
  let (_, messages, trees) ← IO.processCommandsWithInfoTrees context parser command
  let messages ← messages.mapM REPL.Message.of
  let (sorries, _) ← (REPL.sorries trees none).run {}
  let response : REPL.CommandResponse := { env := 0, messages, sorries }
  return (Json.mkObj [("native", toJson response)]).compress

end GpuSmtPrepared
