# Public Lean code-verification profiles

Pinned official sources, native versions and retained preparation:
[assets and limitations](../../artifacts/lean-code-verification-2026-10-25/README.md).

run-verina.py uses original189Verina reference files and its own4.18.0SDK/
Mathlib pins, native CLI and builtin profiler/structured trace. The published
synchronous checker default is120s per file; this is distinct from the old
miniF2F300s request point. Both retain CPU8–11, at most2actual Lean processes,
24GiBAS per child and48GiBaggregate sampledRSS. Explicitly admitted reference
files remain incomplete even on native exit0. Trace-wall weights are not CPU.

With the retained Kimina Python environment:
    python bench/lean-code-verification/run-verina.py --phase qualification --out /tmp/a-fresh-verina-qualification

The real qualification and full189reference profile are pending while the
original480profile remains the sole collection. run-source/commands/logs/
actual limits will be retained by each group. SDK/cache setup is not a proof
result. No other system's generation/prover baseline is reproduced.
