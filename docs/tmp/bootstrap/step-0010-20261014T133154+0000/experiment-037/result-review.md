# Independent result review: E037 completed full-Init host setup

Observed 2026-10-16 UTC. Fresh reviewer, independent of root implementation and the round-1 plan reviewer. I read the complete human-instruction file, Initial Narrative and RQ4, E037 plan/review/root disposition/source record, executed-source overlays, successful and failed build records, both completed execution records, the E036 full-Init reference and original optimized native controls. I recomputed every row of all three 59,626-row CSVs. I did not rerun a verifier, build, launch a GPU, change implementation or OMP files, publish Git, or poll an unfinished acquisition.

## Five judgments

- **Run status: valid** for the two completed, instrumented host-setup observations and their within-input attribution. The planned heterogeneous preflight and three-corpus matrix remain incomplete and unexecuted here.
- **Tested hypothesis: contradicted at the admitted host-setup boundary on full Init.** Canonical state improves prospective support modestly, but the new supported paid-work fraction remains small and the computational overhead grows substantially. The complete GPU superiority relation is **inconclusive**, since no GPU or qualified replacement executed.
- **Research value: supporting**, specifically a negative mechanism-selection result within RQ4. Successful compilation/input readiness alone is dependency-only; the actual supported-work/cost and ablation observations add the useful evidence.
- **Paper impact: mechanism or workload boundary.** This does not directly challenge the complete original prepared-state/service thesis or answer all of RQ4.
- **Next paper decision:** retain this implementation and all negative evidence, and decline an unchanged GPU port based on declaration counts. A continuation needs a different credible paid-work/whole-cost case; another narrow kernel or a larger-arena grid does not follow from this result. Root retains route disposition.

## Complete populations and independent arithmetic

The actual retained input has 347,555,345 bytes; its header reports lean4export/format 3.1.0 and Lean 4.34.1 / 5045d0056413266e57c625dcd7c365b10e377c52. Its official construction and complete source-input audit are retained in E036. Both E037 commands consume that same actual full Init path. This is not the Prelude fixture, historical Mathlib prefix, source-attempt population, or a generated toy.

All three CSVs contain exactly 59,626 unique ordered indices, 0–59,625. Every same-index kind agrees across them: 15,227 definitions, 42,070 theorems, 247 opaques, and 2,082 native-only declarations. All 57,544 body rows have strictly positive native body-thread CPU; all native-only rows have zero. In every CSV, host_positive is binary and is true exactly when host_reason is zero.

For a comparison unaffected by changing native timing after the host pass, I independently joined both E037 outcomes onto the **fixed E036 per-declaration body CPU weights**, asserting index and kind identity. The common denominator is 6,973,006,231 ns:

| Condition | Positive bodies | Positive body-count fraction | Fixed-reference positive CPU ns | Fixed-reference positive CPU fraction |
| --- | ---: | ---: | ---: | ---: |
| Frozen E036 | 23,367 | 40.6072% | 337,581,756 | 4.8412657% |
| E037 canonical computation off | 23,367 | 40.6072% | 337,581,756 | 4.8412657% |
| E037 canonical computation on | 25,314 | 43.9907% | 437,432,238 | 6.2732231% |

Canonical-off reproduces every frozen positive and reason. Canonical-on gains 1,947 positives and loses none; every gained positive was previously capacity-exhausted. Those gains carry 99,850,482 ns, only 1.8491% of the old capacity group's recorded CPU. Other transitions are capacity→not-equal 595, capacity→unsupported 50, and unsupported→capacity 2. Their outcomes were retained rather than excluded.

| Body reason | Canonical-on bodies | Fixed-reference corresponding CPU ns |
| --- | ---: | ---: |
| Positive, 0 | 25,314 | 437,432,238 |
| Capacity, 1 | 24,788 | 5,113,536,791 |
| Not-equal/undecided, 9 | 6,508 | 1,239,933,251 |
| Unsupported, 3 | 934 | 182,103,951 |

Capacity still carries 73.3333% of the fixed-reference body CPU. All these inputs are accepted by the native checker; unsuccessful host answers mean prospective fallback, not bad native proofs. The new result supports neither a large paid-work coverage claim nor the inference that resolving some allocation failures captures their dominant native cost.

The root fixed-reference-opportunity.json agrees with these independently computed integer sums and transitions. Its host_terms/envs “median” values 12,110/1,497 are upper-middle order statistics. Conventional even-population medians over all body rows are **12,109 / 1,496.5**. State that convention or correct those two labels; this has no effect on the scientific decision. Canonical-on maxima are terms 65,536, envs 33,995, levels 148 and frames 852; nearest upper index p95 values are 65,536, 8,638, 18 and 172. Canonical-off maxima are 65,536, 65,536, 145 and 506. Maximum steps are 149,918 on and 171,465 off, below the existing two-million allowance.

Own-run body CPU sums are 5.308012674 s on and 5.423120703 s off; their own-run positive fractions are 6.5498% and 5.1113%. These differ from the fixed-reference quantities and must not silently replace them. Native cache state, instrumentation, worker assignment and scheduling make these attribution observations, not marginal saved time. The timer starts after check_declar_info_v and excludes header/type/universe/native-only obligations. Summed worker CPU is not wall time and supplies no rigorous Amdahl ceiling.

## Actual complete costs and causal limits

Both E037 processes exit zero and print “Checked 59626 declarations with no errors”. Both use the same input and four-thread diagnostic binary with --stdin --nat-extension --string-extension --axiom-allow-all --threads 4 --print-success-message. Full process timing includes all host support work, native checking, CSV emission and cleanup.

| Observed path | Whole seconds | Parse seconds | Finalize / eager packing seconds | Host query seconds | Native check seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| E036 frozen eager diagnostic | 7.930333 | 0.333048 | 0.621892 | 5.025242 | 1.932996 |
| E037 canonical off, fused parse | 9.288275 | 0.949055 | 0.022506 | 6.799025 | 1.497961 |
| E037 canonical on, fused parse | 27.950997 | 1.482948 | 0.104074 | 24.874817 | 1.467680 |

The on/off host-pass ratio is 3.6586 and whole-process ratio 3.0093 for these observations. They are not replicated effect estimates. Canonical-on user/system CPU is 105.96/0.81 s and peak RSS 855,940 KiB; off is 33.86/0.27 s and 1,009,196 KiB. The lower RSS in the slower condition is not a proven memory advantage. Packed bytes remain 126,843,428, with 6,132,277 nodes, 578 levels, 59,626 declarations and 842 rules.

Parse fusion removes a separate graph traversal, not its cost. Source now performs pointer-keyed lookup/emission while parsing and retains final name fixups. Parse plus finalization is 1.587022453 s on and 0.971561029 s off, compared with E036 parse plus eager pack 0.954939420 s. Therefore this observed fused version does not establish cheaper preparation. **Do not causally attribute the on/off parse-time difference to canonical computation:** getenv is read when workers are created after parsing; both use the same parser. That difference exposes single-observation/run-order/load variability.

The unchanged tables are allocated in the off condition too, so off isolates computation with the same structural storage, not “all added memory removed”. Based on the actual POD layouts and allocations, explicit worker arrays total 10,158,080 bytes (9.6875 MiB) per worker, about 38.75 MiB for four, before vector/allocator/thread overhead and native/parser storage. Future GPU memory/occupancy cannot be inferred from packed input bytes alone.

The original optimized native competitor is real and accepts the full input: 2.249777186 s at four threads; 2.001414431 s with the actual 24 eligible CPUs. Its 24-thread resource receipt reports 14.12/8.16 s user/system and 2,688,892 KiB peak RSS. Neither single observation establishes a thread optimum or uncertainty. The competitor was not made to fail or denied input. However, these instrumented diagnostics retain every native body and are not replacement verifiers; comparing their whole wall directly as though they were final hybrid methods would be invalid. The four-thread diagnostic also is not an equal-resource superiority test against the 24-thread reference.

Native/GPU superiority is unmeasured. Nor can one subtract all host wall, subtract a fixed CPU sum from native wall, multiply the earlier 84% check fraction by 6.27%, or extrapolate GPU speed from host runtime. Even an idealized zero-host-query scenario retains preparation and unknown fallback/dependency costs; any such calculation must be explicitly conditional, not a strict bound.

## Source engagement, actual faults and semantic scope

I inspected the canonical .cu, C++ wrapper, Rust bridge and patch, and the actual private src/e037.rs is byte-identical to the canonical bridge.

- The parser captures successful native typed constructors. Each immutable native expression/level pointer receives an append-only packed identity; children capture that identity immediately. Overwritten raw slots do not retarget earlier parents. Native name-pointer interning and later declaration fixups remain; this is not raw-ID-as-address or a second permissive JSON parser.
- Exact term keys include all seven fields, environments include ordered key/value/next, and levels compare complete triples after hashing. Hash collisions are checked. MDATA no longer mutates an interned term's substitution field.
- Memoization is direct-mapped with exact operation/original-input/mode comparisons. Only completed error-free operations are stored; false E/LE answers are not promoted to positives. Worker-private epochs reset per declaration, with explicit wrap clearing. The declaration limit is constant within that epoch; context-bearing term/environment identities remain in keys. Fresh local identities are not reused across an active task.
- Source leaves the old 65,536 arena / 8,192 frame / two-million-step defaults unchanged, reuses workers in chunks of 64, and charges allocation/initialization inside the process. Arena-size tuning did not manufacture the improved count.
- W/I constant access now conservatively rejects indices at or after the current declaration. That is useful scope handling, **not proof of complete replacement equivalence**. Unsafe metadata is not comprehensively propagated, full native obligations and rejected-input qualification remain, and existing partial recursor/universe/projection semantics persist.
- Most decisively, actual main calls e037_prepare_host_diagnostic and then check_all_declars unconditionally. check_def_like_v still performs header checking, native inference, native declared-type evaluation and native equality for every body. Host_positive never selects a native skip. There are no CUDA invocations or device kernels in this result.

The first C++ build succeeds, but the first Rust build fails with exit 101 for an unclosed delimiter in the generated bridge. Its original stderr is retained. The repaired build exits zero in 22.97 s. No failed build was counted as a timed checker result. Existing PGO is reused, with documented CFG mismatches, including changed parser functions and up to 8,027 checker-dispatch and 72 main counts discarded. This diagnostic build is not silently the exact optimized CPU baseline.

A small reproducibility gap remains: terminal command arrays do not themselves record GPU_SMT_CANONICAL_OFF or GPU_SMT_ARENA_TRACE values. Root identifies off as GPU_SMT_CANONICAL_OFF=1, and source disables computation on **presence**, irrespective of value. Preserve that exact launch environment in the ordinary record (including unset for on); no rerun or new control schema is needed merely to repair metadata. The full identical frozen/off output relation independently supports the intended off engagement, but is not a substitute for retaining the launcher details.

All original final verdicts here come from the unchanged native checking path, which is adequate for this narrow cost decision. No correctness-only campaign is needed to retain a negative setup result. Conversely, accepting an accepted corpus cannot qualify the untrusted host positives to replace bodies.

## Scope and next boundary

The 53 source-attempt CPU cells / 1,401,214 attempt rows remain a different population. Neither these declaration CSVs nor the extra available-CPU baseline enlarge that matrix. No CSLib/Mathlib completion, ordered repetition matrix, source-elaboration acceleration, service arrival/queueing/isolation/cancellation result, prepared-state novelty, SMT result or OSDI acceptance follows.

Input export construction remains outside this declared post-export checker timing, with actual construction recorded in E036. A broader source-verification claim must include or justify reuse of it. Current Workspace discovery records 24 CPUs, no quota, no exposed GPU; no shared RTX5090 allocation was made by these runs.

The causal ablation adds useful negative evidence: exact sharing recovers some capacity failures, but their fixed-reference paid CPU is only about 0.10 s and the host algorithm costs substantially more. Cheap declaration count is still an unreliable reason to implement this GPU port. Record the boundary, avoid promoting known hash-consing/cache/worker primitives into novelty, and return to root for the highest-value substantive route. These findings do not prohibit a materially different GPU algorithm, and do not certify the main heterogeneous experiment as run.
