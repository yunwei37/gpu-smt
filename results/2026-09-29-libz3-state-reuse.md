# Initial libz3 state-reuse experiment — 2026-09-29

This is the first executable experiment for the project. It is a **synthetic upper-bound**, not paper evidence.

## Environment

- stock system `libz3.so.4`
- Z3 version: 4.13.3.0
- CPU: Intel Xeon Platinum 8573C
- visible CPUs: 5
- Linux x86_64
- benchmark: `bench/libz3_state_reuse_bench.py`

The benchmark constructs a QF_BV chain with a shared prefix and then runs 64 alternating SAT/UNSAT deltas.

Two modes are compared:

- **fresh:** create a new Z3 context/solver and reconstruct the full shared prefix for every query;
- **reuse:** construct the shared prefix once, then use `push` / per-query delta / `check` / `pop`.

All fresh/reuse results matched the expected SAT/UNSAT sequence.

## Results

| Shared prefix constraints | Fresh total | Reuse total | Total speedup | Fresh q/s | Reuse q/s |
|---:|---:|---:|---:|---:|---:|
| 16 | 362.08 ms | 52.04 ms | 6.96x | 176.8 | 1229.8 |
| 64 | 944.26 ms | 37.03 ms | 25.50x | 67.8 | 1728.2 |
| 256 | 730.52 ms | 29.75 ms | 24.55x | 87.6 | 2151.0 |
| 1024 | 1916.81 ms | 199.17 ms | 9.62x | 33.4 | 321.3 |

A separate 32-query / 256-prefix run measured:

- fresh: 1.105 s total;
- reused: 44.7 ms total;
- 24.7x total speedup;
- semantic results identical.

## Interpretation

This result only establishes that **live solver-state reuse can have a large upper-bound benefit** when independent queries really share most of their context.

It does **not** establish:

- that real Verus/Dafny/Viper/Kani queries have this much common structure;
- that an external runtime can always recover the right context cheaply;
- that incremental solving always beats fresh solving;
- that GPU execution is useful;
- that these numbers generalize across Z3 versions or theories.

The non-monotonic timings across prefix sizes are also a warning that solver behavior is noisy and heuristic-dependent. Future experiments need repetitions, confidence intervals, randomized query order, multiple theories, and separate construction/solve timing.

## Next experiment

The next high-value step is to capture real solver traces from Verus / VeruSAGE-Bench and measure:

1. exact duplicate rate;
2. nearest recent shared-prefix fraction;
3. prefix/delta size distribution;
4. solver call runtime distribution;
5. how often a reused context would be available under realistic arrival order.

Only after that workload study should we invest in the context-DAG runtime or GPU backend.
