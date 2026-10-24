import Mathlib
open Lean
private partial def positions (s : Syntax) : Array Json := Id.run do
  let mut out := #[]
  if let .node _ _ args := s then
    if let some first := args[0]? then
      if let .atom _ text := first then
        if ["linarith","nlinarith","linarith!","nlinarith!"].contains text then
          if let some start := s.getPos? then
            if let some stop := s.getTailPos? then
              return #[Json.mkObj [("start",toJson start.byteIdx),("end",toJson stop.byteIdx),("tactic",toJson text)]]
    for arg in args do out := out ++ positions arg
  return out

def main : IO Unit := do
  let env ← importModules #[{module := `Mathlib}, {module := `Counterexample}] {}
  let input ← IO.getStdin
  let output ← IO.getStdout
  repeat
    let line ← input.getLine
    if line.isEmpty then return
    let result := do
      let request ← Json.parse line
      let text ← request.getObjValAs? String "body"
      let id ← request.getObjVal? "id"
      match Parser.runParserCategory env `command text with
      | .ok stx => pure (Json.mkObj [("id",id),("positions",Json.arr (positions stx))])
      | .error e => pure (Json.mkObj [("id",id),("error",toJson e),("positions",Json.arr #[])])
    output.putStrLn ((match result with | .ok j => j | .error e => Json.mkObj [("error",toJson e)]).compress)
    output.flush
