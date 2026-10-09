# Round 2: Section conventions

Started: 2026-10-09T21:46:00+00:00 (review start, approximate to minute). Completed: 2026-10-09T21:48:30+00:00. Parent: BOOTSTRAP step-0005-20261009T194100+0000 / iter-refine-writing-20261009T213300+0000. Reviewer: independent read-only section-conventions subagent.

Objective: check full-paper abstract and introduction conventions, explicit design goals, established RQ overview and evidence-block organization, grouped related work, and conclusion. No scientific-contract review or source editing.

## Sources and entry revision

Read `docs/user-instruction.md` first. Read the complete `docs/paper/main.tex` (236 lines) and complete `docs/paper/references.bib`; chunked rereads supplied material omitted by tool-output truncation. Read the actual filesystem procedures in full:

- `/workspaces/.agent-state/codex/skills/check-paper-structure-flow/SKILL.md`
- `/workspaces/.agent-state/codex/skills/check-paper-structure-flow/references/full-paper-12p.md`
- `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`
- `/workspaces/.agent-state/codex/skills/rewrite-abstract-intro/SKILL.md`
- `/workspaces/.agent-state/codex/skills/rewrite-abstract-intro/references/abstract-intro-structure.md`
- `/workspaces/.agent-state/codex/skills/rewrite-abstract-intro/references/abstract-intro-revision.md`

No Skill tool exists in this environment; the actual instructions above were loaded directly, without claiming a fictional invocation. No prior round reports, status documents, or experiment artifact internals were read. No external citation-verification search was performed; bibliography reading supported structural grouping only.

Entry paper SHA-256: `de333ed5d7a3bcfbb05cc73e02e9aa4cd1c8dc67a6510f7eede943fdcef3bc3f`. Entry bibliography SHA-256: `f55c6af75bd07eb090c76c243a82a703719be50e682edeea64f1be77fbd9ceb2`. Hashes recorded at 2026-10-09T21:48:00+00:00; no Git commands performed and no evidence artifacts inspected.

## Method and observations

Mapped abstract sentence roles to introduction paragraphs, counted abstract whitespace words after replacing the `missing` macro by its argument text, traced the named design goals to RQs, and mapped each experimental operation to an RQ block. Reviewed related-work topic groups and the conclusion against the full-paper reference. The initial word-count command used unavailable `python`; a successful `python3` rerun supplied the count. This has no source effect.

The abstract has 230 words including result-placeholder argument text, within the prescribed 200–300 words. It has eight substantive sentences and a ninth result-placeholder slot, in the required background → problem → root cause → existing reuse → insight → challenges → system → methodology → results order. The optional root-cause and challenges roles are warranted by the mechanism's native-history and safe-boundary concerns. Introduction paragraphs at lines 26, 28, 30, 32, 34, 36, 38, and 40–46 occupy the corresponding eight roles separately. Four concrete contributions and section references are present. Challenges at line 36 receive corresponding high-level mechanisms at line 38.

Design opens at line 79 with three explicitly numbered goals derived from Motivation, then describes the branching overview and includes an architecture figure and operation walkthrough. Evaluation explicitly lists exactly four established RQs at lines 171–174. The four noun-phrase evidence blocks at lines 188–206 open with their corresponding RQ and close with an explicit unanswered status and specific evidence requirements. Setup and Limitations are outside that count. Ordering/locality and preparation-depth experiments are subordinate to RQ1; interface, native history, artifacts and cancellation comparisons to RQ2; offered load, equal-resource services and mechanism ablations to RQ3; profiling, CPU/device comparisons and crossover costs to RQ4. No orphan experiment found.

Related work has four topic groups: persistent verification state, verification caching, prepared execution, and heterogeneous checking. Prior capabilities and comparison dimensions are described rather than listing isolated papers. Conclusion is one paragraph, restates the preparation/history thesis, reserves a final-result slot, introduces no new mechanism, and contains no future-work agenda.

## Findings

### Must-fix

None within this round's authorized section-conventions scope.

### Should-fix

1. **MICRO — Introduction, existing-solutions paragraph, line 32.** The paragraph names the unresolved comparison, then lists established reuse capabilities, but leaves the specific connection between these alternatives and the paper's preparation/history/lifetime distinction mostly implicit. The canonical existing-solutions role calls for the problem-specific comparison boundary as well as capabilities. **Concrete fix:** after the capability sentences, add one concise sentence using the already-present comparison dimensions from Related Work (lines 218–223): these mechanisms provide the native-reuse baseline, while the matched comparison must additionally establish independent native execution, cancellation and bounded fleet resources. Preserve the explicit uncertainty; do not assert that warm services or native snapshots fail those dimensions without evidence. No change to RQs, novelty, or baseline strength is warranted.

### Consider

1. **MICRO — Abstract result slot, line 22.** Its placeholder asks for service latency/throughput/memory/behavior findings, whereas the corresponding introduction result slot at line 38 also explicitly asks for measured device-benefit scope. Methodology already mentions RTX 5090, so this is a small correspondence issue in the placeholder scope, not a missing empirical result defect. **Concrete fix:** include the introduction's existing measured heterogeneous-scope requirement in the abstract placeholder, keeping all actual values absent until sourced. This would align the planned result sentence with the corresponding introduction paragraph and conclusion result slot.

2. **MICRO — Introduction contributions, lines 42–45.** The first deliverable is characterization, preceding design and implementation; the canonical reference prefers design/model → system/method → evaluation. The present order nevertheless mirrors the paper's opportunity-to-mechanism argument and all four deliverables are concrete. **Concrete fix if useful:** move the existing design and implementation items before characterization without rewriting the items or section references. Keeping the present order is also defensible because characterization is a load-bearing first contribution and RQ1 remains scientifically unchanged.

## Preservation limits and disposition

No fixes were applied or rejected by this reviewer: root owns all paper, canon, code and Git changes. Findings are suggestions, with the contribution-order item explicitly optional. The intended completed-system present tense is authorized for BOOTSTRAP and is not a defect. Missing final values, hardware/configuration details and explicit unanswered RQ endings are preserved as placeholders; they are not review defects in this stage. No replacement values or empirical success claims are proposed.

All four RQ meanings, observable-response/artifact scope, supported-native-boundary fallback, source verification versus solver-session/post-export boundaries, tactic screening versus enclosing verification, strong bounded warm/cache/native reuse and CPU baselines, and RTX 5090 remain protected. Suggestions do not change native resource handling, deterministic versus wall-time scope, or qualification versus online verification costs.

No builds, page-count checks, native reruns, benchmarks, citation verification, source diffs or Git operations were performed. The only tree change is this requested review report; no memory or scientific source changes. Root should evaluate the Should-fix and Consider findings, record its decisions and any source edits, perform its own required compilation and preservation checks, then advance to Round 3. Final empirical answers remain future evidence requirements rather than structural failures here.

## Root disposition 2026-10-09T21:49:15.282025+00:00

S1 accepted: append comparison dimensions already in Related Work without asserting competitor deficiencies. C1 accepted align abstract result slot with existing intro device-benefit scope; no data added. C2 rejected: keep opportunity→design→implementation→evaluation deliverable order because characterization motivates design and Evaluation explicitly ties RQ1 to first contribution; changing it adds no clarity. `round-2-build.log` exits0/eight pages. Source diff examined, all44 citations/23 entries/12 slots and fourRQ preserved, no numerical or technical content change. User scope remains complete real Lean/SMT verification with RTX5090. Next fresh Round3.

## Outer-audit chronology disposition 2026-10-09T22:16:52.954620+00:00

Approximate first-read start21:46 is unreliable and must not establish launch timing. Root checks the actual native journal response-item/function-call for spawn_agent: step5_writing_round2 launches2026-10-09T21:47:33.006Z, after Round1 root completion21:47:24. Actual post-Round1 source hash and handoff establish serial ordering; original approximate report retained, no invented replacement start/read time or repeated round.
