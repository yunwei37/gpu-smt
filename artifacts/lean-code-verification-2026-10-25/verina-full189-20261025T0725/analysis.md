# Verina original-source native characterization — root self-review

Unmodified official reference sources at pinned Lean4.18. Structured trace uses exclusive elapsed slices between children with default trace thresholds. threadCPUDelta is synthesized from wall slices by upstream exporter, never measured CPU. Weights sum across traces/threads/files, not whole-group elapsed or removable work. Admitted stubs separated.

Sources: 189
Native counts: {"incomplete_reference": 139, "lean_error": 4, "native_exit0_no_explicit_admission": 46}
Diagnostic counts: {"incomplete_reference": 139, "lean_error": 4, "native_exit0_no_explicit_admission": 46}
Status changes: []

## incomplete_reference (139 sources)

| Exclusive traced component | Accumulated wall-slice seconds |
|---|---:|
|runFrontend|21.880941|
|Elab.step: tacticDecreasing_trivial|4.703456|
|Elab.def.processPreDef|3.846566|
|Elab.step: Lean.Parser.Tactic.tacticSeq1Indented|1.790455|
|Kernel|1.787982|
|Elab.command|1.447014|
|Elab.step: Lean.Parser.Term.app|0.842160|
|Elab.step: Lean.Parser.Term.let|0.560042|
|Elab.step: Lean.Parser.Tactic.first|0.523999|
|Elab.step: Lean.Parser.Tactic.simp|0.429509|
|compiler|0.422005|
|Elab.step: Lean.Parser.Term.match|0.317240|

| Nearest traced tactic family | Accumulated wall-slice seconds |
|---|---:|
|outside traced tactic|31.892516|
|other tactic|7.128726|
|simp|0.429509|
|omega|0.288925|

## lean_error (4 sources)

| Exclusive traced component | Accumulated wall-slice seconds |
|---|---:|
|runFrontend|2.889816|
|compiler|0.083835|
|Elab.command|0.067395|
|Elab.step: Lean.Parser.Term.app|0.044279|
|Elab.step: Lean.Parser.Term.let|0.034969|
|Elab.step: Lean.Parser.Term.match|0.013802|
|Elab.step: Lean.Parser.Term.arrow|0.011772|
|Elab.lint|0.010354|
|Elab.def.processPreDef|0.001509|
|Elab.step: Lean.Parser.Term.forInMacro|0.001392|
|Elab.step: Lean.Parser.Term.do|0.001137|
|Elab.step: Lean.Parser.Term.fun|0.000417|

| Nearest traced tactic family | Accumulated wall-slice seconds |
|---|---:|
|outside traced tactic|3.161212|

## native_exit0_no_explicit_admission (46 sources)

| Exclusive traced component | Accumulated wall-slice seconds |
|---|---:|
|runFrontend|33.926187|
|Elab.step: Lean.Parser.Tactic.simpAll|3.918496|
|Elab.step: Lean.Parser.Tactic.simp|2.653424|
|Elab.step: Lean.Parser.Tactic.tacticSeq1Indented|1.302177|
|Meta.Tactic.simp.discharge|1.041965|
|Meta.isDefEq|0.701100|
|Meta.synthInstance|0.646832|
|Elab.command|0.544862|
|Meta.check|0.441449|
|Kernel|0.329803|
|Elab.lint|0.228903|
|Meta.instantiateMVars|0.205453|

| Nearest traced tactic family | Accumulated wall-slice seconds |
|---|---:|
|outside traced tactic|35.444890|
|simp|8.909486|
|other tactic|3.229396|

A missing tactic trace can be below the default threshold; absence is not zero cost.
Native exit0 without an explicit admission token is deliberately narrower than a complete theorem-soundness certification.
This is workload characterization, not a comparison with another prover system or a GPU result.
