# Round 9 — Language flow and polish

Started: 2026-10-09 22:01 UTC immediately before the first source read. Clock observed during review: 2026-10-09 22:01:32 UTC.

Parent step: `docs/tmp/bootstrap/step-0005-20261009T194100+0000/`. Run: `iter-refine-writing-20261009T213300+0000`. Objective: fresh serial read-only review of every paragraph's topic/stress positions, old-to-new information thread, transitions and register. Findings propose the smallest useful local changes.

## Sources and actual procedure

Read `docs/user-instruction.md` FIRST, then the FULL actual filesystem skills `/workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md` and `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`. Read all 236 lines of the sole paper `/workspaces/repository/docs/paper/main.tex`; a supplementary direct read of lines 120–140 recovered text truncated in the initial tool output. No Skill tool exists; filesystem reads are the actual skill procedure. No prior reviews, canonical sources, code, Git, native execution, builds or other agents were consulted.

| Source | Entry SHA-256 |
|---|---|
| `docs/paper/main.tex` | `c10fab2d1ef8a3c00a900e4cd5e69587420b511b10c1cdd720c470295fbcbebc` |
| `docs/user-instruction.md` | `27cbb0d37485cd698ce6e41b26eaa748623e8bc979f95f39ce1e97d0cd3cce76` |
| `paper-writing-style/SKILL.md` | `e28b057233d8f5a184219b589b7e28c73e5819e57ec5fd0555b7c51ea977d668` |
| `iter-refine-writing/SKILL.md` | `647b2676d953c16c69755b93872e1c31a530d338576f3e1040b05e4be9f8b75a` |

The caller identifies the actual spawn as explicit `gpt-6.1-sol`, fork `none`. This is caller-supplied provenance, not an inherited-model-override claim or independent model introspection.

For every prose paragraph, I checked its first subject against preceding information, each subsequent sentence's subject and emphatic ending, the closing sentence's link forward, and register. Intended completed-system present tense is accepted during BOOTSTRAP; missing final result values are not defects. No scientific framing or experiment change was considered.

## Complete-paper coverage

| Passage | Assessment |
|---|---|
| Abstract L14–22 | Service problem → history → prior reuse → separation → mechanism → comparison thread is coherent. Density carries technical content. |
| Introduction L26–45 | Services, preparation, history, reuse, separation and requirements advance in order. Contributions close appropriately. |
| Background L50–61 | Source verification, outcomes, tactic screening and state are distinguished before use. Optional conjunction polish below. |
| Motivation L65–72 | Preparation value and history concerns converge on joint behavior/resource evaluation. |
| Design L75–138, caption L105 | Goals, architecture, preparation, behavior, lifetime, placement and device accounting maintain a clear thread. Local ownership/execution overload below. |
| Implementation L141–166 | Qualification precedes process/resources and device execution. Final synthesis could link to evaluation. |
| Evaluation L169–211 | Four RQs and their evidence blocks have parallel openings/closures. Boundaries and competitors remain clear. |
| Discussion L214 | Mutation/lifetime connects preparation to fleet resource use. |
| Related work L218–229 | Register and grouping are stable. One caching-to-session transition benefits from an explicit backward link. |
| Conclusion L232 | Returns to separation and matched evidence without inventing findings. |

## Must-fix

None. No flow defect requires technical changes or makes the argument uninterpretable.

## Should-fix

### S1 — Design overview, L109

Quote: “The parent owns the immutable preparation, while each supported branch owns candidate mutation and its lifetime and executes on CPU with supported device operations where available.”

Problem: “owns … and … and executes” unevenly combines ownership and execution; the CPU/device condition arrives after three relationships. A local split clarifies the actor while preserving all details.

Concrete fix: “The parent owns the immutable preparation, while each supported branch owns candidate mutation and its lifetime. Each supported branch executes on CPU with supported device operations where available.”

Keep CPU execution, supported device availability, branch ownership and parent immutability. This pair is not a three-sentence run of short declaratives.

### S2 — Related work, Verification caching, L223

Quote: “Caching and session reuse retain different parts of verification work. Native SMT interfaces support incremental command histories and requested artifacts~\cite{z3api}.”

Problem: The SMT-interface sentence does not identify itself as the session-reuse side of the preceding comparison. A small backward link improves local continuity.

Concrete fix: “Caching and session reuse retain different parts of verification work. For session reuse, native SMT interfaces support incremental command histories and requested artifacts~\cite{z3api}.”

Keep the citation and the following warning about reconstruction unchanged.

## Consider

### C1 — Background, Prepared native state, L61

Quote: “The solver's own command interface saves state across evaluations~\cite{z3api}, while a resource limit can bound internal work independently of elapsed time~\cite{z3params}.”

Problem: “while” can imply contrast, although these two properties jointly explain reuse. The next sentence introduces a real contrast with “but.”

Concrete fix: replace this “while” with “and”; retain the rest verbatim, including “can” and both citations.

Disposition recommendation: accept if the intended relationship is additive. Existing wording remains understandable, so this is optional.

### C2 — Implementation closing synthesis, L166

Quote: “The Linux implementation integrates native SMT session evaluation in C++, Lean context reuse and matched CPU/device execution through these adapters.”

Problem: The synthesis repeats the implementation inventory without preparing the reader for the following Evaluation. A small forward link can improve its stress position.

Concrete fix: “The Linux implementation integrates native SMT session evaluation in C++, Lean context reuse and matched CPU/device execution through these adapters for the evaluation below.”

Disposition recommendation: optional; accept only if the forward reference helps the final layout. Keep all implementation details and do not imply missing results have been supplied.

## Disposition boundary and preservation

Raw findings: 0 Must-fix, 2 Should-fix, 2 Consider. The top three useful changes are S1's ownership/execution split, S2's session-reuse bridge and C1's additive conjunction. These are local changes, not structural alternatives. This subagent applied no paper changes and rejected no findings. The caller must record its disposition for each item and apply any accepted changes.

The four RQs at L171–174 were read verbatim and are outside all suggestions. All numbers and twelve round slots, scope hedges, native histories/resources, responses/artifacts, cancellation and device cleanup, full-source/post-export/tactic-screen boundaries, strongest warm/cache/native/CPU competitors and RTX 5090 remain protected. No benchmark, baseline, fidelity result, qualification outcome or device benefit is invented. The sole paper source was not edited.

Only this report was written; no memory change or other tree change was made. The initial report-write command failed because `python` was unavailable; the report was then written with `python3`. No compilation, page evidence or cumulative audit is claimed: these are caller duties after applying findings. No remaining Must-fix flow concern was found. Next node: caller disposition/application, compilation and preservation checks, then serial Round 10 citation review.

Completed: 2026-10-09 22:03:03 UTC

## Root disposition 2026-10-09T22:03:35.039918+00:00

S1 accepted with alternative split: ownership is separate, then supported CPU/device execution joins unsupported native fallback in a contrast clause. This avoids restoring Round6 four-short-declarative rhythm and keeps all actors/boundaries. S2 accepted session-reuse backward link. C1 accepted additive and with both source citations/can/work-vs-time restriction retained. C2 rejected unnecessary forward reference: section order already leads to Evaluation and adding below adds no substance. Three local edits, no technical/quantitative/RQ change;44citations/23entries/12slots preserved. round-9-build.log exits0/eight pages. Next serial fresh Round10 citation Pass3 unless annotation defect discovered.
