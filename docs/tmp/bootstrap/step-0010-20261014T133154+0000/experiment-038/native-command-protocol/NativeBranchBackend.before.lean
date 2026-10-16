/- Native stateless candidate backend using the stock Kimina BatchCommand protocol.
   Branch metadata is separate from native responses; general FFI remains unqualified. -/
import REPL.Main

open Lean
namespace NativeBranchBackend
@[extern "gpu_smt_prepare_refs"] opaque prepareRefs : IO Unit
@[extern "gpu_smt_branch_begin"] opaque beginBranch (enabled : Bool) : IO UInt64
@[extern "gpu_smt_branch_end"] opaque endBranch (handle : UInt64) : IO String
@[extern "gpu_smt_emit_line"] opaque emitLine (line : String) : IO Unit

unsafe def execute (base : REPL.State) (enabled : Bool) (header query : String) : IO Json := do
  let json ← IO.ofExcept (Json.parse query)
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
  let needsFallback := (branch.getObjValAs? Bool "fallback").toOption.getD false
  let mut finalResponse := response
  let mut fallbackResult := Json.null
  if needsFallback then
    let executable ← IO.getEnv "GPU_SMT_FALLBACK_REPL"
    let libraryPath ← IO.getEnv "GPU_SMT_FALLBACK_LIBRARY_PATH"
    match executable, libraryPath with
    | some executable, some libraryPath =>
      let output ← IO.Process.output {
        cmd := executable
        env := #[("LD_LIBRARY_PATH", some libraryPath), ("GPU_SMT_BRANCH_OFF", none)]
      } (some (header.trimAscii.toString ++ "\n\n" ++ query.trimAscii.toString ++ "\n\n"))
      finalResponse := Json.mkObj [("error",toJson "original fallback returned no native frame")]
      let mut nativeFrames := 0
      for frame in output.stdout.splitOn "\n\n" do
        if let .ok parsed := Json.parse frame then
          nativeFrames := nativeFrames + 1
          finalResponse := parsed
      if output.exitCode != 0 || nativeFrames < 2 then
        finalResponse := Json.mkObj [("error",toJson "original fallback terminated without candidate response")]
      fallbackResult := Json.mkObj [
        ("exit_code",toJson output.exitCode.toNat),("stdout",toJson output.stdout),
        ("stderr",toJson output.stderr)]
    | _, _ =>
      finalResponse := Json.mkObj [("error",toJson "original fallback path is not configured")]
  let completed ← IO.monoNanosNow
  return Json.mkObj [
    ("response",finalResponse), ("branch",branch),
    ("discarded_response",if needsFallback then response else Json.null),
    ("fallback_result",fallbackResult),("completed_ns",toJson (completed-before)),
    ("internal_ready_ns",toJson (ready-before)),("released_ns",toJson (released-before))]

unsafe def batch (base : REPL.State) (enabled : Bool) (header : String)
    (json : Json) : IO Unit := do
  let request ← IO.ofExcept (fromJson? json : Except String REPL.BatchCommand)
  unless request.env == some 0 && request.mode == some "naive" && request.timeout.isNone do
    throw (IO.userError "this experiment supports the prepared env=0 naive batch without internal timeout")
  let tasks ← request.cmds.mapM fun cmd => do
    let command : REPL.Command := {
      toCommandOptions := request.toCommandOptions, env := some 0, cmd, gc := some true }
    IO.asTask (execute base enabled header (toJson command).compress)
  let mut responses := #[]
  let mut metadata := #[]
  for task in tasks do
    let result ← IO.ofExcept task.get
    responses := responses.push ((result.getObjVal? "response").toOption.getD Json.null)
    metadata := metadata.push (Json.mkObj [
      ("branch",(result.getObjVal? "branch").toOption.getD Json.null),
      ("completed_ns",(result.getObjVal? "completed_ns").toOption.getD Json.null),
      ("internal_ready_ns",(result.getObjVal? "internal_ready_ns").toOption.getD Json.null),
      ("released_ns",(result.getObjVal? "released_ns").toOption.getD Json.null),
      ("discarded_response",(result.getObjVal? "discarded_response").toOption.getD Json.null),
      ("fallback_result",(result.getObjVal? "fallback_result").toOption.getD Json.null)])
  let err ← IO.getStderr
  err.putStrLn ((Json.mkObj [("gpu_smt_batch",Json.arr metadata)]).compress)
  err.flush
  emitLine (Json.arr responses).compress

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
  prepareRefs
  emitLine (toJson response).compress
  repeat
    let query ← getLines
    if query.trimAscii.toString.isEmpty then break
    let json ← IO.ofExcept (Json.parse query)
    if (json.getObjVal? "cmds").isOk then
      batch base enabled initial json
    else
      emitLine (← execute base enabled initial query).compress
end NativeBranchBackend
