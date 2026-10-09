# Round 7 — Word choice

Started: 2026-10-09 23:43:58 UTC. Completed: 2026-10-09 23:44:37 UTC.

Parent: BOOTSTRAP step-0006-20261009T222500+0000; WRITE run iter-refine-writing-20261009T233309+0000. Reviewer: serial read-only subagent assigned after the root's Round 6 fixes and compile. Objective: review current complete paper for word-choice mechanics while preserving scientific meaning.

Read `docs/user-instruction.md` first, then reread complete current `docs/paper/main.tex`, lines 1–238. The initial display truncated a central span; an overlapping read of lines 117–142 completed coverage. Complete root `iter-refine-writing/SKILL.md` and `paper-writing-style/SKILL.md` were loaded in the preceding serial review and retained. No Skill invocation tool is available; their actual file instructions govern this review. Current source SHA-256: `97d46f2e3599a77b6bb3b614fca66755c44c8192cfe4ab2fbf2a210946cca879`.

Method: examined every sentence for nominalizations, compound-term inflation, vague antecedents, stacked hedges, verbose phrases, unnecessary intensifiers and precise verb choice; applied the full sentence checklist as a secondary check. No searches or external evidence are required for this prose-only review. Intended completed-system tense remains fixed; missing results remain explicit.

## Must-fix

None. No word-choice defect requires changing the scientific contract.

## Should-fix

### S1 — Motivation, Preparation and candidate lifetime, line 65

Quote: “A service must also account for the attempts that reject, remain incomplete or exhaust their resources.”

Problem: “reject” normally names the verifier's action, whereas the grammatical subject is the attempt. The intransitive use obscures the outcome actor.

Concrete fix: “A service must also account for attempts that are rejected, remain incomplete or exhaust their resources.” Preserve the following lifetime/capacity sentence. All three unsuccessful outcome classes remain.

### S2 — Design, Observable behavior, line 123

Quote: “Any residual mismatch in a supported comparison invalidates that path's fidelity claim and is retained with its complete input and output.”

Problem: a mismatch is an observed relation, while “its complete input and output” refers to the mismatching comparison case. Naming the retained evidence makes the antecedent concrete.

Concrete fix: “Any residual mismatch in a supported comparison invalidates that path's fidelity claim. The service retains the mismatching case with its complete input and output.” This preserves invalidation for every residual mismatch and complete evidence retention; it adds no new qualification or fallback rule.

## Consider

### C1 — Motivation, Preparation and candidate lifetime, line 67

Quote: “The relevant question is whether sharing native preparation changes concurrency, cancellation and aggregate memory relative to bounded versions of these services.”

Problem: “The relevant question is whether” is a verbose framing phrase.

Concrete fix: “We ask whether sharing native preparation changes concurrency, cancellation and aggregate memory relative to bounded versions of these services.” This preserves uncertainty, all metrics and bounded native-reuse comparison. The existing version is clear and can remain if its impersonal framing is preferred.

## Compound-term frequency and negative checks

A read-only Python surface-form scan found 87 hyphenated tokens and 50 distinct forms in the entire raw source, including labels, headings and placeholders. This is a reproducible surface count, not a count of invented jargon. Most frequent raw forms: `prepared-state` 9; `copy-on-write` 5; `proof-state`, `SMT-backed`, `end-to-end` 4 each; `equal-resource`, `fan-out`, `resource-bounded`, `per-input` 3 each. Case variants remain separate in this count. Established technical expressions, ordinary descriptive modifiers, baseline names and scope distinctions account for the compounds; no inflation-only replacement is recommended. In particular, do not replace prepared-state, native resource-bounded or post-export distinctions merely to lower the count.

No stacked redundant hedge, vague intensifier standing in for a number, or checklist phrase such as “in order to,” “utilize,” “due to the fact that,” “has the ability to,” “prior to,” or “subsequent to” was found. Nominalizations such as preparation, verification, elaboration, qualification, cancellation and resource accounting denote established processes or comparison boundaries; mechanical conversion to verbs would often lose precision. No additional nominalization fix is warranted. Other “this/it/they” references have sufficiently clear local antecedents. The “where one is produced” qualification, wall-time scope, supported-boundary conditions, strongest measured CPU comparisons and source-versus-post-export distinctions are substantive protected scope, not redundant hedging.

## Disposition and preservation

Raw findings: 0 Must-fix, 2 Should-fix, 1 Consider. Top three improvements: clarify the rejection actor, name the retained mismatching case, shorten the question framing. Applied fixes: none. Rejected fixes: none; caller dispositions all findings. Sentences changed: 0.

Only this report was written. No paper/source, canonical record, Git, build or native execution was modified or run. Compilation/page evidence is outside this read-only assignment, so no verification success is claimed. Suggestions preserve all numeric values and citations, four RQ meanings, complete verification, strong warm/cache/native competitors, qualification restrictions, cancellation, matched CPU/memory, RTX 5090 setup/transfer/fallback costs and protected hedges. Missing values remain unfilled. More aggressive compression was rejected because it would remove comparison boundaries or technical mechanisms.

Next node: root applies or explicitly dispositions findings, compiles and checks preservation, then proceeds to serial Round 8. No additional scientific-contract defect is inferred by this round.

Root disposition: bothShould andConsider accepted. Rejection actor explicit, mismatchingcase evidence retained explicitly with unchanged pathinvalidation, questionframing simplified. Reviewedlocaldiff; no citations/numbers/RQ/technicalscope deleted,47cites/12slots unchanged. make exits0/build-round7.log; actualpdfinfo Pages:           9. New conceptnames notintroduced; source/complete/GPU/strongnativebaseline scope preserved. NextRound8terminology/claimtone.
