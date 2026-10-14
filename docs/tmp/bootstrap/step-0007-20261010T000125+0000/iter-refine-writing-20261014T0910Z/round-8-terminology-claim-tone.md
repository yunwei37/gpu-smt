# Round 8 — Terminology and claim tone

Started: 2026-10-14T09:10:57.213626+00:00
Completed: 2026-10-14T09:10:58.311831+00:00
Parent: BOOTSTRAP step0007 WRITE_GATE. Entry HEAD582132d969286899e35c72ad74643aaa58bf30da, dirty paper source.

## Objective and method
Checked first definitions, synonym drift, invented names and scope-bearing hedges. Must-fix: PSS is used in the resource table interpretation without an explicit abbreviation expansion, despite earlier explaining proportional memory. Define proportional set size (PSS) on first use in Design/Placement. Existing service, native preparation, snapshot, branch and fallback vocabulary is standard or described. Preserve narrow supported Meta-reducer scope, source-native/post-export distinction, no-exclusive-affinity warning and single-profile limits. Reject deletion of negative results or defensive-looking operational qualifiers because those carry actual evidentiary scope.

Sources read: entire docs/paper/main.tex, references.bib, original entry source in root memory, docs/user-instruction.md, docs/evaluation.md and the designated writing skill/reference.
Raw subagent findings: none. Human explicitly forbids delegation; these are root self-review findings, not independent review.

## Applied changes
Location: Design / Bounded placement and execution

Before:
> Proportional memory attributes each shared page across the processes sharing it~\cite{procMemory},

After:
> Proportional set size (PSS) attributes each shared page across the processes sharing it~\cite{procMemory},


## Preservation, alternatives and remaining work
PSS retains the same proportional shared-page accounting meaning. No memory measurement or claim changes. 'Supported', 'measured cohort', 'single instrumented conditions', CPU fallback and final native checking qualifiers are preserved.
No invented results, numerical edits, scope removal or RQ changes were applied. No citations were removed. No memory files changed. Reviewer independence remains unavailable; complete research evidence remains open.
Compile exit: 0; pages: 9. Full output is retained beside this report.
Next node: Round9 language flow.
