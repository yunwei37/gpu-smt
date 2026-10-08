# Ordinary Mathlib module profiles

Supporting BOOTSTRAP experiment003 under RQ4; full36cell matrix has reached terminal status. A fresh independent [result review](../../docs/tmp/bootstrap/step-0002-20261007T224656+0000/experiment-003/result-review.md) and root audit accept this as valid supporting local scope evidence; completion alone is not a research verdict. The first real preflight is complete but is dependency evidence only. The [approved plan](../../docs/tmp/bootstrap/step-0002-20261007T224656+0000/experiment-003/plan.md) fixes six complete purposively selected Mathlib modules, two paths, three repetitions and alternating paired order. This is ordinary source elaboration and checking of new declarations, with compiled imports; it does not recheck every transitive proof, measure a prepared service or establish GPU benefit.

Exact Lean4.9.0-rc1 `be6c4894e0a6c542d56a6f4bb1238087267d21a0`, Mathlib `2f65ba7f1a9144b20c8e7358513548e317d26de1`, sources/vendor adaptation/build logs and restoration commands are in [native-setup](../lean-candidate-source-2026-10-07/native-setup/README.md). Dependency build is already terminal. Do not repeat archive restoration into its adapted manifest. GNU time is Debian package `1.9-0.2`; its actual `--version` string reports `UNKNOWN`, retained without substitution in environment-observations.json. This file also retains actual Lean/Lake versions, CPU topology, affinity and initial load.

From repository root, with these exact dependencies and ordinary GNU time installed:

```bash
capture_root=/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture
export XDG_CACHE_HOME="$capture_root/cache"
taskset -c 0 python3 bench/lean_profile_modules.py \
  --workspace "$capture_root/mathlib4" \
  --lake "$capture_root/lean-4.9.0-rc1-linux/bin/lake" \
  --lean "$capture_root/lean-4.9.0-rc1-linux/bin/lean" \
  --out artifacts/lean-module-profile-2026-10-08/reproduction --repeats 3
python3 tools/analyze_lean_module_profile.py \
  --input artifacts/lean-module-profile-2026-10-08/reproduction \
  --out artifacts/lean-module-profile-2026-10-08/reproduction-analysis
```

Outputs must be new directories; preserve existing runs. A separate `--preflight` invocation checks the first original module once per path. The runner sets exact release-bin PATH, LC_ALL=C, LEAN_NUM_THREADS=1 and child CPU0 affinity. Its native command is `/usr/bin/time -v -o <receipt> <lake> env <lean> -j1 --json [--profile] <module>`, with no emitted olean/ilean/C flags or trust/checking changes. Affinity does not establish host isolation. Native `--profile` uses its default100ms display threshold; short calls still enter cumulative totals. Executed capture/analyzer bytes are under executed-source/, including the exact version used for these measurements.

`full/events.jsonl`, per-cell raw stdout/stderr/GNU time/result records and six source snapshots retain every planned cell, load observation, command and terminal outcome. `full-analysis/summary.json`, cells.jsonl and tables.md recompute the full matrix, paired diagnostics/exit identity, category displays, wall differences, CPU and maximum RSS. Presence of terminal records does not itself establish successful checking or valid interpretation; failures, malformed data and admissions must be inspected. Raw preflight and its distinct analysis remain under preflight/ and preflight-analysis/.

Driver invocation wall includes time/Lake/Lean launch, event capture and up to20ms completion polling; subsequent fsync/result serialization/source hashing and outer taskset startup lie outside it. Corpus makespan includes capture lifecycle. GNU time CPU and maximum RSS are separate raw diagnostics; maximum RSS is not fleet proportional memory. Native category times are rounded exclusive elapsed scopes within a thread and can overlap across threads. Shares of those categories are descriptive only, not CPU/wall fractions, critical paths, Amdahl bounds or dynamic GPU-ready work. Type checking includes AddDecl wrappers and auxiliary declarations; residual elaboration is not a measure of shareable theorem preparation. Profile/normal wall ratios include system variability and cannot isolate instrumentation causally.

No module cost from a partial matrix is promoted to a result. Full completion, fresh result review and root interpretation are established. Native AddDecl/type-checking accounts for3.8–5.5% of observed accumulated categories; larger frontend/meta scopes motivate deeper profiling at this local boundary. This is not a wall/CPU fraction or a universal GPU upper bound. Profile/normal invocation ratios span1.008–1.079; variability and observer cost remain explicit. All paired Lean JSON outputs are identically empty and native exits0; seven identical Lake vendor-packaging warnings remain in every stderr, so the data are not warning-free. All four paper RQs stay open.
