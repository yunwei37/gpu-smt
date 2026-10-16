# Published GC REPL source reconstruction

Observed 2026-10-16. This closes a concrete source-publication/reconstruction check for one measured baseline component. It is not a new benchmark, independent scientific audit, complete project reproduction, or new systems contribution.

## Materialized source and build

Source commit: e163baf50600f5830eee2818afb4cc1de05befd6. Root materialized all 16 tracked files under the published source snapshot's gc-repl base using git show into /tmp/gpu-smt-published-gc-repl-20261016. No working-tree source, full repository clone/checkout, active package or measurement was modified.

The exact existing Lean 4.27.0 SDK builds this source package with lake build repl. All 22 build tasks complete, exit 0; the rebuilt native binary exists. The raw log retains upstream String.trim deprecation warnings, without unrelated source repairs. The source package has no external Lake dependencies, so this build does not rebuild or mutate Mathlib.

[Committed source and actual command](build-command.json), [raw build log](build.log), [terminal build result](build-result.json).

## Original accepted/rejected source controls

Inputs are the exact original Proof_00000 and Proof_00004 source rows retained in the already published full E033 archive; no proof or compiler option is changed. They are original public Goedel source controls, not an accepted-only performance sample.

Each input is sent with gc=true to both the original measured GC binary and the reconstructed binary, in the existing pinned Mathlib project environment. The compiled producer options remain native in the reconstructed source. All four processes complete with exit 0 and parseable native JSON. Proof_00000 has no error/sorry diagnostic and Proof_00004 retains an error; both per-source native JSON responses match exactly across binaries.

The process input is closed normally and subprocess completion includes EOF. Whole captured stdout/stderr, original source inputs, environment path provenance, actual commands and diagnostic elapsed times are retained. Elapsed values are not used as a performance comparison.

[Original source controls](original-controls.json), [all four native results](control-results.json), [existing dependency environment](dependency-runtime-path.json), [classification and equality check](control-validation.json).

## Scope remaining open

This reconstructs the published GC base in the owning Workspace using an existing pinned SDK and Mathlib dependency tree. It does not validate a new machine, dependency bootstrap, every native/Farkas/product overlay, the Python HTTP service, full corpus behavior, full RQ coverage or a GPU backend. Existing complete benchmark outcomes and all failure qualifications remain authoritative.

No live source, capture driver, GPU allocation, model configuration or other Workspace was changed. The private build output is disposable; the committed sources, commands and raw results preserve the evidence. This is root validation of a baseline artifact, not independent review or a novelty claim.
