# E036: batch complete declaration checks with native fallback

Observed2026-10-16. Parent: unfrozen BOOTSTRAP step0010. Proposed by root, who owns Lean/GPU implementation. Not an admitted/run experiment or a replacement of any existing RQ. This plan is one integrated mechanism comparison; initial CPU cost/representation work is a dependency, never an independent paper result.

## Research question and decision value

RQ4 verbatim: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

Specific uncertainty: can an accelerator process enough actual type inference/conversion work across independent whole declarations, over a shared immutable exported environment, to improve complete exported-proof checking against the strongest runnable CPU checker after charging parsing, native representation conversion, device/context setup, all transfers, unsupported native checking and shutdown?

Largest credible positive: meaningful complete Lean proof-checking acceleration on standard formal corpora over an optimized parallel native checker, with a causal explanation of work granularity, representation cost and fallback. It would be substantive supporting/decisive RQ4 evidence, not complete source elaboration acceleration, a novel prepared-serving system by itself, or OSDI acceptance. Negative/mixed evidence closes or bounds this complete-declaration mechanism and its workloads, rather than all GPUs. RQ1–3, Lean/SMT service scope and full paper remain.

The strongest reject argument is the lack of costly independently ready work beyond tiny synchronous beta/zeta packets. Prior E022 loses with extremely little work; E034 offers pairs before native shortcuts; E035 lacked a concrete mechanism. This proposal targets entire definition/theorem/opaque body checks, with explicit evaluator continuations, not early speculative argument pairs. It directly changes the unit of useful parallel work and the complete-checker boundary. Native CPU already parallelizes declarations and caches sessions, so neither batching, integer arrays, closures nor persistent GPU workers alone is claimed novel.

Best competing next work is deeper source-service preparation reuse. Existing original attempts have nearly one import root, cost reanalysis bounds import-only gain on that cohort, and known snapshots/AXLE already provide generic mechanisms; no measured differentiated deeper prefix currently exists. A new CPU tuning grid or standalone operand census cannot resolve the present GPU mechanism question. Current official checker source and existing closure engine provide a concrete broader route with real standard tests, while keeping the original full objective intact.

## Mechanism and competing explanation

Use the pinned sokonanoda official parser as the single authoritative parser and host environment. Serialize its immutable typed expression/level/declaration/recursor metadata into the existing closure engine's ordinary native array representation. Preserve declaration visibility/order/universe scope and literal/metadata semantics; unsupported content never becomes a positive answer.

Submit definition/theorem/opaque checks as whole independent tasks. Caller-owned continuation/closure arenas are private per active worker and reused after each task; a persistent task cursor decouples scratch memory from the total declaration count. Shared input is immutable. Only actual positive supported checks may suppress corresponding native body work. Native CPU still checks all unsupported declarations and the axiom/inductive/recursor/quotient/environment obligations needed for a complete final verdict. Every candidate declaration is checked by one qualifying path or native fallback; a failed/incomplete device execution cannot silently discharge it.

The existing frozen closure engine is a partial semantic implementation. It is not already a complete modern Lean kernel: symbolic levels, projections, K/structure/quotient/numeral extensions and metadata limits must stay explicit. First implementation is conservative positive offload plus the complete pinned native fallback, not acceptance from a fragment. Existing E018 source/export integration mismatches stay closed; this standard post-export experiment does not revive that source-verification path.

Counterprediction: native cached checking is already cheap, packing and private scratch dominate, GPU support misses costly declarations, skew strands lanes, or CPU/GPU duplication/fallback outweighs parallelism. This could fail even with high declaration-count coverage.

## Cost first, inside this mechanism experiment

Before implementing its GPU batch backend, use the official same-checker parse-only path and direct parse/check boundaries in the pinned native source to establish the complete-checking opportunity and the actual representation/support work needed for this algorithm. This is the mechanism's admission/setup dependency, not another full5-hour Meta census or a new paper experiment. Existing Meta35%/outer23.6% data do not transfer to exported checking.

Observe whole process and parse/check wall/CPU on unchanged official data. The conditional zero-cost-erasure calculation must refer to the same native run/boundary and remain a conditional model, not a guaranteed wall bound under altered caches/contention. Then relate supported whole-declaration work to that mechanism; counts cannot replace time. Stop an unpromising constructor by scientific disposition, without arbitrary numerical quotas or claiming a universal negative. A high fraction alone is not GPU evidence; actual full candidate costs remain the main test.

## Real assets, baseline and controls

Primary protocol: pinned official Lean Kernel Arena315f24d4cd90d70854df862597cc152c1b211898, export3.1.0, its native accept/reject/decline/error outcomes and measured wall/RSS, not instruction-derived virtual CPU time.
Main CPU competitor: sokonanoda7645b1e1fcacfe410c99141f1234381d995b325d, source-native official options and PGO/native-target recipe. Official command:
target/release/sokonanoda --stdin --nat-extension --string-extension --axiom-allow-all --threads 4 < INPUT
Recipe trains PGO on Init.Prelude, not the evaluated large test. Preserve the existing default/prefix builds; private integration is a dependency package in this same Workspace, not a new gpu-smt checkout.

One same-algorithm host control uses the identical supported closure algorithm and representation plus native fallback without GPU; it separates new algorithm/coverage from hardware. Parse-only is a component control, not a checker baseline. No official-kernel-only weak acceleration denominator or redundant CPU ranking rerun.

Whole large workloads: official Init, CSLib and Mathlib at the pinned test identities. All expected outcomes are accepted. The public small tarball excludes large inputs and is only correctness/development coverage; it cannot replace large-workload performance. Use the official tests' native exported inputs without source migration or fabricated proof tasks. Obtain official cached/generated input through its documented path; corpus construction is setup outside checker timing, and exact identities/commands/dependencies remain retained. No unexplained current-site/pinned-snapshot mix.

Correctness: run the official available correctness suite including expected rejections, verify complete final native verdicts and retained decline/error cases. Compare GPU/host-control answers to the pinned native checker and official expected outcomes; do not turn a decline into acceptance or count unexercised support as success. A baseline's own declined cases remain explicit. Candidate-wide qualification checks complete decisions, not an accepted-only microfixture. Finite tests do not prove universal kernel correctness.

## Planned complete comparison

The single primary relation is complete exported checking with versus without this GPU execution mechanism. Three ordered repetitions for each of the three real large corpora, alternating method order:
- optimized native CPU;
- same-algorithm host execution plus native fallback (control);
- GPU execution plus native fallback.
All27 primary cells must be terminal before a complete performance conclusion. Retain every error/decline/operational failure; no partial run splicing. Separately record complete component times/device execution/peak allocation and system resource observations; no additional broad tuning matrix. The public small suite supplies correctness scope and real implementation qualification, not performance headline.

Primary metric: process-start-to-final-verdict/exit wall time, including input read/parse, representation, initialization/JIT, device transfers/execution/synchronization, native fallback and cleanup. Input construction/build are separate. Report total CPU/RSS and actual GPU resources with observation limits, plus actual supported useful work/dispatch width and fallback reasons. Added RTX5090 hardware is disclosed; no claimed GPU isolation, exclusive slot or cost equivalence.

Existing time-sliced RTX5090 owner path is reused and the other workload remains. Code/build/test preparation occurs only in existing gpu-smt Workspace. Any actual device benchmark uses the already established finite owning-PVC K8s route; no B300, replacement Workspace, service, scheduler, reservation or persistent configuration.

## Execution readiness and return

This is a prospective mechanism/development plan, not a claim of an executable GPU command today. The official baseline/parse-only commands and native parser exist; the typed bridge, complete final-verdict integration and batched device candidate are not yet built. Root must retain actual private build/source/CLI commands as implemented and establish executability before requesting a full run. No invented launcher or protocol is reported as existing.

Real preflight, once ready: the actual official Init export through all3 whole methods with actual device engagement, supported checks/native fallback and final exit. Existing partial-closure E021 attempts are not silently reset; this is a different native-parser/complete-declaration mechanism and standard boundary, with its own honest provenance. Preflight proves execution only. The declared full scope includes all3large corpora, repetitions and original correctness cases.

Positive: consistent complete-checking gain with native outcomes, actual hardware work and attributable full costs, against the competent matched CPU path. Negative: complete loss or no useful cost opportunity closes this constructor. Mixed: preserve workload/skew/overhead limits without a universal gain. Inconclusive: retain incomplete/invalid scope; no favorable subset claim. Target figure: whole wall ratios per corpus alongside parse/representation/check/fallback/device cost and useful-work support, never kernel-only acceleration.

No paper/RQ/scientific-contract rewrite, memory change, model switch or completed gate is authorized by this proposal.
