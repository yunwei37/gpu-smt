# Same-native stage setup: actual build and execution

This completed setup builds the pinned sokonanoda source with the published [small CLI timing patch](../../../../../bench/lean-gpu/arena-stage-timing.patch), existing Init.Prelude-trained PGO and native CPU target. All four executions complete normally with exit0. Full official Init.Prelude4.34.1 accepts2106declarations; the retained Mathlib4.9 prepared prefix accepts29709. Parse-only output is not acceptance. Exact commands, input metadata, stdout, stderr and /usr/bin/time resource outputs are retained next to this report.

| Input | Whole process, s | Same-process parse, s | Same-process check, s | Check / whole |
|---|---:|---:|---:|---:|
| Official Init.Prelude4.34.1 |0.037280|0.005711|0.018397|49.35%|
| Retained prepared Mathlib4.9 prefix |1.569244|0.908618|0.654685|41.72%|

For the retained prefix, erasing the entire measured check stage at zero cost while holding everything else fixed gives a conditional1.715847x speedup. GPU support covers only a still-unmeasured subset, so this is not a realizable GPU benefit or a rigorous complete-verification bound. Per-stage times do not include all process lifetime; the tiny Prelude whole measurement is sensitive to launch/scheduling noise. Separate parse-only wall is a component control and is not subtracted to manufacture a removable fraction.

The Mathlib prefix is159423522bytes from the original retained experiment021/preflight2 producer4.9export; it includes preparation/warmup, is neither the official4.34full Mathlib input nor a source-verification workload. These single setup observations establish no repeated performance estimate, version transfer or source-to-proof gain. The existing PGO profile has a retained changed-main CFG warning (72counts); this diagnostic binary is not promoted to a new exact official baseline.

No GPU is invoked, no native obligations are bypassed and no complete GPU preflight passes. Native typed bridge/support and actual paid supported body costs are next necessary mechanism work. The preexisting resident evaluator still uses per-query scratch and online CPU checking; those costs cannot disappear from future comparisons by assumption.

Storage: after private dependency build and bounded159MBinflation, project volume had8.621GiBfree at11:27Z. The three declared official large inputs sum8.955GB; they cannot be expanded together with current build/capture state. The small official suite deliberately omits files >10MB. No deletion of active state, retained source results, volume resize or new storage entity is performed.

[Machine-readable arithmetic](native-stage-cost-analysis.json), [native observations](native-stage-observations.json), [build command](native-stage-build-command.json), [build terminal](native-stage-build-terminal.json), [compiler discovery repair](compiler-discovery-repair.md), [input provenance](native-stage-inputs.json), [official small-suite receipt](small-suite-download.json), [official GHA artifact discovery](official-run-artifact-discovery.json).

## Later filesystem qualification

At11:48:52Z root checks actual df/device identities: the project is the existing67.3GBLonghorn/workspacesvolume with7.13GBfree, while the owning Workspace /tmp lives on its existing overlay filesystem with317.03GBfree. Private native builds and the159MBinflation are on the latter, not the project volume. Thus cleaning those private build intermediates would not recover project space. None is deleted, and no active/original state changes.

The earlier statement about fitting all8.955GBinputs on the project volume is a project-volume-only constraint, not a demonstrated benchmark blocker. Regenerable official input/build state may use the already-available owning Workspace /tmp without a new volume, Workspace, mount or storage configuration. Source/raw results and durable provenance remain in the project repository. [Actual filesystem receipt](storage-filesystem-qualification.json).
