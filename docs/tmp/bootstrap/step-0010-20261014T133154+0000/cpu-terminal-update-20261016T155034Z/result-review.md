# Independent terminal CPU result review

Reviewed 2026-10-16 in the owning gpu-smt Workspace. Scope: the original HiGHS 12 conditions, stock-products 8 conditions, and the third GC/native primary pair. No experiments/builds, active acquisition inspection, implementation changes, OMP edits or Git operations were performed. This review does not complete GC profiles, Full/Fast, a GPU comparison or the paper's RQs.

## Evidence and independent method

Read docs/user-instruction.md, this node's admission.md, original highs-native-cpu-plan.md and stock-products-plan.md, run-highs-native-cpu.py, run-stock-products.py, run-gc-repaired-header.py, analyze-native-oracle.py and ResourceCapture. Read all 22 scoped terminal files, commands, input/results and original HTTP response members from original ZIPs. For each cell independently verified exact input.jsonl byte equality against artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl; 29,750 unique ordinals; matching proof IDs/source indices in original submission order; and recomputed basic counts against terminal counts. No source/order issues. Responses finish out of order: ordinals, not completion order, establish submitted population identity.

Independent whole effects use terminal whole_seconds directly; response comparisons retain the whole HTTP envelope and remove only results[*].response.time, matching pinned backward.py's extend(check_response.response, time=check_response.time). No internal identifiers, failures, messages or nested timing fields were normalized. All primary and profile difference counts agree with root's reused-primary-evidence.json, gc-third-primary-pair.json and complete-profile-analysis.json. Whole clocks, counts, source checks and same-group commands agree. Historical latency quantile conventions differ between existing analyzers (round versus floor index); no wall conclusion relies on inter-analyzer percentile comparisons.

The original archives stay authoritative. Under artifacts/lean-modern-native-compilation-2026-10-14/, groups are highs-native-cpu-full1, stock-products-full1, full-gc2; each label has its .terminal.json and .zip. This node's root source/analysis/execution receipts are an offline publication step, not additional native trials.

## HiGHS: original 12 conditions

Every cell returned 29,750 with failure=null. Primary order is tiered/hybrid/highs; highs/tiered/hybrid; hybrid/highs/tiered. Profiles are separate observations, not a fourth primary repetition. C/R/O = complete/rejected/operational.

| Condition | Whole seconds | C/R/O | Status |
|---|---:|---|---|
| rep0 tiered | 9784.204512 | 27320/2376/54 | terminal complete |
| rep0 hybrid | 10822.595804 | 27321/2375/54 | terminal complete |
| rep0 highs | 10941.698500 | 27316/2377/57 | terminal complete |
| rep1 tiered | 13778.600431 | 27320/2375/55 | terminal complete |
| rep1 hybrid | 14498.522869 | 27319/2376/55 | terminal complete |
| rep1 highs | 12200.736637 | 27319/2377/54 | terminal complete |
| rep2 tiered | 11048.572191 | 27320/2376/54 | terminal complete |
| rep2 hybrid | 13637.502772 | 27320/2376/54 | terminal complete |
| rep2 highs | 13420.390541 | 27319/2377/54 | terminal complete |
| profile tiered | 10902.364347 | 27319/2376/55 | terminal complete |
| profile hybrid | 10428.177846 | 27320/2376/54 | terminal complete |
| profile highs | 10997.022017 | 27302/2377/71 | terminal complete |

Positive change below means longer than same-block tiered.

| Primary rep | hybrid change | HiGHS change | hybrid native/basic differences | HiGHS native/basic differences |
|---|---:|---:|---:|---:|
| 0 | +10.612935% | +11.830231% | 181/4 | 1301/8 |
| 1 | +5.224932% | -11.451553% | 187/10 | 1305/12 |
| 2 | +23.432264% | +21.467193% | 187/10 | 1306/13 |

Hypothesis: external sparse support plus exact repair can improve complete Lean verification versus native tiered/hybrid. Result: hybrid is longer in all three matched blocks; HiGHS is mixed, with one lower and two higher whole observations. Mean changes +13.090044% and +7.281957% are descriptive averages of three block ratios, not confidence intervals or causal estimates. Neither result selects an unqualified universally faster replacement.

Research value: this closes the originally admitted arithmetic comparison and documents the real competitor frontier, with unfavorable outcomes preserved. Paper impact: supporting CPU evidence only; not a novel system contribution or GPU benefit. Next decision: retain tiered/hybrid/HiGHS's actual complete measurements and outcome distinctions; do not promote a filtered accepted-only or single-winning-block ratio. No new matrix is required by this review.

Profiles have hybrid 186 native differences (5 operational->complete, 4 complete->operational) and HiGHS 1321 (22 complete->operational, 6 reverse, 1 complete->rejected) versus profile tiered. In particular the profile HiGHS resource/timing result cannot erase its 71 operational outcomes. Primary HiGHS has one complete->rejected change per repetition (and an operational->rejected change in rep1). These are not transparent identical-output execution claims. The difference sets are retained by the root evidence; no certificate or message variation was silently discarded.

## Stock-products: original 8 conditions

Every cell returned 29,750 with failure=null. Alternating order stock/products; products/stock; stock/products. Original solver and native library composition remain the intended comparison; product plugin setup is charged.

| Condition | Whole seconds | C/R/O | Status |
|---|---:|---|---|
| rep0 stock | 15385.790012 | 27319/2376/55 | terminal complete |
| rep0 products | 15475.962495 | 27318/2376/56 | terminal complete |
| rep1 stock | 16245.634151 | 27319/2376/55 | terminal complete |
| rep1 products | 15415.520173 | 27317/2376/57 | terminal complete |
| rep2 stock | 14942.761836 | 27319/2376/55 | terminal complete |
| rep2 products | 12805.478077 | 27319/2376/55 | terminal complete |
| profile stock | 13059.507467 | 27318/2376/56 | terminal complete |
| profile products | 9819.070867 | 27320/2376/54 | terminal complete |

Whole reductions: -0.586076%, +5.109767%, +14.303137%; descriptive mean 6.275609%, observed range [-0.586076%,14.303137%]. Native/basic differences exactly 11/11, 10/10, 10/10; these are operational<->complete transitions, not arbitrary hidden artifact equality. Profile has 8/8 differences (5 operational->complete, 3 reverse). Its 24.812855% reduction is an instrumented separate observation and cannot be pooled as primary repetition four.

Hypothesis: invocation-local product construction has a benefit independent of changing the arithmetic oracle. Result: mixed whole effect, one slight regression and two reductions; not a robust universal gain. Research value: bounds earlier composed Farkas/Fast results and establishes the actual original-solver comparison. Paper impact: supporting CPU-frontier evidence and a limitation on generality; generic application reuse is not the project's novel contribution. Next decision: preserve full repeated range/outcomes, including the negative block; no extra tiny-kernel or ad-hoc control is admitted by this review.

## GC/native third primary pair only

rep2 original 32484.597840s, compiled 13149.047983s: reduction 59.522208%. Outcomes original 27316/2376/58, compiled 27319/2376/55. Exactly 23 native/basic differences: 10 complete->operational and 13 operational->complete. Source bytes, IDs and 29,750 attempts match. This independently confirms root's third-pair arithmetic/difference set.

Run status: third primary pair terminal complete; GC's separate profiles remain unfinished and were not inspected. Hypothesis: whole-library native compilation reduces this matched service's whole work. This pair supports that measured CPU comparison; it does not justify a transparent identical-output claim or complete resource result. Paper impact: a necessary competent baseline, not an original CPU compilation contribution. Next decision: publish this completed pair now; keep unfinished profiles unfinished and the broader RQs open.

## Resource observations and measurement limits

Independently streamed all five completed resources.jsonl.gz files and recomputed sample count, incomplete-sample count, maximum sampled aggregate PSS and private bytes. Every value agrees with original resources-summary.json and root's complete-profile-analysis.json.

| Profile | Samples / incomplete | sampled PSS KiB | sampled private KiB | recorded rusage CPU seconds |
|---|---:|---:|---:|---:|
| HiGHS group tiered | 5905/28 | 7005488 | 5690872 | 10031.249406 |
| HiGHS group hybrid | 5721/22 | 7668612 | 6063376 | 8972.480160 |
| HiGHS group highs | 6582/1448 | 8723814 | 7112196 | 8861.636122 |
| Products group stock | 7947/20 | 7486707 | 5787416 | 20509.652282 |
| Products group products | 6442/22 | 8005904 | 5798272 | 11821.742785 |

CPU is ResourceCapture's delta RUSAGE_SELF+RUSAGE_CHILDREN, including observer activity; exact/exhaustive descendant coverage is not established. The summary's whole_process_tree_cpu_seconds key is not proof of such coverage. Non-atomic process-tree memory sampling misses peaks and disappearing children; PSS changes with outside shared-file mappings. HiGHS has 1448 incomplete samples out of 6582, making exact peak/saved-memory interpretations especially indefensible. These are one separate profile per method under shared background, not replicated resource effects or exclusive hardware.

Telemetry limitation: original goedel427-profile-tiered.zip member goedel427-profile-tiered/oracle.jsonl has a malformed JSON line at line 9976, uncompressed byte offset 59,498,527, 10,782 bytes; parser reports expected comma at line 2 column 1 (char 10740). Some valid telemetry integers also exceed Python's default 4300-digit conversion limit. This blocks claiming the entire route log is a complete parsed census without handling its original errors; it does not invalidate the complete native HTTP acquisition. No route/hit-rate superiority conclusion or new profiling campaign follows. Original raw bytes are retained.

## Fairness and acceptance

Within-group command fields other than method/PID are matched: HiGHS CPUs4-7, GC CPUs8-11, products CPUs0-23. All use four requests in flight with the same group's private port and recorded stock 12GiB/300s/maxpool policy. Stock-products must not be ranked numerically against four-core HiGHS/GC acquisitions or composed Farkas results. Shared background scheduling/cache/disk variability remains; alternating orders do not create random IID trials.

The whole timer includes input persistence/readiness/import/library loading, proof verification, HTTP/logging/replacement and observed shutdown/drain. Builds and post-clock ZIP are excluded. Capture deliberately terminates the completed server and waits/drains; returncode -15 is expected service termination under the same protocol, not a claimed normal natural exit of every native background task. Closed-loop request latencies are not independent offered-load queueing, and overlapping request times cannot be summed into a wall decomposition.

Disposition: accept root's completed-cell publication and the qualified negative/mixed supporting interpretations. No blocking numerical/source-population discrepancy found. Do not claim full GC profiles, Full/Fast completion, end-to-end GPU superiority, universal product benefit, transparent identical outcomes, exact CPU/peak memory or novel system contribution. No experiment restart, extra workload, matrix expansion or correctness campaign is required. The next scientific decisions should use the completed results and original full system objective.
