# Corrected-family pair 2: complete

Captured and published 2026-10-18 UTC. Executor/reviewer: owning Codex thread (self-review).

Oracle-first alternating order, then strong native; original 1,000 sources, width 4, CPU 12–15, 48 GiB. Native 2234.142870456 s; CPU oracle 1751.171954856 s; ratio 1.275798681x. Both return 992 complete and 8 rejected, no operational failures. The 88 JSON differences are warning-only; source verdict and non-message differences are empty. All candidate spans are present.

This is one closed pair, not the final three-pair decision. Pair 3 proceeds under its frozen launch. The GPU route remains open pending corrected-family wall profiling and the admitted size-gated race/batching experiment. Neither prior GPU failure nor this CPU ratio alone closes that route.

The collector generated launch.json replaces the early driver receipt when copied; driver-launch.json preserves that original receipt verbatim from the preceding Git version. Compressed raw responses, candidate intervals, process observations and native I/O are retained.
