import Export.Parse
import Lean

-- Return actual metadata computed by Lean expression constructors for every
-- input expression. This validates the standalone CPU/GPU primitive; it does
-- not replay declarations or decide whether a proof is valid.
def main (args : List String) : IO Unit := do
  let [input, output] := args | throw <| IO.userError "expected input export and output binary"
  let start ← IO.monoNanosNow
  let handle ← IO.FS.Handle.mk input .read
  let (_, state) ← Export.Parse.M.run Export.Parse.parseFile (.ofHandle handle)
  let parsed ← IO.monoNanosNow
  let mut bytes := ByteArray.emptyWithCapacity (state.exprMap.size * 4)
  for i in [:state.exprMap.size] do
    let some expr := state.exprMap[i]? | throw <| IO.userError "expected dense expression indices"
    let n := expr.looseBVarRange
    for shift in [0, 8, 16, 24] do
      bytes := bytes.push (UInt8.ofNat ((n >>> shift) &&& 255))
  IO.FS.writeBinFile output bytes
  IO.println <| (Lean.Json.mkObj [("expressions", Lean.toJson state.exprMap.size),
    ("parse_ns", Lean.toJson (parsed - start)),
    ("serialize_ns", Lean.toJson ((← IO.monoNanosNow) - parsed))]).compress
