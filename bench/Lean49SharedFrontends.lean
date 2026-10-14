/-
Thin adapter for the pinned Lean 4.9 native incremental frontend.
Snapshot creation, reuse guards, elaboration and kernel checking are stock Lean.
Sorry rendering follows the pinned producer REPL (Apache-2.0, Scott Morrison).
This is baseline qualification code, not an implemented verification service.
-/
import Lean.Elab.Frontend
import REPL.JSON
import REPL.Snapshots
import REPL.Lean.InfoTree

open Lean Lean.Elab

namespace Lean49PreparedBranches

structure Input where
  index : Nat
  header : String
  code : String
  deriving FromJson

structure Root where
  header : String
  importPrefix : String
  parser : Parser.ModuleParserState
  initial : Command.State
  importMessages : List Message
  previous : Option IncrementalState := none
  headerParser : Option Parser.ModuleParserState := none
  headerState : Option Command.State := none
  importedSearchPrepared : Bool := false

-- Keep the producer's diagnostic and sorry representations. Numerical proof
-- handles are local observations; this executable offers no tactic API.
def renderSorries (trees : List InfoTree) : IO (List REPL.Sorry) := do
  let mut result := []
  let mut nextHandle := 0
  for ⟨ctx, g, pos, endPos⟩ in trees.bind InfoTree.sorries do
    let proofState ← match g with
      | .tactic g => REPL.ProofSnapshot.create ctx none none [g]
      | .term lctx (some t) => REPL.ProofSnapshot.create ctx lctx none [] [t]
      | .term _ none => throw <| IO.userError "sorry without a recorded term"
    let goal := "\n".intercalate <| (← proofState.ppGoals).map fun s => s!"{s}"
    result := result ++ [REPL.Sorry.of goal pos endPos (some nextHandle)]
    nextHandle := nextHandle + 1
  return result

-- Equality of these observations is a discriminator, not semantic equivalence.
def declarationWitness (env : Environment) : Json :=
  toJson <| env.constants.map₂.toList.map fun (name, info) => Json.mkObj [
    ("name", toJson name.toString),
    ("levels", toJson (info.levelParams.map Name.toString)),
    ("type_hash", toJson (hash info.type).toNat),
    ("value_hash", toJson (info.value?.map (fun e => (hash e).toNat)))]

def makeRoot (input : Input) (existing : Array Root) : IO (Root × Bool) := do
  if !input.code.startsWith input.header then
    throw <| IO.userError "candidate does not start with its exact recorded header"
  let ctx := Parser.mkInputContext input.code "<input>"
  let (header, parser, messages) ← Parser.parseHeader ctx
  let importBytes := input.code.extract 0 parser.pos
  -- Reuse only genuine post-import state. Distinct command headers retain
  -- their own previous snapshots; no candidate's final state is adopted.
  -- Same filename/options and exact parsed import bytes are required here.
  if let some imported := existing.toList.find? (·.importPrefix == importBytes) then
    return ({ imported with header := input.header, previous := none, headerParser := none, headerState := none, importedSearchPrepared := false }, true)
  let (env, messages) ← processHeader header {} messages ctx (trustLevel := 0)
  return ({
    header := input.header
    importPrefix := importBytes
    parser
    initial := { Command.mkState env messages {} with infoState.enabled := true }
    importMessages := messages.toList
  }, false)

-- Stock unchanged-command path retains the exact finished task. Count only
-- this observed prefix; it says nothing about reuse inside a changed command
-- and may include the terminal parser snapshot. It is not a safety oracle.
unsafe def reusedPrefix (now old : Lean.Language.Lean.CommandParsedSnapshot) : Nat :=
  if ptrEq now.data.finishedSnap.task old.data.finishedSnap.task then
    1 + match now.nextCmdSnap?, old.nextCmdSnap? with
      | some n, some o => reusedPrefix n.get o.get
      | _, _ => 0
  else 0

@[extern "gpu_smt_native_checkpoint"]
opaque nativeCheckpoint (index : UInt64) (stage : String) : IO Unit

unsafe def process (mode : String) (input : Input) (root : Root) : IO (Root × Json) := do
  if !input.code.startsWith root.header then
    throw <| IO.userError "candidate header differs from the selected root"
  let ctx := Parser.mkInputContext input.code "<input>"
  let (_, parser, _) ← Parser.parseHeader ctx
  if input.code.extract 0 parser.pos != root.importPrefix then
    throw <| IO.userError "import bytes or boundary differ from the selected root"
  let old := if mode == "full" then root.previous else none
  -- The SAME post-import state is passed for each candidate. Never use a
  -- previous candidate's terminal command state as the next initial state.
  nativeCheckpoint input.index.toUInt64 "frontend_begin"
  let state ← IO.processCommandsIncrementally ctx
    (root.headerParser.getD root.parser) (root.headerState.getD root.initial) old
  nativeCheckpoint input.index.toUInt64 "frontend_complete"
  let messages ← state.commandState.messages.toList.mapM REPL.Message.of
  let importMessages ← root.importMessages.mapM REPL.Message.of
  let trees := state.commandState.infoState.trees.toList
  let sorries ← renderSorries trees
  -- Use the exact producer serializer, including omission of empty lists and
  -- its default empty AST. The observation handle is never continued here.
  let response : REPL.CommandResponse := {
    env := 0
    messages := messages
    sorries := sorries
    ast := some (toJson ([] : List Json))
  }
  return ({ root with previous := if mode == "full" then some state else none }, Json.mkObj [
    ("index", toJson input.index), ("response", toJson response),
    ("import_diagnostics", toJson importMessages),
    ("complete_diagnostics", toJson (importMessages ++ messages)),
    ("old_snapshot_supplied", toJson old.isSome),
    ("public_header_state_supplied", toJson root.headerState.isSome),
    ("reused_command_snapshot_prefix", toJson ((old.map fun previous =>
      reusedPrefix state.initialSnap previous.initialSnap).getD 0)),
    ("final_command_state", toJson true),
    ("local_declaration_fingerprints", declarationWitness state.commandState.env)])


-- Appended to the unchanged baseline definitions by the build script. These
-- functions are embedding glue. Default imports mode never elaborates a
-- candidate in the parent; optional full mode records a real seed check.
@[export gpu_smt_lean49_start]
unsafe def startPrepared (sysroot : String) : IO (Array Root) := do
  initSearchPath sysroot
  enableInitializersExecution
  return #[]

-- Default remains the already qualified import-only implementation. The
-- optional full mode is an unqualified preparation-depth candidate; it keeps
-- stock prior snapshots, NEVER the seed's final environment as initial state.
def parentPreparation : IO String := do
  let mode := (← IO.getEnv "GPU_SMT_PARENT_PREPARATION").getD "imports"
  if mode != "imports" && mode != "header" && mode != "header-cache" && mode != "full" then
    throw <| IO.userError "GPU_SMT_PARENT_PREPARATION must be imports, header, header-cache or full"
  return mode

-- This checks the visible stock snapshot tasks only. It does not certify
-- arbitrary imported FFI, private promises, allocator state, or global quiescence.
partial def visibleTasksFinished (tree : Lean.Language.SnapshotTree) : BaseIO Bool := do
  match tree with
  | .mk _ children =>
    for child in children do
      if !(← IO.hasFinished child.task) then return false
      if !(← visibleTasksFinished child.get) then return false
    return true

@[extern "gpu_smt_native_persist_root"]
opaque persistRoot (root : Root) : IO Unit

unsafe def prepareImportedSearch (root : Root) (input : Input) (emit : Bool) : IO Root := do
  if root.importedSearchPrepared then return root
  let begin ← IO.monoNanosNow
  let header := root.initial
  let ctx := Parser.mkInputContext root.header "<input>"
  let hb ← IO.getNumHeartbeats
  let (foundDecls, state, _) ← (Lean.Meta.LibrarySearch.libSearchFindDecls (mkConst ``True)).toIO
    { fileName := "<input>", fileMap := ctx.fileMap, options := header.scopes.head!.opts,
      currNamespace := header.scopes.head!.currNamespace, openDecls := header.scopes.head!.openDecls,
      initHeartbeats := hb, maxHeartbeats := 0 }
    { env := header.env }
  if state.messages.hasErrors then
    throw <| IO.userError "native imported-search index initialization reported errors"
  if emit then
    IO.println <| (Json.mkObj [("event", toJson "prepared_imported_search"),
      ("source_index", toJson input.index), ("query", toJson "Lean.True metadata lookup"),
      ("query_matches", toJson foundDecls.size),
      ("elapsed_ns", toJson ((← IO.monoNanosNow) - begin)),
      ("candidate_body_evaluated", toJson false)]).compress
    (← IO.getStdout).flush
  return { root with importedSearchPrepared := true }

@[export gpu_smt_lean49_prepare]
unsafe def prepareOne (roots : Array Root) (line : String) : IO (Array Root) := do
  let input ← IO.ofExcept (Json.parse line >>= fromJson? (α := Input))
  let mode ← parentPreparation
  let existing := roots.toList.find? (·.header == input.header)
  if mode == "imports" && existing.isSome then return roots
  if mode == "header" && (existing.bind (·.headerState)).isSome then return roots
  if mode == "header-cache" && (existing.map (·.importedSearchPrepared)).getD false then return roots
  let root ← match existing with
    | some root => pure root
    | none => Prod.fst <$> makeRoot { input with code := input.header } roots
  let root ← if mode == "header" && root.headerState.isNone then do
    -- Use the same synchronous frontend as the official REPL. It prepares
    -- only the published header, with no background parser snapshot tasks.
    let ctx := Parser.mkInputContext input.header "<input>"
    let state ← IO.processCommands ctx root.parser root.initial
    let messages ← state.commandState.messages.toList.mapM REPL.Message.of
    let response : REPL.CommandResponse := { env := 0, messages, ast := some (toJson ([] : List Json)) }
    IO.println <| (Json.mkObj [("event", toJson "prepared_header"),
      ("source_index", toJson input.index), ("native", Json.mkObj [
        ("index", toJson input.index), ("response", toJson response),
        ("public_header_only", toJson true),
        ("preparation_frontend", toJson "stock synchronous processCommands")])]).compress
    (← IO.getStdout).flush
    pure { root with headerParser := some state.parserState, headerState := some state.commandState }
  else if mode == "full" && root.previous.isNone && input.code.startsWith input.header then do
    -- The first ACTUAL candidate is checked with an ordinary task manager.
    -- Its response and all preparation cost are retained. The host tears down
    -- that manager only after this visible snapshot graph has completed.
    let (seeded, record) ← process "full" input root
    let some state := seeded.previous
      | throw <| IO.userError "full preparation returned no native snapshot"
    if !(← visibleTasksFinished (Lean.Language.toSnapshotTree state.initialSnap)) then
      throw <| IO.userError "visible native snapshot tasks remain unfinished"
    IO.println <| (Json.mkObj [("event", toJson "prepared_seed"),
      ("source_index", toJson input.index), ("visible_snapshot_tasks_finished", toJson true),
      ("native", record)]).compress
    (← IO.getStdout).flush
    pure seeded
  else pure root
  let root ← if mode == "header-cache" && !root.importedSearchPrepared then do
    -- Initialize only native imported-search metadata through the public API.
    -- No proof goal, candidate body or declaration is prepared or accepted.
    prepareImportedSearch root input true
  else pure root
  return if existing.isSome then
    roots.map fun prior => if prior.header == input.header then root else prior
  else roots.push root

@[export gpu_smt_lean49_execute]
unsafe def executeOne (roots : Array Root) (line : String) : IO String := do
  let input ← IO.ofExcept (Json.parse line >>= fromJson? (α := Input))
  let eligible := input.code.startsWith input.header
  let root ← if eligible then
    match roots.toList.find? (·.header == input.header) with
    | some root => pure root
    | none => throw <| IO.userError "missing prepared header"
  else
    Prod.fst <$> makeRoot { input with header := "" } #[]
  let mode ← parentPreparation
  let (_, record) ← process (if mode == "header" || mode == "header-cache" then "full" else mode) input root
  let response := (Json.mkObj [("native", record), ("rootless_fallback", toJson (!eligible))]).compress
  nativeCheckpoint input.index.toUInt64 "response_ready"
  return response

unsafe def runSnapshotStreamCore (args : List String) (initialRoots : Array Root)
    (workerReply : Bool := false) : IO UInt32 := do
  let [mode, inputFile, sysroot, retireString] := args
    | throw <| IO.userError "usage: Lean49NativeSnapshots full|imports INPUT.jsonl|- SYSROOT RETIRE_AFTER"
  if mode != "full" && mode != "imports" then
    throw <| IO.userError "invalid mode"
  let some retire := retireString.toNat? | throw <| IO.userError "invalid retirement count"
  if retire == 0 then throw <| IO.userError "retirement count must be positive"
  initSearchPath sysroot
  enableInitializersExecution
  -- Same ordinary per-candidate inputs over a file or persistent stdin.
  -- Streaming lets the external owner measure admission-to-response and
  -- dispose only this process on a native timeout; it adds no cloning API.
  let stream ← if inputFile == "-" then IO.getStdin
    else IO.FS.Stream.ofHandle <$> IO.FS.Handle.mk inputFile .read
  let mut roots : Array Root := initialRoots
  let mut used := 0
  repeat
    let line ← stream.getLine
    if line.isEmpty then break
    if line.trim.isEmpty then continue
    let input ← IO.ofExcept (Json.parse line >>= fromJson? (α := Input))
    if used >= retire then
      roots := #[]
      used := 0
    let start ← IO.monoNanosNow
    let record ← try
      -- Missing code fences and changed headers are real candidate outcomes.
      -- Check their exact source in a fresh native environment; never omit
      -- them or turn a cache-ineligible candidate into an adapter rejection.
      let eligible := input.code.startsWith input.header
      let selected := if eligible then roots.toList.find? (·.header == input.header) else none
      let (root, sharedImport) ← match selected with
        | some root => pure (root, false)
        | none => makeRoot (if eligible then input else { input with header := "" })
                    (if eligible then roots else #[])
      let root ← if eligible && !root.importedSearchPrepared then do
        let prepared ← prepareImportedSearch root input false
        persistRoot prepared
        pure prepared
      else pure root
      let (root, record) ← process mode input root
      if eligible then
        roots := match selected with
          | some _ => roots.map fun existing => if existing.header == input.header then root else existing
          | none => roots.push root
      pure <| Json.mkObj [("native", record), ("rootless_fallback", toJson (!eligible)),
        ("shared_import_state_on_new_header", toJson sharedImport)]
    catch e =>
      pure <| Json.mkObj [("index", toJson input.index), ("adapter_error", toJson e.toString)]
    let finish ← IO.monoNanosNow
    if workerReply then
      IO.println record.compress
    else
      IO.println <| (Json.mkObj [
        ("record", record), ("elapsed_ns", toJson (finish - start)),
        ("root_count", toJson roots.size), ("mode", toJson mode),
        ("retire_after", toJson retire)]).compress
    (← IO.getStdout).flush
    used := used + 1
  return 0


-- Ordinary warm baseline preserves its empty initial root table and framing.
@[export gpu_smt_lean49_stream]
unsafe def runSnapshotStream (args : List String) : IO UInt32 :=
  runSnapshotStreamCore args #[]

-- Warm workers inherit only the prepared import/cache roots. Their incremental
-- candidate snapshots remain private and use the same native stream algorithm.
@[export gpu_smt_lean49_seeded_stream]
unsafe def runSeededSnapshotStream (roots : Array Root) (args : List String) : IO UInt32 :=
  runSnapshotStreamCore args roots true


-- Native per-worker transition: identical candidate body to the seeded stream.
-- Shared prepared roots are immutable; updated snapshots are returned to their worker.
@[export gpu_smt_lean49_shared_evaluate]
unsafe def evaluateSharedCandidate (initialRoots : Array Root) (line : String) :
    IO (Array Root × String) := do
  let mode := "full"
  let mut roots := initialRoots
  let input ← IO.ofExcept (Json.parse line >>= fromJson? (α := Input))
  let record ← try
    -- Missing code fences and changed headers are real candidate outcomes.
    -- Check their exact source in a fresh native environment; never omit
    -- them or turn a cache-ineligible candidate into an adapter rejection.
    let eligible := input.code.startsWith input.header
    let selected := if eligible then roots.toList.find? (·.header == input.header) else none
    let (root, sharedImport) ← match selected with
      | some root => pure (root, false)
      | none => makeRoot (if eligible then input else { input with header := "" })
                  (if eligible then roots else #[])
    let root ← if eligible && !root.importedSearchPrepared then do
      let prepared ← prepareImportedSearch root input false
      persistRoot prepared
      pure prepared
    else pure root
    let (root, record) ← process mode input root
    if eligible then
      roots := match selected with
        | some _ => roots.map fun existing => if existing.header == input.header then root else existing
        | none => roots.push root
    pure <| Json.mkObj [("native", record), ("rootless_fallback", toJson (!eligible)),
      ("shared_import_state_on_new_header", toJson sharedImport)]
  catch e =>
    pure <| Json.mkObj [("index", toJson input.index), ("adapter_error", toJson e.toString)]
  return (roots, record.compress)

end Lean49PreparedBranches
