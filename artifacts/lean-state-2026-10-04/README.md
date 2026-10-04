# Real Mathlib replay and RTX 5090 metadata evidence

Reports: `results/2026-10-04-lean-mathlib-state-reuse.md` and
`results/2026-10-04-lean-gpu-dag.md`. Prior branch history and arena results
remain unchanged. Checkouts/builds and raw inputs remain in the owning workspace.

- `mathlib-gcd/`: eight completed runs, plus 59 responses from the final fresh
  pass interrupted by session handoff. `runs.json` contains only completed runs;
  `jobs.jsonl` also includes those partial responses. Per-candidate decisions,
  errors, warnings, response times and sampled REPL RSS are retained.
- `mathlib-gcd-resumed-final-fresh/`: the missing full 156-job fresh pass, a
  separate invocation with local repeat 0. Combine with the eight completed
  original runs, not the interrupted 59 jobs, for three complete passes/mode.
  `mathlib-summary.json` records this explicitly: 1404 completed decisions.
- `source.lean`, `cases.json`, `command-spans.json` within these directories:
  exact original proof source, each mutation/full prefix, parser-observed byte
  spans. Source/toolchain/binary hashes and arguments are in metadata/provenance.
- `mathlib-gcd-debug-{1,2}/`: failed development trials (sorry warning quotation
  and standalone comment-only request); preserved, excluded from speedups.
- `mathlib-gcd-unbounded-session/`: initial fresh-import design accumulated
  environments; one complete cold pass and a partial fresh pass. It was stopped
  through its parent, not used as a timing baseline. The selected raw journal
  observations in `unbounded-memory-observations.json` retain the 71.6 GiB
  process-RSS sample and contemporaneous cgroup pressure. They are selected
  observations, not a complete journal or post-response RSS series.
- `continuation-pressure-snapshot.json`: actual CPU/memory pressure, affinity,
  load and topology. These do not establish exclusivity or diagnose past load.
- `dag-cpu-{serial,wave1,wave8}.json`: initial CPU measurements.
  `dag-cpu-matched-*.json` and provenance retain the later seven-pass comparison
  after deliberate Lean measurements completed. Both sets are kept.
- `init-lean-reference.json`: actual official parser/reference serialization
  timings. `init-dag.json` / `init-dag-pack.log`: DAG composition, widths, roots,
  preparation time and input/packed hashes. No proof acceptance is inferred.
- `init-dag-inputs.tar.gz`: exact packed DAG, official Lean reference and metadata;
  all members rehashed against originals. `dag-archive-manifest.json` records
  member/archive hashes. Originals remain under
  `/workspaces/.agent-state/gpu-smt-lean-dag` and `/tmp/lean-init-lbv*`.
- `dag_bounds.ptx` / build logs: CPU-only NVRTC build, target compute_80.
  `gpu-execution-script.py` is the submitted stdlib ctypes runtime snapshot.
  `gpu-submitted-identity.json` records the hardware instruction, paths/hashes,
  image and the outer observation available at resume; its pending-state note
  is superseded by the actual runtime record.
- `dag-gpu.json`: actual RTX 5090 run, seven complete arrays matching official
  Lean. All input/reference/PTX hashes match submitted files.
  `gpu-runtime.json`: assigned healthy device, image identity, runtime, node,
  container exit 0 and actual execution timestamps. Outer coordination owns
  the temporary Job cleanup; no GB300 computation ran.
- `dag-summary.json`: derived times and ratios, with host/device stages separate.
  One run with seven resident passes is not seven independent GPU launches.
- Build/test logs, licenses and `provenance.json`: pinned Mathlib/REPL/exporter
  revisions, local REPL toolchain override, Lean/compiler/NVRTC identities.
  `measured-scripts/` reconstructs completed-run harness versions by reverting
  the only post-measurement change (empty-output/positive-repeat guard); this
  reconstruction is described in `measured-script-provenance.json`, not a
  contemporaneous source snapshot. GPU source/runtime were kept unchanged.

The GPU primitive cannot accept/reject proofs. Complete Mathlib proof replay
uses the established community REPL and normal Lean frontend/kernel checking.
Neither fixed corpus is a real model-generated candidate stream.

Repository SMT smoke assertions also passed in `smt-smoke-final`, using explicit
bundled CLI Z3 4.16.0 and installed libz3 4.13.3. The initial setup logs are
retained: `z3` was absent from PATH and the output directory had not yet been
created. These are smoke checks, not additional research speedup evidence.
