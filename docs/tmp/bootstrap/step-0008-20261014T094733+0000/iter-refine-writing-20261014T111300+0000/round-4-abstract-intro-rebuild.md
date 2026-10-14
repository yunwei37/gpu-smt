# Round 4 — Abstract and introduction rebuild

Started: 2026-10-14T11:18:30.374003+00:00
Completed: 2026-10-14T11:18:31.887023+00:00
Parent: BOOTSTRAP step0008 WRITE_GATE. Entry HEAD0fb19766675f423821e253125e0160d077a100d2, dirty paper source.

## Objective and method
Ran root rewrite-abstract-intro procedure: remapped P1 verification streams, P2 repetition/shared-lifetime tradeoff, P3 native-history cause, P4 established reuse/gap, P5 thesis, P6 runtime/resource requirements, P7 system/evaluation promise, P8 contributions. Diagnosed only P6's long causal chain: explain runtime boundary first, then retained-memory benefit, then the resource frontier. Plan retains all eight roles/order and all thesis/cost/goal claims; rebuild P6 individually and retain each other paragraph after review because it already serves its assigned role. Derive the abstract requirement sentence last from the rebuilt P6. Do not insert a claim of useful acceleration from the new negative comparison.

Sources read: entire docs/paper/main.tex, references.bib, original entry source in root memory, docs/user-instruction.md, docs/evaluation.md and the designated writing skill/reference.
Raw subagent findings: none. Human explicitly forbids delegation; these are root self-review findings, not independent review.

## Applied changes
Location: Introduction / paragraph6

Before:
> Realizing this separation requires runtime safety, faithful resource handling and bounded memory. A branch boundary must be quiescent and safe for the verifier runtime, and native configuration and resource accounting must remain faithful when process creation changes timers or descriptors~\cite{fork}. Preparation sharing must improve service capacity within a memory budget that bounds retained states. These requirements connect compatibility to the service's resource frontier, the achievable combinations of latency, throughput and memory use at matched CPU capacity and memory limits.

After:
> Realizing this separation requires runtime safety, faithful resource handling and bounded memory. A branch boundary must be quiescent and safe for the verifier runtime. Native configuration and resource accounting must remain faithful when process creation changes timers or descriptors~\cite{fork}. Preparation sharing must improve service capacity within a memory budget that bounds retained states. Together, these requirements connect compatibility to the service's resource frontier: the achievable combinations of latency, throughput and memory use at matched CPU capacity and memory limits.

Location: Abstract / requirement sentence derived last from Introduction paragraph6

Before:
> Realizing this separation requires supported quiescent runtime boundaries, faithful native configuration and resource handling, and bounded memory as candidates modify branch-local state.

After:
> This separation requires supported quiescent runtime boundaries, faithful native configuration and resource handling, and bounded memory as candidates modify branch-local state.


## Preservation, alternatives and remaining work
All runtime/resource requirements, fork citation, defined frontier and bounded branch-local memory meaning remain. Original CPU/GPU/SMT scope and missing final results unchanged. No quantitative edit or new supporting concept name.
No invented results, numerical edits, scope removal or RQ changes were applied. No citations were removed. No memory files changed. Reviewer independence remains unavailable; complete research evidence remains open.
Compile exit: 0; pages: 10. Full output is retained beside this report.
Next node: Round5 consistency.
