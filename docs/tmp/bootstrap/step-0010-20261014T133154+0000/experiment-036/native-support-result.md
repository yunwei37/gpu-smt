# Complete-declaration bridge: actual associated native costs

E036 integrated setup now includes an implemented native typed-DAG bridge, a same-algorithm host execution control, and per-native-declaration body CPU association. **No GPU backend, native-check replacement or full experimental result is claimed.** The native checker still checks every declaration and returns its original complete verdict. This is not another Meta argument census, a source-verification speedup, or a standalone paper contribution.

## Implemented and actually executed

The root agent implements [arena-native-bridge.rs](../../../../../bench/lean-gpu/arena-native-bridge.rs), [arena-native-support.cpp](../../../../../bench/lean-gpu/arena-native-support.cpp) and the [native integration patch](../../../../../bench/lean-gpu/arena-native-support.patch). The bridge runs inside pinned sokonanoda7645b1e1fcac, after its original parser. Native pointer-keyed expression/level/name maps produce contiguous closure input arrays; immutable native declaration order supplies query indices. This avoids using the earlier Python export adapter or a cross-version name join.

The C++ control reuses the **unchanged** published closure-checker.cu and its existing capacity65536, frame8192 and step2000000 defaults. Four host workers claim ordinary declaration batches and reuse private caller-owned scratch. This is host setup only; it does not implement a CUDA task queue or validate GPU scratch occupancy. Original optimized baseline binaries remain untouched. The private diagnostic build is /tmp/gpu-smt-arena-native-stages-20261016/source; commands and full compiler outputs are retained. No package installation or persistent runtime/model/storage setting changes.

Native timing starts after check_declar_info_v and surrounds body inference, declared-type evaluation and conversion. The Linux thread CPU clock records paid work on the current native worker. Each successful original body records against native decl_idx, and CSV output enumerates the identical original declaration map. All body rows in these accepted inputs have nonzero clocks. It excludes declaration metadata/type well-formedness, all inductive/quotient/other native-only work, parsing, bridge, host querying and cleanup. Rejecting bodies would need explicit censoring because a panic does not reach body_end.

## Exact source revisions and honest support limits

V1 deliberately omitted Proj and nondep Let and incorrectly placed is_k in the unsafe bit. Its unmodified source is retained as native-support-v1-executed-bridge.rs, with all original raw outputs. Independent first-support review identified K-bit and singleton-constructor issues. V2 was built but never measured; its build-only source and logs remain separately retained.

Root verifies pinned native eval.rs: all Let nodes extend the binder environment regardless of the nondep hint. V3 therefore maps every Let to the existing binder-preserving tag7; it does not invent a new evaluator rule. It maps Proj to existing tag10, stores K in bit3 as in the frozen adapter, and supplies a constructor witness only for genuine singleton inductives. The shared closure engine is unchanged. The formatted canonical Rust module byte-equals the actual V3 compiled module; [validation receipt](native-support-source-validation.json) records this and the unchanged frozen engine.

These mappings do **not** make host positives trusted native support. The frozen engine lacks full declaration-visibility enforcement, universe obligations and general K/quotient/normalization semantics. Capacity, partial/undecided conversion and unsupported results stay fallback candidates. Native complete checking currently retains every obligation; zero native checks are skipped. No adversarial soundness or replacement qualification has occurred. A positive is a prospective algorithm answer on a native-accepted input, not a certified replacement.

## Measured revised result

| Input/revision | All declarations | Definition/theorem/opaque bodies | Prospective host positives | Positive / body count | Positive / recorded body-thread CPU |
|---|---:|---:|---:|---:|---:|
| Official Init.Prelude4.34.1 V1 |2106|1691|867|51.27%|25.96%|
| Official Init.Prelude4.34.1 V3 |2106|1691|1291|76.35%|46.03%|
| Retained prepared Mathlib4.9 prefix V1 |29709|27579|2888|10.47%|1.55%|
| Retained prepared Mathlib4.9 prefix V3 |29709|27579|13935|50.53%|14.53%|

Each is one setup observation. All four diagnostic processes exit0 with their complete native declaration count accepted. These are not four randomized performance repetitions or the declared full official corpus matrix.

V3 retained-prefix whole diagnostic is3.892510s: original parsing0.887497s; native graph bridge0.283193s; host control2.010717s; native complete checking0.699251s. The process also includes unpartitioned startup/output/teardown costs. Bridge packs59197140bytes over2832318nodes. The separate earlier stage-only binary measured1.569244swhole with0.908618sparse and0.654685scheck; source/instrumentation/cache/PGO differ, so subtracting those observations is not a clean causal overhead experiment.

In the V3 prefix, all observed body intervals sum2.068800671thread-CPU seconds. The13935positive bodies sum only0.300677258s,14.5339%. The8190capacity outcomes account for1.053321846s,50.91% of body CPU;5152undecided/not-equal outcomes account for0.711195981s,34.38%;302unsupported outcomes account for0.003605586s. None is a native rejection: the full native checker accepts all29709declarations.

This is the important distinction from counting covered expressions: about half of the bodies receive positive algorithm answers, yet most observed paid body work is outside that set. Packing alone costs almost as much **wall time** as the entire positive set's summed **thread CPU**. Those clocks are different quantities; four-worker critical paths, cache priming, scheduling and unsupported-work changes prevent treating that comparison as an exact removable-time bound.

## Root research decision

The current eager pack + frozen bounded closure algorithm does **not** justify implementing the GPU batch backend. The earlier V1 low coverage was partly a bridge artifact; faithful V3 fixes recover count coverage but still leave limited paid-cost coverage and substantial preparation cost. This is adverse engineering evidence for this exact constructor, not proof that GPU Lean checking is impossible.

GPU work should not begin by increasing batch size, tuning launch flags, reporting a positive-count fraction as cost coverage, or silently dropping unsupported/native work. A continuation must change a consequential mechanism: retain substantially more expensive declaration work and/or avoid the eager bridge burden, with a complete same-native accounting and final verdict. Existing capacities are not a user quota or research budget, and exceeding them is not a negative native verdict. A richer algorithm or integration cannot inherit V3's numbers; it needs its own actual setup and complete performance result. No additional standalone census or CPU compilation matrix is launched here.

The earlier23.6%outer-Meta flags and inclusive defeq percentages remain different captures/boundaries. They are not multiplied into these native complete-declaration observations. Source elaboration, preparation, verifier services, SMT and allfourcanonical RQs remain in scope and unfinished. The full official Init/CSLib/Mathlib4.34inputs and matrix have not run; the small suite omits >10MBinputs, and the retained4.9prefix is not renamed as the full official benchmark.

## Provenance, failures and storage

All CSVs, native stdout/stderr, exact terminal commands, /usr/bin/time outputs, compiler output and analyzer source are retained. The analyzer checks contiguous indices, nonzero accepted-body intervals and positive/reason consistency, and recomputes all weighted fractions. [Analysis source](native-support-analysis.py) and per-input analysis JSONs are adjacent. Initial C++ missing-exception-header failure is preserved; the header was repaired and the actual shared library build succeeded. A too-long Windows SSH command failed before remote launch; source transfer then used bounded chunks of the same existing transport, without a new helper/service or host recovery.

Reuse of the existing PGO profile emits retained CFG mismatches: up to8027counts in checker dispatch and72main counts discarded. Thread clock/atomic operations, diagnostic traversal, host workers and cache warming perturb the run. No matched uninstrumented support fraction, repeated estimate or rigorous Amdahl ceiling is claimed. The original-stage patch, binary copy and logs preserve the earlier measurement condition.

At the later setup checkpoint the project volume has about7.58GiBfree, after private compilation dependencies. No all-three-corpus expansion is started, no active storage/capture state is deleted and no storage boundary changes. Original captures continue in their original processes; root checks only final completion at natural checkpoints and does not spend goal turns polling healthy row counts.

[Fresh independent review](first-support-review.md) distinguishes revision-specific validation from future code and whole-paper claims. Root integration/disposition is a separate record. Native and analysis implementation/publication are root-owned; canonical README/docs/paper and specialist experiment-script authors retain their original OMP file scopes.
