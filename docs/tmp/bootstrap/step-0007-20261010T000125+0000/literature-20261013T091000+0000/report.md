# Main formal Lean4.9 external-checking interface

2026-10-13, step0007 E96, EXPERIMENT source/dependency node under RQ4. Full human intent, Initial Narrative, current paper and complete owning literature procedure were read before the decision. This is engineering/source grounding for the complete formal GPU route, not a completed experiment or a replacement contribution.

## Declared questions and coverage

Can the original Lean4.9 ProofNet/miniF2F candidate pools reach an independent CPU/GPU checker without transplanting Lean4.21 APIs or charging a redundant native kernel check as the intended accelerated path? The finite coverage boundary is exact4.9 declaration dispatch/kernel API, exporter/consumer format compatibility and strongest native reference. Completion means identifying the necessary explicit adapter and remaining qualification, not asserting that it already checks the main corpus.

Search strings: `lean4export github Export.lean c77b4f275cb7`, `site:github.com/leanprover/lean4export v4.9`. Opened official exporter repository/source/format and exact official Lean4.9 AddDecl. Search results on Comparator version mismatch are compatible-version leads, not measured performance. Initial web fetch of kernel environment.cpp failed; direct public raw retrieval succeeded. No source absence was inferred from the cache error. [Source observations](source-observations.json) retain exact URLs/bytes/hashes. Read complete relevant functions and compared SDK/owned-runtime local sources with retrieved primary bytes.

## Verified version boundary

- [Official AddDecl](official-AddDecl.lean), [kernel environment.cpp](official-environment.cpp), [environment.h](official-environment.h) at be6c4894e0a6 match the retained exact4.9 SDK/source. The Lean dispatch calls addDeclCore; C++ lean_add_decl invokes environment.add(declaration) with default check=true. `debug.skipKernelTC` from the4.21 producer is absent in that path. Import trustLevel is not an unchecked-declaration switch.
- The C++ public environment.add(declaration, bool check) has an explicit unchecked path for definitions/theorems/opaque values. Inductive/quotient addition still follows native kernel routines. A future isolated witness producer can select this interface without changing the running SDK or any active binary. It must emit **unverified** terms, preserve the native reference, and require complete independent checking/fallback before acceptance. Source availability is not semantic qualification or a runtime result.
- The official c77b4f [Export.lean](official-Export.lean) and [format3.1](official-export-format.md) target4.21; old4.9 has different HashMap/JSON/ConstMap APIs and `InductiveVal.isNested` rather than `numNested`. Thus merely compiling/importing the current module under4.9 is not demonstrated official compatibility.
- Exact current sokonanoda7645b1e frontend/parser.rs supports format3.1–<3.2 and maps the serialized nested count to an `is_nested = num_nested > 0` flag. Old4.9's nested flag can be preserved for this particular consumer using an explicit0/1 projection; that is not the original count or a general round-trip format claim. Unsupported/ambiguous cases must remain visible and use complete native fallback rather than fabricated fields or acceptance.

## Actual dependency preparation and failures

Isolated source/API adaptation is under `artifacts/lean-gpu-checking-2026-10-13/formal49-dependency/`. Build1 fails on old container iteration/JSON helpers and missing numNested. Build2 resolves those API differences but fails because unqualified toJson helper names recursively resolve to themselves. Build3 explicitly calls Lean.toJson and compiles Export.olean/Export.c normally with the retained4.9 SDK. All three source/log/exit records remain; no active SDK/exporter/producer/PTX changed.

The build3 compatibility note explicitly records the old nested flag projection and source provenance. No proof candidate, imported graph, independent CPU verdict, GPU command, correctness preflight or corpus timing was run in this branch. Compile success is dependency-only evidence with zero independent research value. It neither consumes an E019 preflight nor changes its review2/3/preflight2/3/full2 state. Existing E020 native scope also remains fixed.

## Baseline and experiment handoff

Keep the exact strongest native4.9 full-snapshot pool as the native/current-practice reference. Keep the official optimized closure CPU checker as the alternative complete-checking competitor, with any format/API glue explicitly disclosed. Compare actual GPU plus full official CPU fallback to that resident complete CPU path; the same-source CPU fragment is a control, never the strongest main baseline. Kernel Arena later-version round factors remain citation/context, not reproduced whole-candidate speedups.

The future main formal producer must retain original code/header/order and public task statements, all5952/7808 outcomes, native defaults and full costs. Preparation may use public statement/import dependencies with equal input information; candidate declarations or generated proof bodies must not silently become shared verified prefix facts. Import-only export state and candidate overlays remain distinct. Setup/export/representation/device initialization/queueing/upload/check/fallback/archive/EOF and failed native processing must all be measured. Statement-only throughput, exported bytes or startup cannot answer RQ4.

Needed real qualification is necessary basic original native acceptance/rejection/incompleteness and actual GPU/CPU engagement on the complete protocol, followed by full formal matrix and independent result review. Do not add diagnostic-string, backend-thread or small-checker self-proof loops. Do not migrate proof language/toolchain to avoid this boundary or substitute supporting4.21 LeanPolish for the formal main benchmark. The current finite5090 E019 matrix already owns the available runtime path; no duplicate Job or unrequested second GPU acquisition is started.

## Coverage, contradiction and novelty disposition

The source disproves direct4.21-hook compatibility, but does not show the formal route impossible. It identifies a concrete isolated native witness/export adapter and an explicitly versioned consumer projection. The standard exporter/container/unchecked-add interfaces are established mechanisms, not novelty. Same-claim risk and all four RQs remain unchanged; no thesis reconstruction or narrower metadata/checker contribution is adopted.

Finite interface/source coverage is complete enough for implementation choice. Full producer/backend integration, imported graph correctness, supported fragment coverage, GPU main performance and broad service contribution remain unmeasured. The next paper-valued decision comes from complete native service and complete CPU/GPU comparisons, including honest negative results. No new empirical experiment was admitted from source/build success alone.
