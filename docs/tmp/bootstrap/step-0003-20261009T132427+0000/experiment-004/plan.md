# Experiment004: native Z3 construction order

2026-10-09; supporting BOOTSTRAP experiment, selected by the root before new solver runs.

## Research question and admission

RQ2 exactly: **Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?** This experiment tests the prerequisite of a faithful fresh native frontend, not branching, concurrency or cancellation. The earlier complete experiment found five ordered decision changes already in fresh API execution. No existing data vary the CLI-owned manager's construction time, so reanalysis cannot settle that cause.

Role: supporting causal discriminator. The largest credible story it can unlock is qualified native preparation followed by independent candidates, evaluated against established native snapshots and competent bounded warm/cache services. The strongest current reject argument is that the interface changes responses before any service optimization. The competing dynamic Lean synthesis profile would identify expensive work but would not resolve that blocker; another module/fixture profile has lower decision value. Exact real streams and a matched source comparison give this experiment independent evidence. A positive result admits a concrete frontend for later branch qualification. A negative result rejects it or the construction-order explanation. Neither result closes RQ2 or changes the ambitious Lean/SMT/GPU contract.

## Expected and alternative outcomes

Hypothesis: the CLI-native lazy driver matches stock native behavior; forcing the same owned manager to exist before factory installation/input options can change resource-bounded responses. The expectation is source-grounded but unproved. Rebuilding/toolchain differences, other API ownership/plugin differences, or no effect of this factor are competing explanations. Lazy mismatch contradicts interface qualification. Lazy/eager parity contradicts the expected effect on this cohort, without explaining every old API difference. An eager difference establishes this factor's effect only within this matched source implementation; similarity to the old API pattern does not prove sole causality of that API failure.

## Primary assets and precedent

Use all 156 original retained VeruSAGE streams from the 100-task public proof replay, with 440 native checks and five model requests. These are actual captured Verus/Z3 sessions, not constructed formulas or authentic generated candidate traffic. Input authority is `artifacts/native-branch-2026-10-07/full/inputs/*.original`, backed by the original retained trace archive. No acceptance/parity filtering. The [source investigation](../../step-0002-20261007T224656+0000/literature-20261007T225255+0000/z3-cli-api-boundary.md) and [primary source provenance](../../step-0002-20261007T224656+0000/literature-20261007T225255+0000/z3-source/provenance.md) establish the exact constructor/configuration boundary. Official Z3 commit `ddb49568d3520e99799e364fb22f35fc67d887b1` is version4.16.0. Native SAT/UNSAT/UNKNOWN and requested artifacts follow the [official SMT-LIB command protocol](https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf) and [Z3 native shell](https://github.com/Z3Prover/z3/blob/ddb49568d3520e99799e364fb22f35fc67d887b1/src/shell/smtlib_frontend.cpp). Published workload/behavior precedents and strong service baselines are already grounded in `docs/background-related-work.md`; no published result settles this exact factor/cohort.

## Comparison and fairness

One native reference, three necessary controls/ablations; these are not speed baselines.

| Condition | Role | Exact path | Decision consequence |
|---|---|---|---|
| release | Original native behavior reference | Retained official4.16.0 release, `-in -smt2` | Defines each original input response independently of the proposed driver |
| source | Rebuild control | Unmodified same-commit stock CLI, `-in -smt2` | If it differs, source/toolchain effects prevent release-equivalence attribution |
| lazy | Frontend qualification control | CLI-owned initially manager-less command context | Matching source/release qualifies this fresh frontend on the cohort |
| eager | Constructor factor ablation | Identical executable, only `ctx.m()` before factory installation | Compared directly with lazy, isolates creation timing in this implementation |

Driver retains stock memory/environment initialization, command families, strategic factory and interactive stdin parser. Stock global display helpers inactive under these command flags are omitted; signal/cancellation equivalence is not claimed. No API manager, command reconstruction, added scope/check/reset, counter subtraction or fork. All four paths read identical original bytes from file-backed stdin with `-in`/interactive semantics. This descriptor choice differs from older pipe delivery and is recorded, not silently attributed to constructor effects. Original options and budgets remain untouched; cohort inspection finds no timeout/thread options. Affinity CPU8 applies equally, is not isolation, and topology/load are retained. Compilation flags, generated official registrations, exact binary/source hashes and logs are retained. Release-versus-source comparisons explicitly expose build differences.

## Metrics and complete matrix

Primary: per-input ordered check identity and response completeness, native errors/exits, per-request model availability and exact non-statistical response identity. Models may differ validly, so differing model bytes would require native validation before a semantic-equivalence claim; this experiment first records response identity, not accepted-job counts. Native `<<DONE>>` echoes delimit each original check/get-info/get-model response. Retain raw frames, statuses, command indices, stderr and requested artifacts. Statistics are diagnostic; changing time/memory statistics does not by itself invalidate behavior parity. Missing/truncated/empty responses never count as successful identity. No proof/core requests occur in this cohort; no proof/core equivalence follows.

All156 streams ×4 conditions ×3 repetitions =1,872 terminal process cells, 5,280 planned check responses. Each condition/repetition has440 checks,1,751 get-info requests and5 get-model requests (2,196 delimited responses). Three whole repetitions use forward/reverse/forward condition order. Report all differences and repeat stability descriptively; no population confidence interval or deterministic hardware-independent guarantee. Process elapsed time is diagnostic only; no speed headline, CPU/PSS or per-request latency claim. Raw size/runtime may resemble prior native runs, but no new measurement is invented as a cost estimate.

## Execution and completion

Build commands/provenance are retained at `artifacts/native-frontend-2026-10-09/build-driver.sh` and `source-provenance.json`; build has completed without solver input. The real preflight uses original stream46 (prior resource-sensitive counterexample), all four paths, one repetition and separate output directory:

```bash
python3 bench/verus_native_frontend_probe.py artifacts/native-branch-2026-10-07/full/inputs --release /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/z3 --source artifacts/native-frontend-2026-10-09/z3-source --driver artifacts/native-frontend-2026-10-09/native-z3-frontend --cores 8 --repeat 1 --index 46 --out artifacts/native-frontend-2026-10-09/preflight
python3 tools/analyze_native_frontend_probe.py artifacts/native-frontend-2026-10-09/preflight
```

Preflight proves engagement/completion, not parity or hypothesis support. A completed native error/different response is a legitimate observation; a broken runner/metric is repaired under the skill's at-most-three attempts. Then full run, unchanged except removing selection and using three repetitions:

```bash
python3 bench/verus_native_frontend_probe.py artifacts/native-branch-2026-10-07/full/inputs --release /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/z3 --source artifacts/native-frontend-2026-10-09/z3-source --driver artifacts/native-frontend-2026-10-09/native-z3-frontend --cores 8 --repeat 3 --out artifacts/native-frontend-2026-10-09/full
python3 tools/analyze_native_frontend_probe.py artifacts/native-frontend-2026-10-09/full
```

Completion requires all declared cells terminal, with all outcomes preserved; invalid/missing native output prevents qualification, not matrix accounting. No process timeout replaces solver options. On interruption inspect actual process/group; retain partial data and resume the same path or record rerun of affected comparisons into a new directory, never overwrite raw results. Owned process sessions avoid affecting unrelated jobs. One fresh result reviewer recomputes raw results and independently assesses source/release/lazy/eager contrasts. No new data are interpreted before the full matrix completes.

## Interpretation and reproducibility

Target is a bootstrap constructor/qualification table in the research record, not a final paper speed figure. Matching lazy/source/release with eager differences supports a concrete fresh frontend and a local causal boundary; matching all four qualifies only the tested frontend and rejects the predicted construction effect here. Source/release disagreement leaves original-executable qualification unresolved even if lazy/source match. Lazy/source disagreement rejects wrapper qualification. Mixed differences or unstable repetitions remain explicit; no result validates fork safety, native candidate sharing, end-to-end service benefit or GPU checking.

Binary/source/compiler identities and original stream hashes are mandatory ordinary provenance. Analysis runs on raw output files and preserves per-input comparisons with each reference plus eager-versus-lazy. This is supporting bootstrap evidence from an inspected fixed cohort, not fresh frozen-version final RQ evidence. All four RQs remain open.
