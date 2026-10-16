# Official full Init: completed native opportunity setup

## Actual workload and complete outcomes

Root builds the official full Init test from pinned Lean Kernel Arena315f24d4 using its actual lka.py build-test init entrypoint and tests/init_module.lean (import Init). The release SDK is Lean4.34.1, git5045d0056413266e57c625dcd7c365b10e377c52. The generated lean4export3.1.0 / format3.1.0 input is347555345bytes and6487065lines. It contains59626declarations. This is the full official standard-library test, not the small Prelude fixture or a relabeled producer4.9prefix.

The official build succeeds in18.167911s, excluding SDK download/extraction and Python dependency setup. lka.py follows lean4export master; the actual fetched exporter is df81913eee5519d5a88ae5b0fd701b5298cc29ab. Input size, line count and Lean/header identity match the retained official snapshot, but this does not establish historical byte identity. Upstream metadata/digest remain original provenance; no new checksum gate is added.

[Complete input archive](../../../../../artifacts/lean-arena-2026-10-16/init-4.34.1.ndjson.gz) is71746353bytes. Root verifies decompression byte-for-byte against all347555345source bytes and retains the original file in the existing owning Workspace /tmp. Lean and exporter upstream license files accompany the artifact. The archive is a real generated input, not a manifest for absent data.

Three actual full-check executions succeed and accept all59626declarations:

| Method / condition | Whole process, seconds | Native parse wall | Native check wall |
|---|---:|---:|---:|
| Original optimized sokonanoda CPU baseline |2.249777|not instrumented|not instrumented|
| Private same-native stage-only diagnostic |2.167728|0.332859|1.827905|
| V3 bridge + host algorithm + all native checks |7.930333|0.333048|1.932996|

All use the real input, --nat-extension --string-extension --axiom-allow-all --threads4 --print-success-message. Complete commands/stdout/stderr/GNU-time resources/terminal receipts are adjacent. No GPU is invoked and no native check is skipped. The7.930333s diagnostic adds a host control before complete native checking; it is not GPU performance. Cross-build single timings are not an optimization A/B or uncertainty estimate.

## Cost coverage, not expression counts

The existing native typed bridge and frozen bounded closure evaluator are unchanged from V3. The new official input makes the previously unresolved complete-workload boundary executable now. There are57544definition/theorem/opaque bodies; every recorded native body interval is nonzero and associates through the actual native declaration index.

| Prospective host outcome | Bodies | Summed corresponding native body-thread CPU, seconds | Fraction of all body-thread CPU |
|---|---:|---:|---:|
| Positive algorithm answer |23367|0.337581756|4.8413%|
| Capacity exhausted |27378|5.399984143|77.4413%|
| Undecided equality |5913|1.056839108|15.1561%|
| Other unsupported |886|0.178601224|2.5613%|
| All bodies |57544|6.973006231|100%|

Positive body count is40.6072%, far larger than its paid-cost fraction4.8413%. The successful stage-only checker spends about84.3%of whole wall inside its check stage, but that is **not** the supported fraction. Do not multiply this wall fraction by a different-run body CPU fraction to manufacture a strict speedup bound.

V3 packing builds6132277expression nodes and126843428packed bytes in0.621891826wall seconds. The host algorithm takes5.025242010s. Packing alone is longer wall time than the positive set's0.337581756s CPU sum. CPU sums across four workers and process wall are different quantities; this is adverse implementation evidence, not a mathematical removable-time bound.

Capacity here means the existing interpreter cannot finish within one of its term/environment/level arenas. Maximum observed steps171465is below the existing two-million-step allowance. The CSV does not identify which arena hit capacity. These are native-accepted bodies, not invalid proofs or a justification to exclude expensive cases. Merely expanding positive counts, increasing arenas or tuning GPU launch flags would not establish a gain.

## Root decision

Retain this completed official-input setup and **do not implement a GPU backend for the unchanged eager bridge/frozen interpreter**. The earlier prefix result was not the only basis: the formal full Init result shows the same poor relation between selected paid cost and preparation overhead, with dominant native cost in arena-exhausted bodies.

Any substantive continuation must change the evaluator/representation so it can retain expensive work without paying away the prospective saving. Exact closure/environment-aware sharing is a possible mechanism to assess, not a proven contribution or permission to report a smaller microkernel. Ordinary CPU compilation remains a baseline. A new mechanism needs its own concrete complete-cost rationale and actual native/device comparison; these measurements do not pre-certify it.

The goal remains the full Lean-first research system and allfourcanonical RQs. This is component setup under RQ4. It does not accelerate source elaboration, answer prepared-state service/SMT questions, provide full CSLib/Mathlib results, establish novel systems contribution or complete EXPERIMENT/WRITE/REVIEW. A source-verification claim must include or justify reuse of export construction, rather than quietly drop it.

## Independent audit and limitations

A fresh independent native reviewer reads the full actual input and all59626CSV rows, directly verifies source/index/cost association, actual producer identity and complete native outcomes, and checks original build/resource/failure provenance. [Independent report](official-init-independent-review.md) supports the narrow adverse decision and preserves the unresolved scope. Root reads the full report before accepting that judgment.

The PGO diagnostic CFG mismatches remain (up to8027checker dispatch counts and72main counts). Added clocks/atomics, prior graph traversal and host queries perturb cache/allocation/scheduling. These are single sequential observations on shared infrastructure. Host positives are unqualified prospective answers, not certified replacement checks: declaration visibility/universe/partial semantics and rejected-input qualification remain relevant before any native skip. Full native checks supply all final outcomes here. No correctness-only investigation is needed to reject this particular cost case.

The copied stage-only diagnostic initially failed to launch with exit126 because copyfile had not preserved its execute bit. That complete failed launch is retained under official-init-stage-only-attempt1.*; root restores the private copy's intended mode0644to0755, preserves bytes, and runs the repaired stage control once. Original optimized baseline is not rerun or changed. The failed1.49mslaunch is not included in performance/acceptance aggregates.

## Evidence and reproducibility

- official-init-source-acquisition.json: pinned Arena sources, release asset URL/identity and existing Python SDK.
- official-init-sdk-download/extraction/version records; exact native SDK git identity.
- official-init-build-command.json and official-init-build.terminal.json, original stdout/stderr and resolved exporter source.
- official-init-upstream-stats.json: original upstream generated metadata, including producer/size/line provenance.
- official-init-lossless-input-archive.json: bytewise roundtrip and retained source/archive paths.
- official-init-native-baseline.*, official-init-stage-only.* and native-support-v3-official-init.*: all real native commands, process results and resources.
- native-support-v3-official-init.csv and its independently recomputed analysis JSON; native-support-analysis.py reproduces the weighted arithmetic.
- stage-copy-mode-repair.json and original failed launch records.
- Earlier published V1/V3 source, native patches, frozen evaluator, private build commands and independent source reviews.

The existing Workspace /tmp has room for regenerable SDK/export/build state on a different filesystem from the project PVC. No new Workspace, mount, volume, benchmark Pod, persistent helper or model setting is introduced. Durable scientific source/input/result evidence is published from main.
