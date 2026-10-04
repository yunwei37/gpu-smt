# Real VeruSAGE tasks: reuse exists, but simple prefix reuse changes results

A deterministic mixed sample of 100 real repository-level tasks produced 156
Z3 sessions and 440 queries. Exact reuse across distinct tasks was sparse;
simple shared-prefix execution changed `unsat`/`unknown` outcomes. This narrows
the serving hypothesis: common commands alone do not justify a transparent
incremental runtime. A warm-process reset baseline showed modest savings in
three completed replay passes, with limitations below.

## Workload and verification coverage

The dataset is [VeruSAGE-Bench](https://github.com/microsoft/verus-proof-synthesis/tree/cbf9c0c6337b224fd8e5b7cb4e01ae65c0f98bc1/benchmarks/VeruSAGE-Bench),
revision `cbf9c0c6337b224fd8e5b7cb4e01ae65c0f98bc1`, 849 tasks.
Selection used `random.Random(20261004).sample(records, 100)` in the returned
order, with original `ground_truth` code. This is published proof replay, not
a generated candidate stream. Benchmark tasks include trusted/admitted context;
verification of these tasks does not certify their whole source projects.

Stock [Verus release 0.2026.09.27.3cf1832](https://github.com/verus-lang/verus/releases/tag/release/0.2026.09.27.3cf1832)
(`3cf18325f0fd0c3040fbdec8c0f2255c0504c91a`), Rust 1.98.1 and bundled
Z3 4.16.0 ran through the existing transparent capture shim. The previous
network/download block was resolved. Exact commands, binary/archive hashes,
selection identities and ground-truth hashes are retained in the artifacts.

| project code | tasks | Verus exit 0 | tasks reaching SMT |
|---|---:|---:|---:|
| IR | 18 | 11 | 11 |
| AC | 8 | 5 | 6 |
| ST | 2 | 1 | 1 |
| MA | 13 | 4 | 9 |
| NO | 5 | 5 | 5 |
| NR | 23 | 11 | 11 |
| OS | 21 | 10 | 10 |
| AL | 8 | 8 | 8 |
| VE | 2 | 2 | 2 |
| total | 100 | 57 | 63 |

All 57 successes have retained verification reports. Of 43 failures, 37 occurred
before any SMT session: examples include changed mutable-reference syntax,
transparent-struct/type errors, unavailable vstd APIs, unresolved imports and
an `assert_by_compute` recursion limit. Six reached SMT and reported verification
errors: five MA tasks failed a shared `pow2` postcondition and one AC task failed.
Do not label every failure a version incompatibility or a rejection of the target
proof. Fresh trace replay returned six `unknown` queries and no `sat`; these
failures do not establish that the published proofs are logically invalid.
No task timed out. Full capture elapsed was 77.162 s, a single run with
instrumentation, `--num-threads 1`, affinity 8–15; it is not an acceleration
baseline. A separate successful IronKV smoke is retained but not counted twice.

## Cross-task structure

`tools/analyze_verus_jobs.py` uses actual task run order and session timestamps.
It excludes candidates from the same `task_id`. Each query reconstructs active
assertions and scoped declarations in observed order; `pop` removes scoped
declarations, and information/output requests are excluded. Quoted whitespace
is preserved. Options remain as observed command history. These are conservative
syntactic metrics, with no alpha-renaming or semantic equivalence inference.

Eight of 440 queries (1.82%) exactly match a query from a previous distinct task
over the complete history. With a 256-query lookback, 439 queries have a prior
distinct task available:

| metric, comparable queries | mean | median |
|---|---:|---:|
| longest matching ordered prefix, commands | 191.71 | 208 |
| prefix / current context commands | 32.14% | 29.05% |
| exact-command multiset overlap / context commands | 71.25% | 72.48% |
| exact-command multiset overlap / context bytes | 52.60% | 50.39% |

Aggregate matching-prefix bytes / aggregate query-context bytes is **6.51%**.
Repeated expanded query contexts count separately in that denominator; it is
not a fraction of the 48,556,449 captured input bytes. Large commands explain
why command counts overstate ordered byte sharing. Best prefix and best
unordered match may come from different prior queries. Per-query source
identities and windows 16/64/256 are retained. A project-grouped ordering
simulation gives 6.43% aggregate prefix-byte sharing at window 256, offering no
clear improvement here; it is not a measured scheduler or real arrival order.

The generic analyzer previously kept declarations after `pop` and reordered
them ahead of assertions. Those errors were fixed, alongside preserving quoted
identity and excluding `get-info`. Regression tests include scope, reset,
command order and exclusion of within-task hits. Earlier synthetic reports
are preserved; their metrics have not been silently recomputed.

## Actual stock-Z3 replay experiment

`bench/verus_session_replay.py` replays all 156 complete captured streams on CPU
8, three times per path, reversing mode order in the middle repeat. Original
options, resource limits, declarations, assertions, checks and output requests
are sent to stock Z3. Parsing/group selection occurs before the timed interval;
process creation, pool setup, transfers, responses and teardown are included.
Each query's `sat`/`unsat`/`unknown` identity is retained, not just totals.

| path | makespans, seconds | median | per-query agreement with first cold pass |
|---|---|---:|---|
| fresh executable per original session | 16.026 / 16.935 / 17.046 | 16.935 | 1320 / 1320 |
| one executable, `reset` before each original session | 14.986 / 15.135 / 15.306 | 15.135 | 1320 / 1320 |
| shared-prefix process pool, job suffix under push/pop | 13.955 / 14.209 / 14.103 | 14.103 | 1227 / 1320 |

The reset path's median was 1.119× faster (10.63% less elapsed) in these complete
passes. All returned 434 `unsat` and six `unknown` per pass. This is fixed-corpus
post-capture throughput, not full Verus acceleration, per-request arrival latency,
or preservation of models/proofs. A retained initial strict trial aborted on a
reset-path mismatch at `NR__definitions_u__impl3__lemma_entry_sizes_increase`;
the partial log records the failure but not the differing response values.
Three successful complete passes do not erase that observation or establish
universal reset fidelity.

The prefix pool has two compatibility groups selected by initial options:
106 sessions share 108 initial commands (9464 bytes), and 50 share one command
(30 bytes). Prefixes stop before observable requests/scope changes. Every suffix
is run inside a fresh scope and its final outstanding scopes are popped.
Each pass nonetheless changed **30 `unsat` to `unknown` and one `unknown` to
`unsat`**, in 31 sessions. It returned 405 `unsat`, 35 `unknown`, and zero `sat`.
These elapsed times are **not a semantic-preserving speedup**.
Do not deploy this path as a transparent drop-in replacement. Cold fallback and
careful UNKNOWN/artifact handling would need separate implementation/validation.

### Controlled investigation of all 31 differences

`bench/verus_scope_ablation.py` ran all 156 streams twice per variant in fresh
executables, reversing variant order. It retained original options/resource
limits and added only an outer `push`, either before declarations or after the
shared prefix. `get-info :reason-unknown` was inserted after checks for diagnosis.

| fresh-executable variant | session differences from cold, each pass |
|---|---:|
| original stream, diagnostic requests only | 0 |
| one outer scope before declarations | 29 |
| one outer scope after the common prefix | 29 |

Those 29 changed queries became `unknown`, with reason
`(incomplete (theory arithmetic))`. They are the same 29 differences in the
pooled path. Additional scope is sufficient to reproduce them without any
preceding job history. This isolates an interface/solver-mode effect; it does
not identify the internal arithmetic algorithm responsible.

`bench/verus_history_probe.py` then targeted the remaining OS and AC sessions,
twice each. With a new prefix worker and the target as its first request, both
matched the cold baseline. Replaying the recorded preceding requests reproduced
both pool differences, and every other query matched the original pool run:

| target | first request after prefix setup | after recorded history |
|---|---|---|
| OS `in_subtree_imply_exist_in_child` | `unsat` | `unknown`, reason `canceled` |
| AC `spec_of_previous_phases_entails_eventually_new_invariants` | `unsat`, `unknown` (second reason `canceled`) | `unsat`, `unsat` |

Thus history is sufficient to change these two outcomes under unchanged query
limits. Learned state, resource accounting and heuristic changes are candidate
mechanisms; this does not isolate them individually. The literal `canceled`
reason does not by itself prove a wall timeout or a particular resource-limit
implementation. A useful runtime must handle this behavior rather than equating
incremental assertion equality with identical SAT/UNSAT/UNKNOWN responses.
All ablation and history-probe inputs, decisions, mismatch outputs and commands
are retained. These tests explain the negative result and provide regression
workloads for a future semantics-preserving fallback or snapshot design.

## Reproduction and retention

Raw evidence lives in `artifacts/verusage-2026-10-04`: `selection.json`,
`provenance.json`, `cross-job-reuse.json`, and complete replay records. The
hash-verified `mixed100-raw.tar.gz` contains all 100 sources, stdout/stderr,
156 SMT streams and metadata (616 files). Uncompressed originals remain on
the owning PVC at `/workspaces/.agent-state/gpu-smt-verusage-20261004/mixed100`.
Extract the archive under `artifacts/verusage-2026-10-04/mixed100` before
replaying repository paths. The original `/tmp` Verus/Z3 installation was lost
in the later container replacement. Obtain the bundled Z3 4.16.0 from the pinned
Verus release and set `VERUS_REPLAY_Z3` to its executable; solver-only replay
does not require Rust. [Recovery instructions](../docs/reproduce-checkpoint.md)
cover setup and reconstruction of the sampled source JSONL for full recapture.

```bash
VERUS_REPLAY_Z3=/path/to/unpacked/verus-x86-linux/z3
tar -xzf artifacts/verusage-2026-10-04/mixed100-raw.tar.gz \
  -C artifacts/verusage-2026-10-04/mixed100
python3 tools/analyze_verus_jobs.py artifacts/verusage-2026-10-04/mixed100 \
  --json /tmp/verusage-cross-job.json
python3 bench/verus_session_replay.py artifacts/verusage-2026-10-04/mixed100 \
  --z3 "$VERUS_REPLAY_Z3" --cores 8 --repeat 3 \
  --out /tmp/verusage-session-replay
python3 bench/verus_scope_ablation.py \
  --run-dir artifacts/verusage-2026-10-04/mixed100 \
  --replay-dir artifacts/verusage-2026-10-04/session-replay \
  --z3 "$VERUS_REPLAY_Z3" --cores 8 --repeat 2 \
  --out /tmp/verusage-scope-ablation
python3 bench/verus_history_probe.py \
  --run-dir artifacts/verusage-2026-10-04/mixed100 \
  --replay-dir artifacts/verusage-2026-10-04/session-replay \
  --ablation-dir /tmp/verusage-scope-ablation \
  --z3 "$VERUS_REPLAY_Z3" --cores 8 --repeat 2 \
  --out /tmp/verusage-history-probe
```

CPU 8 is in the lower maximum-clock group; Lean replay ran concurrently on CPU
0. Shared memory/system load and other work were not isolated. These two core
groups must not be compared as equal CPU-cost baselines. No GPU SMT result or
general serving advantage follows from this run. The next useful SMT step is
version-aligned task coverage and testing controlled state snapshots against the
identified scope/history regressions, before adding scheduling or GPU solving.
[Issue 2](https://github.com/yunwei37/gpu-smt/issues/2)
now has actual real-workload evidence in this branch; it remains open and was
not modified through an external write.
