import Mathlib
import Aesop
import GpuArithmetic.Stages
import GpuArithmetic.Baseline
import GpuArithmetic.Oracle
import GpuArithmetic.BatchOracle
open Lean Elab Command
elab "#arith_handlers" : command => do
  for key in [`Mathlib.Tactic.linarith, `Mathlib.Tactic.nlinarith, `Lean.Parser.Tactic.linarith, `Lean.Parser.Tactic.nlinarith] do
    for entry in Lean.Elab.Tactic.tacticElabAttribute.getEntries (← getEnv) key do
      logInfo m!"{key}: {entry.declName}"
#arith_handlers
