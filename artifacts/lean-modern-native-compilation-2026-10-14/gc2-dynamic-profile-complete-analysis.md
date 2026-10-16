# Complete source-native diagnostic capture

2026-10-15T06:43:42.410852+00:00

Complete original-source diagnostic acquisition; body-profile coverage is separately reported. Native Firefox synthetic threadCPUDelta and leaf weights are wall intervals, not measured CPU. Threshold10ms and uninstrumented regions hide work. Threads/requests overlap; sums are not makespan/CPU fractions or GPU eligible coverage. Missing/partial/unmatched profiles are retained, never assigned zero cost.

Original sources returned: 29750. Matched body profiles: 29689 over29689sources. Header profiles:76. Sources without body profiles:61. Partial:0; unmatched:0.

| Recorded trace class | Summed leaf wall ms | Body profiles |
|---|---:|---:|
|linarith|96968618.220|21219|
|linarith.detail|5465395.729|20738|
|Elab.step: Lean.Parser.Tactic.simp|4606109.744|2656|
|Elab.step: Lean.Parser.Tactic.simpAll|2452212.245|2632|
|Elab.def.maxSharing|2297376.106|15961|
|Elab.step: Mathlib.Tactic.Ring.ring1|2188675.294|21384|
|Kernel|1791181.298|22866|
|Meta.appBuilder|1289702.627|20318|
|Meta.synthInstance|1205027.999|17220|
|Meta.isDefEq|945815.528|10288|
|Elab.step: Mathlib.Tactic.nlinarith|820791.801|18933|
|Elab.step: Mathlib.Tactic.RingNF.ringNF|790880.894|5260|
|Elab.definition.header|777142.598|24454|
|runFrontend|636784.328|29689|
|Elab.lint: Lean.Linter.UnusedVariables.unusedVariables|522426.452|10103|
|Elab.step: Lean.Parser.Tactic.allGoals|486380.803|7220|
|Elab.step: Lean.Parser.Term.app|457450.185|18994|
|Meta.Tactic.simp.discharge|431364.708|1778|
|Elab.step: Mathlib.Tactic.FieldSimp.fieldSimp|385595.501|5563|
|Meta.instantiateMVars|377126.500|3403|

The whole capture clock includes profiler/observer costs and is not a primary speed comparison. These observations support operation selection only; they do not answer a complete RQ, establish GPU cost coverage or identify a fastest CPU route. Repetitions/resources of the already running performance comparisons remain required.
