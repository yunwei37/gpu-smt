# Native Lean preparation experiment: failed branch qualification

This retained BOOTSTRAP experiment007 is **incomplete**: all three actual preflight attempts are terminal, but **0/18 main matrix cells ran**. It supplies no branch speedup, full RQ answer, general fork safety or complete GPU verification. See [plan](../../docs/tmp/bootstrap/step-0006-20261009T222500+0000/experiment-007/plan.md), [result review](../../docs/tmp/bootstrap/step-0006-20261009T222500+0000/experiment-007/result-review.md) and [step report](../../docs/tmp/bootstrap/step-0006-20261009T222500+0000/step-report.md).

Public sources are official Lean4.21.0/6741444a63ee, Mathlib308445d7985027f538e281e18df29ca16ede2ba3 and LeanPolish HF64422193ada0449e2a60d4486955e7319920ed69. Exact URLs, bytes, hashes, package pins and acquisition/build failures are in source-provenance/. Broader upstream archives contain additional corpora without blanket redistribution permission; they remain local and are rebuilt from recorded public URLs. Published input archives contain the licensed Mathlib subset plus actual attempt metadata. The original and corrected input constructions are both retained; the initial construction was never executed. Corrected construction uses actual menu_name and the publisher's formatter rather than successful optimized final_tac. It preserves14913 attempted edits across24 original contexts, all outcomes/kinds; some published elaboration spans are not explicit statement-preserving tactics. This is a new whole-source checking campaign, not exact historical tactic calls or production arrivals.

## Retained execution

- preflight1: invalid missing interpreter exports / unsupported fork boundary. Stock original succeeds; all four complete edited sources reject, including recorded tactic-screen successes.
- preflight2: native original fully checked; logical paths crash on initializer globals, fork refuses3/2TIDs after UVstop.
- preflight3: exact final variant5 native original fully checked. LogicalP1/P4 each complete four rejected full sources with stock-equivalent diagnostics. Fork refuses4/3TIDs despite zero owned unjoined registry records and produces no candidate responses. Residual thread ownership is unknown; count alone does not identify a cause. No method-paired results exist.

The full snapshots use kernel checking (debug.skipKernelTC=false, trust0), checked environment finalization and direct local-sorry screens. Structural declaration fingerprints are comparison witnesses, not semantic equivalence proofs or an imported-axiom audit. Empty/missing/crashed responses are operationally unknown, never proof rejection. Affinity0 versus0,1,2,3 establishes CPU permission, not isolation. Whole-command costs, sampled own-fleetPSS (100ms, may miss peaks) and maximum individual-processRSS retain distinct meanings. Preflight timings are setup diagnostics, not benchmark headlines.

Variant5-final is an explicit runtime extension in both methods: official initializer setup, owned joinable UV lifecycle, exact native lthread pthread lifecycle tracking, manager stop/restart and unchanged one-TID guard plus zero-owned-record check. Foreign threads are not stopped. Full source snapshots being complete does not establish a single-threaded or universally safe runtime boundary. Each executed variant has source snapshots/build commands/hashes; initial failures and unexecuted builds remain retained. Final executable SHA592cadeb85364be313e42bc150bfc01c83eda0833776529a25cbe73f9f92fa9f.

## Analyze retained raw data (no native rerun required)

From repository root:

```sh
python3 bench/analyze_lean_prepared_native.py --run artifacts/leanpolish-native-2026-10-09/preflight3 --controls artifacts/leanpolish-native-2026-10-09/preflight1-controls --out /tmp/lean-native-preflight3-summary.json
```

Earlier preflight1/2 use their matching paths. Original stdio, input identities, run configuration, GNUtime, process-group samples, complete JSON responses, exits and binary/source hashes are retained. CLI controls execute unchanged stock release on original and the SAME four corrected source edits, with matching module-relative filenames. Shared controls are reused because stock binary/input/config did not change. No full-corpus semantic or performance claim follows from four rejected edits.

## Reconstruct dependencies and executed version

Temporary /tmp dependencies are ephemeral; retained sources/results do not assert they survive a container replacement. `source-provenance/acquire.py` downloads the recorded official release, pinned Mathlib and package archives, and public LeanPolish archives. It preserves exact sources and rejects unverified existing downloads. Original package manifests remain unmodified; official Lake package-overrides provide archive-extracted package paths. The official Lake override/cache path is:

```sh
export PATH="/tmp/gpu-smt-lean421-native/lean-4.21.0-linux/bin:$PATH"
cd /tmp/gpu-smt-lean421-native/mathlib4
lake --packages /workspaces/repository/artifacts/leanpolish-native-2026-10-09/source-provenance/lake-package-overrides.json build cache
lake --packages /workspaces/repository/artifacts/leanpolish-native-2026-10-09/source-provenance/lake-package-overrides.json env lean --run /workspaces/repository/artifacts/leanpolish-native-2026-10-09/source-provenance/CacheNativeGet.lean
```

Recorded cache build/download/unpack outputs are cache-build.log/cache-native-get.log. The cache helper does not regenerate or weaken Mathlib proofs. The LEAN_PATH in the retained pathfile is absolute and must point to these reconstructed package build directories. Fetch and extract the pinned runtime-source and libuv archives into the recorded source roots before compiling the extension; their public URLs/SHA are runtime-full-source.json/libuv-source.json. Native build logs and receipts record actual compiler/link commands. `CacheNativeGet.lean` uses official cache hash/download/unpack APIs; optional browser-widget release download requiring Git metadata is omitted, not Lean OLean checking. Runtime source and matching libuv1.48 headers are from runtime-full-source.json/libuv-source.json. C++14 headers supply bundled-clang header lookup; no STL-valued runtime API crosses the extension.

Reassemble each archive from its ordered inputs[-corrected]-chunks/part-* files (chunks.json records identities; input-archives.json records complete hashes). The full archive and unpacked directories also remain local. In a fresh clone, the corrected inputs restore with the following commands; check the assembled SHA256 against input-archives.json before extraction. The uncorrected archive is provenance only. Do not extract over modified existing inputs.

```sh
cat artifacts/leanpolish-native-2026-10-09/inputs-corrected-chunks/part-* > /tmp/leanpolish-corrected-inputs.tar.gz
sha256sum /tmp/leanpolish-corrected-inputs.tar.gz
tar -xzf /tmp/leanpolish-corrected-inputs.tar.gz -C artifacts/leanpolish-native-2026-10-09
```

To rebuild exact final executed native source after dependency reconstruction:

```sh
python3 bench/build_lean_prepared_native.py --sysroot /tmp/gpu-smt-lean421-native/lean-4.21.0-linux --runtime-source /tmp/gpu-smt-lean421-native/lean4-source --uv-source /tmp/gpu-smt-lean421-native/libuv-source --out /tmp/lean-native-rebuilt --receipt /tmp/lean-native-rebuilt.json
```

Recorded final entry point (reference only, not a new authorized protocol attempt):

```sh
python3 bench/run_lean_prepared_native.py --native /tmp/gpu-smt-lean421-native/variant5-final/LeanPreparedNative --sysroot /tmp/gpu-smt-lean421-native/lean-4.21.0-linux --lean-path "$(cat artifacts/leanpolish-native-2026-10-09/source-provenance/lean-path.txt)" --inputs artifacts/leanpolish-native-2026-10-09/inputs-corrected --out /tmp/lean-native-reproduction --workers 1 4 --modes logical fork --repetitions 1 --case-indices 8466 8469 8481 8484
```

No fourth protocol attempt or full matrix is claimed. Complete reproduction requires the pinned cache/toolchain and dependencies above; a build alone is not experiment evidence. The next direction must measure consequential complete native verification against strong existing reuse or resolve a new source-backed runtime boundary, rather than repeat this refused path or remove its guard. RTX5090 generated-candidate allocation is a separate pending experiment002 prerequisite; neither generation nor this CPU work establishes GPU checking.
