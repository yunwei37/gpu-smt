# Round 11 — Cumulative meaning-preservation audit

Parent: BOOTSTRAP step-0003-20261009T132427+0000 / iter-refine-writing-20261009T154400+0000. Objective: independent read-only audit of cumulative paper changes against entry baseline `c62e4276df4f87c3e8fa81cd758e2c6e7dcffa1e`; no execution or source-fix role.

Timing and recovery: precise initial dispatch time was not captured. The original review was active by the actual 2026-10-09T17:54:29.812348+00:00 measurement. Root subsequently reported an unknown host interruption around 17:57 and found the designated report empty at recovery; this reviewer also observed zero bytes on resume. Earlier chat completion is not durable report completion and no terminal journal event is invented. This is completion of the SAME incomplete Round11, not a new round or restoration audit. Resume rereads were completed by the actual clock observation 2026-10-09 18:25:13 UTC. Final serialization time appears below.

Read scope: docs/user-instruction.md FIRST, full actual /workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md, entire current docs/paper/main.tex and entire baseline main.tex through read-only git show. Initial combined outputs truncated; explicit baseline first-half and current second-half reads recovered omitted text. On recovery the direct-user file, full skill, full current paper and complete cumulative diff were reread; a separate Motivation read recovered the small truncation in the combined reread. All reports0–10 and root dispositions in this same run were read, with separate rereads recovering the initially truncated reports2–7. Complete step-report.md (including W1) and experiment-004/result-review.md were read. No Skill tool exists; full filesystem skill reading supplied the checklist. No external source reverification, solver, build, Git mutation or paper copy occurred.

Blind status: fresh reviewer with no execution role; not blind to previous findings, because tracing every deletion to explicit findings is the required audit method. No desired scientific verdict was assumed. BOOTSTRAP present-tense descriptions represent the intended completed submission; explicit missing results and unanswered RQs are valid at this gate.

## Diff coverage and deletion trace

Complete `git diff <entry-baseline> -- docs/paper/` has only main.tex (26 added /20 removed lines) and rebuilt binary main.pdf. No bibliography/source artifact deletion is present. All source hunks were inspected against baseline/current paragraphs and logged dispositions:

| Current section / changed content | Authorizing finding or evidence | Preservation judgment |
|---|---|---|
| Abstract and Intro problem topic, “Serving independent attempts” / repeated preparation versus shared execution | Round4 paragraph-role plan and abstract-last derivation | Same tradeoff; concrete imports, contention and cancellation example retained. |
| Abstract established-mechanism subject and split comparison/device sentence | Round6 S1 safer alternative and S2 | All four established mechanisms, unresolved equal-resource comparison, complete Lean/SMT/public-stream baselines, 5090/setup/transfer/fallback retained. No cache benefit recast as preparation alone. |
| Abstract shared mutation → branch-local mutation | Round5 S1 disposition | Resolves ownership against immutable parent/private COW writes; bounded memory remains. |
| Contribution observable-behavior compound → ordinary phrase | Round7 S1 | Same contribution and reference. |
| Background kernel citation and frontend-stage citations | Round10 Consider and Should-fix | Existing verified keys added, factual text retained. |
| Background post-export contrast cue | Round9 S1 | Source/post-export boundary unchanged. |
| Background admitted proof → unproved obligation using sorry | Round8 S2 root disposition | Admission warning and completion criteria retained; inaccurate proposed denial of proof-term construction was explicitly rejected. |
| Background logical-equality sentence and fidelity inference removed from that location | Round0 S0.1 | Logical-equality sentence moved verbatim into Motivation; concluding inference integrated as native resource/runtime properties in faithful-boundary argument. No technical inference silently lost. Neutral interface/counter/COW/timer/descriptor/thread facts and citations remain Background. |
| Design admitted prepared state → approved by service | Round8 S3 | Service admission disambiguated from proof admission; policy and fallback unchanged. |
| Parent lifetime absolute shorthand → retention beyond configured policy | Round3 Consider root disposition, Round7 C1 | Explicitly ordered clarification using the existing policy, not silent removal of isolation. Other-candidate independence, cancellation/private-memory release, parent retention policy and no incomplete/cancelled parent remain. |
| High-sharing workload expansion | Round7 C2 | Same preparation-sharing operating range and negative cases. |
| Artifact-checking qualifier “where one is produced” | Round3 S1 | Explicitly ordered repair for UNKNOWN/artifact-free outcomes; response fidelity, online-check costs and no mandatory second replay remain. |
| Device compatibility paragraph split before fallback costs | Round1 S1 | All original sentences retained with above qualifier. |
| SMT native context/parser/construction order, same-source executable control, visible differences | W1 accepted method clarification and experiment004 independent result review; later Round7 S2 and Round8 S1 phrase expansions | Evidence supports CLI-owned context/order and matched-source metadata discrimination. No release byte identity, universal passed qualification, branching/cancellation proof or speed result introduced. Original command sequence, options/scopes/checks/artifacts and rejected-adapter exclusion retained. |
| Native construction/qualification paragraph split and purpose/visibility order | Round1 S2 and Round9 C2 | Original semantic components retained; every observed response difference remains visible. |
| Implementation qualification comparison verbs and post-comparison reuse measurement | Round6 S3 | Same fresh-interface → prepared-branch → reuse order; no assertion all adapters pass. |
| Native resource-control qualification / measured wall-time scope | Round3 S2, later Round7 S3 | Added explicit link to existing hazards/limitations, without invented timer reset or universal counter-based equivalence. |
| Device-path representation cue | Round9 C3 | Existing technique credit and no new checking-algorithm claim retained. |
| RQ1 unrelated-work control wording | Round7 C3 then Round9 S2 | Same control and preparation-depth experiment. |
| RQ1 complete source-native measurement shorthand → complete original candidate streams | Round8 C2 | Completeness/order/CPU-state measurements and full source scope remain in setup and owning paragraph; no exported-term substitution. |
| Related-work assertion-equivalent reconstruction phrase expanded | Round7 C4 | Same distinction between equivalent assertions and original native execution history. |

Round2 found no new actionable repair. Optional abstract result-slot expansion, figure fallback/output cue, duplicate quiescence explanation and generic-state COW rewording were explicitly deferred; no silent deletion was attributed to them. Every substantive deletion/replacement in the cumulative diff has a finding or W1 authorization. No new polish is proposed here.

## Raw findings

Must-fix: none. No unrestored technical loss, qualifier weakening without explicit scope repair, citation loss, quantitative drift, RQ drift or changed scientific framing was found.

Should-fix: none in this restoration-only scope.

Consider: none. The previously deferred cosmetic considerations do not warrant a new Round11 change.

## Protected checks and remaining scope

- exact RQs: 4 → 4, exact ordered equality True
- result slots: 12 → 12, exact ordered equality True
- numeric tokens: 12 → 12, exact ordered equality True
- Citation commands: 37 →39. All baseline citation occurrences/keys remain; additions are lean4 and verus/z3api in Background. The cumulative diff contains no bibliography change.
- Four RQ-owning evidence blocks and all honest unanswered closures remain. Twelve result slots are exact, including source-native setup, full resource matrix, heterogeneous crossover and conclusion scope.
- All numeric tokens are unchanged, including RTX5090, document/geometry settings and numbered design goals/RQs. No constructor-run count or performance result entered the paper.
- Supported/quiescent boundaries, original ordered preparation and untouched suffixes, no extra logical scope/warm solver call, native/reference authority, inherited native counters versus service accounting, UNKNOWN and requested artifacts, residual mismatch invalidation and retained complete outcomes remain.
- Strong bounded warm/cache/native logical/serialized baselines, matched CPU/memory/admission order, fleet proportional memory, private dirty pages, failed/incomplete attempts and cancellation costs remain.
- Source verification versus post-export checking, dynamic binder/constant dependencies, strongest complete CPU competitors, full setup/representation/transfers/synchronization/online-check/fallback costs, negative/mixed operating range and GPU primitive/certificate distinctions remain.
- Direct-user Lean/SMT acceleration, RTX5090 rather than B300, requested model preference and OSDI-level complete research intent have not been replaced by a smaller constructor/metadata proxy. Actual empirical obligations remain open; this writing audit does not close RQs.

Reviewed current main.tex SHA256: `6a6f9e4ddd5a6881ff6b4f2916716a46e97e56b669da3ebc5dc58c0a0f4fa6db`. Baseline main.tex SHA256: `5f2e8f3396ff4b5b0c0e78127454890deb95b398b4ce30217302add1982b74a5`.

No fixes applied or rejected by this reviewer because no live loss was found. No paper/bib/code/raw/memory edit, solver run, build or Git mutation occurred. Only this designated report is persisted by atomic replacement; its transient sibling is removed by replacement. Root owns final compilation/PDF/page evidence; preceding reports record build exit0/eight pages, which is not an independent build claim here. The binary PDF diff was identified, not rendered or used as scientific evidence. Alternative of adding polish or filling BOOTSTRAP results was rejected as outside restoration-only scope. No remaining meaning-preservation concern requires restoration; next node is root disposition/build and the independent whole-step outer audit. A restoration confirmation rerun is necessary only if root applies a restoration.

Completed and durably serialized: 2026-10-09T18:26:23.952065+00:00

Root return —2026-10-09T18:27Z: actual nonempty10,813byte report read in full, its baseline/current hashes and cumulative trace checked against source. No restoration warranted; a restoration-only rerun has no entry condition. Final actual compileexit0/PDF8pages after second container-dependency restore. Four exactRQ strings,12exactslots,unchangednumeric tokens/bib and39≥37citation expressions independently match. This completes the original12serial round loop; no empty-file/chat-only return is counted as complete. Full user scope and all empirical limits are intact. Next gate REVIEW, not a second writing loop.
