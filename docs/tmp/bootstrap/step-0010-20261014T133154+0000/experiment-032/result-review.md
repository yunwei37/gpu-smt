# Complete native CPU sampling: preliminary exclusive-cost review

Observed 2026-10-15T16:27:03.734527+00:00. Root executes and reviews personally; no independent audit is claimed.

All 29,750 unchanged Goedel4.27 inputs return: 27,318 complete, 2,376 rejected,
56 operational outcomes, whole instrumented clock 19,542.261591159 s. Exact
input/order qualification has no issues. This diagnostic uses CPU12–15 and
instrumentation; its wall clock is not a matched acceleration comparison.

The inherited recorder closes with actual exit0. The report contains 5,401,763
user-CPU samples, no reported lost samples, and exclusive leaf periods sum
exactly to the report event total 54,563,262,080,630. Native-repl contributes
98.755943% of recorded period; Python/lake/git remain separate. Native unknown
symbols retain 1.274106% of the native denominator.

Across all native task TIDs, lean_dec_ref_cold is10.815452% and mi_malloc_small
is9.230167% of native sampled period. These two disjoint exclusive functions
account for20.045619%. The six explicitly named reference/deallocation/allocation
leaf symbols in [the aggregation](full-exclusive-symbol-costs.json) total
30.078814%; this is not a complete runtime-cost category.
The SimplexAlgorithm DSO has5.102218% exclusive native sampled period; its
inherited runtime functions may execute elsewhere. Neither a DSO share nor
leaf allocations identify which proof stage caused the cost. Caller-level
attribution remains unfinished. Do not sum overlapping inclusive fractions.

This result supports keeping the synchronous scalar GPU provider closed:
there is material native object-management cost after compilation, while the
existing device path only moves narrow operations and retains launch/transfer/
synchronization/fallback. It does not causally decompose the earlier GPU loss,
prove these functions cannot be optimized, or admit a replacement GPU system.
No native sample fraction is GPU coverage or an Amdahl/wall-time bound.

The full5,665,548,374-byte raw recording is directly byte-compared/fsynced onto
the existing owning PVC outside Git. Original temporary raw stays retained.
The standard perf archive attempt exits1 with no build-ids found; retain its
log, do not call code-symbol archival complete. All95 available recorded ELF paths are now also archived on the samePVC with
byte-verified payloads; the one missing temporaryvDSO remains unrecovered.
Inclusive callchains and final result disposition remain open. Existing full
CPU comparator matrices continue; no new native/GPU run is launched.

[Full source qualification](full-source-qualification.json),
[weighted report command](full-weighted-report-receipt.json),
[raw retention](full-raw-retention-receipt.json),
[code-archive attempt](full-code-retention-receipt.json).

## Resource CPU scope correction (2026-10-15T17:58:42.557978+00:00)

The same capture's getrusage SELF+CHILDREN counter is19,439.725955s, while
the all-recorded user-CPU sampleperiod divided by1e9 is54,563.262081s(native
53,884.464108s). These distinct observations do not reconcile as exhaustive CPU
totals. Sampleperiod estimates must not replace the APIcounter or become a
missing-CPU amount, correction factor, whole-wall fraction or GPU bound.

The actual ResourceCapture code uses getrusage deltas, not integration of every
observedprocess'sCPU. The API includes only reaped descendant usage propagated
through intermediate waits. The current data do not establish exhaustive
coverage. Do not diagnose a specific orphan/thread/cleanup cause from this
difference, change livecollectors or rerun sources to erase it.
[Source/API/numeric evidence](cpu-accounting-scope.json) preserves exact pointers.
https://man7.org/linux/man-pages/man2/getrusage.2.html

SMT's declared waited_tree fields are also getrusage deltas plus the acquisition
process clock. Existing percentages remain numerical observations of that
counter; they are not validated all-descendant CPUoverheads. Whole-source wall
clocks, input/native outcomes, sampledPSS and exclusive sampleperiod fractions
are unchanged. The tested wall-time negative constructors remain closed.

## Compatible CPU-frontier qualification (2026-10-15T18:42:02.301206+00:00)

Allthree primaryFast/hybrid+product comparisons now showlowerelapsed, with
distinct original-oracle no-gain and resource/repetition controls stillpending.
The CPUweights in this E032capture belong to its plaincompiled original route;
they do not transfer to that composed alternative or establish finalbestCPU
residuals. If a materially different route isselected, deviceoperation selection
still requires its relevant residual. No extra profile/native run is launched
while currentcost/matrix work continues, and no newGPUkernel isadmitted.

## Complete full-raw inclusive result and source attribution (2026-10-16T00:09:30.560564+00:00)

Result status: complete supporting E032 CPU capture and offline exclusive/
inclusive analysis, root self-reviewed; independent audit and whole RQ4 remain
open. All29,750 original inputs and failures remain included. The original
full-raw perf report completes with actualreturn0 at21:02:46UTC. Its54,468
symbol aggregates reconcile exactly with the earlier exclusive report:
5,401,763samples and54,563,262,080,630exclusive periods overall; native-repl
5,334,562samples and53,884,464,107,620periods. No samples or source attempts are
replayed. [Exact reconciliation](full-inclusive-count-reconciliation.json).

| Actual reported symbol/path | Children display, % of all recorded user-CPU period |
|---|---:|
|lean_is_expr_def_eq|35.00|
|Meta isExprDefEqAuxImpl lambda|34.77|
|linarith runLinarith|26.06|
|sparse simplex certificate-oracle lambda|16.96|
|typeclass synthInstanceCore? lambda|10.81|
|C++ type_checker::infer_type_core entry|2.32|

These are perf's rounded inclusive displays, not disjoint stage fractions.
Nested wrappers and their callees overlap, so never add the rows, subtract
one from another to isolate a phase, or interpret them as wall-time/GPU/Amdahl
bounds. The denominator here is all recorded user-CPU period; earlier allocator
self shares use native-only exclusive period. Generic lean_apply dispatch
entries are high-level call paths, not isolated useful GPU kernels. The full
[summary](../../../../../artifacts/lean-modern-native-compilation-2026-10-14/native-cpu-sampling-full1/goedel427-compiled-profile-sampling/inclusive.summary.json)
and compressed all-symbol rows preserve every reported entry.

Direct installed4.27source inspection finds export lean_is_expr_def_eq on
Lean.Meta.isExprDefEqAuxImpl, returning MetaM Bool. This is elaborator/metaprogram
definitional equality, distinct from C++ kernel type_checker entries. Sparse
simplex and synthInstance mappings are also checked at their actual installed
source paths. The corresponding upstream kernel source and primary perf
manual are opened; the external Meta raw-page tool error is retained while
local SDK source succeeds. [Source/line/evidence receipt](full-inclusive-source-attribution.json).
The selected C++ entry's2.32% must not be called total kernel cost. Unknowns,
attach gaps, sampling/unwind limits and source/request attribution remain.

The earlier disjoint exclusive lean_dec_ref_cold/mi_malloc_small sum20.045619%
of native recorded period remains valid; six named runtime leaf symbols
sum30.078814%, not an exhaustive runtime category. The SimplexAlgorithm DSO's
5.102218% exclusive native period differs from its16.96%inclusive oracle entry
because descendant runtime work may occur elsewhere. These denominators and
overlapping views are kept separate.

The observer tool session ultimately reports a transport disconnect, while the
remote command's own receipt and full closed output show perfreturn0. Exact
transport output is private and [its scoped receipt](full-inclusive-observer-transport-receipt.json)
is retained. Current remote reads work; no host/Workspace/network recovery or
native/report rerun is justified by the historical observer disconnect.

Root's subprocess-to-gzip packaging mistake produced71,953,741bytes of actual
plain report plus a39byteempty gzip member. The entire71,953,780byteoriginal is
privately retained and byte-compared before repair. The empty trailing member
is validated and exact child stdout is correctly gzip-compressed; lossless
decompression matches every original report byte. [Recovery receipt](full-inclusive-output-recovery-receipt.json).
This repairs only derived packaging, not raw sampling or the native experiment.

Disposition: E032 now yields actual full-cohort CPU cost evidence. It supports
keeping the failed narrow synchronous scalar-GPU constructor closed and makes
Meta/proof-construction/solver work explicit. It does not select a replacement
GPU system, prove batching readiness or replace competent CPU competitors.
These weights belong to the compiled original arithmetic route; if a different
strong CPU composition is selected, its relevant residual must be established.
Finish the existing matched CPU/resource matrices, then choose a materially
different acceleration mechanism around demonstrated expensive useful work.
AllfourRQs, end-to-end/device/real-stream/resource/cancellation evidence and
full paper/independent audit remain open. No additional benchmark or writer.

Primary-source retrieval follow-up (2026-10-16): the web raw/blob cache misses remain recorded. Ordinary HTTPS to the pinned upstream raw Meta source returns200; all94,626bytes exactly match the installed SDK file used for the export/MetaM attribution. No source or runtime is changed.

## Existing full-capture import-entry observation

Root reuses the already complete weighted all-symbol report, without native
replay, new sampler or selected-prefix result. The exact native importModules
and processHeaderCore entries each display0.36%inclusive Children weight;
finalizeImport0.33% and importModulesCore0.03% overlap and must not be added.
The denominator is all recorded cpu-clock:u period in this same compiled
original-route capture, not corpuswalltime or a differentFast/hybridroute.

Actual installed v4.27Environment.lean2316–2327 calls importModulesCore then
finalizeImport under importModules. Elab/Import.lean45–69 calls that importer
from processHeaderCore. Exact source excerpts and ordinary pinned-upstream
retrieval outcomes are retained in [source/rows](full-import-entry-observation.json).

Decision: the observed competent warm baseline does not justify prioritizing
another import-only tuning proposal over measured residual verification work.
This strengthens the existing no-new-microtuning decision; it does not prove
all native preparation is cheap or answer allRQ1. Native extension/other
initialization, dynamic/lazy loading, I/O/wait, missed/unwound frames and
capture-attachment coverage can lie outside these entries. No subtraction,
CPU-to-wall transfer, speedup ceiling, causal explanation for priorbranchloss
or GPUadmission follows. Existing fullE033 and CPUmatrices continue.
Rootdirect self-review only; no fresh independent audit.
