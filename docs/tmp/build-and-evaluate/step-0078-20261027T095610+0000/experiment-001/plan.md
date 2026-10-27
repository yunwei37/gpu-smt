# Plan — implement opt-in closed-CNF native frontend

Use Step0077checked correspondence with unchanged native verifyCert. Emit one
closed CNF definition,load it for the existing SAT solver and check the returned
certificate against that definition using stock ofReduceBool. Keep native
normalization,config,proof closing and SAT counterexample mapping.
Expose explicit shared core plus stock first-combinator fallback to bv_decide.
Test core directly so fallback cannot hide a broken positive path.
No default replacement,arithmeticCPUoracle,GPUkernel or cross-candidate reuse.

Compile definitions/bounded development controls onCPU11 under existing1s
combined own-tree48GiBmonitor,not another fullpopulation/performance group.
Build output stays in/tmp. Preserve failures and frozen original capture.
Compiled dataflow does not prove physical sharing/wholemodule speedup/novelty.
No agent delegation;root self-review only.
