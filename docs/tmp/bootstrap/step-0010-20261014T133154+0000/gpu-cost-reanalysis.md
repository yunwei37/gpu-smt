# Native6 GPU cost and coverage: all three complete ProofNet primary repetitions

Supporting RQ4 analysis of existing complete source-native captures, not another experiment or complete RQ answer. Recompute with python3 gpu-cost-reanalysis.py in this directory. The script reads the original three ZIPs through the established E022 raw analyzer and retains per-PID cumulative maxima, never summing repeated checkpoints. It reproduces all stored provider aggregates exactly.

| Rep | Warm s | GPU s | Slower | Supported / calls | Observed support | Provider summed wall s | Init s | Allocation/upload s | Launch/sync s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|0|310.478|315.870|1.74%|2201 / 2380684|0.0925%|3.1693|1.3258|0.1162|0.0259|
|1|311.544|322.891|3.64%|2201 / 2380181|0.0925%|4.9208|1.1778|1.0531|1.2913|
|2|318.572|323.607|1.58%|2201 / 2380685|0.0925%|6.1579|1.2739|1.6506|1.7438|

## What the existing mechanism actually does

bench/lean-gpu/closure-native-provider-v5.cpp issues cuLaunchKernel with grid=(1,1,1) and block=(1,1,1), followed by cuCtxSynchronize. It offloads one narrow beta/zeta reduction synchronously, not a batch of independent reductions or the complete Lean kernel. One active CUDA thread cannot use this GPU's broad parallel arithmetic capacity. Host classification, packet preparation, allocation/upload, synchronization, readback and quotation accompany useful work; ordinary native fallback and final kernel checking remain.

Observed successful support is approximately 0.0925% of provider calls in each repetition. Unsupported native heads are largely rejected before packet construction by the existing conservative native Expr walk. This is a call-count result, not a measured fraction of checking time: expensive and cheap calls differ, and the failed native worker lacks terminal counters. Each GPU repetition contains one censored worker; the basic cohort remains complete because normal replacement returns every original input.

## What can and cannot explain the negative whole result

The mechanism engages RTX5090 and returns 2201 supported native results, but most provider calls still need the ordinary CPU path. Device initialization plus serialized tiny operations add measured costs rather than displacing most work. Upload and launch/sync observed sums rise substantially across repetitions. These timers measure steady-clock duration and include waits; they are not isolated CUDA kernel execution time.

The complete warm-vs-GPU slowdown is 1.74%, 3.64%, 1.58%, superseding the reader-facing old native4 ~33% number for the current native6 implementation. This does not establish a causal improvement across versions. Nor can provider sums be subtracted from whole makespan: workers overlap and uninstrumented wrapper/native costs remain. Shared-GPU contention is a possible contributor to variable waits, but no matched concurrent-owner trace or controlled comparison establishes it as the cause.

## Research disposition

These data reject the current single-operation provider as an acceleration result on this cohort. Merely shortening already-small transfers or another metadata-only speedup cannot establish complete Lean acceleration. Any next GPU mechanism must reach expensive native work and expose parallel independent work, then beat the strongest measured CPU path on the full formal cohorts with transfers/fallback/final checking included. The current complete stock-service acquisition continues unchanged; no speculative parallel GPU run is launched on top of it. Wider CPU/GPU/concurrency and miniF2F evidence, all four RQs and the full paper objective remain open.

This report is root analysis/self-review under the human no-delegation instruction; it is not independent audit.
