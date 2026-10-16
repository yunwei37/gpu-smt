# Formal kernel benchmark and mechanism admission from primary sources

Observed 2026-10-16. This node reuses official results and pinned source. It runs no checker, dataset acquisition campaign, GPU job, new profiler or performance matrix. Its purpose is to choose a meaningful complete-checker boundary and reject weak comparisons before writing another device implementation.

## Finite source coverage

Queries: Lean Kernel Arena benchmark nanoclo GitHub GPU proof checking; Lean4 GPU kernel proof checker GPU verification. Primary reads: [official Arena repository](https://github.com/leanprover/lean-kernel-arena), [current Arena protocol/site](https://arena.lean-lang.org/), its public results.json, and pinned sokonanoda source listed below. Unopened/adjacent search hits are not novelty evidence. This finite search establishes neither absence of prior GPU checkers nor a new system contribution.

The raw public JSON was retrieved with HTTP200 and retained compressed at /workspaces/.agent-state/gpu-smt-arena-results-20261016.json.gz in the owning Workspace, outside Git. The original is4,777,222bytes; compressed512,168bytes. [Context and selected fields](official-snapshot-context.json), [18 selected result rows](official-selected-results.csv), [offline extractor](analyze-official-arena-snapshot.py), [actual command](analysis-command.json) and [log](analysis.log) make the selection reproducible. Full third-party descriptions/stack traces are not republished here.

## Official boundary and facts

The pinned running snapshot is Arena315f24d4, generated2026-10-15T17:30:35Z:27checkers,234tests,6318results. It is not a closed round. The source framework checks exported proof objects, with accept/reject/decline/error outcomes and real-world plus adversarial tests. The advertised small downloadable test pack excludes large corpora. Official source: [protocol](https://github.com/leanprover/lean-kernel-arena).

The mathlib input is6,184,415,052bytes, Lean4.34.1, lean4export3.1.0. Its published wall seconds are:

| Checker | Wall seconds | Result |
|---|---:|---|
| official | 3995.026 | accepted |
| sokonanoda | 68.654 | accepted |
| mathgraph | 185.046 | accepted |
| nanoclo | 335.118 | accepted |
| parse-only | 141.992 | accepted |
| nanoclo-fortran | 625.118 | rejected, incorrect |

Source: [official raw results](https://arena.lean-lang.org/results.json). These are third-party measurements. The site displays instruction-derived virtual CPU at6.0Ginstr/s, separately from measured wall time; for mathlib official/sokonanoda virtual seconds are1935.511/81.722. Use one pinned snapshot and the actual metric rather than mixing page/round values. Source: [performance/round protocol](https://arena.lean-lang.org/).

## What the facts change, and what they do not

This is a formal standardized full-checker protocol, not a proxy metadata kernel. A GPU implementation seeking a benefit at this boundary must face the fastest compatible complete CPU mechanism and its actual configuration. Comparison only to the much slower official implementation would not settle RQ4's strongest-CPU question.

The official metadata gives sokonanoda a four-thread command and PGO/native-target build; mathgraph uses two threads and a similar optimized build; nanoclo uses four. These configurations already compete using parallelism, caching and optimized representation. A matched local performance claim must state CPU eligibility, build, input/version, device ownership and complete boundaries. The published wall differences do not isolate algorithms, thread count or compiler effects. No ratio from this table is a project gain or GPU upper bound.

The Fortran mathlib row is incorrect in this snapshot, so that row's time cannot support a correct full-checking performance comparison. Retain its coverage fact rather than selecting its timing as a convenient baseline. Other error/decline cases remain in the extracted all-test coverage counts; no checker is called universally sound/complete from accepted mathlib alone.

Parse-only is a control, not a competing proof checker. Its accepted valid input does not establish verification. The official parser and the optimized Rust parsers differ: subtracting the official parse-only time from another checker's full time would be invalid. The faster complete Rust checker even finishes before that different parser control. The raw fields remain separate rather than producing a fabricated checking fraction.

This boundary begins after proof export. It cannot establish a speedup of candidate source elaboration/verification without accounting for export and comparing at that larger boundary. It uses newer versions than the current producer4.27 source campaigns. No existing CPU percentage or gain transfers across those routes. Invalid E018 source/export integration remains closed; this node does not repair or resurrect it.

## Pinned architecture and a concrete differentiation test

Source reads use sokonanoda7645b1e1fcacfe410c99141f1234381d995b325d, the actual published checker revision:

- [main.rs](https://github.com/intgrah/sokonanoda/blob/7645b1e1fcacfe410c99141f1234381d995b325d/src/main.rs): parsing precedes declaration checking; a native same-checker parse-only branch exists. This offers a meaningful component control if a future admitted mechanism needs it; it is not a reason to run another generic profiler now.
- [tc.rs](https://github.com/intgrah/sokonanoda/blob/7645b1e1fcacfe410c99141f1234381d995b325d/src/checker/tc.rs), especially140–200 and215–261: native threads already claim declaration chunks and maintain per-session local caches/arenas, while checking against the published environment.
- [context.rs](https://github.com/intgrah/sokonanoda/blob/7645b1e1fcacfe410c99141f1234381d995b325d/src/checker/context.rs): exported terms/declarations and local typechecking contexts/caches are distinct structures.
- [eval.rs](https://github.com/intgrah/sokonanoda/blob/7645b1e1fcacfe410c99141f1234381d995b325d/src/checker/eval.rs) and [conv.rs](https://github.com/intgrah/sokonanoda/blob/7645b1e1fcacfe410c99141f1234381d995b325d/src/checker/conv.rs): conversion is closure-based and intertwined with reduction/type contexts. Moving integer arrays or adding a work queue would not alone distinguish a new checker from this established CPU design.

Root inference: a potentially consequential device proposal must replace a substantial part of actual complete declaration checking, retain the required context/rules, and explain why its GPU execution handles irregular reduction and local cache/state costs better than this already-parallel CPU alternative. An immutable exported environment plus private per-declaration work gives a more concrete candidate boundary than raw Meta-entry offered pairs, but that organizational boundary is prior art. A device-resident environment, explicit closure/state execution and real declaration batching are a candidate architecture, not an implemented or novel system established by this source read.

The engineering/experiment question is whether a complete supported execution algorithm can exploit that boundary after parser/representation/transfer/fallback costs. No algorithm is admitted solely by a large corpus, many declarations or lack of a GPU entry in the visible table. Do not start by implementing another scalar reduction or a metadata-only benchmark and call it complete checking.

## Disposition and handoff

[E035 fresh review and root disposition](../experiment-035/disposition.md) close the independent child-cost profiler before execution. Retain its missing quantity without inventing a global closed-operand bound. Source/algorithm admission comes next for a meaningful complete mechanism; any necessary diagnostic belongs inside that experiment. Existing formal source captures continue unchanged and are collected on completion.

This node strengthens formal-workload/competitor selection and the source-level differentiation test. It supplies no new measured RQ answer, GPU engagement or OSDI-level contribution. RQ1–RQ3's real multi-context native service, strongest warm/snapshot/cache comparison and behavior/resource/cancellation evidence remain required; full post-export checking cannot silently replace those promises. Canonical paper/literature/evaluation integration remains assigned to the existing OMP owners, while root retains native implementation and scientific disposition.
