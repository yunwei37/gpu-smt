import Lean
import Lean.Language.Lean
import Lean.Util.Sorry

open Lean Lean.Elab Lean.Language System

@[extern "gpu_smt_prepared_fork"]
opaque preparedFork (parentWorkers : UInt32) : IO UInt64
@[extern "gpu_smt_wait_child"]
opaque waitChild : IO UInt64
@[extern "gpu_smt_own_pid"]
opaque ownPid : IO UInt32
@[extern "gpu_smt_reap_detached"]
opaque reapDetached : IO UInt32
@[extern "gpu_smt_join_detached"]
opaque joinDetached : IO UInt32

-- Ordinary input adapter: original file, actual whole-source candidate file,
-- and result filename. These records are data, never research gate state.
structure Input where
  base : String
  input : String
  output : String
  deriving FromJson

structure Prepared where
  fileName : String
  snap : Lean.Language.Lean.InitialSnapshot

def nativeOptions : Options :=
  Options.empty |>.setBool `internal.cmdlineSnapshots false
    |>.setBool `Elab.async true |>.setBool `debug.skipKernelTC false
    |>.setNat `maxHeartbeats 800000

def processSource (fileName text : String)
    (old? : Option Lean.Language.Lean.InitialSnapshot) : IO Lean.Language.Lean.InitialSnapshot := do
  let inputCtx := Parser.mkInputContext text fileName
  let setup (stx : HeaderSyntax) :=
    pure <| Except.ok {
      mainModuleName := (fileName.dropRight 5).splitOn "/" |>.foldl Name.str .anonymous
      isModule := stx.isModule
      imports := stx.imports
      opts := nativeOptions
      trustLevel := 0
      : Lean.Language.Lean.SetupImportsResult }
  let snap ← Lean.Language.Lean.process setup old? { inputCtx with }
  let tree := toSnapshotTree snap
  let finished ← tree.waitAll
  discard <| IO.wait finished
  return snap

def collectResult (snap : Lean.Language.Lean.InitialSnapshot) : IO Json := do
  let snaps := (toSnapshotTree snap).getAll
  let mut diagnostics : Array Json := #[]
  let mut hasErrors := false
  for s in snaps do
    for msg in s.diagnostics.msgLog.toList do
      hasErrors := hasErrors || msg.severity == .error
      diagnostics := diagnostics.push (← msg.toJson)
  let mut decls : Array Json := #[]
  let mut admitted : Array String := #[]
  let final? := Lean.Language.Lean.waitForFinalCmdState? snap
  if let some state := final? then
    -- Force the checked kernel environment, rather than inspecting the async
    -- elaborator environment or treating goal closure as acceptance.
    let env := state.env.toKernelEnv
    -- Imported constants occupy map₁. map₂ contains local additions/realizations;
    -- const2ModIdx excludes realized imports from the local-source audit.
    for (name, info) in env.constants.map₂.toList do
      if !(env.const2ModIdx.contains name) then
        if info.type.hasSorry || (info.value? true).any Expr.hasSorry then
          admitted := admitted.push name.toString
        decls := decls.push <| Json.mkObj [
          ("name", toJson name.toString), ("type_hash", toJson (hash info.type).toNat),
          ("value_hash", toJson ((info.value? true).map (fun e => (hash e).toNat)))]
  return Json.mkObj [
    ("diagnostics", toJson diagnostics), ("has_errors", toJson hasErrors),
    ("final_state", toJson final?.isSome), ("local_sorry_declarations", toJson admitted),
    ("local_declaration_fingerprints", toJson decls),
    ("accepted", toJson (final?.isSome && !hasErrors && admitted.isEmpty))]

def writeResult (i : Input) (started : Nat) (cached : Bool) (result : Json) : IO Unit := do
  let ended ← IO.monoNanosNow
  let record := Json.mkObj [
    ("base", toJson i.base), ("input", toJson i.input), ("pid", toJson (← ownPid).toNat),
    ("start_ns", toJson started), ("end_ns", toJson ended),
    ("cached", toJson cached), ("result", result)]
  IO.FS.writeFile i.output (record.compress ++ "\n")

def runInput (i : Input) (text : String) (started : Nat)
    (old? : Option Lean.Language.Lean.InitialSnapshot) : IO Json := do
  let result ← try
    collectResult (← processSource i.base text old?)
  catch e =>
    pure <| Json.mkObj [("exception", toJson e.toString), ("accepted", toJson false)]
  writeResult i started false result
  let reaped ← reapDetached
  if reaped != 0 then throw <| IO.userError s!"owned worker reap error: {reaped}"
  return result

def cacheable (result : Json) : Bool :=
  (result.getObjValAs? Bool "accepted").toOption.getD false

unsafe def main (args : List String) : IO UInt32 := do
  let [mode, workersText, inputFile, sysroot] := args
    | throw <| IO.userError "usage: LeanPreparedNative MODE WORKERS INPUT.jsonl LEAN_SYSROOT"
  let some workers := workersText.toNat? | throw <| IO.userError "invalid worker count"
  if workers == 0 then throw <| IO.userError "workers must be positive"
  initSearchPath sysroot
  let lines := (← IO.FS.readFile inputFile).splitOn "\n" |>.filter (!·.isEmpty)
  let inputs ← lines.toArray.mapM fun line => IO.ofExcept (Json.parse line >>= fromJson?)
  let started ← IO.monoNanosNow
  let mut prepared : Array Prepared := #[]
  -- Both methods use the same exact (filename, full bytes, fixed configuration)
  -- cache. Only complete admission-free successes are reused; incomplete/error
  -- responses are never promoted. Preparation itself checks the original source.
  let mut cache : Std.HashMap (String × String) Json := {}
  for i in inputs do
    if !prepared.any (·.fileName == i.base) then
      let text ← IO.FS.readFile i.base
      -- Official frontend startup before EACH sequential import: withImporting
      -- resets the flag. Candidate snapshots reuse existing headers/imports.
      enableInitializersExecution
      let snap ← processSource i.base text none
      let result ← collectResult snap
      IO.println <| (Json.mkObj [("preparation", toJson i.base), ("result", result)]).compress
      if !cacheable result then
        (← IO.getStdout).flush
        throw <| IO.userError s!"original source did not qualify for complete prepared reuse: {i.base}"
      prepared := prepared.push { fileName := i.base, snap }
      if cacheable result then cache := cache.insert (i.base, text) result
  (← IO.getStdout).flush
  let preparedAt ← IO.monoNanosNow
  let getOld (i : Input) := if mode == "fresh" then none else
    (prepared.find? (·.fileName == i.base)).map (·.snap)
  if mode == "fork" then
    let mut pending : Std.HashMap Nat (Input × String) := {}
    for i in inputs do
      let requestStart ← IO.monoNanosNow
      let text ← IO.FS.readFile i.input
      -- Work-conserving completed-result cache, with in-flight coalescing.
      -- A duplicate of an incomplete/error result still executes independently.
      while (cache[(i.base, text)]?).isNone &&
          (pending.size == workers || pending.toList.any (fun (_, j) => j.1.base == i.base && j.2 == text)) do
        let status ← waitChild
        if status &&& ((1 : UInt64) <<< 63) != 0 || status &&& 0xffffffff != 0 then
          throw <| IO.userError s!"child wait failure {status}"
        let pid := (status >>> 32).toNat
        let some (done, text) := pending[pid]?
          | throw <| IO.userError s!"unexpected owned child {pid}"
        pending := pending.erase pid
        let record ← IO.ofExcept <| Json.parse (← IO.FS.readFile done.output)
        let result ← IO.ofExcept <| record.getObjVal? "result"
        if cacheable result then cache := cache.insert (done.base, text) result
      if let some result := cache[(i.base, text)]? then
        writeResult i requestStart true result
      else
        let pid ← preparedFork workers.toUInt32
        if pid &&& ((1 : UInt64) <<< 63) != 0 then
          throw <| IO.userError s!"unsupported fork boundary/OS failure {pid}"
        if pid == 0 then
          discard <| runInput i text requestStart (getOld i)
          IO.Process.exit 0
        pending := pending.insert pid.toNat (i, text)
    while !pending.isEmpty do
      let status ← waitChild
      if status &&& ((1 : UInt64) <<< 63) != 0 || status &&& 0xffffffff != 0 then
        throw <| IO.userError s!"child wait failure {status}"
      pending := pending.erase (status >>> 32).toNat
  else if mode == "logical" || mode == "fresh" then
    if workers == 1 then
      for i in inputs do
        let requestStart ← IO.monoNanosNow
        let text ← IO.FS.readFile i.input
        if let some result := cache[(i.base, text)]? then
          writeResult i requestStart true result
        else
          let result ← runInput i text requestStart (getOld i)
          if cacheable result then cache := cache.insert (i.base, text) result
    else
      let mut pending : List (Input × String × Task (Except IO.Error Json)) := []
      for i in inputs do
        let requestStart ← IO.monoNanosNow
        let text ← IO.FS.readFile i.input
        while (cache[(i.base, text)]?).isNone &&
            (pending.length == workers || pending.any (fun (j, t, _) => j.base == i.base && t == text)) do
          match pending with
          | [] => throw <| IO.userError "empty pending queue"
          | x :: xs => discard <| IO.ofExcept (← IO.waitAny (x.2.2 :: xs.map (·.2.2)))
          let mut active := []
          for (done, text, task) in pending do
            if ← IO.hasFinished task then
              let result ← IO.ofExcept task.get
              if cacheable result then cache := cache.insert (done.base, text) result
            else active := (done, text, task) :: active
          pending := active
        if let some result := cache[(i.base, text)]? then
          writeResult i requestStart true result
        else
          let t ← IO.asTask (runInput i text requestStart (getOld i)) .dedicated
          pending := (i, text, t) :: pending
      for (_, _, task) in pending do discard <| IO.ofExcept task.get
  else throw <| IO.userError s!"unknown mode {mode}"
  let joined ← joinDetached
  if joined != 0 then throw <| IO.userError s!"owned worker final join error: {joined}"
  let ended ← IO.monoNanosNow
  IO.println <| (Json.mkObj [
    ("mode", toJson mode), ("workers", toJson workers), ("jobs", toJson inputs.size),
    ("start_ns", toJson started), ("prepared_ns", toJson preparedAt),
    ("end_ns", toJson ended)]).compress
  return 0
