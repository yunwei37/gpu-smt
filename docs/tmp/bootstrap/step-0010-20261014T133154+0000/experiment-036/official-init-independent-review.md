# Independent result audit: official full Init setup (E036)

Observed 2026-10-16 UTC. Reviewer is a fresh native child reviewer, independent of root implementation and the earlier E036 plan/support reviews. This is one source/raw-grounded result audit of the completed **official full Init setup observation**. It is not a new plan-admission round, GPU experiment, completed three-corpus result, or whole-paper review. I made no implementation, build, benchmark, GPU, Git, or agent changes.

## Disposition

**Accept the raw population, attribution, and narrow diagnostic conclusion; do not continue the unchanged eager bridge plus frozen interpreter into a GPU backend on the strength of this result.** The official benchmark input path is now executable, the original native checker accepts the whole input, and the support join is real rather than another descriptor-count proxy. However, the current host-positive set captures only **4.8413% of observed native body-thread CPU**, despite covering **40.6072% of body declarations**. Packing all reachable terms already costs **621.9 ms**, while all observed native CPU attributed to those prospective positives sums to only **337.6 ms**. Those two different timing quantities are not a strict impossibility proof, but they are a strongly unfavorable cost indication for this exact eager design.

The native body checks still all execute and supply the final result. The 7.930 s diagnostic is therefore **not the implementation of a hybrid accelerated verifier** and its slowdown must not be described as measured GPU slowdown. Conversely, its positives cannot be called certified replacement coverage. Root retains scientific disposition and route choice. All four original RQs, the paper's system contribution, and OSDI readiness remain open.

## Input identity and complete population

I inspected the actual retained upstream sources under `/tmp/gpu-smt-arena-native-stages-20261016/arena-source`: `tests/init.yaml`, `tests/init_module.lean`, `tests/lean-toolchain`, `schemas/test.json`, and the relevant `lka.py` source path, together with acquisition, SDK download/extraction/version, build command and terminal records. The official YAML declares `leanfile: tests/init_module.lean`, expected acceptance, performance comparison enabled and skip-on-CI true. The module is simply `import Init`; toolchain is `leanprover/lean4:v4.34.1`. The schema recognizes that source-native leanfile path. The upstream helper builds module Test and runs lean4export; there is no project-generated substitute benchmark.

The recorded actual command is upstream `lka.py build-test init`, exit 0, 18.1679 s input construction. The downloaded official Linux SDK is 580,432,872 bytes and reports Lean 4.34.1 / commit `5045d0056413266e57c625dcd7c365b10e377c52`. I read the generated full NDJSON once, independently counting **347,555,345 bytes and 6,487,065 lines**. Its header reports exporter/format 3.1.0 and the same Lean identity. It contains 6,132,277 expression records and direct body-record counts of **15,227 definitions, 42,070 theorems and 247 opaques**, totaling 57,544 bodies.

The retained upstream results snapshot has git revision `315f24d4cd90d70854df862597cc152c1b211898`, timestamp 2026-10-15 17:30:35 UTC and round null. Its Init size, line count, exporter version and Lean version/hash match the generated input. This is persuasive workload identity at the stated source/metadata level, **not a byte-identity claim against an unavailable archived export**. In particular, the upstream helper clones lean4export master. The actual resolved local exporter commit is independently confirmed as `df81913eee5519d5a88ae5b0fd701b5298cc29ab`; the snapshot metadata does not identify its exporter commit. Preserve that distinction in reproducibility documentation. No additional digest gate was introduced.

Primary upstream paths: [Init YAML](https://github.com/leanprover/lean-kernel-arena/blob/315f24d4cd90d70854df862597cc152c1b211898/tests/init.yaml), [module](https://github.com/leanprover/lean-kernel-arena/blob/315f24d4cd90d70854df862597cc152c1b211898/tests/init_module.lean), [helper](https://github.com/leanprover/lean-kernel-arena/blob/315f24d4cd90d70854df862597cc152c1b211898/lka.py).

## Same-index cost join independently checked

I read all **59,626 CSV rows**, not an initial prefix, independently recomputed the aggregates, and checked that declaration indices are exactly 0 through 59,625, unique and ordered. Kind counts are:

| Kind | Rows |
| --- | ---: |
| Definition | 15,227 |
| Theorem | 42,070 |
| Opaque | 247 |
| Native-only | 2,082 |

All 57,544 body rows have positive native body-thread CPU counters; all 2,082 native-only rows have zero body counter. All 23,367 host-positive body rows have reason 0. Aggregate recomputation agrees exactly with the analysis JSON:

| Prospective host outcome | Count | Native body-thread CPU seconds |
| --- | ---: | ---: |
| Positive, reason 0 | 23,367 | 0.337581756 |
| Capacity, reason 1 | 27,378 | 5.399984143 |
| Not-equal/unsupported answer, reason 9 | 5,913 | 1.056839108 |
| Unsupported, reason 3 | 886 | 0.178601224 |
| All body rows | 57,544 | 6.973006231 |

The positive count fraction is 23,367 / 57,544 = **40.6071875%**; its body-thread CPU fraction is 337,581,756 / 6,973,006,231 = **4.8412657%**. The capacity group alone carries about **77.44%** of observed body-thread CPU, so the expensive work lies predominantly outside the current successful prospective subset. A capacity failure establishes neither successful completion at a larger capacity nor a hardware acceleration opportunity; it can also expose an inefficient evaluation/substitution strategy.

The join is grounded in the actual Rust source, not just asserted by analysis: native parser `add_declar` assigns the insertion index to the declaration's interned name; bridge declarations and CSV output iterate the same ordered native declaration map; `body_end(d.info().name.as_ref().decl_idx(), begin)` accumulates into that answer slot. The actual executed `src/e036.rs` equals the canonical `bench/lean-gpu/arena-native-bridge.rs` byte for byte when inspected. C++ uses the same query index to write answers. This supports within-process identity for the complete accepted input.

Timer scope is deliberately narrower than complete declaration checking: `check_declar_info_v` runs before `body_begin`; timed work includes body type inference, evaluating the declared type, and native definitional equality. Header/type well-formedness, universe parameter checks, theorem-Prop checks, native-only declaration checks, parsing, packaging, and final process lifetime are not all in this denominator. The timer is `CLOCK_THREAD_CPUTIME_ID`, across four native workers; its sum is **not wall time**, and must not be multiplied with separate wall fractions or older Meta captures to manufacture an Amdahl ceiling.

## Actual observed timings and comparison limits

I read terminal records, stdout/stderr and GNU time resources for all three actual successful observations:

| Path | Whole process seconds | Parse wall seconds | Native check wall seconds |
| --- | ---: | ---: | ---: |
| Original optimized native baseline | 2.249777186 | Not instrumented | Not instrumented |
| Stage-only native diagnostic | 2.167727732 | 0.332858587 | 1.827904733 |
| V3 bridge/host/native diagnostic | 7.930332960 | 0.333047594 | 1.932996241 |

All three exit 0 and print `Checked 59626 declarations with no errors`. Stage-only parse plus check is 2.160763320 s, leaving about 6.96 ms for the rest of that whole-process observation. Its check wall is about 84.32% of whole-process time: full native checking is significant on this official input. That observation does **not** transfer to the currently successful host subset, nor show that all native checking is offloadable.

The V3 stderr separately reports bridge pack **0.621891826 s**, packed arrays **126,843,428 bytes**, and host query **5.025242010 s**. Together with parse and native checking, those stages total 7.913177671 s, close to the whole-process measurement. The packed expression count matches the input's full 6,132,277 expression-record population: this is an eager whole-graph cost. The packed byte total is the listed wire arrays, not peak host memory or total GPU memory requirements. Host-side traversal maps, native arenas, worker scratch and future CUDA allocations/transfers need separate accounting.

GNU time independently supports plausible resource accounting: original baseline user/system 7.60/0.18 s and peak RSS 845,696 KiB; stage-only 7.39/0.18 s and 826,256 KiB; diagnostic 28.26/0.29 s and 914,628 KiB. These are one-run observations, not controlled estimates of steady-state throughput, isolation, significant speedup or memory savings. Run order was original then stage-only then V3; file-cache state was not randomized or reset, and scheduling/load can differ. The setup does not support claiming the 82 ms apparent stage-only advantage over the original as an improvement.

The native baseline uses the pinned optimized sokonanoda source and official-style flags `--stdin --nat-extension --string-extension --axiom-allow-all --threads 4` (plus success printing). Diagnostic builds reuse the existing Init.Prelude-trained PGO profile and target-cpu=native, rather than retraining each new binary. Build warnings explicitly discard mismatched profile counts in changed code. Instrumentation, cache history after the sequential host pass, scheduling, and native worker cache behavior can change body costs. The cost join is a good diagnosis of this actual run, not the counterfactual removal cost from an untouched optimum.

The original stage-only execute-mode failure is retained as exit **126**, stderr permission denied, and an attempt-specific terminal/resource record. The repair restores the private copied binary from mode 0644 to 0755 without changing bytes or rerunning the original baseline. Exclude that 1.49 ms failed launch from timing/acceptance aggregates. The successful stage-only run is a legitimate later observation after repairing a real setup fault, not a hidden replacement of a native rejection.

## Why these are prospective answers

The bridge and host wrapper are explicitly diagnostic: host answers are prepared first, then **every native check still runs**. No GPU is called and no host answer replaces a native result. The C++ wrapper runs the frozen closure interpreter on four host workers, with 65,536 term/environment/level entries, 8,192 frames and 2,000,000 maximum steps per active worker task; scratch is reused between tasks. The reason enumeration establishes that reason 1 means capacity, reason 9 means unsuccessful equality, and reason 3 means unsupported. Since the native checker accepts all declarations, those host failures are fallback cases here, not incorrect native input.

The positive path is also not certified native-equivalent checking. Native `check_simple_declar` establishes an ordered declaration environment limited by current name and runs complete declaration/type obligations. The packed interpreter represents only a subset of semantics and metadata, does not reproduce that ordered environment limit in the CHECK input, and a clean accepted input provides no adversarial rejection qualification. Root need not launch a correctness-only investigation to interpret the negative opportunity: keeping these results labeled prospective and retaining the native final verdict is sufficient for the present cost decision. A future replacement implementation would need appropriate semantic qualification of the actual replacement path.

## Research consequence and next boundary

This setup resolves an important prior ambiguity: **official full Init can be generated and checked now through the official path**, and inexpensive versus expensive declaration coverage can be joined on native identity. It also contradicts the tempting count-based story that roughly forty percent of declarations already offers a large accelerator opportunity.

It does not establish GPU performance, a strict upper bound, a replacement-verifier correctness result, or any source elaboration/verification speedup. Input construction took a recorded 18.17 s outside the post-export checker boundary; a future source-verification claim must include or explicitly justify reuse of that work. There is no completed CSLib/Mathlib matrix, repetition distribution or end-to-end GPU comparison.

The scientific decision should be: retain this complete negative setup result, **do not port this unchanged eager representation and frozen interpreter to GPU simply because the check phase is large**, and select a mechanism that covers the dominant paid work while avoiding the eager overhead. This is a decision boundary, not an invitation to run another standalone descriptor census or repeat the settled baseline for activity. It also does not show that GPU checking in general is unpromising: a native representation, fundamentally better evaluator/sharing or a workload with genuinely expensive supported work would be a different mechanism and must justify itself from actual complete costs.

## Evidence inspected

All paths below are relative to the existing owning repository; temporary third-party sources/input were read in place.

- This directory: `official-init-source-acquisition.json`, `official-init-build-command.json`, `official-init-build.stdout`, `official-init-build.stderr`, `official-init-build.terminal.json`, SDK download/extraction/version records, upstream-path record and official input qualification.
- This directory: all original baseline, stage-only (including failure) and V3 official-Init stdout/stderr/terminal/resource records; `stage-copy-mode-repair.json`.
- Entire `native-support-v3-official-init.csv`; `native-support-v3-official-init-analysis.json` checked by fresh independent aggregation, not accepted as authority.
- Canonical bridge, C++ host wrapper, native patch and frozen closure interpreter; actual overlaid `src/e036.rs`, main, infer, parser declaration insertion, name index and native worker/checker sources.
- Actual generated full `init.ndjson`, actual resolved lean4export git HEAD, pinned Arena `lka.py`/YAML/module/toolchain/schema, and retained published results snapshot's Init and sokonanoda metadata.
- Build command/stderr/terminal records, source-equivalence record and native PGO warning details. No new checker or accelerator execution was needed for this audit.
