# Round0 — macro structure

Entry baseline: 9e0663444b7e7e1d6f1798819883b7d24eefc954 with declared root entry patch below. User forbids stash operations, so git stash create is not used. This baseline plus explicitly recorded existing patch separates entry changes from cumulative writing changes without copying sources.

```diff
diff --git a/docs/paper/main.tex b/docs/paper/main.tex
index 98e59c2..ccd6a93 100644
--- a/docs/paper/main.tex
+++ b/docs/paper/main.tex
@@ -149,7 +149,7 @@ A preparation boundary can separate parser invocations while retaining the nativ
 
 For source verification backed by this SMT adapter, the measured interval also includes the native frontend's translation and its original solver interaction. Solver-session replay alone is reported at its narrower boundary.
 
-The Lean adapter retains accepted context and keeps branch-local proof construction independent. It qualifies runtime quiescence, thread ownership and mutable extensions before enabling native process branching.
+The Lean adapter retains accepted context and keeps branch-local proof construction independent. It waits for source snapshots and the checked declaration environment before qualifying runtime quiescence, thread ownership and mutable extensions. Frontend completion alone does not establish that runtime workers, their finalizers and event loops have stopped. The adapter enables native process branching only after that separate runtime qualification.
 
 \subsection{Process and resource handling}
 Linux copy-on-write branches retain the parent address space, with candidate writes creating private pages~\cite{fork}. The parent stays quiescent and never executes candidate suffixes, while branch communication uses separate descriptors. The service reaps children after response, cancellation or failure and distinguishes native solver resource counters from service elapsed and CPU accounting.
```

Root entry patch expresses source-backed runtime qualification, not new RQ/claim/numeric result. Paper read entirely; fourRQ fixed; all12result slots open. Reviewer report follows.

## Read-only reviewer findings

Started 2026-10-09T23:33:09+00:00; completed 2026-10-09T23:33:38+00:00. Parent: BOOTSTRAP step0006 WRITE_GATE / serial iter-refine-writing Round0. Objective: Level1 macro review of the intended completed full submission, preserving the four scientific RQs, complete Lean/SMT/RTX5090 scope and all open result slots.

Actual instruction provenance: read complete filesystem files `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`, `/workspaces/.agent-state/codex/skills/check-paper-structure-flow/SKILL.md`, and its `references/full-paper-12p.md`. No Skill invocation tool exists in this session; these were direct source reads, not a claimed Skill-tool invocation. Read `docs/user-instruction.md` first. Read the entire `docs/paper/main.tex` through overlapping complete line intervals after an initially truncated combined read, its embedded TikZ architecture, `docs/paper/Makefile`, and the baseline/entry patch already recorded above. Context read: complete `docs/idea-story.md`, `docs/research-plan.md`, `docs/design.md`, `docs/implementation.md`, and `docs/evaluation.md`; supporting bibliography/related-work/step-report combined output was consulted but truncated, so is not claimed as a complete read. No external literature or scientific verification was undertaken in this macro round. No Git operation, paper edit, compilation, native execution or canonical-document edit was performed.

Method: compare section sequence, subsection roles and evidence-block organization against the full-paper reference; trace the four numbered RQs to the fixed Initial Narrative; inspect design/implementation separation and the source architecture diagram. Existing compile/page status is contextual evidence from implementation.md (eight pages), not a fresh reviewer measurement. Root retains compilation, fixes and disposition ownership.

### Must-fix

None. Required sections are present in the full-paper order: Introduction, Background, Motivation, Design, Implementation, Evaluation, Discussion, Related work, Conclusion. Background and Motivation are separate. Design opens with three explicit testable goals and a system overview (main.tex:74–75), has an architecture diagram and operation walkthrough (77–109), and contains five design subsections. Concrete C++/native parser/Linux/container mechanisms are in the separate Implementation section (140–166). Evaluation opens with the existing four numbered RQs (168–175), followed by Setup, one primary evidence block for each RQ in order (188, 193, 198, 203), and Limitations outside the RQ count (208). Every block states its RQ and retains an explicit unanswered evidence condition. Open placeholders are appropriate to this BOOTSTRAP review and are not macro defects or invitations to invent results.

### Should-fix

None. Current subsection lengths are proportionate to their roles: the comparatively longer native-adapter subsection covers both backend families and staged original-interface qualification; Setup covers shared methodology; the four RQ blocks have similar two-paragraph evidence outlines. No evidence block is orphaned and no additional RQ is needed.

### Consider

1. **MACRO — Design architecture (main.tex:85–105, Figure1).** The diagram represents plural independent branches as one vertical box, while cancellation independence and shared-parent parallel fan-out are central architecture properties. Concrete optional fix: depict two sibling branch boxes beneath the same parent, route the cancellation arrow to one sibling and show each sibling's response/cleanup ownership, using only the already stated components and guarantees. Preserve unsupported native fallback and supported CPU/device execution. This improves the architectural explanation without changing the mechanism or asserting measured concurrency safety. The existing plural label and caption already state the property, so this is optional visual clarification, not a missing-architecture finding.

2. **MACRO — Full-paper page budget (main.tex:188–206 and 213–229).** Existing source is a compact full-scope outline; the implementation frontier records eight pages, while the selected reference targets a 12–14-page completed systems paper. Concrete optional fix at root's layout-planning level: record a completion budget allocating the principal added result figures/tables and interpretation to the existing four RQ blocks, with Motivation retaining characterization evidence and Design/Implementation retaining mechanism detail. Keep the present section/RQ ordering and all result slots. Do not pad prose or fill values to reach a page count. Actual final balancing can only be checked after the promised evidence is available; this review does not equate present length with venue readiness or require scientific scope changes.

Claim/number preservation: findings request no scientific change, RQ rewording, numerical replacement, citation removal, future-tense downgrade or narrower scope. Raw findings only; applied/rejected fixes, compilation/page evidence and next serial round are root-owned. Only this round report was appended; its entry baseline and patch were preserved.

Root disposition: no Must/Should findings. Consider sibling diagram expansion deferred: plural branch box plus explicit independent cancellation caption already communicate intended branches; a completed lifecycle figure may later benefit from actual service implementation. Consider page budgeting accepted as final evidence/layout concern, not current zero-result embellishment; current8pages/all12resultslots preserved. No paper edits thisround, citecount47/fourRQ/12slots unchanged. make -C docs/paper exits0 (build-round0.log); only declared root entry patch appears in paperdiff. User objective unchanged; nextRound1 microstructure.
