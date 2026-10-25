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
the original7808 first-success scheduling matrix is now the sole full collection. Root only;48GiB aggregate/max2REPL/24each requirements remain.

## Prepared native environments

Verina4.18.0/Mathlibaa936c36 SDK and6,471cached files are ready in the
owningWorkspace temporary directory; [actual commands/failure repair](sdk-preparation-review.md).
The original189file native/profile implementation is in
[bench/lean-code-verification](../../bench/lean-code-verification/README.md);
actual qualification and all189 native/profile records are retained above.

Lean-mlir's exact nightly SDK and source are ready, but both official cache
paths return zero objects, so its dependency build is not ready despite
cache exit0. The real SLLVM file's static import closure is retained for
source build, including its version's import-all syntax. No extra cache
URL grid, substitute version, or second collection is launched.
