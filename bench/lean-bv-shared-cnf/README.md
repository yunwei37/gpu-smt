# Experimental closed-CNF bv_decide frontend

Pinned Lean4.27nightly-2025-12-01 only. Explicit opt-in prototype;the Rust engine
and stock bv_decide defaults are unchanged. It is not a measured acceleration.

CnfBridge proves native-CNF correspondence plus unchanged verifyCert success
imply the original reflected goal is unsatisfiable. SharedCNF generates one
closed CNF declaration,loads it for the existing solver and references it in
native certificate reflection. SAT results use native variable reconstruction.
Meta evalConst is unsafe host evaluation;final proof checking remains stock
ofReduceBool/trustCompiler. No new proof axiom or skipped check is introduced.

bv_decide_shared_core executes this path directly. bv_decide_shared first tries
it and uses the native first combinator to restore/fall back to unchanged
bv_decide with the same config. This fallback can repeat search/compilation and
retain compiled data;its costs are not free. Core is experimental and can fail.
No arbitrary native-context/FFI compatibility is asserted.

## Build and development controls

Use the existing matching SDK,an absolute BUILD directory outside the checkout,
and its default Std imports. From this directory:

    export PATH="$SDK/bin:$PATH"
    export LEAN_SYSROOT="$SDK"
    export LEAN_PATH="$BUILD"
    mkdir -p "$BUILD"
    lean -o "$BUILD/CnfBridge.olean" CnfBridge.lean
    lean -o "$BUILD/SharedCNF.olean" SharedCNF.lean
    lean ControlsPositive.lean
    lean ControlsNative.lean

FalseCore.lean,FalsePublic.lean and FalseNative.lean intentionally exit1 with
the same x=15#4counterexample. These are native build/unit controls,not original
workload speed measurements. Use the owning aggregateRSS/CPU budget and preserve
the one fullcollection rule. For project workloads,prepend BUILD to the existing
Lake-discovered import path rather than replacing project imports.

[Exact qualification,commands,raw outputs and failures](../../docs/tmp/build-and-evaluate/step-0078-20261027T095610+0000/step-report.md)
record actual core/public/backtracking/native proofs and SAT rejection.
The initial missing-parser-namespace compile failure remains. Positive trace
has3shared certificate checks;it is not fallback-only acceptance. Native and
prototype printed axiom lists match and contain no sorryAx.

## Measurement still required

One source-level declaration does not guarantee physical meta/native heap or
computation sharing. Existing compilation barriers can outweigh saved work.
Complete unchanged original-module/import-only/prototype measurements must
include preparation,solver,checker,fallback,queue and retirement through the
[existing capture path](../../docs/benchmarking.md). Keep variant edits explicit.
Unequal development files/proof counts/tracing cannot form a speed ratio.

No original-module accepted-set conclusion,GPU implementation or novelty is
claimed. Ordinary within-proof sharing alone is not a paper contribution.
The frozen arithmetic CPU oracle and excluded cross-candidate prefix/certificate
reuse are not part of this implementation.
