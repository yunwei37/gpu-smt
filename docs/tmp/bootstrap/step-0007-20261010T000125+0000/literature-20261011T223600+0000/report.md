# Native compilation and arithmetic CPU baseline scope

Observed2026-10-11T22:21–22:36UTC. Parent step0007 E50 and prior literature-20261011T074412+0000; EXPERIMENT_GATE, unchanged RQ4: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

## Claim question and finite coverage

Does the current arithmetic comparison accidentally omit a mandatory native-compilation prerequisite of the external CPU competitor, and is general native metaprogram compilation a credible stronger competing explanation for the apparent device opportunity? This question can invalidate an unfair baseline or prevent unnecessary rebuild/extra matrix work. It does not create a new contribution, redefine RQs, promise GPU LP gains or rerun the global novelty survey.

Read user-instruction.md, complete Initial Narrative/evolution, current paper and existing closest-work map. Preserve Lean-first complete verification, existing SMT scope, RTX5090, all outcomes and OSDI-level goal. Names removed, the candidate claim remains consequential heterogeneous complete verification after strong CPU reuse/search; arrays, native compilation, exact oracle replacement and hypothesis selection are prior mechanisms.

Coverage boundary: version-specific official Lake semantics; the exact external Farkas configuration and replay protocol; actual deployed binary symbols and shared-library maps; native arithmetic default selection; source versus measured performance distinction. Completion is a source-grounded baseline disposition for these axes, not generic literature exhaustion or a numerical CPU/GPU conclusion.

## Search and primary verification

Queries2026-10-11: `Lean precompileModules tactic performance Mathlib native interpreter supportInterpreter`; `Farkas Lean native oracle numerical hypothesis selection repository`. Sources: official Lean/Lake code/docs and talk, official Farkas artifact, Mathlib issue/source. Current Lake documentation supplies a lead only; its newer fields are not transplanted to4.9. The official2022talk PDF retrieval errors; no claim derives from unread slides. Secondary tutorial/reddit/Wikipedia leads are excluded. Mathlib issue27231 is a different2025toolchain feasibility caution, not evidence this pinned4.9build fails.

- [Pinned4.9library configuration](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/lake/Lake/Config/LeanLibConfig.lean), [package configuration](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/lake/Lake/Config/Package.lean): native shared-module compilation is an existing optional metaprogram optimization, default false. It is neither GPU work nor our innovation.
- [Pinned4.9executable configuration](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/lake/Lake/Config/LeanExeConfig.lean): supportInterpreter exports linked native symbols; exporting globals is distinct from compiling/linking all imported tactic implementations. [IR interpreter](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/library/compiler/ir_interpreter.cpp) consults native symbols and otherwise interprets retained IR.
- [Exact Farkas library configuration](https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/lean/lakefile.toml) does not set native module compilation; [4.31library default](https://github.com/leanprover/lean4/blob/v4.31.0/src/lake/Lake/Config/LeanLibConfig.lean) remains false. This alone is not a dynamic performance measurement.
- [Farkas evaluation](https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/docs/evaluation.md) labels the reference oracle interpreted. Its438published solution files include179version-drift failures under4.31; original failed generation attempts are a different population. Do not describe its replay as accepted-input-filtered, transfer author ratios here, or equate its marginal sum with our complete command clock.
- [Official replay](https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/scripts/replay_live.py) imports Farkas.Instrument, retains telemetry, uses env0, strips imports, defaults4workers and40theorem replacement, and separately sums imports/marginal theorem clocks. Our whole candidate/root/shutdown, original4.9, one-worker/common256replacement and separate main/profile protocol are disclosed adaptations, not that exact published execution recipe.

## Actual deployed source and binary evidence

Raw copies/commands/nm outputs/loaded-library observations are in artifacts/lean-native-compilation-2026-10-11/source-inspection/. No original binary/source or running acquisition changes. Ordinary inspection.json is raw reproducibility evidence, not a gate/control manifest.

Both deployed arithmetic build3and original snapshot build16 export38Lean.Meta.simp-family and19Lean.Meta.synthInstance-family symbols. Current arithmetic exports Context globals but zero Farkas.nativeWithTrace or Linarith functions; snapshot likewise has zero Linarith exports. Actual runtime loaded-native-library observations supplement binary symbols: absence from one executable alone would not prove absence from loaded shared objects. This distinguishes already-native core operations from interpreted imported tactics; do not call all Lean execution interpreted.

Actual pinned Verification.lean selects cfg.oracle.getD(.simplexAlgorithm). Frontend's older Fourier-Motzkin prose is stale for the executable default; Datatypes explicitly provides both alternatives. The prior report already verified this default. Current public exact Rust simplex compares against that same default algorithm family; do not invent a Fourier-Motzkin-versus-simplex explanation from the stale comment.

Actual Instrument.lean conditionally wraps oracle/preprocessors only when telemetry is enabled. Thus main does not perform the expensive loggingOracle LP serialization; clocks/route/checkpoint adapter work still exists and is charged. A quick excerpt of loggingOracle alone would misdiagnose the main path. Separate profile and main semantics remain declared; no source repair is justified by that disproved suspicion.

## Baseline handoff and paper decision

| Competing position | Official mechanism/status | Input and boundary | Required numerical decision | Risk and interpretation |
|---|---|---|---|---|
| Exact CPU search plus selected-hypothesis preprocessing captures arithmetic gains without GPU | Pinned Farkas simplex/selection;4.9port passes scoped original-input feedback qualification, whole E011active | Same full candidates/version/common warm preparation and whole shutdown; raw original feedback retained | Complete current E011determines CPU effect/residual demand; available author publication cannot quantify this workload | No whole-corpus port correctness/performance yet; version/population/protocol adaptations disclosed |
| Native compilation of remaining metaprograms captures apparent accelerator headroom | Official Lake4.9supported path; core native symbols already engage, imported arithmetic lacks native implementations; full tactic build not reproduced | Same source/oracle/candidate policy; compile/setup/storage cost and complete verification boundary required | Admit a matched compiled comparator only when completed residual profiling makes interpreted imported work load-bearing and the path is runnable | No assumed speedup, guaranteed build or additional mandatory matrix now; fullMathlib compilation is not implied by exporting Context |

Root accepts this evidence within existing strongest-CPU family. The current E011comparison does not omit a native-compilation requirement of the selected published Farkas axis. Continue its fixed matrix; do not replace working owners or rebuild their dependencies. General native metaprogram compilation remains a conditional stronger CPU competitor before any claimed GPU advantage in that operation. Cite the official mechanism now, then use completed profiles to decide a nonredundant matched run rather than automatically adding every configuration as a main baseline.

Same-claim risk for generic native reuse/offload remains high; no contribution change is adopted. The larger intended result remains full behavior-preserving service/resource improvement with complete device cost against best CPU. Missing whole measurements are not fixed by a compiler flag, source report or more names.

## Completion, limitations and next action

Declared source axes resolve sufficiently for this baseline disposition; current performance and build feasibility remain explicitly unmeasured. No experiment result, RQ closure, publication-superiority claim, scientific-contract freeze, new source migration or GPU verification is produced. E008/E011remain active and incomplete. Canonical related-work entry links this report; the root updates operational frontier without changing Initial Narrative/evolution/RQs. The later fresh step outer audit owns this node.

Next: finish unchanged whole comparisons and their fresh result reviews, quantify actual costly residual work with its proper intervals, then select the strongest fair CPU/device implementation. Reopen this compilation branch if those complete profiles or reproducible external data show that interpreted imported code changes the device decision. This is a falsifiable revisit condition, not a quota/deadline or instruction to stop valid work.
