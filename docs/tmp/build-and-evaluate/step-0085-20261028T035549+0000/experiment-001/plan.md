# Plan — fused LRAT action checking implementation and native qualification

RQ4:After preparation reuse,when does heterogeneous execution improve complete
verification over the strongest measured CPU path?

Scope contract:only add explicit experimental fused-checker/frontend modules
and necessary proof/negative/native controls under bench;do not change Std,
active4.9SDK,existing engine/tactics/defaults,CPUoracle or the frozen fullmatrix.
Novelty is unestablished;ordinary deforestation alone is not a contribution.

Pinned4.27Std LRAT.check first builds an IntAction list,maps conversions,filters
converted/RAT-wellformed actions,then sequentially checks. Implement the same
conversion and checking in one traversal,with stock CNF/parser/RUP/RAT operations.
Prove equality with stock for allaction lists/CNFs/certificate strings,not just
positive fixtures. Preserve skipped malformed-action and earlyterminal behavior.
The frontend uses stock bitblast/SAT/certString/compiler trust,changing only
the reflected checker constant;unlike closed-CNFnegative it adds no CNFdecl.

This is supporting mechanism/correctness qualification,not performance evidence.
Compile/prove in the pinnedSDK;exercise validcertificate,invalid/malformed/
RAT/delete and SAT boundaries plus actual frontend proofs. Existing combined
RSS guard includes the current fullmatrix and newbuild tree,CPU11;abort only
newhelper on pressure. No second fullpopulation/performance capture runs.
If safeheadroom exists,a bounded actual first original lean-mlir theorem may
qualify engagement;no ratio from these concurrent controls. Whole-module
native/import/fused performance comparison waits for sole fullmatrix retirement.

Preserve allcompile/proof failures and everyattempt. Root self-review,not
independent audit. A correctness success does not establish speedup orGPU/
systems novelty. No timeout threshold,parameter grid or researchstopping gate.
