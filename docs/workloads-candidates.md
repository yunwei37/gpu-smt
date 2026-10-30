# Released workload coverage and native evidence

The [18-row catalog](../workloads/catalog.csv) pins sources, licenses,
toolchains and selection. [Candidate tables](../workloads/candidates/README.md)
cover all 68,932 EPFL evaluation programs and all 1,835 APRIL test tuples.
[OpenAI source analysis](../workloads/openai-math/README.md) covers all
163,097 Lean files. These are complete static results, not native builds.

## What changes workload selection

EPFL adds real outputs of three recent provers and ProofNet to miniF2F.
The validity rates differ sharply: miniF2F 25,702/41,638 versus ProofNet
2,443/27,294. However, the release excludes timeout/operational failures,
precisely the tail needed for current resource questions. Future native
replay must preserve every budget interruption, not infer cost from labels.

Training's 55.2% invalid rate is a publisher full-statistics observation,
not compute-time share. APRIL tests deliberate mutations, not natural arrivals.
Neither a strategy failure nor budget diagnostic proves a goal false.
OProofs lacks released failure/status fields; Nemotron's viewer is partial.
Goedel V2 repository data are 612 templates containing sorry, while its
actual candidate outputs are available as an EPFL evaluation subset.

Research-level compute differs: OpenAI contains 1,354,379 explicit
decide +kernel forms; LNSym has 62 bv_decide, 153 native_decide and one
direct ofReduceBool token. These are lexical, not executed calls or compiled
transitive axiom dependencies. The latter still needs native inspection.

## Research and computational certificate artifacts

| Artifact | Pin / Lean version | Coverage |
|---|---|---|
| Erdős647 / decanus | 91d178dc / 4.30.0 | 265 files, 43,664,965 bytes; release certificates separate |
| Flag algebra | 439d3e64 / 4.27.0 | 199 files, 3,986,217 bytes; seven publisher-verified cases |
| Aristotle Erdős728 | 8822f7dd / versioned 4.24.0 path | selected Erdos728b.lean, 108,390 bytes; no root SDK/license observed |
| LeanMarathon ErdosGraham | c084fe62 / 4.28.0 | two Lean files, 488,153 bytes |
| LeanMarathon Erdos1196 | 1e960723 / 4.30.0-rc2 | two Lean files, 188,100 bytes |
| LeanMarathon Prim | a303f6bd / 4.30.0-rc2 | two Lean files, 720,962 bytes |
| FrontierMath Erdős results | fd09021e / per-result | truncated tree gives at least 28,817 Lean files |
| LNSym | 5c05220f / nightly-2024-10-07 | complete lexical scan of 196 files |

Decanus, flag-algebra and LNSym licenses are Apache-2.0. The selected
Aristotle, FrontierMath-results and LeanMarathon delivery repositories have
no root license observed. Public access does not authorize redistribution.
The [LeanMarathon harness](https://github.com/YuanheZ/LeanMarathon/tree/e2febe2ce717ef5d8410909683f6f5b301bda4c2)
is Apache-2.0, but that does not automatically license its delivery repos.
We inspected already published outputs and ran no harness or agent.

Primary sources: [Erdős647](https://arxiv.org/abs/2608.17880),
[flag algebra](https://arxiv.org/abs/2607.23500),
[Erdős728](https://arxiv.org/abs/2601.07421),
[FrontierMath Erdős](https://arxiv.org/abs/2609.25050).
Published verification claims are not independently reproduced native results.

## Native sampling feasibility

W remains limited to 5 GiB, one Lean process and natural heartbeat termination,
with no capture longer than 30 minutes. The replacement container has no
lean/lake/elan on PATH or root/.elan/toolchains; the PVC had about 1.7 GiB
free at inspection. Existing older research caches are preserved. Installing
whole new dependency environments needs a machine and cost decision rather
than consuming shared disk. No native sample or full build ran here.

Stratify a qualified pilot by source size, import depth, project, certificate
tactic and candidate label. Use exact SDK/dependency pins and retain time,
peak RSS, native/replay budgets, interruptions and supported causal classes.
Until then, combinatorial expansion, closed computation, rewrite
nonconvergence and search expansion have unknown time shares. Token counts
are not causal evidence.

The flag-algebra publisher reports 26–37 GB for six heavy library modules,
45 min / 43 GB for ErdosPentagon, 27 min / 30 GB for K5freeEdge and
18 min / 27 GB for C5freeEdge on i7-14700K. These are publisher costs,
not W measurements; they do not fit W's current budget.
OpenAI full build CPU-hours are unknown. Mean 1 s/file and 10 s/file give
45.30 and 453.05 CPU-hour planning sensitivities before dependencies,
not measured extrapolations from bytes.

## Cross-workload tail check

Existing AutoVerus direct native receipts cover 3,566 candidates and three
separate repetitions. The top ceil(0.016 × 3566) = 58 candidates consume
3.399%, 3.338%, 3.315% of each repetition's summed process elapsed time.
Thus the current Lean 1.6%/73% pattern does not reproduce at this particular
program-verification point. The denominator excludes model generation and
is not batch wall time or a comparison between hardware points.
