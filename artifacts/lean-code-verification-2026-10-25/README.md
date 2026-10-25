# Public Lean code-verification source preparation

Pinned official code/inputs, licenses, native toolchains and untruncated
GitHub metadata. Original Verina native/profile measurements are now complete.
Source archives preserve original UTF8 text and paths. Source-census.json
is comment-stripped lexical filtering, never execution/CPU attribution.

[Primary-source review and next measurements](../../docs/tmp/bootstrap/step-0011-20261023T195335-0700/literature-20261025-code-verification/report.md).
[All189 original Verina files measured](verina-full189-20261025T0725/result-review.md): 46 exit0 without explicit admission, 139 admitted stubs, four native API errors; profiled statuses match.
CLEVER carries many stubs; miniCodeProps includes library/test modules;
lean-mlir's generated sorry files are retained but are not verified proofs.
FVAPPS gated access is not accepted. The 480-source failure profile has retired;
the original7808 first-success scheduling matrix is now the sole full collection. Those historical captures used48GiB aggregate/max2REPL/24GiBeach;
new captures follow the current dynamic point in [architecture](../../docs/architecture.md).

## Prepared native environments

Verina4.18.0/Mathlibaa936c36 SDK and6,471cached files are ready in the
owningWorkspace temporary directory; [actual commands/failure repair](sdk-preparation-review.md).
The original189file native/profile implementation is in
[bench/lean-code-verification](../../bench/lean-code-verification/README.md);
actual qualification and all189 native/profile records are retained above.

Lean-mlir's exact nightly SDK and source are ready, but both official cache
paths return zero objects, so its dependency build is not ready despite
cache exit0. The old556module lexical graph is retained but superseded: it missed
meta imports. The [native header parser result](native-header-closure-20261025/receipt.json)
contains860source modules(58project/802external), with all/meta/export flags.
No workload imports or candidate bodies execute in this parsing step. Native
external prerequisite compilation has completed below; no second full capture.


## Current capture boundary

The original Verina189capture and its fixed resource point remain historical
evidence. The legacy run-verina driver still reproduces that point; it is not
the new dynamic-admission path. New code-workload captures require the current
48GiB aggregate/CPU-coupled controller after the sole old group retires.
No second proof collection has started. Lean-mlir's [native-parser-driven prerequisite build](native-prerequisite-build-20261025/launch.json)
completed all802external modules after zero-hit upstream caches.
It excludes all58project/workload modules. Existing capture plus setup RSS was
sampled each second; no monitor error or pressure termination occurred. Native-parser860module
closure supersedes lexical556. These are dependency preparation, not a native
workload measurement or baseline-system reproduction.

## Original root-package preparation

The completed 802-module external build uses the Mathlib/subproject context.
It is useful prerequisite evidence, not readiness for the complete root.
The original root manifest chooses a different Cli revision, and LeanMLIR
modules import SSA in reverse. The [library-only partial failure](native-leanmlir-library-build-20261025/result-review.md)
and [root dependency mismatch](native-project-prerequisites-20261025/result-review.md)
are retained. A corrected [native root graph](native-root-header-closure-20261025/receipt.json)
still has 860 modules, resolves every dependency at original root-manifest pins,
and retains public/meta/import-all flags. The corrected mixed prerequisite
build excludes the actual bv_decide workload root; no SAT/LRAT performance or
additional candidate run is claimed from preparation.
