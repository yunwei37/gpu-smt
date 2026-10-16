# E036 first support/cost diagnostic review

Observed 2026-10-16T11:41:07Z. Reviewer: native Codex `/root/complete_declaration_plan_review`, follow-up 1 to the existing E036 plan review, not a fresh admission round, completed experiment review or full-paper audit. Root retains implementation and scientific disposition. Only this report was written; no build/rerun, benchmark, GPU call, source edit, Git mutation, model/runtime change or new experiment was performed.

## Verdict and scope

**The recorded V1 setup is a real executed dependency with reproducible CSV arithmetic and credible native-declaration indexing. It is not qualified replacement support, GPU engagement, a complete preflight, or a paper performance result.** Native checks still execute on every declaration and supply both successful final decisions. The current retained-prefix evidence is unfavorable for implementing a GPU backend around this exact eager representation and V1 positive set. It does not establish a complete-declaration mechanism ceiling, because ordinary already-supported constructs are deliberately omitted or misencoded by V1.

Source inspection supports a bounded representation correction within the existing mechanism: native lets retain the binder for either nondep hint; existing projection tag10 can represent the native construct within the frozen engine's documented restricted projection semantics; K metadata belongs in bit3 rather than the unsafe bit0. Singleton constructor metadata must remain truthful. These are findings about existing source and representability. **No revised bridge, new support fraction, replacement correctness or future execution is certified here.** Root reported a forthcoming V2; that report does not substitute for inspecting its final source and raw outputs.

## Material examined

Read `bench/lean-gpu/arena-native-bridge.rs`, `arena-native-support.cpp`, `arena-native-support.patch`, the frozen `closure-checker.cu`, both raw native-support CSVs, both analysis JSONs, terminal/stdout/stderr/resource records, native stage-only patch/results/observations/inputs/arithmetic, and stage/support build commands and compiler output. At initial inspection the installed `/tmp/gpu-smt-arena-native-stages-20261016/source/src/e036.rs` matched the repository bridge byte-for-byte; bench closure source matched the frozen runtime source. Root subsequently preserved that executed bridge as [native-support-v1-executed-bridge.rs](native-support-v1-executed-bridge.rs), 10,875 bytes, containing the reviewed omitted Let/Proj and K-bit mapping. This report describes that V1, not a concurrently changing current bench file.

Also inspected pinned native parser declaration-index assignment, pointer Eq/Hash definitions, declaration environment cutoff, type/body checking, `RecursorData::major_idx`, native Let inference/evaluation and actual two input headers. Workspace branch was `main`. No native implementation was changed by this reviewer.

## Independent recomputation and completed observations

Recomputed directly from each complete CSV:

| V1 observation | Prelude4.34.1 | Retained Mathlib4.9 prefix |
|---|---:|---:|
| Declaration rows | 2,106 | 29,709 |
| Definition/theorem/opaque bodies | 1,691 | 27,579 |
| Prospective host positives | 867 | 2,888 |
| Positive share of body count | 51.2714% | 10.4717% |
| Summed observed body-thread CPU, seconds | 0.031501609 | 2.073336152 |
| Same sum for prospective positives, seconds | 0.008178846 | 0.032142881 |
| Positive fraction of this body-thread CPU | 25.963264% | 1.550298% |
| Native graph packing wall, seconds | 0.004011875 | 0.301257487 |
| Host-query wall, seconds | 0.009594500 | 0.153725342 |
| Native check wall after host diagnostic, seconds | 0.017098268 | 0.705567033 |
| Whole support-diagnostic process, seconds | 0.044495391 | 2.060378365 |

Rows use every declaration index exactly once in contiguous order. Every recorded body has a positive clock value, native-only rows have zero body clock, and every prospective positive has reason0. Prelude reason counts are unsupported3=473, positive0=867, unsafe6=21, undecided equality9=329, capacity1=1. Prefix counts are3=21,079;0=2,888;6=245;9=3,360;1=7. Maximum recorded interpreter steps are23,312 and126,670 respectively. Both native processes report exit0 and complete declaration-count success messages. This independently validates these arithmetic/coverage facts, not the logical validity of every prospective host answer.

Stage-only observations are a different earlier diagnostic build: Prelude whole0.037279730s/parse0.005710508s/check0.018396510s; prefix whole1.569244451s/parse0.908617990s/check0.654684683s. Its quoted fixed-other-cost erasure calculations, about1.9742x and1.71585x, reconcile arithmetically. They erase the entire measured check stage, including native-only work, so they are conditional scenarios rather than attainable supported GPU gain. Do not multiply those check/whole ratios by V1 CPU shares or subtract separate parse-only clocks to invent an end-to-end bound.

## Index and representation assessment

The index mapping is credible. Native parser `add_declar` assigns each insertion index to its name; the bridge enumerates that same ordered declaration map; native timing uses `decl_idx`; CSV writing enumerates the same map again. The complete nonzero body clocks and contiguous rows corroborate that path. No string-name join or cross-version source-ID heuristic is used for per-declaration cost association.

Typed expression/level IDs are native pointer-keyed deduplication maps with stable buffers during the joined host query. The iterative worklist visits registered roots and discovered children; declaration types/values and recursor RHS roots are seeded. Parent-before-child numeric order is permissible for the frozen engine's direct array lookup and does not depend on the old Python converter's topological-ID validation. Universe parameters and level-parameter names share one native-name mapping. Const/rule constructors use native declaration lookup; parameter/motive/minor/index counts match the frozen recursor major-position formula. This is materially more credible than reparsing and relabeling the old NDJSON adapter.

It remains an incomplete diagnostic representation:

- **Nondependent Let:** V1 maps every `nondep=true` Let to default tag0. Native inference and evaluation ignore that hint operationally and still extend the binder environment; the frozen engine already has tag7 binder handling. Thus this V1 exclusion is not evidence that the frozen algorithm intrinsically lacks that native construct. A faithful mapping still needs its final source and results examined.
- **Projection:** V1 maps every native Proj to tag0, despite existing frozen tag10. Enabling it does not give arbitrary projection support: frozen inference restricts to a genuine singleton constructor, no indices/recursive or reflexive flag, suitable non-Prop type, and required field/parameter conditions. V1 currently chooses `all_ctor_names.first()` even for nonsingletons. That field must not be treated as a singleton witness when projection is enabled.
- **K metadata:** V1 writes `u32::from(is_k)` to flags, setting bit0. Frozen constant inference/reduction interprets bit0 as unsafe; the frozen adapter uses bit3 for K. Therefore at least some unsafe6 classifications can arise from this representation mismatch. Correcting the bit does not implement absent K reduction; stuck/undecided fallback must remain conservative.
- Oversized literals, universe-normalization incompleteness, restricted recursor/projection/quotient/string behavior and finite interpreter arenas continue to limit prospective support. Reason3 or9 aggregates cannot identify which omitted construct caused all affected cost, nor promise how much a mapping repair recovers.

Before any native replacement, preserve more than accepted-corpus compatibility: the new bridge bypasses old converter validation, and the frozen engine alone does not enforce the native declaration-visibility cutoff or duplicate-uparam policy on all inputs. Native full checks currently retain those obligations. Do not begin skipping them because accepted inputs produced host positives. Parser acceptance is not complete declaration validation; final native acceptance and agreement on valid bodies are not adversarial soundness qualification.

## What the timing measures

The body clock begins **after** `check_declar_info_v`, then covers body inference with `Check`, evaluation of declared type and final conversion. It excludes declaration-type well-formedness, universe checks preceding the timer, all native-only declaration checking, parse, packing, host querying, output and teardown. It is a per-current-worker `CLOCK_THREAD_CPUTIME_ID` interval, not wall latency or total process CPU. The lookup/end-clock path enters the interval; clock/atomic calls and instrumentation also perturb the whole run. A panic before `body_end` would omit that body interval, so rejected/failed future inputs require explicit censoring. The two current native-accepted observations show no zero body clocks; this does not solve censoring generically.

Summing across four threads is valid for recorded body CPU but cannot be equated to check makespan. Cached work shared across declarations makes removal nonadditive: skipping positive bodies can remove cache priming, change subsequent work, scheduling and memory. The host diagnostic itself first traverses/allocates the whole graph and executes four C++ workers before native checking, changing cache/memory/CPU conditions. Thus these are observed costs in the instrumented diagnostic condition, not unmodified baseline residuals or a guaranteed removable fraction.

Compiler output confirms reused PGO is not fully matched after instrumentation. The support build discards up to8,027 profile counts for `check_declar_with` and72 for main, plus zero-count mismatches; stage-only had its separate changed-main warning. The C++ host library is `g++ -O3` and not the exact Rust PGO competitor. This is acceptable for diagnostic evidence, but precludes promoting the support binary to the fully qualified official optimized baseline or attributing cross-build differences to bridge overhead alone. The unchanged binary path was rebuilt: reproducing the earlier stage measurement requires its recorded earlier patch/build, not merely rerunning today's binary with the same filename.

On the retained prefix, packing0.301257s alone materially exceeds the total0.032143s CPU observed in prospective-positive bodies, before device/JIT/transfers/fallback. Host querying adds0.153725s and does not replace any native work. This is strong adverse engineering evidence for this exact V1 cold eager bridge/positive set; high positive counts would not rescue it. CPU-sum versus wall and cache/profile caveats prevent turning the comparison into a rigorous universal upper bound. Neither one setup repetition nor this older prefix forecasts the full official4.34 Mathlib outcome.

## Research judgment and return

Run status: **valid completed V1 setup observations with explicit methodological limits; E036 full experiment remains incomplete**.

Tested heterogeneous-acceleration hypothesis: **not tested**. No GPU execution or native replacement occurred; Init.Prelude is not the full Init preflight, and the retained producer4.9 prepared prefix is not the declared official large Mathlib workload.

Research value: **dependency-only**. Native graph traversal, bounded per-worker host scratch and real associated native costs are useful setup. Counts/build completion are not scientific contributions. V1 cannot justify a complete-kernel negative, a useful GPU frontier, or a source-verification/service speedup.

Paper impact: **current representation/workload boundary**; no RQ completion or direct thesis challenge. Lean-first, SMT/service/four-RQ and full-paper objectives remain unchanged.

Next owner contract: root may use the source-grounded Let/Proj/K/singleton mapping findings to assess the faithful representation already intended by E036, while preserving V1 source/raw and separately identifying any revised source/results. Do not interpret low V1 coverage as an immutable engine ceiling or claim repaired coverage before measuring it. The current V1 costs do not support GPU-backend investment. Any continuation decision must come from the actual revised useful-cost/whole-cost evidence and root's scientific judgment, retaining native checks and all unsupported outcomes until real replacement qualification. No additional experiment, baseline family, numeric quota, control schema, authority gate or implementation task is created by this review.


## V3 follow-up — second and final follow-up of this plan-review round

Observed 2026-10-16T11:44:09Z. This section preserves all preceding V1 findings and reviews the actual revised diagnostic, not a predicted V2/V3 outcome. Reviewer remains native Codex `/root/complete_declaration_plan_review`. No new admission round, build/rerun, GPU call, source edit, Git action or extra experiment was performed. Only this existing review file was appended.

### Source and execution identity

Read the complete latest canonical `bench/lean-gpu/arena-native-bridge.rs`, both `native-support-v3-{prelude,mathlib49-prefix}` raw CSVs, analysis JSONs, stderr/stdout, terminal records and `/usr/bin/time` resources. Rechecked C++ worker source and current installed native module. The installed `src/e036.rs` equals the canonical bridge byte-for-byte at inspection, and canonical `closure-checker.cu` equals the frozen runtime engine. Current generic `native-support-rust-build-command.json`/terminal/stderr identify the successful final build at11:41:12–11:41:34Z; the explicitly saved v1 and v2 build records distinguish earlier source revisions. V2's retained build-only bridge still has earlier metadata encodings and must not be mistaken for the V3 executed source.

V3 maps every native Let to tag7 with its binder type/value/body, matching the previously inspected native inference/evaluation rule that always extends the binder environment, regardless of nondep hint. Native Proj becomes existing tag10 with actual inductive declaration ID, field index and structure. Recursor K uses bit3 (`is_k * 8`), and the singleton constructor field is populated only when the native constructor list has length1. These resolve the specific V1 exclusions/misencoding reviewed above. No new evaluator semantic implementation was required for those representation corrections, and the interpreter/worker defaults remain cap65,536, frames8,192 and steps2,000,000.

This validates those mapping changes, not unrestricted projection/K/kernel support. Existing frozen projection restrictions, missing K reduction and other partial semantic limits remain. The source comment “Existing projection checker not admitted here” is stale relative to actual tag10 dispatch; the executable mapping and documented restricted scope govern this diagnosis. All native declaration checks still execute and supply the final decision. No host positive bypasses native checks. The prior visibility, duplicate-uparam, rejected-input/censoring and accepted-only qualification limitations remain before any replacement use.

### Independently reconciled V3 results

| V3 observation | Prelude4.34.1 | Retained Mathlib4.9 prefix |
|---|---:|---:|
| Complete declaration rows | 2,106 | 29,709 |
| Body rows | 1,691 | 27,579 |
| Prospective host positives | 1,291 | 13,935 |
| Positive fraction of body count | 76.345358% | 50.527575% |
| Observed summed native body-thread CPU, seconds | 0.039453298 | 2.068800671 |
| Positive bodies' share, seconds | 0.018161515 | 0.300677258 |
| Positive fraction of body-thread CPU | 46.032945% | 14.533892% |
| Packed expression nodes | 54,799 | 2,832,318 |
| Packed table bytes | 1,258,640 | 59,197,140 |
| Packing wall, seconds | 0.003991142 | 0.283193423 |
| Host-query wall, seconds | 0.023046758 | 2.010716532 |
| Native check wall after host diagnostic, seconds | 0.024094568 | 0.699251402 |
| Whole diagnostic process, seconds | 0.062716576 | 3.892510154 |

Raw CSV recomputation matches the supplied analysis for both inputs. Each index again appears exactly once, every body has a nonzero native clock, all native-only clocks are zero, and all positive answers have reason0. Both native runs exit0 with complete expected declaration-count success messages. All V1 positives remain V3 positives at the same declaration indices: Prelude gains424 and prefix gains11,047 prospective positives; none is lost. This supports an actual representation-coverage improvement, not a measured GPU improvement or independently validated soundness.

Prelude reason counts are positive0=1,291, undecided equality9=345, capacity1=34 and unsupported3=21. Prefix counts are0=13,935;9=5,152;1=8,190;3=302. No unsafe6 remains in either observation. The maximum interpreter steps are154,062 and157,601, below the configured step limit; reason1 denotes one of the frozen arena capacities, not a measured two-million-step exhaustion or a native failure. The CSV lacks per-arena peaks, so it does not identify which term/environment/level capacity exhausted.

Independent grouping of the prefix CSV by host reason assigns native body-thread CPU as follows: positives0.300677258s; capacity1.053321846s; undecided equality0.711195981s; other unsupported0.003605586s. Thus the larger positive count still misses most observed paid native body work. Capacity-limited bodies are operationally significant; they cannot be called semantically unsupported, silently excluded, or assumed recoverable cheaply by increasing arenas. Likewise reason9 is undecided in this partial algorithm, not a native invalid-proof judgment. This observation does not require another tuning matrix or impose a new resource setting.

### Interpretation and owner return

Root's stated unfavorable interpretation is warranted for the present design. On the retained prefix, current cold eager packing already costs0.283193423s versus0.300677258s total observed native CPU in prospective-positive bodies, before device initialization, transfer, execution, synchronization or native fallback. Current host evaluation costs a further2.010716532s while every native check remains. The currently observed bridge/host path supplies no convincing complete-cost case for immediate GPU-backend development. The higher count alone is insufficient.

That comparison remains diagnostic. Packing is wall time and the prospective amount is CPU summed across four native workers; they are different units/boundaries. Removing declarations changes native session-cache reuse and scheduling, while the preceding graph traversal/host query changes cache/allocation/CPU conditions. Current build stderr still reports the PGO CFG mismatches, including up to8,027 discarded counts for `check_declar_with` and72 for main. One observation per revision on shared resources supplies no uncertainty interval or clean cross-revision causal timing estimate. In particular, do not multiply the14.53% by a separately captured check-stage fraction, subtract it from whole wall, or claim a strict speedup ceiling.

V3 materially corrects V1's underrepresentation; the remaining unfavorable costs therefore have a stronger implementation-specific basis. They still do not establish GPU impossibility, a fundamental full-kernel support limit, or results on the declared official large Init/CSLib/Mathlib4.34 workloads. The retained159MB producer4.9 prepared prefix and small official Prelude keep their original setup-only identities. The 59.2MB number counts flat tables, not total host peak memory, device/context memory or simultaneous corpus storage. Reported RSS is a single diagnostic observation, not a replicated resource frontier.

Run status: **completed V3 host/native diagnostic; E036 integrated device experiment remains incomplete**. Heterogeneous speedup: **not tested**. Research value: **dependency-only**. Paper impact: **current representation/workload/cost boundary**, with no RQ completion or direct thesis challenge.

Root may close/defer this current eager bridge/interpreter constructor on these adverse actual costs while retaining the source/results and broader uncertainty. These results do not independently admit a GPU backend, larger arenas, selective/lazy representation, a new experiment or another review round. Any different implementation route requires its own concrete consequential rationale under the existing scientific scope, rather than promoting counts or weakening costs. Root retains scientific disposition; all Lean-first/SMT/service/four-RQ/paper obligations remain unchanged.
