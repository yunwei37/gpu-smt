# Pinned real VeruSAGE evidence

Report: `results/2026-10-04-verusage-real-traces.md`.

- `selection.json`: 100 task identities, original dataset revision/hash, seeded
  selection and ground-truth hashes. The later container replacement lost the
  temporary 849-task dataset and sampled full-record JSONL. The archive retains
  all selected ground-truth sources and task order needed by the harness;
  `docs/reproduce-checkpoint.md` explains reconstruction and pinned dependencies.
- `provenance.json`: Verus/Rust/Z3 versions, release and dataset URLs, exact
  capture command, binary/download hashes and concurrency/affinity scope.
- `mixed100/runs.jsonl` and `summary.json`: original task order, per-task elapsed,
  exit, timeout, captured sessions/bytes; 57 successes, 37 failures before SMT,
  six failures reaching SMT. Ground truth does not imply success under this
  Verus/vstd version. All actual stdout/stderr reports are retained.
- `mixed100-raw.tar.gz`: sources, logs, traces and metadata, 616 hash-verified
  files. `raw-manifest.json` and `raw-archive.json` record every member's identity.
  Uncompressed originals were moved intact to
  `/workspaces/.agent-state/gpu-smt-verusage-20261004/mixed100` after replay,
  retaining data on the owning PVC. Extract under `mixed100` to reproduce
  repository-relative trace paths. The capture wrapper has owning-workspace
  absolute paths; use the harness to regenerate it when moving environments.
- `cross-job-reuse.json`: actual run order, task compatibility coverage,
  all trace hashes, exact query identities and per-query source matches. Search
  excludes the same task. Project grouping is an ordering simulation. The
  48,556,449 raw bytes and repeated expanded query-context byte denominators are
  different quantities; syntax sharing does not establish speedup/equivalence.
- `session-replay/`: nine complete runs, 156 sessions and 440 decisions per
  pass. All 1320 decisions match first cold baseline in each completed cold/reset
  mode. Prefix pooling changes 31 sessions per pass. Per-query identities,
  expected/actual statuses and full mismatch output are retained. No model/proof
  fidelity or full Verus acceleration is claimed.
- `session-replay-strict/` and its log: earlier development trial stopped on a
  reset-path mismatch. That failing response was not written before the strict
  exception; do not infer its differing values from later runs. The observation
  is preserved and limits generalization from the completed reset trials.
- `scope-ablation/`: two complete passes of original, extra outer scope and
  fresh prefix-scope variants. Scope alone reproduces 29 pool differences,
  with arithmetic-incomplete reasons, in fresh executables.
- `history-probe/`: two first-request versus recorded-history tests of the
  remaining OS/AC sessions. History reproduces both differences. All other
  replayed decisions match the original pool run. Literal cancellation reasons
  do not identify their internal mechanism.
- `smoke/`: first IronKV task verified and generated a real trace; not counted
  as an additional task in the 100-task totals.
- `dataset-README.md`, `dataset-LICENSE`: pinned upstream methodology/license.

No original project source was rewritten to force compatibility. These are
published proof replays with benchmark-provided trusted context, not full
project certification or a captured agent arrival/candidate stream.
