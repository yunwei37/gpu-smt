import Lean
open Lean
def main : IO Unit := do
  let retained <- IO.mkRef (#[] : Array CompactedRegion)
  let lines <- IO.FS.lines "/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-olean-types-363/inputs.tsv"
  let stdout <- IO.getStdout
  let mut groups : Std.HashMap (Expr × List Name × Bool) Nat := {}
  let mut nextId := 0
  let mut exprGroups : Std.HashMap Expr Nat := {}
  let mut nextExprId := 0
  for line in lines do
    let fields := line.splitOn "\t"
    let moduleLabel := fields[0]!
    let file : System.FilePath := fields[1]!
    let (mainData, region) <- readModuleData file
    retained.modify (fun rs => rs.push region)
    let mut data := mainData
    if mainData.isModule then
      let parts <- readModuleDataParts #[file, file.withExtension "olean.server", file.withExtension "olean.private"]
      for (_, region) in parts do retained.modify (fun rs => rs.push region)
      let some last := parts.back? | throw (IO.userError "empty module data parts")
      data := last.1
    stdout.putStrLn ("MODULE " ++ moduleLabel)
    stdout.flush
    for ci in data.constants do
      let .thmInfo value := ci | continue
      let name := ci.name
      let isPrivate := name.toString.startsWith "_private."
      let auxiliaryName := decide ((name.toString.splitOn "_proof").length > 1)
      let decideShape := auxiliaryName &&
        value.value.getAppFn.isConstOf (Name.mkSimple "of_decide_eq_true")
      let mut groupJson := Json.null
      let mut exprJson := Json.null
      if auxiliaryName then
        let key := (value.type, value.levelParams, isPrivate)
        let id := match groups[key]? with | some id => id | none => nextId
        if (groups[key]?).isNone then
          groups := groups.insert key id
          nextId := nextId + 1
        groupJson := toJson id
        let exprId := match exprGroups[value.type]? with | some id => id | none => nextExprId
        if (exprGroups[value.type]?).isNone then
          exprGroups := exprGroups.insert value.type exprId
          nextExprId := nextExprId + 1
        exprJson := toJson exprId
      let j := Json.mkObj [
        ("module", toJson moduleLabel), ("name", toJson name.toString),
        ("is_private", toJson isPrivate), ("auxiliary_name", toJson auxiliaryName),
        ("decide_shaped_auxiliary", toJson decideShape), ("type_group", groupJson), ("expr_group", exprJson),
        ("proof_value_head", toJson ((value.value.getAppFn.constName?.map Name.toString).getD "")),
        ("axioms", Json.null)]
      stdout.putStrLn ("AUDIT " ++ j.compress)
      stdout.flush
  let regions <- retained.get
  stdout.putStrLn ("DONE " ++ toString lines.size ++ " " ++ toString regions.size)
