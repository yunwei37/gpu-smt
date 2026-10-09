# Round 3: logic and argument flow

Started: 2026-10-09T21:49:12Z (invocation; exact first-tool time not recorded). Completed: 2026-10-09T21:51:00Z. Parent: BOOTSTRAP step-0005-20261009T194100+0000 / iter-refine-writing-20261009T213300+0000.

## Sources, revisions and method

Read docs/user-instruction.md first; then the actual filesystem iter-refine-writing/SKILL.md, complete docs/paper/main.tex and complete references.bib. Re-read the middle design subsections separately to recover omitted combined-tool output. No previous reviews, canonical status, code, experiments, Git, or external sources were read.

SHA-256 revisions recorded at 2026-10-09T21:49:31Z:

| Source | SHA-256 |
| --- | --- |
| user-instruction.md | 27cbb0d37485cd698ce6e41b26eaa748623e8bc979f95f39ce1e97d0cd3cce76 |
| main.tex | 55f71b8a030101d216deca95629879f9ab7a2a0301ef8d80bf17a51f53570caa |
| references.bib | f55c6af75bd07eb090c76c243a82a703719be50e682edeea64f1be77fbd9ceb2 |
| iter-refine-writing/SKILL.md | 647b2676d953c16c69755b93872e1c31a530d338576f3e1040b05e4be9f8b75a |

Reviewed as the intended completed BOOTSTRAP submission. Protected all result placeholders. Traced the introduction’s contributions through motivation, design, implementation, four explicit RQs, discussion and conclusion. Assessed writing support and internal causal consistency, not external novelty or empirical truth.

The chain is coherent: costly shared preparation motivates RQ1; scope/history differences motivate native boundary and interface qualification in RQ2; branch-local lifetimes and bounded retention motivate matched fleet-resource RQ3; reduced remaining checking work motivates conditional RQ4. Fresh-adapter qualification precedes branch qualification and performance comparison. Discussion and conclusion retain a conditional systems benefit. No Must-fix contradiction was found.

## Must-fix

None.

## Should-fix

### S1: Clarify the independent-candidate behavior reference

**Sections:** Introduction lines 30–34; Preparation boundaries line 112; Observable behavior lines 117–119; RQ2 lines 194–196.

**Problem:** The introduction says earlier requests alter heuristics/counters, while the reference is “original native execution of the same ordered preparation and candidate suffix.” Although the boundary paragraph excludes candidate-produced state, readers can interpret “original” as replay of a continually mutated session containing preceding alternative attempts. Under that interpretation, eliminating candidate history appears to conflict with response preservation. This is a definition-order ambiguity, not a demonstrated contract contradiction.

**Concrete fix:** Add a short sentence at the reference definition explaining that an independent candidate’s reference contains its own original preparation and suffix, and preceding alternative-candidate suffixes are not inserted into that preparation. Keep accepted context already in the original preparation. Optionally connect RQ2’s “preceding unrelated attempts” control to this fixed reference. Do not erase history within a dependent multi-check session or promise fidelity to arbitrary sequential service histories.

### S2: Explain what the placement ablation removes

**Sections:** Bounded placement line 129; Process/resource handling line 161; RQ3 line 201.

**Problem:** Placement favors states whose observed preparation work is reused enough to offset creation and retention costs. Implementation calls this a “preparation-reuse criterion,” and evaluation replaces placement with ordinary bounded retention. The criterion is currently a qualitative goal; the reader cannot identify the observable policy choice removed by the ablation. Preparation-depth and lifetime ablations have clearer causal roles.

**Concrete fix:** Explain the already intended policy inputs and resulting admission/retention choice in the placement or implementation subsection, including how it differs from ordinary bounded retention. If detailed policy is intentionally deferred, point to its specification rather than treating the qualitative goal as a concrete criterion. Do not invent thresholds, an optimizer, numbers, or mechanism claims during writing refinement.

## Consider

### C1: Bridge RQ4’s complete-checking evidence to service-frontier language

**Sections:** Evaluation overview line 169; Heterogeneous execution lines 204–206.

**Problem:** The overview connects RQ4 to the service frontier, while its evidence block focuses on complete verification cost and crossover. These are compatible, but the connection through queueing and supported-operation coverage is implicit. A reader could equate a complete-checking improvement with a measured latency/throughput frontier shift.

**Concrete fix:** Briefly state that complete CPU/device paths use the service accounting and matched workload boundary of RQ3, or distinguish the measured complete-checking crossover from any service-frontier effect established by those costs. Preserve the RQ wording and strongest-CPU comparator scope. This is a bridge between existing measurements, not a new experiment request.

## Preservation, disposition and limits

All four RQ meanings, values and placeholders were protected. Recommendations preserve native/full source verification versus post-export versus tactic screening; Lean admissions/unresolved obligations; SMT SAT/UNSAT/UNKNOWN and requested artifacts; resource counters versus service accounting; qualified runtime boundaries; wall-time operational scope; competent native/warm/cache competitors; tuned CPU checkers; and RTX 5090. Cancellation instrumentation correctly distinguishes reaping after native progress from interruption inside a native check. GPU qualification does not imply universal full CPU replay, and fallback/setup/transfer costs remain charged.

Only this report was written. No paper edits, builds, experiments, Git actions or publication occurred. Build/page verification belongs to root. Bibliography annotations were read as supplied, not independently verified. No external whole-paper critique or subagent was invoked. Root disposition is pending for S1, S2 and C1; no fixes were applied or rejected by this reviewer. Next node: root applies or explicitly rejects findings, verifies diff/build, then Round 4.

## Root disposition 2026-10-09T21:51:31.993323+00:00

S1 accepted: explicitly preserve accepted context and within-candidate native history while excluding preceding alternative suffixes from independent reference. C1 accepted: connect full CPU/device paths to existing RQ3 accounting, without equating primitive speed to service gain. S2 deferred to root scientific-contract audit: a concrete cost-sensitive placement policy versus bounded retention has not yet been specified in accepted mechanism evidence. Writing cannot invent policy thresholds or optimizer; the qualitative intention remains, and this is an explicit unresolved mechanism specification before freeze, not a reason to weaken RQ3. Diff preserves technical meanings/44citations/23entries/12slots/fourRQ; build round-3-build.log exits0/eight pages. Next root full Round4 procedure.
