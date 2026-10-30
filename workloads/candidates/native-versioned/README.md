# Version-matched candidate replay
EPFL:144 sources from68,932 released candidates,36 strata
(benchmark/model/status/within-group median source length),4uniform reservoir
selections per cell,seed20261030.
APRIL:39 published incorrect/correct pairs from1,835test errors,by subset/
recorded-budget-diagnostic/median length,up to3per cell,seed20261031.
15of20 released budget-diagnostic cases sampled. selected.csv has unequal
inclusion probabilities; use weights. No new candidate generation.

Lean4.15.0/4.22.0-rc4; public Mathlib release pins in environments.csv.
Original dataset Mathlib commits unknown; version-matched reconstruction,
not exact dependency reproduction. APRIL uses its published import Mathlib
preamble on both reference and mutation.
APRIL version: https://arxiv.org/html/2602.02990v2 and official code
uw-math-ai/lean-error-correction at152829196deb5c1f5e9abe7e683cadd409e64b16.

lake exe cache get completed5,826/6,982entries. Serialized Cache/Batteries
bootstrap; no Mathlib source build. Setup1s tree sampling peak1,539,272,704bytes,
max1observed Lean; sampling can miss transient peaks.
SDKs/caches/source/raw on PVC outside Git.

Replay:phobos-vt,CPU0-7,one Lean,-j1,-M8192(native allocation option,not hard RSS
quota),200000HB. Source HB0/>200000 capped in replay copies; edits recorded.
No OpenAI autoImplicit=false imposed; baseline no profiler/stats.
Signals denied errno13; natural exits required.

EPFL labels also encode expected-declaration/forbidden-proof policy: compiler
success does not reproduce the full judge. Released timeouts/infrastructure
failures are censored; their missing tail cannot be reconstructed.
APRIL is an error-mutation distribution. Budget exhaustion does not mean false.
Raw root:/workspaces/.agent-state/gpu-smt-captures/workloads/
candidate-mathlibs-setup,candidate-native-inputs,candidate-native-v1.
The launch is not a completed native result.
