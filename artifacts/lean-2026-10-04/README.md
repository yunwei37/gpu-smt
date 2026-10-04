# Retained Lean research data

The path-availability statements below describe the measurement container.
The later 22:16 UTC recovery retained this repository/PVC but lost `/tmp`
dependencies and large original exports. Fixture archives, measurement logs
and pinned metadata remain; see `docs/reproduce-checkpoint.md` and
`docs/lean-resource-status.md` for current availability and reconstruction.

All paths are in the owning `gpu-smt-dev` workspace. These records preserve the
first worker's measurements and the Codex continuation without changing source
checkouts, input exports or branch history.

- `persistent-small.json` / `.log`: 18 trials of 920 repeated fixed-fixture jobs;
  per-job path, status, message and response time; input and binary hashes;
  requested affinity and exact harness arguments. This is a throughput proxy,
  not a real agent candidate stream. Parent affinity is also retained in JSON;
  checker children use the `settings.cores` taskset mask.
- `persistent-validation.json` / `.log`: the broader fixture pass, recorded when
  each full mode finishes. If the JSON is absent/incomplete, the pass is still
  running or failed; do not interpret that as a result.
- `frontend-profiles/`: paired skip/normal-check source copies and complete
  stdout/stderr, exact invocations, hashes and exit codes in `runs.json`.
- `fixture-inputs.tar.gz`: exact built bugs/other/corner/tutorial/perf inputs and
  tutorial info files. Extract into the original `_build/tests` directory or
  pass matching paths to the harness. It contains 215 NDJSON exports; originals
  remain under `/tmp/lean-kernel-arena/_build/tests`.
- `manifest.json`: original arena revision, full corpus hashes and metadata,
  export headers, input declaration-record counts and derived decimal KB per
  record, plus fixture archive hash. Init/std were rehashed at continuation;
  Mathlib/CSLib hashes come from retained original sha256sum records. CSLib was
  exported by Lean 4.34.0; the other three by 4.34.1. Checker toolchain is 4.34.1.
  The multi-GB inputs stay in the owning workspace; rebuild using the pinned
  arena metadata if moved. Never infer their presence from metadata alone.
- `prior-raw/`: original timing/perf/build logs and scripts, retained byte-for-byte.
  `bw.c` is retained as flawed evidence, not a valid bandwidth measurement.
- `arena-local-results/`: previous local harness per-input observations, including
  outcomes, exceptions, RSS and correctness scores. Some wrappers classify all
  nonzero failures as rejection. These are finite scored observations.
- `arena-public-results.json`: downloaded public snapshot from another runner,
  dated 2026-10-03 and revision b1d6e91d; not a workspace measurement.
- `prior-commands.json`: selected actual research shell calls with original UTC
  timestamps, extracted from the prior journal. `prior-journal-evidence.json`
  retains selected original tool outputs, including the erroneous grind profile.
  These are not a full shell history. Some intermediate manual configs were
  overwritten; final copied configs cannot prove historical settings.
- `official-Main.lean` / `official-lakefile.toml`: exact measured official wrapper
  and build definition; the exporter dependency is pinned in checkout metadata.
- `checkout-versions.json` and checker/test YAML: checkout revisions, pinned
  dependencies, final configs and build/run metadata. See per-run commands for
  historical overrides and thread counts.
- `cpu-topology.txt`, `lscpu.txt`: distinct higher/lower maximum-clock core groups;
  affinity alone never establishes exclusive CPU access.
- `validation-pressure-snapshot.json`: contemporaneous cgroup/host memory-pressure
  evidence during the broader pass. It does not retrospectively diagnose earlier
  timing differences or identify which other process caused host load.
- `lean-version.txt`, `persistent-build.log`, `lean-unit-tests.log`: build and
  Lean-specific test validation. `unit-tests.log` also retains the unchanged SMT
  analyzer test failure in full-repository discovery.

Reproduction commands are in `results/2026-10-04-lean-persistent.md`. The arena
and upstream source licenses apply to archived fixtures; the pinned arena license
is retained here as `arena-LICENSE`.
