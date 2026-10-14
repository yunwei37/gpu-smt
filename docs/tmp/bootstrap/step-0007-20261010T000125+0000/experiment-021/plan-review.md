# Experiment021 plan review

## Round 1 — 2026-10-13

**Verdict: scientifically admitted as decisive formal-workload RQ4 evidence; execution blocked by one concrete capture defect.** This is a fresh independent PLAN REVIEW, preceding empirical preflight. No native candidate, external checker, GPU, build, acquisition mutation, or Git action was run by this reviewer. The only write is this report. Dependency compilation is not a scientific result.

Reviewed the full research-experiment-design skill and plan template, user instructions, complete idea-story Initial Narrative/current frontier, evaluation frontier, background-related-work baseline map, E96 primary-source interface handoff, E021 plan and runner, bench producer/deferred native interface/capture, archived producer-build6/build3/native-interface-build1 sources and receipts, frozen executed capture and its imported helpers, native E020 build1 frontend framing, and the official CPU/resident GPU service adapters. Read-only Python compared original inputs and frozen source bytes; this was not an empirical preflight.

### Blocking finding B1: rejected/incomplete responses crash the frozen external capture

The producer initializes `backendRecord := Json.null` and only replaces it inside `if accepted && deferred`. Ordinary frontend-rejected and sorry/incomplete sources therefore intentionally return `result.backend: null`. In both `bench/lean_capture_formal_backend.py` and the actual `experiment021/executed-source/lean_capture_formal_backend.py`, `finish` executes:

```python
value = record['result']
checked = value.get('backend', {}).get('checked', {})
```

A present JSON null becomes Python `None`; the default `{}` does not apply. Consequently `.get` raises `AttributeError` before the row is persisted. The surrounding transport handler does not catch AttributeError. The acquisition exits instead of retaining the rejected/incomplete outcome or proceeding to later original candidates. This directly affects the declared first ProofNet preflight input 0, as well as the failure-inclusive full pools. It invalidates executability and population completeness; it is not an optional diagnostic or correctness expansion.

Minimal repair: handle an absent/non-object backend before extracting its optional checked record, and retain errors/sorry outcomes independently of whether backend checking was attempted. Update the actual executed capture as well as its source before freezing it. Do not solve this by removing failed sources, labeling their ordinary rejection as an operational failure, or adding a new controller. This repair does not alter the expected scientific answer, workloads, baselines, or budgets. A follow-up review of the changed lines is sufficient before the existing integrated real preflight.

### Admission and hypothesis

Admission holds. E018/E019 use separate4.21 LeanPolish contexts and cannot supply whole4.9 ProofNet/miniF2F evidence by reanalysis; E015 profiles identify residual work but cannot reconstruct the new external/device verification boundary. E020 tests lifecycle/preparation reuse rather than this heterogeneous checking relation. The new matrix supplies genuinely unmeasured full-source verification after reuse. Its success would admit a measured heterogeneous operating region; failure would reject this implementation as a whole-verification acceleration explanation. Neither outcome requires changing the four RQs or narrowing the human goal.

The strongest reviewer objection is directly tested: tiny supported GPU coverage, frontend cost and representation/fallback may erase component gains. Complete source verification is the appropriate decisive next discriminator, and higher value than further small fragment/readiness/diagnostic work. The plan should be interpreted as decisive within the fixed formal pools, not complete RQ4 or thesis closure. Prior metadata speedup, candidate-generation GPU execution and build receipts are properly excluded from its effect estimates.

### Baselines, workloads and fairness

The two CPU competitors meet the skill's baseline rules. Actual optimized E020 native full-snapshot reuse is the strongest compatible current-practice source path; official optimized resident closure CPU checking represents a distinct algorithmic competing answer. Both need matched complete-boundary measurements because published post-export/later-version checker numbers do not settle source construction, representation and fallback here. The same-source CPU fragment is correctly an internal control rather than a headline competitor. Superiority must use the faster valid complete CPU method; interface failure/nonengagement cannot count as a GPU win. No additional baseline is required.

The original full populations remain5952/7808 and the24whole-condition matrix gives165120 outcomes. Read-only comparisons confirmed all selected preflight records exactly equal their original E014 records: ProofNet0/257/2913/5879/5880 and mini0/1/723. Both preflight task files are byte-identical to the full original task files, so prefix preparation exercises the actual public-task population. Literal None sources are not rewritten or filtered. Full acquisition reads the original E014 input paths directly.

Equal CPUs21–24, per-dataset widths4/1, caller success-only exact-source caching, original300s source deadline and default frontend threads are explicit. The external four-thread CPU backend can oversubscribe; that cost is measured rather than a hidden resource advantage. Public types select imported dependencies, while native need not perform unnecessary export work. There is no split leakage claim because this is offline verification of unchanged candidate pools, not generated-proof accuracy. Separate device acquisition prevents literal interleaving of all three methods despite nominal rotation; host-load records and shared-device disclosure limit precision. This is a scheduling limitation, not an independent blocker or reason to add a campaign.

### Deferral, prefix, export and outcomes

The isolated native interface defaults to checking and only defers safe definition/theorem/non-unsafe opaque addition; other constructors stay native. Witness construction does not by itself accept a proof. The archived build3 exporter explicitly discloses the nested-Bool0/1 consumer projection, with complete runtime qualification still necessary. Compilation establishes no acceptance/performance evidence.

Prefix preparation uses native-checked public statement types solely to select imported dependencies; synthetic type axioms are discarded. Candidate bodies do not enter the immutable prefix. CPU service checks the prefix before sealing; every accepted candidate overlay receives fresh official suffix checking or qualified GPU discharge plus official CPU remainder. Exported-local coverage is checked independently: missing local export changes the code to declined2 and invokes a fresh normal native fallback without a deferred previous snapshot. A backend decline uses the same path. Opaque values are included in local sorry detection/export. Backend3 is explicitly operational failure, while rejected/declined/unsupported distinctions must remain visible in raw records. Basic parity with original native decisions and the matched native method is still a real-preflight/full-review obligation, not established here.

The source's negative/incomplete paths intentionally skip external acceptance and preserve native diagnostics/sorry observations. That design is compatible with the hypothesis, but B1 currently prevents their persistence. Missing/partial frames, timeout, backend EOF and producer failure have explicit capture terminal paths; native envelope framing matches the E020 normal stream. Recovered original operational failures require the plan's separate independently checked reporting. No diagnostic-string or thread-cleanup expansion is requested.

### Commands, metrics and completion

The actual run.py selects producer-build6, CPU prefixbuild4, GPU backendbuild5 and exact E020 build1 reference. Producer-build6 archived source is byte-identical to bench; the frozen capture/snapshot/resource helpers checked are byte-identical to their bench counterparts. Builds do not replace the unchanged resident GPU backend/PTX2. The imported analysis helper exists in the executed-source directory and native framing uses its ordinary basic response interpretation.

Whole makespan/terminal throughput and admission-to-terminal distributions have an explicit standard service precedent (SOCK) and retain all original outcomes. CPU/wait accounting and separate sampled PSS profiles appropriately supplement whole time. Gzip witness work and final worker/backend EOF/wait are inside capture. The later ZIP packaging is explicitly outside the measured acquisition; do not include that later packaging as a measured service cost or claim repeated PSS confidence. Shared whole-card snapshots are not isolated per-method VRAM. Failed/partial conditions cannot be stitched into complete times.

`preflight` runs the native and CPU legs; the available `preflight-gpu` entry is needed for the real device leg. The integrated preflight is not complete until both datasets/all three paths finish with the fixed basic oracle and actual GPU engagement. `full-cpu`/`full-gpu` together specify18primary+6profile conditions; heavy mini is gated on E015's existing terminal receipt and absence of its heavy handles. The runner's per-condition count/exit summary is not itself the promised full basic/resource reconciliation or fresh result review, which remain required before any result claim.

The GPU entry inherits `LEAN_GPU_*` configuration and does not create an owner request. The unchanged resident GPU service can legally run complete CPU fallback if that configuration/device worker is missing. Therefore the existing owner workflow must supply the frozen tool/CPU-library/PTX/output mounts and actual5090 runtime, and retain engagement/error records. This is an explicit prerequisite already in the plan, not a second GPU launch authorization or a new baseline request. A CPU-only GPU-labeled condition cannot answer the device hypothesis. No GPU request/action was performed here.

### Disposition and follow-up limit

Repair B1 in the actual capture and preserve the fixed full experiment. Request one changed-artifact follow-up in this same report; at most two total follow-ups remain after this first review. No additional baselines, broader workloads, diagnostic-string checks, thread campaign, source mutation during acquisition or rewritten hypothesis is recommended. After the minimal repair, the strongest runnable next step remains the declared integrated real preflight, followed by full formal performance acquisition and fresh complete result review. Lean-first formal/SMT/service/RTX5090/four-RQ/paper/OSDI-quality obligations remain intact.


## Round 2 — changed-artifact follow-up, 2026-10-13

**Verdict: admitted for the declared real preflight and subsequent unchanged full matrix; no remaining blocking plan defect found. B1 is resolved.** This is the first of the maximum two follow-ups. No empirical preflight or candidate/backend/GPU execution was performed by this reviewer.

Independently inspected both changed captures. They now use:

```python
checked = (value.get('backend') or {}).get('checked') or {}
```

A producer's intentional JSON null backend now yields an empty optional checker record, allowing the existing has_errors/has_sorry branches to persist rejected/incomplete outcomes. Actual checker records retain their code3 operational classification and complete acceptance logic. This repair changes neither the oracle nor the accepted-source workload and removes the exact uncaught AttributeError identified in round1. The bench and actual executed-source capture are byte-identical.

Read-only AST parsing succeeded for run.py and all four executed-source Python dependencies. All four exact selected executables exist and are executable: producer-build6, E020 build1 native reference, official CPU prefixbuild4 and resident GPU backendbuild5. Archived producer-build6 source remains byte-identical to bench. These checks verify static executability/dependency presence only; they are not empirical qualification, backend engagement or performance evidence.

The round1 scientific admission, two strongest CPU competitors, whole metrics, original5952/7808 failure-inclusive populations, fixed300s deadline,24whole conditions/165120outcomes and basic native outcome oracle remain unchanged. No extra baseline, workload, diagnostic-string check or thread campaign is needed. Existing GPU runtime/configuration/actual5090 engagement and the E015 heavy-mini terminal dependency remain the plan's execution prerequisites; a GPU-labeled CPU fallback-only run remains insufficient device evidence. The declared integrated preflight must still complete both datasets/all three paths before it is counted complete. Basic outcomes, fallback/local-export coverage, real device engagement and whole-cost accounting require actual preflight and full-result review rather than inference from this static follow-up.

Proceed on this fixed admitted path. No third review round is required absent a materially changed artifact or new invalidating defect. Full Lean-first formal/SMT/service/RTX5090/four-RQ/paper/OSDI-quality obligations remain preserved.


## Round 3 — final changed-artifact follow-up, 2026-10-13

**Verdict: admit the repaired build7 path for integrated real preflight2; no remaining blocking plan defect found in the changed artifacts.** This is the second and final permitted follow-up (review3/3). Static repair review does not qualify the new prefix at runtime or complete the integrated preflight. No candidate, native/backend/GPU execution, build or acquisition mutation was performed by this reviewer; only this report was appended.

Read the actual preflight1 raw per-input results and worker stdout. ProofNet native/CPU both retain0 rejected,257 complete,2913 incomplete,5879 operational_failure and5880 rejected. Mini native/CPU both retain0/1 complete and723 rejected. Thus the capture-null repair worked on real rejected/incomplete paths, and all eight selected source decisions agree in these legs. The GPU leg is absent, so attempt1 never completed integrated readiness.

The baseline-preparation defect is real: mini stdout reports244 public types,244 unavailable,0 constants/expressions; the CPU service reports prefix_verified for zero declarations. The original244 task statements all end `:= by`; ProofNet's186 all end `:=`. A verified empty prefix is not evidence that the intended prepared mini CPU competitor engaged. Attempt1 remains useful failed qualification evidence, not a heterogeneous performance result or final repetition. ProofNet reports8 unavailable public types and29709 verified imported declarations in both worker sessions; that partial type availability must remain visible rather than assumed repaired.

Independently compared archived producer-build6 and producer-build7 source. The sole producer difference is statementTypeCommand recognizing and stripping exactly the original trailing `:= by` in addition to the existing `:=`, before constructing the same type-only axiom command. Five trailing characters are removed for `:= by`; generated proof bodies are not consumed, source candidate verification is untouched, and the synthetic type declarations remain discarded before prefix export. This is an input-adapter repair to restore the already-declared public-type preparation, not outcome/coverage tuning or a new hypothesis. Bench source equals the archived build7 source. All four archived build7 compile/link receipt return codes are0 and its executable is present/executable. This remains dependency evidence.

The actual runner now selects producer-build7 and parses successfully. Its explicit attempt argument maps `preflight 2` and `preflight-gpu 2` to preflight2; existing per-condition exclusive directory/file creation prevents overwriting prior attempt1 outputs and keeps CPU/GPU legs distinct in the common attempt directory. CPU prefixbuild4, resident GPU backendbuild5/PTX2, native E020 build1, original input paths/populations, basic oracle,300s deadline, whole boundaries and24condition/165120outcome matrix are unchanged. No full condition or E021 GPU result is promoted from attempt1.

The plan correctly records the failed mini preparation and retained1/3 actual attempt count. Run repaired integrated preflight2 on the fixed original inputs. Actual public-prefix construction/official verification must engage for mini, and the real5090 leg must complete with the same basic outcomes and retained coverage/fallback/cost records before integrated readiness is asserted. Remaining unavailable public types are scoped observations provided the complete original overlays/fallback remain checked; no all-types-success gate or extra diagnostic campaign is introduced. If runtime remains broken, apply the skill's finite preflight repair rules rather than opening a fourth plan-review round or changing the scientific contract.

Scientific admission remains decisive within the complete formal pools against the faster valid native/official-CPU competitor. No broader baseline, workload, thread or diagnostic-string campaign is requested. Full Lean-first formal/SMT/service/RTX5090/four-RQ/paper/OSDI-quality ambition remains unchanged.
