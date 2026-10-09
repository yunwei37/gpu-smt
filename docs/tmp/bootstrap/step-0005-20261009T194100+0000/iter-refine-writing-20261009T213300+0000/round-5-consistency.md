# Round 5: paper consistency review

Started: 2026-10-09T21:52:00Z (approximate first-read time). Completed: 2026-10-09T21:55:00Z. Parent: BOOTSTRAP step-0005-20261009T194100+0000, iter-refine-writing-20261009T213300+0000. Reviewer: fresh read-only serial Round 5 subagent.

Objective: diagnose architecture, ownership, cancellation, fallback, CPU/device workflow, interface/mechanism agreement, figure alignment, contribution/goal/RQ/evidence mapping, and paper-wide claim and number consistency. No paper, code, build, Git, or empirical changes were performed. This report is the only written artifact.

## Sources and identities

Read `docs/user-instruction.md` first and completely. Then read the complete `docs/paper/main.tex` (236 lines) and `docs/paper/references.bib`, followed by complete actual filesystem skill instructions (initial tool output was truncated, so the relevant sources were separately reread). No old reviews or desired-fix lists were read.

| Source | SHA-256 |
| --- | --- |
| docs/paper/main.tex | 2d0cf23b6596fe8e9ae4e41e188943e67083be1ba44d799f3cdb8c60ea646e84 |
| docs/paper/references.bib | f55c6af75bd07eb090c76c243a82a703719be50e682edeea64f1be77fbd9ceb2 |
| /workspaces/.agent-state/codex/skills/check-terminology-infoflow/SKILL.md | c688b995fd38022d6c0d5589f94efc5a8d3a7030d2f046d2ea455475df9cadb6 |
| /workspaces/.agent-state/codex/skills/check-terminology-infoflow/references/paper-consistency.md | c0ebdb733a72df59129f1351ffad04d6476e0d4b152a785d8158eb8f1abb74b5 |
| /workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md | 647b2676d953c16c69755b93872e1c31a530d338576f3e1040b05e4be9f8b75a |

Hashes were recorded at 2026-10-09T21:53:29Z. The paper source hash, rather than a Git revision, identifies the reviewed input because this review performs no Git operations.

## Method and factual anchors

Applied paper-consistency scope, extracting interface, execution, accounting and evidence anchors before comparing all sections. Treated completed-system present-tense prose as explicitly authorized BOOTSTRAP submission prose; implementation progress does not require a tense downgrade. Kept missing results as honest placeholders. No actual numerical inconsistency appeared, so no artifact inspection or absence search was warranted. Bibliography annotations were read as contextual scope anchors, not independently reverified citations.

| Anchor | Authoritative locations | Cross-check outcome |
| --- | --- | --- |
| Preparation retains original ordered configuration/context, not alternative-candidate suffix history | Background 64–70; Design 105–115 | Abstract and introduction describe the same separation; source/session distinctions remain explicit. |
| Parent does no post-boundary candidate verification; branches own mutable candidate state, communication and lifetime | Figure nodes/caption 91–103; Design 105–125; Implementation 155 | CPU ownership and parent quiescence agree. Device ownership needs the clarification below. |
| Original interface is the reference, before branching qualification | Design 113–119; Implementation 141–150; RQ2 194–196 | Fresh adapter qualification, split parsing controls and divergent-path exclusion agree. |
| Native counters versus service CPU/elapsed accounting | Abstract 20; Introduction 40; Design 115; Implementation 155–159; limitations 209 | No universal wall-time equality claim; deterministic work and measured wall-time behavior stay distinct. |
| Unsupported boundary/artifact uses native execution; UNKNOWN is not automatic divergence detection | Figure 89–103; Design 119; Device 138; Implementation 164 | Native-boundary fallback and unsupported device-operation CPU execution describe different layers consistently. |
| Source checking versus post-export checking versus tactic screening | Background 54–62; Implementation 150; setup 180–182; RQ4 204–206 | Boundaries are explicit and no tactic screen is promoted to an accepted enclosing proof. |
| Device qualification versus per-request native checks | Design 134–138; Implementation 164; RQ4 204–206 | Offline matched output comparison does not imply a full online CPU replay; online checks and fallback remain charged. |

## 1. Inconsistencies found

### Must-fix

None identified. No conflicting measured values, architecture contradiction, RQ scientific drift, or figure-versus-prose contradiction was found in the reviewed source.

### Should-fix

**S1 — Branch lifetime and device execution leave ownership of outstanding device work implicit.** Section: Design, Branch lifetime and cancellation (123–125), Heterogeneous checking (134–138), Figure 1 caption (103), and Implementation Device path (164). The lifecycle says cancellation stops the branch and releases its private memory, and the caption says it “ends its private work,” while branches may execute device operations. The CPU process ownership is explicit, but the text does not connect outstanding device work and buffers to that same lifetime. This is a cross-layer ownership ambiguity, not a demonstrated implementation defect or a claim that device cancellation is impossible.

### Consider

**C1 — Mirror the exact RQ1 qualifier in its subsection opener.** Section: Evaluation RQ list (171) versus Preparation sharing opener (189). The canonical question contains “across independent jobs”; the opener omits these words. The remainder of the subsection and Design supply independence, so this is not scientific drift. Repeating the qualifier makes the formal RQ and evidence block mechanically stable.

## 2. Why each matters

S1 matters because termination/reaping of a host child alone does not specify the completion boundary of device work. A reader should be able to tell when the service regards a candidate as ended, which device allocations remain attributable to it, and whether waiting for cancellation cleanup is included in service resource measurements. This same ambiguity affects the figure's unconditional cancellation statement and the claimed independent lifetimes. The requested change should specify the intended contract without inventing a particular NVIDIA mechanism.

C1 matters only for consistent presentation: all four numbered questions have matching evidence blocks, and preserving their exact qualifiers reduces accidental wording drift in future result insertion.

## 3. Exact fixes or replacement wording

For S1, add one local sentence in the lifetime subsection or Device path that states the actual intended ownership/completion contract. A suitable mechanism-neutral formulation, if it matches the root's intended design, is: “Device work and buffers remain attributable to their candidate until completion or cancellation cleanup; this cleanup is included in the branch lifetime and service accounting.” Then keep the Figure 1 caption's existing independence statement only if this contract is satisfied. If the root cannot confirm this contract, flag the scientific/mechanism choice to the root rather than inventing immediate kernel preemption, a shared device worker, or a new broker design. This is a clarification of the existing independent-lifetime goal, not a request to add a new experiment or broaden the GPU contribution.

For C1, minimally change the first sentence at line 189 to: “RQ1 asks how much expensive native preparation real verification candidate streams share across independent jobs.” Do not alter the canonical RQ, its units, or the preparation-sharing evidence scope.

## Goal, contribution, RQ and evidence mapping

| Protected goal or contribution | RQ and evidence slot | Alignment |
| --- | --- | --- |
| Characterize expensive sharing in actual ordered attempts (contribution 1, 45) | RQ1 (171), Preparation sharing 189–191, motivation placeholder 73 | Cost and locality, failed/incomplete attempts, ordered prefixes and native-environment sharing remain distinct. |
| Preserve native observable behavior (goal 1, 84); native branching behavior argument (contribution 2, 46) | RQ2 (172), Behavior and isolation 194–196 | Interface qualification precedes branch comparison; outcomes, artifacts, scopes, history, limits and cancellation all have evidence slots. |
| Share preparation and isolate lifetimes (goal 2, 84); bounded implementation/cancellation (contribution 3, 47) | RQ2 isolation plus RQ3 fleet/causal measures | Parent/child isolation and bounded retention are covered; S1 is the remaining device ownership bridge. |
| Improve latency/throughput at matched CPU/memory (goal 3, 84) | RQ3 (173), 199–201; contribution 4 (48) | Strong bounded warm competitors, memory/CPU budgets, load/concurrency sweeps, replacement costs and ablations are present. |
| Causal heterogeneous assessment after preparation reuse (contribution 4) | RQ4 (174), 204–206 | Strongest measured CPU path and complete boundary, dynamic dependencies, setup/transfers/synchronization/fallback, crossover and negative bound are preserved. |

The abstract (14–22), introduction (26–48), design (84–138), evaluation (169–211), discussion (214) and conclusion (232) tell the same conditional systems story. They do not claim a measured positive service or GPU result. Each of the four RQ blocks explicitly states an unanswered evidence condition and retains a result placeholder. The conclusion placeholder requests all four findings, including measured heterogeneous scope. The diagram's paths, labels and caption match the CPU flow; S1 identifies the additional device-lifetime clarification rather than a contradictory arrow.

## 4. Broader follow-up checks and protected meaning

After any accepted S1 clarification, root should reread lifetime paragraph, Figure 1 caption, device design/implementation and RQ2/RQ3/RQ4 accounting together. Do not turn fidelity into identical artifact bytes: Design explicitly permits semantically valid representation differences. Do not turn offline qualification into mandatory full per-request CPU replay. Do not weaken the supported/quiescent-boundary restriction or imply arbitrary multithreaded runtimes can be cloned. Do not erase native-history versus logical-context distinctions, counter inheritance versus service accounting, or source versus post-export versus menu-screen outcomes.

No changes should remove the strongest warm/native reuse comparisons, negative/mixed operating-range interpretation, full CPU fallback costs, or the RTX 5090 scope. No numbers, RQ meaning, citations, contribution count, or design goal count need change. The canonical RQ set has four questions and remains within the skill's two-to-five requirement. RQ2–RQ4 subsection openers preserve their canonical meaning; C1 is optional exact-wording alignment only.

Limits: no external citation search, artifact/code audit, sibling-document audit, empirical rerun, build, rendered-figure inspection, or Git operation was performed. There is no claim that an experiment or artifact is absent. Compilation/page evidence and fix acceptance belong to the root. Applied fixes: none; rejected fixes: none. Remaining concerns: S1 and optional C1 only. Next node: root evaluates these findings, applies authorized local clarification if warranted, compiles/verifies, and proceeds to Round 6.

## Root disposition 2026-10-09T21:54:59.281297+00:00

S1 accepted as clarification of already intended complete-cost/lifetime accounting, no new preemption/broker mechanism or executed GPU claim: device work/buffers remain candidate-attributed until completion/cleanup, included in lifetime/accounting. C1 already satisfied in actual source when checked: RQ1 opener already contains across independent jobs, so no further wording change. The attempted identical replacement is a no-op, not a claimed scientific fix. Cross-layer reread of caption/lifetime/device/RQ2–4 preserves conditional qualified operation and complete costs. Source diff retains44citations/23entries/12slots/fourRQ/quantities. Build round-5-build.log exits0/eight pages. User scope unchanged. Next fresh Round6 sentence language.
