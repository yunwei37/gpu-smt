/- Source-native header inspection only; no imported candidate module is executed. -/
import Lean.Elab.Import

open Lean

def main : IO Unit := do
  let stdin ← IO.getStdin
  let stdout ← IO.getStdout
  repeat
    let line ← stdin.getLine
    if line.isEmpty then break
    let path ← IO.ofExcept (Json.parse line >>= fromJson? (α := String))
    let source ← IO.FS.readFile path
    let (imports, _, messages) ← Elab.parseImports source (some path)
    let rows := imports.map fun imp => Json.mkObj [
      ("module", toJson imp.module.toString),
      ("isMeta", toJson imp.isMeta),
      ("isExported", toJson imp.isExported),
      ("importAll", toJson imp.importAll)]
    stdout.putStrLn (Json.mkObj [
      ("path", toJson path), ("imports", toJson rows),
      ("header_errors", toJson messages.hasErrors)]).compress
    stdout.flush
