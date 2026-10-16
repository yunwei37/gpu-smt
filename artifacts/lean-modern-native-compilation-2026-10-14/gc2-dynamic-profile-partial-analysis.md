# Partial native dynamic trace observation

2026-10-15T05:36:23.160971+00:00

Partial GC-enabled full-source diagnostic, not wholecorpus or primary performance. Official Firefox synthetic threadCPUDelta and leafweights are wall intervals, not measured CPU. Threshold10ms hides smaller/uninstrumented operations. Different native threads/requests overlap; summed trace work is not makespan/CPU fractions/GPU eligible work. Association uses stock split body bytes and actual native/API monotonic intervals; no ID/response normalization.

Completed requests: 27163; matched completed body profiles: 27110; header profiles: 66; deferred/unmatched retained in JSON.

| Trace class | Summed leaf wall ms | Source profiles |
|---|---:|---:|
|linarith|87325551.319|19471|
|linarith.detail|4976877.785|19018|
|Elab.step: Lean.Parser.Tactic.simp|4100053.913|2397|
|Elab.step: Lean.Parser.Tactic.simpAll|2139553.832|2375|
|Elab.def.maxSharing|2045735.985|14571|
|Elab.step: Mathlib.Tactic.Ring.ring1|1964728.763|19587|
|Kernel|1613062.908|20932|
|Meta.appBuilder|1189429.410|18635|
|Meta.synthInstance|1063340.333|15485|
|Meta.isDefEq|774050.502|9014|
|Elab.step: Mathlib.Tactic.nlinarith|748541.690|17399|
|Elab.step: Mathlib.Tactic.RingNF.ringNF|716039.515|4814|
|Elab.definition.header|698456.100|22247|
|runFrontend|574506.244|27110|
|Elab.lint: Lean.Linter.UnusedVariables.unusedVariables|471504.178|9225|
|Elab.step: Lean.Parser.Tactic.allGoals|466645.692|6607|
|Elab.step: Lean.Parser.Term.app|417474.448|17340|
|Meta.Tactic.simp.discharge|398577.501|1583|
|Elab.step: Mathlib.Tactic.FieldSimp.fieldSimp|349579.544|5083|
|Meta.instantiateMVars|337135.575|3095|

Negative weights are retained and reported, never clipped. This is preliminary operation-selection evidence only. No cost fraction, acceleration ceiling, confidence or native-CPU/GPU gain follows. Full corpus/primary paired results and strongest nativebatch competitor remain open.
