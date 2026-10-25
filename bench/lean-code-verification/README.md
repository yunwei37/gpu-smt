# Public Lean code-verification profiles

Pinned official sources, native versions and retained preparation:
[assets and limitations](../../artifacts/lean-code-verification-2026-10-25/README.md).

run-verina.py uses original189Verina reference files and its own4.18.0SDK/
Mathlib pins, native CLI and builtin profiler/structured trace. The published
synchronous checker default is120s per file; this is distinct from the old
miniF2F300s request point. Both retain CPU8–11, at most2actual Lean processes,
24GiBAS per child and48GiBaggregate sampledRSS. Explicitly admitted reference
files remain incomplete even on native exit0. Trace-wall weights are not CPU.

Historical reproduction of that recorded point (the driver has not yet been
adapted to the new dynamic resource contract), with the retained Kimina environment:
    python bench/lean-code-verification/run-verina.py --phase qualification --out /tmp/a-fresh-verina-qualification

[The real qualification and all189 native/profile records](../../artifacts/lean-code-verification-2026-10-25/verina-full189-20261025T0725/result-review.md)
are complete. Analyze with:
    python bench/lean-code-verification/analyze-verina.py --run <completed-group>

Each group retains run-source, commands, logs and actual limits. SDK/cache setup is not a proof
result. No other system's generation/prover baseline is reproduced.


Current research execution uses the [new aggregate resource contract](../../docs/architecture.md).
Do not interpret the historical24GiB/max2recipe as a new-resource qualification.
Existing completed Verina data remain; source/toolchain preparation for additional
original code workloads does not establish a measured SAT/LRAT target.


Original Verina inputs for the Rust engine can be prepared with prepare-engine.py
from the retained official source archive. The [prepared189input and filename
manifest](../../artifacts/native-source-backend-2026-10-25/verina189-inputs/README.md)
preserve every old reference byte, including admissions/errors. NativeLean uses
the pinned CLI stdin frontend and current Rust resource path; qualify filename
semantics before a new full-workload pair. No new native collection was started.


For nightly lean-mlir source preparation, ParseImports.lean calls that exact
SDK's Lean.Elab.parseImports. parse-closure.py records the transitive source
graph without initializing workload imports or elaborating candidate bodies.
This avoids guessing public/meta/import-all syntax. build-closure.py builds
only external prerequisites in native dependency order,using each module's own
Lake olean facet and Mathlib manifest; it excludes the workload/project modules.
These setup commands require the existing psutil environment and retain combined
research RSS/termination records. They do not constitute a second full capture.

The optional --library LeanMLIR mode retains the native package context, but
this pinned workload has reverse imports into SSA and cannot be prepared by
filtering one library alone. The [retained attempt](../../artifacts/lean-code-verification-2026-10-25/native-leanmlir-library-build-20261025/result-review.md)
records 16 successful modules and the missing-SSA failure. Continue with the
original root package and mixed source dependency order; do not remove imports
or substitute package revisions. Source preparation is not workload timing.

For this pinned lean-mlir workload, use --project-prerequisites with the
native root-manifest graph. Original root package pins can differ from a
subproject's pins (Cli is one concrete example). parse-closure.py now resolves
and records source directories/revisions from the root manifest; it does not
silently take an arbitrary Mathlib package of the same name. Preserve the
older graph as subproject-context evidence. The workload root is excluded
from prerequisite building, and actual candidate execution still requires the
single collection slot.

Prepare the unchanged complete lean-mlir module for the existing Rust Batch API:

    python3 bench/lean-code-verification/prepare-engine.py --workload leanmlir --input artifacts/lean-code-verification-2026-10-25/opencompl--lean-mlir-sources.jsonl.gz --out /tmp/leanmlir-engine-input

The [prepared input and scope](../../artifacts/lean-code-verification-2026-10-25/leanmlir-engine-input/README.md)
retain original source and filename provenance. Prerequisites now compile in
the correct root context, but native original-file/stdin qualification and
profiling await the sole candidate slot. Original source options and root
--tstack=400000 must be preserved. Verina remains the default preparer mode.
