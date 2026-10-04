# Benchmarks

The benchmark layer is deliberately hypothesis-driven. Its first job is to determine whether cross-job state reuse exists in real verification workloads before implementing a large runtime or GPU backend.

## 1. Synthetic prefix benchmark through the Z3 CLI

```bash
python3 bench/synthetic_prefix_bench.py \
  --queries 32 \
  --prefix-constraints 512 \
  --dump-dir traces \
  --json result.json
```

It compares:

- **cold:** one stock Z3 process per query;
- **incremental:** one stock Z3 process with a common prefix and per-query push/pop deltas.

The benchmark checks that both modes return exactly the expected SAT/UNSAT sequence.

Do not use the reported speedup as paper evidence. The workload intentionally has a large shared prefix.

## 2. Direct libz3 state-reuse benchmark

This variant avoids process-startup effects and directly compares fresh vs persistent solver/context construction using stock `libz3` through its C API.

```bash
python3 bench/libz3_state_reuse_bench.py \
  --queries 64 \
  --prefix-constraints 256 \
  --json libz3.json
```

Initial measurements are recorded in:

- `results/2026-09-29-libz3-state-reuse.md`

Again, this is an upper-bound experiment only.

## 3. Trace analysis

```bash
python3 tools/analyze_smt_trace.py traces --json trace-analysis.json
```

The analyzer reports:

- exact duplicate queries;
- commands/query;
- nearest-recent common-prefix fraction;
- nearest-recent common-prefix length.

The current analysis is syntactic and command-order sensitive. This is intentional for milestone M0: if even conservative syntactic sharing is high on real workloads, the case for a context-serving runtime becomes stronger.

## 4. Capturing a generic Z3 client

```bash
GPU_SMT_REAL_Z3=/usr/bin/z3 \
GPU_SMT_TRACE_DIR=$PWD/traces \
python3 tools/z3_capture.py -in
```

For applications that allow choosing the solver executable, point them at a wrapper invoking `tools/z3_capture.py`. The shim forwards stdin/stdout incrementally and records each session.

## 5. Verus / VeruSAGE-Bench

Verus documents `VERUS_Z3_PATH` as the environment variable selecting the Z3 executable, which lets us capture solver traffic without modifying Verus.

Repository:

- https://github.com/microsoft/verus-proof-synthesis
- VeruSAGE-Bench currently contains 849 repository-level tasks from real systems projects.

After installing the Verus revision required by VeruSAGE-Bench:

```bash
python3 bench/run_verus_trace.py \
  --verus /path/to/verus \
  --real-z3 /path/to/verus/z3 \
  --tasks-jsonl /path/to/verus-proof-synthesis/benchmarks/VeruSAGE-Bench/tasks.jsonl \
  --source ground_truth \
  --limit 100 \
  --out artifacts/verusage-100
```

Then analyze every captured Z3 session:

```bash
python3 tools/analyze_smt_trace.py \
  artifacts/verusage-100/traces \
  --window 512 \
  --json artifacts/verusage-100/reuse.json
```

The harness writes:

- per-task source snapshots;
- Verus stdout/stderr;
- every captured Z3 SMT-LIB stdin session;
- task runtime, return code, trace count, and trace bytes.

Start with `--source ground_truth`, and retain actual verification reports: benchmark ground truth can still fail under a different Verus/vstd revision. Separate failures before SMT solving from solver-backed failures.

Useful project-specific slices:

```bash
# NRKernel
python3 bench/run_verus_trace.py ... --project NR

# ATMO microkernel
python3 bench/run_verus_trace.py ... --project OS

# IronKV
python3 bench/run_verus_trace.py ... --project IR
```

## Real workloads after Verus

Priority order:

1. Verus / VeruSAGE-Bench;
2. Dafny / Boogie;
3. Viper-family frontends;
4. Kani / CBMC;
5. Lean/Mathlib is active in parallel under the expanded user scope;
6. SMT-COMP as an unrelated-query control.

The first paper-quality experiment is **not** GPU performance. It is a workload study answering whether independent real verification jobs expose enough repeated context to justify cross-job state reuse.


## Reuse hierarchy experiment

To separate term/AST reuse from live solver-state reuse:

```bash
python3 bench/reuse_levels_bench.py \
  --queries 32 \
  --prefix-sizes 16,64,256,1024 \
  --repetitions 5 \
  --json artifacts/reuse-levels.json
```

The three paths are:

- cold context + ASTs + solver per query;
- one shared Z3 context/AST prefix + fresh solver per query;
- one persistent solver using push/pop.

This experiment helps determine whether the project is merely avoiding parsing/term construction or actually benefits from retaining solver-internal state.

## Fork/COW snapshot benchmark

Synthetic fan-out:

```bash
python3 bench/fork_snapshot_bench.py \
  --queries 16 \
  --prefix-sizes 64,256,1024 \
  --widths 1,2,4 \
  --repetitions 3 \
  --json artifacts/fork-snapshot.json
```

This benchmark compares equally parallel fresh children with children forked from a pre-built solver context. On Linux it also records child PSS from `/proc/self/smaps_rollup`.

Do not use arbitrary multithreaded processes as snapshot parents. A production implementation needs a controlled single-threaded forkserver or equivalent snapshot mechanism.

## Pinned real SMT-LIB workloads

Fetch exact upstream revisions:

```bash
python3 bench/fetch_real_smt.py --out artifacts/real-smt
```

Run fresh-vs-incremental replay:

```bash
python3 bench/smt2_replay_bench.py \
  artifacts/real-smt/*.smt2 \
  --repetitions 20 \
  --json artifacts/real-smt-replay.json
```

Run fork/COW fan-out on files containing at least two related `check-sat` commands:

```bash
python3 bench/related_snapshot_bench.py \
  artifacts/real-smt/z3-loop-unrolling-bitvec.smt2 \
  artifacts/real-smt/z3-loop-unrolling-int.smt2 \
  --repetitions 30 \
  --json artifacts/real-smt-snapshot.json
```

The manifest records upstream repository, revision, and path; third-party benchmark contents are not vendored into this repository.

## Lean export batch serving

The Lean acceleration thread treats a checker as a black box and asks whether
many *independent* Lean checks can be batched (proof-search candidates, repeated
similar goals):

```bash
python3 bench/lean_export_batch.py \
  --checker /path/to/kernel \
  --inputs '_build/tests/other/*.ndjson' \
  --duplicate 20 \
  --widths 1,4,8,16,24 \
  --cores 8-23 \
  --json results/lean-batch-serving.json
```

It reports makespan, jobs/s and accept/reject counts per pool width; the same
binary an application would invoke is the one under test. `--duplicate` is a
fixed-fixture throughput proxy; it does not supply a real candidate stream.

## Current results

SMT serving:

- `results/2026-09-29-libz3-state-reuse.md`
- `results/2026-09-29-preliminary-serving.md`

Lean kernel acceleration:

- `docs/lean-acceleration-plan.md`
- `results/2026-10-04-lean-kernel-stage-split.md`
- `results/2026-10-04-lean-batch-serving.json`
- `results/2026-10-04-lean-mathlib-state-reuse.md`
- `results/2026-10-04-lean-gpu-dag.md`
- `results/2026-10-04-verusage-real-traces.md`

A pinned mixed 100-task VeruSAGE run and real-session reuse experiment are retained in `artifacts/verusage-2026-10-04`; see the result report. Synthetic and small upstream workloads establish mechanism headroom, not the end-to-end systems claim.

## Real-task reuse and GPU continuation

For cross-job characterization, use `tools/analyze_verus_jobs.py RUN_DIR --json
OUTPUT.json`; unlike the generic file-order analyzer it follows recorded task
order and excludes within-task matches. `bench/verus_session_replay.py` compares
fresh sessions, warm reset and prefix pooling through the bundled stock Z3
executable. `bench/verus_scope_ablation.py` and `bench/verus_history_probe.py`
isolate the observed scope/history status differences. Preserve UNKNOWN and
per-query identity; a changed decision disqualifies a transparent speedup claim.
Exact commands and archived source/trace reproduction are in the result report.

`bench/lean-source-trace` and `bench/lean_repl_workload.py` extract actual parser
spans from a pinned Mathlib file and replay complete proofs plus controlled
type-error/sorry variants. They compare established community REPL environment
reuse, fresh commands and cold Lean. They do not reconstruct arbitrary source
scopes or collect actual agent candidate streams. Always use a new output
directory; the harness rejects overwriting old measurements.

`bench/lean_dag_pack.py`, `bench/lean-persistent/LooseBVar.lean`, native
`bench/lean-dag/dag_bounds.cpp`, CUDA `dag_bounds.cu` and `bench/lean_dag_gpu.py`
implement a scoped expression metadata operation on a real export. All CPU/GPU
outputs match official Lean, including the executed RTX 5090 run. This executable
does not verify proofs. Separate original export preparation, packed input
transfer, initialization, resident compute and return transfer. The compressed
exact input/reference is retained in `artifacts/lean-state-2026-10-04`.
