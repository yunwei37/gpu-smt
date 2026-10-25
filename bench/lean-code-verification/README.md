# Public Lean code-verification profiles

Pinned official sources, native versions and retained preparation:
[assets and limitations](../../artifacts/lean-code-verification-2026-10-25/README.md).

run-verina.py uses original189Verina reference files and its own4.18.0SDK/
Mathlib pins, native CLI and builtin profiler/structured trace. The published
synchronous checker default is120s per file; this is distinct from the old
miniF2F300s request point. Both retain CPU8–11, at most2actual Lean processes,
24GiBAS per child and48GiBaggregate sampledRSS. Explicitly admitted reference
files remain incomplete even on native exit0. Trace-wall weights are not CPU.

Historical reproduction of that recorded point (the driver has not yet been
adapted to the new dynamic resource contract), with the retained Kimina environment:
    python bench/lean-code-verification/run-verina.py --phase qualification --out /tmp/a-fresh-verina-qualification

[The real qualification and all189 native/profile records](../../artifacts/lean-code-verification-2026-10-25/verina-full189-20261025T0725/result-review.md)
are complete. Analyze with:
    python bench/lean-code-verification/analyze-verina.py --run <completed-group>

Each group retains run-source, commands, logs and actual limits. SDK/cache setup is not a proof
result. No other system's generation/prover baseline is reproduced.


Current research execution uses the [new aggregate resource contract](../../docs/architecture.md).
Do not interpret the historical24GiB/max2recipe as a new-resource qualification.
Existing completed Verina data remain; source/toolchain preparation for additional
original code workloads does not establish a measured SAT/LRAT target.
