/- Native candidate backend for the finite E038 service experiment.
   Original REPL command/source response path; no general FFI isolation claim. -/
import REPL.Main

open Lean
namespace NativeBranchBackend
@[extern "gpu_smt_prepare_refs"] opaque prepareRefs : IO Unit
@[extern "gpu_smt_branch_begin"] opaque beginBranch (enabled : Bool) : IO UInt64
@[extern "gpu_smt_branch_end"] opaque endBranch (handle : UInt64) : IO String
@[extern "gpu_smt_emit_line"] opaque emitLine (line : String) : IO Unit

unsafe def execute (base : REPL.State) (enabled : Bool) (query : String) : IO Unit := do
  let json ← IO.ofExcept (Json.parse query)
  let id := (json.getObjValAs? String "custom_id").toOption.getD ""
  let request ← IO.ofExcept (fromJson? json : Except String REPL.Command)
  let before ← IO.monoNanosNow
  let handle ← beginBranch enabled
  let response ← try
    let (response, _) ← (REPL.runCommand request).run base
    pure (toJson response)
  catch exception => pure (Json.mkObj [("error", toJson exception.toString)])
  let ready ← IO.monoNanosNow
  let branch ← endBranch handle
  let released ← IO.monoNanosNow
  let branch := (Json.parse branch).toOption.getD Json.null
  emitLine ((Json.mkObj [
    ("custom_id",toJson id), ("response",response), ("branch",branch),
    ("internal_ready_ns",toJson (ready-before)),
    ("released_ns",toJson (released-before))]).compress)

@[export gpu_smt_native_backend]
unsafe def run (_ : List String) : IO Unit := do
  initSearchPath (← Lean.findSysroot)
  if let some manifest ← IO.getEnv "LEAN_SERVER_NATIVE_DYNLIB" then
    for library in (← IO.FS.readFile manifest).splitOn "\n" do
      unless library.isEmpty do Lean.loadDynlib library
  let enabled := (← IO.getEnv "GPU_SMT_BRANCH_OFF") != some "1"
  let initial ← getLines
  let header ← match ← parse initial with
    | .command command => pure command
    | _ => throw (IO.userError "first command must prepare the original import root")
  let (response, base) ← (REPL.runCommand header).run {}
  emitLine (toJson response).compress
  prepareRefs
  let mut tasks : Array (Task (Except IO.Error Unit)) := #[]
  repeat
    let query ← getLines
    if query.isEmpty then break
    let task ← IO.asTask (execute base enabled query)
    tasks := tasks.push task
  for task in tasks do
    IO.ofExcept task.get
end NativeBranchBackend
