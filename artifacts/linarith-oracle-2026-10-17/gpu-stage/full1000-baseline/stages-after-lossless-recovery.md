# Native stage attribution after lossless log recovery

The original raw Lean telemetry still contains ten malformed physical lines. Each adjacent pair has exactly one invertible foreign-record splice; the recovery receipt proves exact reassembly without synthesizing a source, timing or value. All134640 JSON records are now readable in the derived stream. Four native numeric requests remain missing source/client IDs; global costs include them, source-specific attribution remains limited. Historical raw evidence is untouched.

| Stage | Calling-thread CPU seconds | Stage timeline occupancy / whole |
|---|---:|---:|
| Preprocess + ring/linearize | 331.666648 | preprocess and linearize separately below |
| nlinarith product proof generation | 288.030006 | 10.708% |
| Internal Lean LP caller CPU | 9.837393 | 43.097% |
| External LP search | 979.803368 | 42.280% |
| Final certificate reconstruction/check | 275.210866 | 10.749% |

Preprocess occupancy is9.248%; ring/linearize occupancy is4.839%.

These are NOT a disjoint wall partition. Each occupancy is that phase\'s own interval union divided by whole2319.668326413s; concurrent phases can overlap. Lean LP wall includes waiting for the external LP, so never add the internal-caller and external-search occupancy. CPU columns count different calling threads and cannot be divided by wall as an Amdahl fraction. Preparation, collector, unattributed work and retirement remain in whole clocks.

External numeric search occupancy is42.280%; its interval sum is980.759955514s. Freezing all other work and certificates, eliminating this search would leave1338.908370899s. This is a conditional sensitivity, not achieved speedup or a certified impossibility bound; source IDs remain missing for four requests and changing solver supports can change proof/fallback work. It does not rule out1.5x, so actual GPU measurement proceeds.

The288s native product stage builds proof terms, whereas the direct AST oracle\'s3.37s numeric product generation is different work. A GPU LP backend does not replace native proof construction; do not credit it with removing288s automatically. Current GPU implementation leaves polynomial products on CPU.

## Matrix shapes

- fallback_fp-scaled_rows: {"count": 13414, "min": 2, "median": 10, "p90": 84, "p95": 130, "p99": 183, "max": 888}
- fallback_fp-scaled_cols: {"count": 13414, "min": 2, "median": 20, "p90": 253, "p95": 347, "p99": 552, "max": 3160}
- fallback_fp-scaled_nnz: {"count": 13414, "min": 3, "median": 74, "p90": 1763, "p95": 2617, "p99": 4648, "max": 26044}

All13414 native FP matrix shapes are present. Product-origin counts were not recorded for these native calls, and remain unknown rather than zero. R2 generated-proof ancestry flags are qualified on a separate24-source capture; do not invent full-cohort provenance from coefficient matrices.

Self-review only; new actual candidate spans are collected in the running fixed1000 GPU/CPU trial. Historical wave times do not become per-candidate times.
