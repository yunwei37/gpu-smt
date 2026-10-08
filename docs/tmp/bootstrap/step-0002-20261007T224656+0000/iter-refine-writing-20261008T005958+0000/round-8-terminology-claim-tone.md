# Round 8 — Terminology and claim tone

Parent: `/root`; reviewer: `/root/step2_writing8`.
Start observed by clock tool: 2026-10-08 01:17:39 UTC.
Review completion observed by clock tool: 2026-10-08 01:19:22 UTC.
Mode: BOOTSTRAP, serial terminology-infoflow and claim-tone review; report only. No paper edits, build, or Git operations performed. The caller owns edits and compilation.

## Instruction and question audit

The delegated instruction explicitly authorizes findings only and prohibits editing the paper. The target and report destination are explicit. No clarification is required. Intended completed prose and missing-result slots are permitted: present-tense design and implementation descriptions are not converted into a proposal, nor are missing outcomes invented. All four exact RQ strings, citations, numbers, native boundaries, fallback behavior, fidelity conditions, complete-cost inclusions, baseline qualifiers, and the broad Lean/SMT/RTX 5090 goal are protected.

## Read and procedure record

Read the complete current `docs/paper/main.tex` (207 lines) and actual bibliography `docs/paper/references.bib` (196 lines). The initial attempted `main.bib` name was corrected to the bibliography declared by main.tex. Read the full filesystem skills `/workspaces/.agent-state/codex/skills/check-terminology-infoflow/SKILL.md` and `/workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md`. No skill tool was used. The selected scope is terminology-infoflow (J/C/F/X), not paper-consistency; the latter's reference is therefore not required by the selected scope. This review does not perform a new external citation audit.

Ran a vocabulary-frequency audit with Python 3 after the `python` alias proved unavailable. Inspected first use, definition, synonyms, caption/body usage, introduction-to-evaluation claim alignment, and self-attacking versus scope-bearing prose. The raw frequency scan includes labels and missing-result slots; these were excluded from invented-term findings when they are not completed narrative prose. No new term, mechanism, research framing, or algorithm is proposed.

### Concept inventory and dependency check

| Concept | First use / explanation | Stability judgment |
|---|---|---|
| Preparation and candidate execution history | Abstract L13–18; Introduction L26–34; native-prefix explanation L55 | Consistent; distinguishes retained preparation from later candidate history. |
| Prepared state / prepared parent / native prefix | Abstract L18; Background L55; Design L98–100 | Refer to related but distinct objects (state, process owner, ordered prefix), not a harmful synonym drift. |
| Independent branch | Abstract L18; Introduction L32–36; process mechanism L57 and L132 | Stable with candidate lifetime and mutable state. |
| Supported quiescent boundary | Abstract L17; Design L100 | Definition delayed; see S1. |
| Observable behavior / fidelity | Abstract L14; Background L50–52; Design L103–107 | Preserves responses and artifacts, admissions, UNKNOWN, runtime/resource caveats. No simplification to logical soundness. |
| Resource/service frontier | Introduction L34; Evaluation L145 and L174 | Defined in prose before repeated use; keep exact-resource scope. |
| Proportional/fleet memory | First fleet-memory use L30; substantive definition L119 | Ordinary system term with a later explicit definition; first-use polish is optional, see C2. |
| Complete verification / post-export checking | Abstract L19; Background L48; Implementation L129; RQ4 L177 | Boundaries distinguished consistently; do not flatten them. |
| Device qualification / online checks / native verification | Design L125 | Distinct stages; no second full CPU replay required. Preserve this clarification. |
| Warm services / persistent environments / logical or serialized reuse | Abstract L15/19; Introduction L30; Setup L157 | Established mechanisms with clear baseline roles; preserve strongest matched competitors. |
| Output identity / exact reference comparison | Implementation L140; RQ4 L177 | Per-operation identity is stronger/different from semantic validity of alternative whole artifacts. See C1; no automatic weakening. |

The term frequency audit found `prepared-state` most frequent (9), followed by familiar standard compounds and boundary qualifiers. The core vocabulary does not exceed a reasonable concept budget. No hardcoded system name occurs; this unnamed service has no `\\sys` macro, so there is no system-name violation to manufacture. No math notation drifts. The architecture caption uses the same parent/prefix/branch vocabulary as the body.

## Must-fix

None found within the assigned terminology and claim-tone scope. The draft has explicit missing-result slots, not fabricated quantitative findings. The exact RQ wording is protected even where a general skill might suggest shortening it.

## Should-fix

### S1 — Abstract / Design, L17 and L100 — C2/J6: late explanation of quiescence

Quote: “supported quiescent runtime boundaries”.

Problem: Systems readers may know quiescence generally, but the precise safe point for this verifier is not explained until Design. The abstract already depends on that deployment constraint.

Concrete fix: “supported runtime boundaries with no pending candidate work or unresolved external effects”. Keep the fuller supported-quiescent-point wording and branch controls in Design. This replaces a compact technical word with its existing definition, not a new compatibility requirement.

Alternative: “supported quiescent runtime boundaries, where candidate work and external effects are settled”. Prefer the first because “settled” is less exact than the existing definition.

Uncertainty: Low; the definition is already supplied by L100. Do not strengthen this into arbitrary process-cloning safety.

### S2 — Related work / Implementation, L191, L197, L140 — self-attacking novelty defenses

Quotes: “This distinction requires matched evidence, rather than a novelty claim for snapshots themselves.” “Verification specialization alone supplies no novelty over these systems.” “so their use does not establish a new checking algorithm.”

Problem: These sentences repeatedly reject novelty claims the paper does not make. Their substance is valuable: prior snapshotting, prepared execution, and checker representations are direct competitors, and the contribution is tested at the native-behavior/equal-resource/complete-cost boundary. State those relationships directly rather than sounding like a rebuttal to the paper itself.

Concrete fixes:

- L191 final sentence: “The matched evaluation tests this distinction against existing snapshot and environment-reuse mechanisms.”
- L197 third/fourth sentences together: “Our comparison tests whether a verification-specific execution mechanism improves on these prepared-execution mechanisms while preserving native behavior and bounding shared preparation.”
- L140 final sentence: “The device path uses established checker techniques, including expression layouts with integer identifiers and delayed substitution~\\cite{nanoclo,nanocloFortran}.”

Alternatives: Keep the L140 original if the preceding rounds established a recurring misinterpretation requiring explicit denial. Do not delete any cited representation attribution or the strong CPU comparison. Do not replace L197 with an assertion that the mechanism is already shown beneficial.

Uncertainty: Medium; tone benefits are clear, but explicit non-novelty language may be an intentional guard against prior overclaiming. Preserve its scope as a direct competitor relationship.

### S3 — Evaluation RQ1–RQ4, L164, L169, L174, L179 — project-status cadence

Quotes: “RQ1 remains unanswered until…”, and equivalent endings for all four RQs.

Problem: Four consecutive RQ sections end as progress reports. Existing result slots already mark the missing evidence. The final sentences contain meaningful evidence conditions and must not simply disappear.

Concrete scope-preserving replacements:

- L164: “Complete source-native measurements are required to establish whether preparation sharing is consequential.”
- L169: “A behavior-preservation finding requires a recorded outcome for every planned comparison and an explanation of residual differences.”
- L174: “The service comparison must cover the complete workload and resource matrix against the strongest competent services.”
- L179: “A heterogeneous-execution finding requires measured complete boundaries that establish a device benefit or a negative opportunity bound.”

Alternative: Put each complete evidence condition inside its existing `\\missing{...}` slot if the caller's missing-result convention explicitly treats these as evidence obligations. Keep either prose or slots, not duplicate formulations.

Uncertainty: Low about the repeated diary tone; medium about preferred slot convention. Do not change exact RQ strings or remove strongest-baseline, all-comparisons, complete-boundary, or negative-result requirements.

### S4 — Design and RQ4, L125, L177, L179 — dense and partly undefined cost vocabulary

Quotes: “A resident primitive speedup is reported separately from complete checking.” Missing-result slot: “Cost coverage, ready-work width, complete CPU/device comparisons and workload crossover.”

Problem: “Resident primitive” compresses two measurement qualifiers, while “ready-work width” is an internal-looking term not defined elsewhere. The latter is in an authorized result slot, so it is not a completed-paper violation, but it should not become a result-table label without explanation.

Concrete fixes:

- L125: “A speedup for a checking operation with its data already on the device is reported separately from complete checking.”
- L179 slot: “Fraction of complete checking cost covered by supported device operations, available independent work, complete CPU/device comparisons and workload crossover.”

Alternative: Retain the precise metric label in the slot, but require its formal definition when inserting results. If “ready-work width” specifically means independent operations simultaneously ready under dynamic dependencies, use that full phrase at first completed-prose use.

Uncertainty: Medium; the draft does not yet specify the readiness metric, so do not invent its denominator or scheduling definition. The first rewrite is low risk and retains the difference between resident primitive timing and complete checking.

## Consider

### C1 — Device path, L140 — C1/C6: output identity could be read as whole-artifact identity

Quote: “preserve per-operation output identity”.

Problem: Design permits alternative valid requested artifacts with different representation, whereas this phrase appears to require exact identity. These are compatible if one refers to internal operation outputs and the other to externally requested artifacts, but the distinction could be easier to scan.

Concrete fix: “A CPU reference and GPU implementation consume the same identified input and preserve output identity for each supported checking operation.” Keep the Design artifact-validation clause unchanged.

Alternative: No edit; existing “per-operation” may already be clear enough. Never replace “identity” with mere semantic equivalence without authoritative qualification evidence.

Uncertainty: Medium; this is a clarity suggestion, not a factual contradiction finding.

### C2 — Introduction, L30 and L34 — C2: fleet-memory first-use clarity

Quote: “complete verification, cancellation and fleet memory”.

Problem: “Fleet” is conventional service vocabulary, but some verification readers may initially interpret it as machine-fleet memory rather than memory summed over service processes. Design later defines the latter accurately.

Concrete fix at L30 only: “complete verification, cancellation and total memory across service processes”. Keep the precise proportional-memory definition in Design and named metric in Evaluation.

Alternative: Keep the conventional term as written; do not add a second new named metric.

Uncertainty: Low factual risk, low priority.

### C3 — Design, L100 — claim-tone scope protection can be direct

Quote: “This restriction is a deployment boundary, not evidence that arbitrary native processes can be cloned safely.”

Problem: The sentence protects a real runtime-safety scope, so it is not deletable self-attack. Its negative contrast can nonetheless sound defensive.

Concrete fix: “Safe process branching is restricted to the runtime boundaries qualified by each adapter.” This retains the prior sentence's unsupported-runtime native fallback.

Alternative: Retain original to emphasize that supported-point evidence does not generalize. Do not remove or weaken the deployment boundary.

Uncertainty: Medium: the original deliberately distinguishes evidence scope from a universal safety guarantee; keeping it is acceptable.

### C4 — Experimental setup, L155 — F5/X1: overlapping control descriptions

Quote: “Published proofs, failed generated attempts and intentionally invalid controls serve different roles in the evaluation. Published proofs and deliberate invalid or incomplete variants are controls for behavior.”

Problem: Two sentences repeat “published proofs” and “controls” before explaining the important control/locality distinction.

Concrete fix: “Published proofs and deliberate invalid or incomplete variants provide behavior controls, while failed generated attempts remain part of the candidate-stream evaluation. These controls do not establish locality in generated candidate traffic.” Preserve the following provenance citations and source-native identities slot.

Alternative: Keep the first sentence and replace only the second with “The published proofs and invalid or incomplete variants provide behavior controls.”

Uncertainty: Medium: the first replacement names a role for failed generated attempts already established in RQ1, but the shorter alternative is safest if stream composition remains unsettled.

## Protected non-findings and rejected edits

- Do not treat unsupported-boundary fallback, resource-bounded UNKNOWN behavior, artifact support, wall-time variability, process-resource handling, CPU fallback, complete verification cost, baseline fairness, or replay/native boundaries as apologetic text. These define what the claim means.
- Keep the no-second-full-CPU-replay clarification at L125; it prevents misreading qualification as per-request redundant execution.
- Keep “Post-export results answer only the latter boundary” and the full-GPU-checking versus metadata/certificate-workload distinction. They prevent result-scope inflation.
- Keep CPU affinity versus isolation qualification and strongest matched CPU/service competitors.
- Do not rename native logical reuse to process branching or collapse native preparation, visible assertion sets, and execution history.
- Do not claim that any of the four RQs has an answer, and do not convert permitted completed design prose to future tense.
- Do not force a system name or add new core concepts. Common compounds such as copy-on-write, resource-bounded, and proof-state are recognizable and carry needed scope.
- No citation, quantitative claim, or exact RQ-string changes are recommended.

## Priority summary

| Category | Must-fix | Should-fix | Consider |
|---|---:|---:|---:|
| J/C terminology and definition order | 0 | 2 | 2 |
| Claim tone / status prose | 0 | 2 | 1 |
| F/X information flow | 0 | 0 | 1 |
| Total | 0 | 4 | 4 |

Top three changes: explain quiescence in the abstract using its existing definition; replace repeated novelty self-denials with direct baseline relationships; retain every RQ evidence requirement while replacing repeated project-status endings.

Pattern: core terminology and cross-section boundary distinctions are already coherent. Remaining tone issues cluster in Related Work and RQ closing sentences. Report-only changes made to paper: 0. Build not run because the caller owns edits and verification.

## Read-order clarification requested by parent

Actual clarification/read timestamp from clock tool: 2026-10-08 01:23:39 UTC.

I did **not** directly read `docs/user-instruction.md` or `docs/questions-for-author.md` at the start of Round 8. The original instruction audit relied on the delegated task, which carried the broad scope and preservation constraints. The original read-order requirement was therefore not fully satisfied; this later read does not retrospectively correct that order.

At the timestamp above I directly read both files in full. The user instruction covers improving verifier performance broadly, including Lean and SMT solvers, investigating GPU Lean or maximal acceleration, using RTX 5090 rather than B300, pursuing an OSDI-quality paper with complete experiments/RQs and the full research loop, and hourly continuation. The questions file states that no research decision currently needs a human answer, OSDI is a quality target rather than an acceptance claim, RTX 5090 is the only authorized GPU family, and the existing hourly heartbeat should be reused.

Comparison with existing findings only: none proposes narrowing the project to a metadata primitive, dropping Lean or SMT, substituting another GPU, weakening the complete-verification comparison, promising OSDI acceptance, or creating a scheduler. The existing report explicitly protects broad Lean/SMT/RTX 5090 scope, complete costs, native fidelity, and strong CPU/service baselines. Its tone suggestions retain evidence obligations and do not claim completed results. No existing finding needs withdrawal on this comparison. The no-clarification conclusion is consistent with the now-read questions file, but its original timing remains as stated above. No fresh review or paper edit was performed.

## Root disposition and completion

S1 retained: quiescence is standard runtime terminology, with the exact deployment definition in Design and explicit safe-boundary condition in Introduction; expanding the abstract alone would disrupt its established correspondence without clarifying a new scientific fact. S2 retained all three non-novelty guards: prior prepared execution and representations are substantive attribution/claim boundaries, and the proposed device rewrite would additionally assume an already selected technique. S3 rejected: BOOTSTRAP structure policy explicitly requires an honest unanswered ending in each RQ block; protected result slots and full evidence conditions remain unchanged. S4 applied the plain definition of resident operation timing in Design; deferred slot terminology until the dynamic metric is admitted, with no invented denominator/readiness definition. C1 applied the operation-output identity clarification. C2 applied total memory across service processes at the first Introduction mention; the precise PSS/fleet definition remains. C3 retained the explicit non-generalization of process safety, necessary given unresolved E6 runtime qualification. C4 combined redundant control descriptions while retaining all failed generated attempts and the control/locality distinction. No scientific requirement is removed or added.

Root independently compared all findings and edits with directly read user log and questions. The reviewer disclosed it omitted these files at review start and completed the direct read at01:23:39UTC; this is a real procedure omission, not retrospective compliance. Its existing findings were rechecked against the actual broad scope without a fabricated review rerun. Root rejected scope-changing or phase-inappropriate recommendations above.

Applied paragraph-sized changes were diff-inspected. Exact4RQ strings,12result slots,34citation expressions and numerical tokens (multisets, allowing already reviewed section movement), and unchanged annotated bibliography match entrybaseline d224cd2d991439940e5b4b108b55b53c6a1b8525. An initial ordered-citation check failed on previously reviewed section movement; multiset check passes, not a source change. make exit0, PDF8pages (previous7; a layout break after expanded prose), no fatal/undefined-reference errors, existing layout warnings retained. Source SHA2561a6afccbcd5a319bf530b7e82ebc1ea6d9698e150c3f4f5dc125d22bdbe3382f. Completion 2026-10-08T01:24:36.120140+00:00. Next Round9 fresh flow review.
