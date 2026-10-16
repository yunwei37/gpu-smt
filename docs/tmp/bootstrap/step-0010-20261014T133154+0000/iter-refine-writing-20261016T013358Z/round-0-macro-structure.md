# Round0 — macro structure

Started at node creation; completed 2026-10-16T01:35:01.051474+00:00. Parent Step0010 / BOOTSTRAP WRITE.
Entry HEAD: fe13c12c77822a22c4a335abdb9f991c04aee94d. The working tree is dirty.

## Authority, baseline and actual sources

Human requires the root to do the work, with no delegation. Root personally
reviews/fixes each round, using actual complete skill files/references; no
fresh independent reviewer or fake Skill-tool invocation is claimed.

Unrelated docs/design.md is untouched. A blanket git stash create would capture
another writer's work, conflicting with the ownership boundary. No stash/index/
ref/branch operation is performed. The two entry-*-vs-head.diff files are
read-only scoped Git differences against this HEAD. Their exact forward
reconstruction from GitHEAD in memory matches each actual dirty entry byte for
byte. No paper source copies are created. The initial GNU-patch-on-stdin path
failed before any paper change; baseline-stdin-patch-failure.log preserves that
actual tool error. In-memory standard unified-diff reconstruction repairs only
the baseline path. Round11 must reconstruct this exact dirty entry and compare
against it. This is an explicit baseline-method adaptation, not a stash commit.

Read complete current main.tex, user-instruction.md and established four RQs;
read full iter-refine-writing, check-paper-structure-flow and full-paper-12p
reference. Current14page draft has Background/Motivation/Design/Implementation/
Evaluation/Discussion/RelatedWork/Conclusion, designgoals/architecturediagram
and separate implementation. Four noun-phrase RQblocks have explicit questions
and unanswered evidence slots; setup/limitations are outside the RQcount.
Missing finaldata is not a BOOTSTRAP writing defect or permission to invent it.

## Root findings, disposition and target outline

Should-fix: RQ4 puts residual profiles before the CPUcomparisons that motivate
their use. Accept: within this one subsection, move the two unchanged original/
compiled-cost blocks after the CPUcomparison paragraphs, before fullsourceGPU.
Target: measurementboundary/CPUfamily -> CPUcomparisons -> residualcost ->
completeGPUcomparison -> unansweredRQ4scope.

Consider: compress the numerous detailed RQ4controls. Reject for now because
removing protected numbers/scope discards accepted evidence. Larger RQ1/RQ2
gaps remain scientific work, not a writing reason to narrow the four questions.

## Applied edit and verification

round-0-reviewed-edit.diff is the exact reviewed block move, applied with the
standard patch edit tool in the owning Workspace, not bulk regex substitution.
Both moved blocks are byte-unchanged. Quantitative-literal/citation-occurrence
multisets remain identical; title/RQs/qualifiers/content are preserved.
ActualTectonicreturn0 in round-0-compile.log. No native input/process/library
or unrelated dirtywork changed. Newlayout/microstructure is inspected next.

Root macro pass complete with declared baseline/review adaptations. No
independent audit, full12roundcompletion, RQclosure or step publication is
claimed. Next Round1 microstructure.
