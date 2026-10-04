import Export.Parse
import Lean

-- Same replay operation as arena official/Main.lean. Every request parses a
-- fresh export and constructs a fresh environment; no accepted-result cache.
def checkFile (path : String) : IO Unit := do
  let handle ← IO.FS.Handle.mk path .read
  let solution ← Export.parseStream (.ofHandle handle)
  let env ← Lean.mkEmptyEnvironment
  let constMap := solution.constMap.erase `Quot.mk |>.erase `Quot.lift |>.erase `Quot.ind
  discard <| env.toKernelEnv.replay constMap

def main : IO Unit := do
  let input ← IO.getStdin
  let output ← IO.getStdout
  repeat
    let line ← input.getLine
    if line.isEmpty then break
    let path := line.trimAscii.toString
    let start ← IO.monoNanosNow
    let (status, message) ← try
      checkFile path
      pure ("accepted", "")
    catch e => pure ("rejected", e.toString)
    let elapsed := (← IO.monoNanosNow) - start
    let response := Lean.Json.mkObj [
      ("path", Lean.toJson path), ("status", Lean.toJson status),
      ("message", Lean.toJson message), ("service_ns", Lean.toJson elapsed)]
    output.putStrLn response.compress
    output.flush
