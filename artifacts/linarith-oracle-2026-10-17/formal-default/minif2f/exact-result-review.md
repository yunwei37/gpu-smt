# Complete original miniF2F exact-prefix comparison

Captured 2026-10-18 UTC; owning-thread self-review.

All7,808 original candidates returned. Exact-prefix wall41,738.632061801 s
versus native-batch28,673.003207251 s. The raw elapsed difference is45.57%
slower; raw batch/prefix ratio0.686965571. It is **not a validated speed ratio**:
batch has319 operational outcomes, prefix326. Default48GiB, original source
order and width4/CPU20--23 remain unchanged.

All2,992 native-complete sources remain complete, with no new complete sources
and no closed prefix missing its required native kernel receipt. Outcomes
transition as follows:2,992 complete→complete,4,485 rejected→rejected,
314 operational→operational,5 operational→rejected,12 rejected→operational.
Operational states are not rejection decisions. All original indices and
requests are retained; no failure was dropped or reclassified to improve time.

Only7 cache lookups execute, with21,588 prefix nodes and4,945 original-source
fallbacks. Native parser cost10.127055477 s is included. The prefix path forces
109 native retirements versus82 in batch, censoring complete CPU accounting.
Timeout/resource behavior dominates these elapsed captures, so the raw
45.57% difference cannot be interpreted as successful-proof compute overhead.

This bounds exact-text prefix sharing on these released candidate files.
It does not benchmark the complete upstream SHRED service or settle the
unit-text reuse condition. The original unit-text collection and ProofNet
driver continue under their existing lifecycle; no replacement capture starts.
