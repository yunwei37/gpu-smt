# CPU preparation and verified LP closest-work update

Observed 2026-10-14T22:09:54.576242+00:00

Primary sources actually opened:
- https://github.com/leanprover/lp-benchmark
- https://github.com/leanprover/lp-tactic
- Producer SDK4.27 local src/lean/Lean/Meta/AppBuilder.lean
- Pinned producer Mathlib/Tactic/Linarith/Preprocessing.lean and Frontend.lean

The official lp-benchmark compares lp with Mathlib linarith on identical rational arithmetic goals, using tactic-profiler execution time and repeated medians. Its recorded toolchain is4.31.0-rc1 and Mathlib syntactic atom-cache PR40110, newer than this real-workload producer4.27 pin. This is strong competing evidence, not a matched end-to-end Goedel speedup baseline. Its scale examples are linear and therefore do not exercise the product-preprocessing optimization; rerunning them alone would not test this candidate.

The lp-tactic repository describes external solver dual multipliers reconstructed into kernel-checked Lean terms, with backend registration and multiple ordered carriers. Thus externally solved LPs followed by native checking, fast arithmetic reconstruction and modular CPU backends are established prior art. Do not claim them as the project's system contribution. The maintained baseline map must not call the producer427 implementation universally current SOTA. Its actual final speed must survive the strongest runnable path for the declared producer workload, while newer lp/atom-cache behavior is compatibility and prior-art pressure to investigate.

The producer AppBuilder source shows mkAppM creates argument metavariables, unifies explicit arguments and synthesizes instance arguments on each application. The local product candidate reuses a fully resolved application inside one unchanged preprocessor invocation. This is ordinary specialization/application construction optimization until external novelty and whole-service evidence establish a larger contribution. It preserves full product search, unlike the closest upstream FarkasFast hypothesis restriction. A positive tiny pilot is a supporting discriminator, not an OSDI-level system result.

Direct open of the PR40110 page and web AppBuilder tag page returned internal errors; no content or PR verdict is inferred from those failures. The baseline README names that PR, and the actual local tagged SDK provides the inspected AppBuilder source.
