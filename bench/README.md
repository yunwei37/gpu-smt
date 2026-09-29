# Benchmarks

The current benchmark layer is deliberately small. Its job is to validate the instrumentation and the main research hypothesis before implementing a large runtime.

## Synthetic prefix benchmark

```bash
python3 bench/synthetic_prefix_bench.py \
  --queries 32 \
  --prefix-constraints 512 \
  --dump-dir traces \
  --json result.json
```

It compares two executions of the same QF_BV workload:

- **cold:** one stock Z3 process per query;
- **incremental:** one stock Z3 process with a common prefix and per-query push/pop deltas.

The benchmark checks that both modes return exactly the expected SAT/UNSAT sequence.

Do not use the reported speedup as paper evidence. The synthetic workload intentionally has a large shared prefix.

## Trace analysis

```bash
python3 tools/analyze_smt_trace.py traces --json trace-analysis.json
```

The analyzer reports:

- exact duplicate queries;
- commands/query;
- nearest-recent common-prefix fraction;
- nearest-recent common-prefix length.

The current analysis is syntactic and command-order sensitive. This is intentional for milestone M0: if even conservative syntactic sharing is high on real workloads, the case for a context-serving runtime becomes stronger.

## Capturing a real Z3 client

```bash
GPU_SMT_REAL_Z3=/usr/bin/z3 \
GPU_SMT_TRACE_DIR=$PWD/traces \
python3 tools/z3_capture.py -in
```

For applications that allow choosing the solver executable, point them at a wrapper/symlink invoking `tools/z3_capture.py`. The shim forwards stdin/stdout incrementally and records each session.

## Real workloads to add

Priority order:

1. Verus / VeruSAGE-Bench;
2. Dafny / Boogie;
3. Viper-family frontends;
4. Kani / CBMC;
5. Lean/Mathlib later;
6. SMT-COMP as an unrelated-query control.

The first paper-quality experiment is **not** GPU performance. It is a workload study answering whether independent real verification jobs expose enough repeated context to justify cross-job state reuse.
