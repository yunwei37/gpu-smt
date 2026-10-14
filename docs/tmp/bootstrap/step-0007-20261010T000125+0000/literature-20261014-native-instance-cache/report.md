# Existing native instance caching

Question: does generic sharing of synthesized instances supply a new mechanism after measured typeclass hotspots? Source boundary: official Lean implementation only; no secondary summary. Complete source obtained from immutable commit eb7bc1e7852a0be63d09836fc4b078bd37dbecf5 on2026-10-14.

Official current source validates recorded option/environment dependencies and caches abstract metavariable results. It has optimizations for closed cached results and differential cache validation. These are prior mechanisms and a strong implementation comparator; generic memoization cannot be claimed as GPU-SMT novelty. The current implementation is not yet a measured baseline in the pinned4.9 candidate stream, and master-source evidence does not establish a released version or performance. Next action is cost/context attribution of common projection families and a fair comparison with native caching, not an unqualified older-cache-only win. Initial Narrative/allRQ/scope unchanged.

Source: https://raw.githubusercontent.com/leanprover/lean4/eb7bc1e7852a0be63d09836fc4b078bd37dbecf5/src/Lean/Meta/SynthInstance.lean
