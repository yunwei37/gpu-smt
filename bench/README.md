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

Start with `--source ground_truth` so the workload represents real successful verification rather than only early failing candidates.

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
5. Lean/Mathlib later;
6. SMT-COMP as an unrelated-query control.

The first paper-quality experiment is **not** GPU performance. It is a workload study answering whether independent real verification jobs expose enough repeated context to justify cross-job state reuse.
