# Native saved-candidate preparation experiment, 2026-10-09

This is experiment006 under [step0005](../../docs/tmp/bootstrap/step-0005-20261009T194100+0000/step-report.md). The [plan](../../docs/tmp/bootstrap/step-0005-20261009T194100+0000/experiment-006/plan.md), [complete result](../../docs/tmp/bootstrap/step-0005-20261009T194100+0000/experiment-006/result-report.md) and [independent review](../../docs/tmp/bootstrap/step-0005-20261009T194100+0000/experiment-006/result-review.md) define its scope.

All 3566 released AutoVerus main-cohort sources enter a NEW whole-file native campaign: two observation paths, three repeats, 21396 terminal calls, no operational timeout. This is saved proof-improvement/program-attempt replay, not recovered historical native/Houdini traffic, deployed arrivals or task-intent equivalence. Source bytes, failures and duplicate attempts are retained.

Observed comparable feedback:10647 equal/0 different/51 unknown pairs. The unknowns are17 repeated syntax-error inputs with no stdout JSON and native exit101. They remain unknown even though raw empty stdout, diagnostics and exits match. Per condition/pass190 exits0,3359 exits1,17 exits101. JSON success=true609 includes419 exit-one/verified-zero pre-SMT failures: it is not acceptance.

Each pass2789 inputs creates2790 solver calls; candidate2757 has two,777 inputs have none. All8370 observed initial-flush snapshots are complete and precede checks. Initial live-task CPU median15.314ms, initial PSS median36955KiB; these are captured-condition live observations, not CPU upper bounds or fleet/peak memory. Literal initial-prefix recurrence is zero under unique candidate filenames;8367of8370 prefixes contain those namespaces. This cannot establish absence of earlier shared frontend/import state or a general SMT/Lean/GPU limit. Capture adds10.59% aggregate invocation wall and11.18% reported OS CPU relative to direct totals, with load and temporal variation; no acceleration or service comparison is claimed. Four paper RQs remain open.

## Restore all raw data and analyses

The complete stable archive is466431416bytes, SHA256 `a975a7a63d018093054905935b19ae4057063c2c05b74066e16896286cce7f81`. Twelve standard40MiB-or-smaller chunks are included in this checkpoint to keep each blob below host limits. From repository root:

```sh
cd artifacts/autoverus-native-2026-10-09
cat retained-native.tar.gz.part-* > retained-native.tar.gz
sha256sum -c SHA256SUMS
gzip -t retained-native.tar.gz
tar -xzf retained-native.tar.gz
cd ../..
python3 tools/analyze_autoverus_native_capture.py artifacts/autoverus-native-2026-10-09/full --out artifacts/autoverus-native-2026-10-09/reanalysis
```

Archive paths are relative to this directory. It contains all full/preflight input copies, receipts, original stdout/stderr, GNU-time outputs, every native solver byte stream and process snapshot, initial and portable full JSON/CSV analyses, executed code versions, initial drafts, build failures, exact source/version/configuration records and portable actual-preflight analysis. The initial numeric analysis is unchanged by the portable input-lookup fix; [recomputation hashes](analysis-recomputation.json) record byte-identical JSON/CSV output. The current analyzer resolves retained inputs within the supplied run root; recorded absolute native execution paths remain provenance. No executable dependency is required to reanalyze.

Uncompressed data and both archives remain on the owning PVC. The first packaging attempt exits1 with a directory-metadata-change warning; its archive and [log](archive-command.log) remain locally. The final archive is written outside the read tree, exits0 and passes gzip validation; [final log](archive-command-final.log) is retained. Neither packaging attempt executes a verifier or adds scientific evidence. Large working directories and unchunked archives are locally ignored, not discarded; chunks retain all raw/derived evidence in Git.

## Rebuild and execute a new campaign

Publisher source/data revision: microsoft/verus-proof-synthesis `cbf9c0c6337b224fd8e5b7cb4e01ae65c0f98bc1`. Original sources/context logs and acquisition hashes are in [the retained cohort](../autoverus-source-2026-10-07/README.md). Exact Verus source revision `33269ac6a0ea33a08109eefe5016c1fdd0ce9fbd`, isolated Rust1.76.0, official Z34.12.5. [Fetch metadata](source-provenance/fetch-metadata.json) gives original public archive URLs and SHA256 hashes; [build products](source-provenance/build-products.json) gives actual binary hashes. Embedded version/commit Unknown is the official Gitless source-archive fallback, not fabricated version provenance. Dependency vstd build784verified/0errors is not a workload result.

The existing matched dependencies are `/workspaces/.agent-state/gpu-smt-deps/autoverus-verus-33269`. If absent, first fetch/extract the exact source archive into its recorded `verus-33269ac6a0ea33a08109eefe5016c1fdd0ce9fbd` directory, checking the recorded SHA256, then use [build-pinned.sh](source-provenance/build-pinned.sh). That script expects the extracted source and lifecycle rustup at `/usr/local/cargo/bin/rustup`; it downloads the exact Z3 release and installs only the isolated pinned Rust toolchain. GNU time must also exist at `/usr/bin/time`. No new project checkout or default-toolchain change is needed. Build/network failures remain external reproducibility dependencies, not proof results.

[full-command.sh](full-command.sh) records the actual invocation environment, backend paths, flags, CPU8 affinity,120s per-invocation cap and three alternating conditions. It requires an exclusive output directory. Preserve the original `full` directory; to execute another campaign, use the same flags with a new `--out` directory rather than overwriting the retained run. This creates new data under the declared naming protocol, not exact-resume fiction. The root runner remains thin glue around the original verifier; the observation shim adds no solver command. `executed-full` preserves the actually executed native runner/shim/analyzer identity, while `executed-analysis` preserves the later portability-only analysis version.

Primary whole-command elapsed/OS CPU/maxRSS, native wait4 lifetime costs and first-DONE live CPU/RSS/PSS differ in scope. Native smt-init starts after initial statistics/prelude flush and omits function buckets; it is not initialization CPU. Process ticks and GNU-time printed fields are quantized, live-task CPU omits departed threads, sequential snapshots are not instantaneous, and CPU affinity does not establish isolation. Per-input/load/variance records remain complete. Direct solver transport was unobserved: source-feedback equality does not certify models, mathematical equivalence or full underlying response parity.
