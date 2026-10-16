/- Experimental native setup for E038; not a production verifier service. -/
import REPL.Main

open Lean
namespace NativeBranchSetup
@[extern "gpu_smt_prepare_refs"] opaque prepareRefs : IO Unit
@[extern "gpu_smt_branch_begin"] opaque beginBranch (enabled : Bool) : IO UInt64
@[extern "gpu_smt_branch_end"] opaque endBranch (handle : UInt64) : IO String

initialize witness : IO.Ref Nat ← IO.mkRef 0

@[export gpu_smt_native_setup]
unsafe def run (_ : List String) : IO Unit := do
  initSearchPath (← Lean.findSysroot)
  if let some manifest ← IO.getEnv "LEAN_SERVER_NATIVE_DYNLIB" then
    for library in (← IO.FS.readFile manifest).splitOn "\n" do
      unless library.isEmpty do Lean.loadDynlib library
  let enabled := (← IO.getEnv "GPU_SMT_BRANCH_OFF") != some "1"
  let initial ← getLines
  let header ← match ← parse initial with
    | .command command => pure command
    | _ => throw (IO.userError "setup requires the original command header")
  let started ← IO.monoNanosNow
  let (prepared, base) ← (REPL.runCommand header).run {}
  IO.println s!"PREPARE {toJson prepared}"
  prepareRefs
  let preparedAt ← IO.monoNanosNow
  IO.println s!"PREPARE_NS {preparedAt - started}"
  if let some path ← IO.getEnv "GPU_SMT_MAP_RECEIPT" then
    IO.FS.writeFile path (← IO.FS.readFile "/proc/self/maps")
  let query ← getLines
  let request ← match ← parse query with
    | .command command => pure command
    | _ => throw (IO.userError "setup requires an original command")
  let before ← IO.monoNanosNow
  let branch ← beginBranch enabled
  let response ← try
    let (response, _) ← (REPL.runCommand request).run base
    pure (toJson response).compress
  catch e => pure s!"EXCEPTION {e}"
  let responseAt ← IO.monoNanosNow
  let counts ← endBranch branch
  let releasedAt ← IO.monoNanosNow
  IO.println s!"RESPONSE {response}"
  IO.println s!"COUNTERS {counts}"
  IO.println s!"TIMING_NS response={responseAt-before} complete={releasedAt-before}"
  -- One integrated alias/task witness: same prepared native ref, per-job value,
  -- a native descendant, and a read of the untouched prepared root afterwards.
  let control ← beginBranch enabled
  let initialValue ← witness.get
  witness.set 37
  let task ← IO.asTask (witness.get)
  let observed ← IO.ofExcept task.get
  let controlCounts ← endBranch control
  let restored ← witness.get
  IO.println s!"WITNESS initial={initialValue} task={observed} root={restored} {controlCounts}"
end NativeBranchSetup
