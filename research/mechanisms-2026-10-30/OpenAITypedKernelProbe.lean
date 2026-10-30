import Lean
set_option maxHeartbeats 200000
set_option maxRecDepth 10000
open Lean
abbrev QueryM := StateT Environment IO
instance : MonadEnv QueryM where
  getEnv := get
  modifyEnv := modify

def dottedName (text : String) : Name :=
  (text.splitOn ".").foldl Name.str Name.anonymous

unsafe def main : IO Unit := do
  let some input ← IO.getEnv "M_OPENAI_TYPED_INPUT" | throw (IO.userError "typed input missing")
  let some output ← IO.getEnv "M_OPENAI_TYPED_OUTPUT" | throw (IO.userError "typed output missing")
  let lines ← IO.FS.lines input
  let mut mods : Array Import := #[]
  let mut known : Std.HashSet String := {}
  for line in lines do
    let fields := line.splitOn "\t"
    let moduleName := fields[0]!
    if !known.contains moduleName then
      known := known.insert moduleName
      mods := mods.push {module := dottedName moduleName}
  let env ← importModules mods {}
  let mut seen : Std.HashSet (Expr × List Name) := {}
  let stream ← IO.FS.Handle.mk output IO.FS.Mode.write
  for line in lines do
    let fields := line.splitOn "\t"
    let name := dottedName fields[1]!
    let some (.thmInfo value) := env.find? name | do
      stream.putStrLn ((Json.mkObj [("name",toJson fields[1]!),("status",toJson "missing")]).compress)
      stream.flush
      continue
    let key := (value.type,value.levelParams)
    if seen.contains key then continue
    seen := seen.insert key
    let axioms ← (collectAxioms name : QueryM (Array Name)).run' env
    let description := Json.mkObj [
      ("name",toJson fields[1]!),("module",toJson fields[0]!),
      ("type_repr",toJson (reprStr value.type)),("axioms",toJson (axioms.map Name.toString)),
      ("status",toJson "started")]
    stream.putStrLn description.compress
    stream.flush
    for repetition in [:3] do
      let fresh := Name.str `MOpenAIBaseline (toString seen.size ++ "_" ++ toString repetition)
      let began ← IO.monoNanosNow
      let checked := env.addDeclCore 200000000 10000
        (.thmDecl {value with name := fresh, all := [fresh]}) none true
      let ok := match checked with | .ok _ => true | .error _ => false
      let ended ← IO.monoNanosNow
      stream.putStrLn ((Json.mkObj [
        ("name",toJson fields[1]!),("status",toJson (if ok then "checked" else "kernel_error")),
        ("repetition",toJson repetition),("kernel_ns",toJson (ended-began))]).compress)
      stream.flush
  stream.putStrLn ((Json.mkObj [("status",toJson "complete"),("distinct_types",toJson seen.size)]).compress)
  stream.flush
