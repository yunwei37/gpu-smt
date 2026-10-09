# Round 1: independent micro-structure review

Started: 2026-10-09T21:40:35Z. Completed: 2026-10-09T21:42:30Z.
Parent: BOOTSTRAP step-0005-20261009T194100+0000; writing run iter-refine-writing-20261009T213300+0000. Next node: root disposition, source edits/build/preservation checks, then serial Round 2.

## Instructions, inputs, and method

Fresh independent review without a desired verdict or prior-review input. Read `docs/user-instruction.md` first in full: Lean/verifier/SMT acceleration research, RTX 5090 rather than B300, OSDI-level paper and complete experimental/research loop. Loaded the complete actual filesystem instructions at `/workspaces/.agent-state/codex/skills/check-paper-structure-flow/SKILL.md`, its `references/full-paper-12p.md`, `/workspaces/.agent-state/codex/skills/rewrite-abstract-intro/references/abstract-intro-structure.md`, and `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`. No Skill tool exists and no invocation is claimed. The attempted structure-skill-local abstract reference was absent; the full-paper template points to the rewrite skill's actual reference, which was read completely.

Reviewed sole paper `docs/paper/main.tex`, SHA-256 `c8317e87a868e7ad16b1d74078773348ae19cee0428c7acf02c736c47485da0d`. User instruction SHA-256 `27cbb0d37485cd698ce6e41b26eaa748623e8bc979f95f39ce1e97d0cd3cce76`. Entry commit/evidence revision belongs to root's Round 0 record; no Git query was performed. No external sources, old reviews, implementation status files, or experiment artifacts informed the verdict.

Read the entire 234-line source, including diagram/caption, and re-read the truncated Motivation/Design range separately. Checked every prose paragraph for role, topic-first structure, one idea, why-before-what, old-to-new progression, and transitions. Mapped intro paragraphs at 26/28/30/32/34/36/38/40–46 to background/problem/cause/existing reuse/insight/challenges/system and methodology/contributions, then matched abstract sentences. Inspected each numbered RQ opening and unanswered ending individually.

Scientific meaning, citations, numbers and scope hedges are read-only. Four protected RQs concern preparation-sharing opportunity; response/artifact fidelity plus candidate/cancellation isolation; equal-resource latency/throughput/memory versus established warm reuse; and heterogeneous complete-verification benefit after reuse versus the strongest measured CPU path. BOOTSTRAP completed-system prose and explicit result placeholders are deliberate. No missing-final-data or unfinished-implementation finding, invented evidence, new RQ, or broadened claim is permitted. Only this report may be written; root alone edits/builds/publishes. No agents, Git operations, or native reruns.

## Must-fix

None identified within this writing-only scope.

## Should-fix

**S1 — MICRO, Introduction existing-solutions paragraph, line 32.** Its first sentence announces reuse benefits; its actual argumentative topic—the unresolved matched-resource comparison—arrives only in the last sentence. Move that already-stated comparison into the topic sentence, then retain the cited mechanisms as support. Combine established reuse with the unresolved comparison of independent native execution at matched resources. Do not invent shortcomings for REPL, snapshots, or Kimina: the existing uncertainty is sufficient.

**S2 — MICRO, Abstract methodology, line 21.** With optional cause/challenges included, the reference expects nine role sentences including the result placeholder. Methodology occupies two prose sentences, making ten overall. Combine the Lean/SMT matched-service comparison and subsequent RTX 5090 assessment into one methodology sentence, preserving complete-verification boundaries and setup/transfer/CPU-fallback charges. Keep the explicit result placeholder intact.

**S3 — MICRO/FLOW, Background verification stages, lines 54 and 56.** These paragraphs explain existing acceptance/stage distinctions but end by prescribing this paper's verification/measurement policy. Preserve the safeguards while making their Background endings neutral definitions of complete proof/source verification. Keep this paper's inclusion rule in Experimental setup or the existing Native adapters source-boundary paragraph (150). Retain the LeanPolish citations and tactic-screening versus declaration-checking distinction. This keeps each Background paragraph in an explanatory role.

## Consider

**C1 — MICRO, Introduction system paragraph, line 38.** Six prose sentences plus a placeholder exceed the reference's typical three-to-five-sentence paragraph, spanning mechanisms, fallback, accounting, and two methodology scopes. Consider locally combining the supported-boundary/fallback sentences and integrating branch-owned communication with the mechanism description. Preserve separate service/device measurement scopes and the placeholder. The existing role is valid; do not remove technical content merely to hit a count.

**C2 — FLOW, Native adapters, line 150.** The standalone source-measurement paragraph interrupts the progression from SMT qualification to the Lean adapter. Consider moving it after the first SMT implementation paragraph (144), or begin it “For source verification backed by this SMT adapter, …”. Preserve the narrower solver-session replay boundary; connect the known adapter to the new measurement scope.

**C3 — MICRO, Experimental setup, line 182.** The paragraph opens with outcome retention and alternating condition order, then changes to metrics and complete-cost accounting. Consider splitting after the first sentence so the second paragraph begins “Primary metrics are …”. Preserve every included stage and the throughput/request-latency distinction.

## Positive checks and protected non-findings

The abstract is one paragraph with the correct causal role order and substantive intro correspondence. Required intro roles remain distinct; native-history cause supports the independent-execution insight, and the challenge mechanisms have system counterparts. Design opens with three explicit goals and an overview/operation; its subsections generally explain need before mechanism. Implementation maps design to mechanisms. Related Work is grouped by topic; Conclusion is a single paragraph with a protected result placeholder.

Evaluation lists exactly four RQs before setup. Preparation sharing (187–189), Behavior/isolation (192–194), Latency/throughput/memory (197–199), and Heterogeneous execution (202–204) each open explicitly with their RQ and close with “RQn remains unanswered” and an evidence requirement. Experiments stay subordinate to those questions; Setup/Limitations are outside the count. No absent final result is faulted, and no empirical answer is proposed.

## Preservation, validation, and root disposition boundary

Recommendations only: root must append applied/rejected dispositions, before/after locations, alternatives chosen, source diff, citation/number/RQ preservation checks, compilation/page evidence, and publication decision. No paper edit, compilation, empirical validation, memory update, or state update was performed by this reviewer. The only tree change is this report. An attempted report write using unavailable `python` failed before creating a file; the report was then created with apply_patch.

Preserve every citation, numerical value, placeholder, scope qualifier, complete/native versus post-export boundary, and RQ meaning when resolving S1–S3/C1–C3. Skipping a Should-fix requires a logged reason; Consider items require individual decisions. No scientific-contract defect was identified. Root alone owns fixes and builds; this report does not assert their completion.

## Root disposition and completion 2026-10-09T21:47:24.581348+00:00

Applied S1 topic-first existing-reuse comparison; S2 combines the two methodology sentences without dropping RTX5090 full-cost scope; S3 moves the paper-specific acceptance policy from Background into Experimental setup while keeping neutral stage definitions and both LeanPolish citations. C1 accepted: integrate branch-owned communication and combine supported-boundary/fallback description; all native accounting and method scopes remain. C2 accepted explicit SMT-adapter connection instead of moving paragraph. C3 accepted separate outcome-retention and primary-metrics paragraphs. No deletion of technical content; six findings individually resolved. `round-1-build.log` make exit0, eight pages. Citation commands remain44, entries23, allfourRQ and12 result slots preserved; source diff examined against5553bfc and Round1 reviewed source. No quantitative value/scientific contract changed. Next fresh Round2 section conventions.
