# Round 5 — Paper consistency

Observed review checkpoint: 2026-10-09 15:56:43 UTC, after the initial complete skill and paper reads. Observed completion checkpoint: 2026-10-09 15:57:00 UTC; mechanical reference checking and report writing followed this checkpoint. Earlier start time was not sampled and is not reconstructed.

Parent node: BOOTSTRAP step-0003-20261009T132427+0000, WRITE gate, iter-refine-writing-20261009T154400+0000. Objective: read-only consistency review of the intended OSDI submission. Entry baseline supplied by the root: c62e427. Current review revision is the root's completed Round 4 working paper, including accepted CLI-owned command context, construction-order, and same-source metadata qualification clarification. No Git operation was performed.

Sources read completely: docs/user-instruction.md first; iter-refine-writing/SKILL.md; check-terminology-infoflow/SKILL.md and references/paper-consistency.md; docs/paper/main.tex and references.bib. A combined read was truncated, so the paper and bibliography/reference were read again separately in full. Figure 1 is inline LaTeX and was reviewed with its caption and references. The docs file inventory was inspected for sibling paper artifacts. No separate extended abstract, poster, or workshop manuscript was identified in that inventory; project design/status documents were not treated as contradictory submission text. No external source re-verification is claimed.

Method: extracted component, interface, preparation boundary, ownership, accounting, fidelity, measurement boundary, and evidence anchors; compared abstract/introduction/design/implementation/evaluation/conclusion; checked the three design goals, four contributions, four read-only RQs and their evidence blocks; checked inline figure paths, labels and citation keys mechanically. BOOTSTRAP implementation prose is valid intended present tense. Missing measurements were neither objections nor filled in.

## 1. Inconsistencies found

### Must-fix

None. No demonstrated architecture, native interface, outcome scope, accounting, RQ meaning, or quantitative contradiction was found.

### Should-fix

- **S1 — Abstract, L17; minor ownership ambiguity.** “bounded memory as candidates mutate shared state” conflicts in its literal reading with the immutable prepared parent in Design L71/L99, branch-owned mutable state L96/L111, and copy-on-write private pages L140. The intended mechanism is clear elsewhere, but the abstract can sound as though candidate writes change shared preparation.

### Consider

- **C1 — Figure 1, L82 versus L90; minor incomplete fallback path.** “Unsupported → native execution” is a side exit with no explicit connection to the final response/artifact stage. Body L96/L108 correctly gives native fallback, so this is diagram completeness rather than a mechanism contradiction.

## 2. Why each matters

S1 affects the primary isolation invariant before a reader reaches the design: immutable shared preparation and candidate-local mutation should have the same ownership meaning in the abstract and body.

C1 affects a reader using only the figure: the side exit should clearly produce the same interface outputs as supported branches. The prose already supplies that meaning.

## 3. Exact fixes or replacement wording

S1: replace only “bounded memory as candidates mutate shared state” with “bounded memory as candidates modify their private copies of prepared state”. This preserves the memory pressure condition and describes existing copy-on-write ownership. An even less implementation-specific alternative is “bounded memory for retained preparation and candidate mutation”; root should choose the wording consistent with its accepted scope expressions.

C1: optionally change only the figure's side-exit label to “Unsupported → native execution → responses/artifacts”, or add to the caption: “Unsupported boundaries obtain the same interface outputs through native execution.” Do not change architecture labels or supported device scope.

## 4. Broader follow-up checks

Root should confirm its selected S1 wording still distinguishes shared physical preparation from branch-owned writes, then compile and inspect the abstract and figure fit. No global terminology normalization is justified. If C1 is rejected as visual clutter, record that the body already makes native fallback outputs explicit.

The semantic anchors agree: ordered original preparation and untouched suffixes; no extra logical scope or heuristic warm check; no candidate evaluation in the prepared parent; native resource counters distinguished from service CPU/elapsed accounting; unsupported boundaries/artifacts use native execution; artifact meaning can be validated despite alternative representations; device qualification is distinct from mandatory full CPU replay; source-native versus post-export measurement boundaries are explicit; strongest bounded warm and CPU comparisons carry matched resource scope.

Design goals map coherently to contributions and RQs: opportunity characterization → contribution 1/RQ1; fidelity and candidate isolation → goals 1–2/contribution 2/RQ2; bounded implementation supports goals 2–3/contribution 3/RQ3; equal-resource and heterogeneous evaluation → goal 3/contribution 4/RQ3–4. RQ restatements retain the numbered questions' meaning. Abstract and conclusion carry placeholders rather than claimed measured gains.

## Preservation, validation, and disposition

Mechanical scan: 12 result slots, four numbered RQs, four explicit unanswered closures, no undefined reference labels, and no undefined citation keys. No experimental numeric result was asserted or changed. Hardware remains RTX 5090. Bibliographic dates and publication numbers were read but not reverified in this writing review. Initial checker invocation found `python` unavailable; rerunning with `python3` succeeded.

Applied fixes: none; this is a read-only subagent. Rejected fixes: none; S1 and C1 are raw proposals for root disposition. No paper, bibliography, code, experiment, Git, or memory changes. Only this report was created. Compilation and page evidence are owned by root after disposition; this report does not claim a new build. Remaining concerns are the two local findings above; no scientific-contract change is requested. Next node: root applies or explicitly disposes of findings, builds, then serial Round 6 sentence structure review.

| Severity | Count | Category |
| --- | ---: | --- |
| Must-fix | 0 | None |
| Should-fix | 1 | Immutable preparation versus candidate mutation wording |
| Consider | 1 | Figure fallback/output completeness |

Most impactful change: S1. C1 is optional; no third change is warranted by this consistency review.

Root disposition: Should-fix applied, abstract memory challenge now refers to branch-local mutation, matching immutable parent/private writes while retaining bounded-memory scope. Consider fallback-figure arrow deferred to final mechanism/figure pass: current figure label and immediate walkthrough already state native fallback/output behavior; no scientific flow is changed. Compile exit0/PDF8pages;4RQ/12slot/37cite and bibliography preservation checks pass. Next Round6 sentence review.
