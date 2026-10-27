# Shared CNF verification contract — uncompiled draft

This is a source-grounded mechanism preparation for the actual lean-mlir
bitvector workload,not a new benchmark result or deployed tactic.

## What the retained native source shows

The pinned frontend bitblasts the reflected expression and converts AIG to CNF
before calling the existing SAT solver. Later its closed verifyBVExpr definition
constructs that CNF again;verifyCert parses the LRAT String and LRAT.check
converts the formula/actions before sequential checker execution. The enclosing
Verifying LRAT certificate span creates the original ofReduceBool auxiliary
lemma. Thus that span includes compiled Boolean reflection work,not just a
small isolated RUP loop or purely logical proof-term traversal.

The native LRAT checker updates formula state on addRup/addRat and deletion
before processing the remaining proof. Blindly treating arbitrary proof actions
as independent GPU jobs does not preserve that transition contract. Actual
dependency width,certificate sizes and the time split are not in the old trace.
Do not infer any of them from42trace threads,89stack contexts or summed slices.

Existing frontend snapshots are reused at their original artifact home and
byte-match this SDK. Only newly inspected Std reflection/checker sources are
retained here with original license headers. No external system is reproduced.

## Concrete contract and open implementation

CnfBridge.lean is an UNCOMPILED contract draft. It requires both equality of a
supplied CNF to the exact native conversion of the reflected expression,and
the unchanged verifyCert result. Supplying an untrusted host formula alone
cannot satisfy it. No axiom,unsafe computation,tactic override or skipped
native check is introduced by this draft. Its syntax/theorem is not qualified
until actual compilation/negative controls at the free resource slot.

The proposed implementation would emit one closed generated CNF declaration,
consume it in the existing SAT frontend,and use that exact declaration in
native certificate reflection with a checked correspondence. Physical runtime
sharing across meta evaluation/compiled reflection is a hypothesis,not shown
by this mathematical bridge. Compilation barriers may serialize work or erase
any benefit. A definition/contract alone is not an implemented shared backend.

Only after contract compilation and valid/invalid CNF/certificate controls,
test a baseline/import-only/prototype complete original module comparison
using existing measure/compare and native profiling. Include construction,
compilation,solver,checker,fallback and retirement. Keep same resources and
original baseline;variant edits must be explicit. This is source preparation,
not a new stopping gate/deadline. No extra collection starts while the current
Mathlib fullpair runs,and no pressure compiler retry occurs here.

No GPU work,accepted-set equivalence,phase percentage,speedup or novelty is
claimed. Ordinary within-proof sharing is not by itself a paper contribution.
The draft is separate from the frozen arithmetic CPU oracle and does not
reuse cross-candidate prefixes/certificates.

The contract handles only the UNSAT transfer. A complete frontend also needs
AIG-variable mapping/model reconstruction for SAT results and original config/
proof trimming/fallback behavior. A CNF constant alone does not implement those
paths. Correspondence and compiled-value sharing therefore must not be
confused with a working replacement for bv_decide.
