# Partial native dynamic trace observation

2026-10-14T18:44:03.043471+00:00

Partial GC-enabled full-source diagnostic, not wholecorpus or primary performance. Official Firefox synthetic threadCPUDelta and leafweights are wall intervals, not measured CPU. Threshold10ms hides smaller/uninstrumented operations. Different native threads/requests overlap; summed trace work is not makespan/CPU fractions/GPU eligible work. Association uses stock split body bytes and actual native/API monotonic intervals; no ID/response normalization.

Completed requests: 181; matched completed body profiles: 181; header profiles: 4; deferred/unmatched retained in JSON.

| Trace class | Summed leaf wall ms | Source profiles |
|---|---:|---:|
|linarith|584149.819|127|
|linarith.detail|34420.852|124|
|Elab.step: Mathlib.Tactic.Ring.ring1|12125.726|131|
|Elab.def.maxSharing|10447.408|87|
|Kernel|8381.924|138|
|Meta.appBuilder|7756.559|121|
|Elab.step: Lean.Parser.Tactic.simp|6761.949|29|
|Meta.synthInstance|6751.229|78|
|Elab.step: Lean.Parser.Tactic.simpAll|6228.147|18|
|Elab.step: Mathlib.Tactic.nlinarith|5874.123|114|
|Elab.definition.header|3866.381|146|
|runFrontend|3618.988|181|
|Elab.lint: Lean.Linter.UnusedVariables.unusedVariables|2964.950|51|
|Elab.step: Lean.Parser.Term.app|2557.738|109|
|Elab.step: Mathlib.Tactic.RingNF.ringNF|2052.001|22|
|Meta.isDefEq|1987.037|41|
|Elab.definition.value|1880.357|170|
|Elab.step: Lean.Parser.Term.binrel|1851.125|94|
|Elab.step: Lean.Parser.Tactic.tacticSeq1Indented|1730.072|170|
|Meta.instantiateMVars|1467.064|13|

Negative weights are retained and reported, never clipped. This is preliminary operation-selection evidence only. No cost fraction, acceleration ceiling, confidence or native-CPU/GPU gain follows. Full corpus/primary paired results and strongest nativebatch competitor remain open.
