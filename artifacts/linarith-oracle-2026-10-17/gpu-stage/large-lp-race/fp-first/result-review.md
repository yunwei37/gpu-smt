# FP-first prototype CPU qualification — root self-review
Real24 original sources,width8,CPU8–11,48GiB, fresh pooled native reference.
Native 30.531879599s; CPU AST oracle 27.654410813s.
All24complete; no verdict/non-message response changes; 2 warning-only changes.
This qualifies the numerical dispatch before GPU hardware testing; it is not a full-population speedup or proof of GPU benefit.
The original CPU fallback and row11 eligibility remain. Only exact-fallback LPs race after FP search/repair in this private build.
The CPU race child starts the original tiered exact engine, rather than repeating the parent's FP search.
Default build-race and run-race paths preserve the already-running whole-LP variant. Its binaries are not touched.
An initial Rust worker compile used the wrong public crate path; failed logs are retained, the path corrected to tiered::produce_certificate_tiered, then the private build and this real native qualification completed.
Next: same24 source hardware qualification, true minimum2request batches, same total4CPU eligibility8–11 for GPU server and client, sequential after current full GPU Job retires; do not overlap onCPU0–3 with the pooled own-clock diagnostic. Self-review only.
