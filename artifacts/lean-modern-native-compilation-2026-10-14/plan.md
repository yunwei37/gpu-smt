# RQ4: modern complete-source CPU native compilation comparison

## Research question
RQ4: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

Specific uncertainty: Does official native compilation materially reduce warm complete-source verification on a modern tactic-heavy producer workload, changing the CPU competitor and residual-cost target for GPU work?

## Admission and decisions
Role: supporting within RQ4's strongest-CPU characterization. Largest credible story is a version/workload-sensitive CPU cost boundary that a heterogeneous checker must beat; official native compilation itself is prior art, not systems novelty. The rejection argument is that old4.9 generated syntax rejects and tiny reductions are poor surrogates for a modern valid tactic-heavy workload.
Existing old ProofNet pairs reduce wall time3.92/1.52percent but do not answer this scope. Static tactic counts on modern proofs do not prove dynamic cost. No prior matched whole modern comparison is available locally; author status metadata are not a performance baseline.
Positive: use the measured improved CPU competitor and characterize remaining costs before heterogeneous changes. Negative: stop treating native compilation of this tactic set as the major missing acceleration. Mixed: identify workload/response classes and replication variation, no global gain. Inconclusive: preserve raw data and repair only actual execution defects.
Best alternative is another narrow beta/projection/LP GPU fragment, already bounded by observed low eligible work. A modern full comparison has greater decision value. Do not create new GPU tiny-operation runs merely for engagement.

## Assets and source-native protocol
Original immutable GoedelWorkbook4.27 archive author Git3c2afe6bfc6bdeca6b78d1f257468164bba56966,29750 source files,41564450 source bytes. Published generated proofs and author migration statuses are not the complete original model rollout/arrival trace. Include every released file, not only published successes. Preserve source bytes, filenames and author statuses.
Official Lean4.27.0/db93fe1608548721853390a10cd40580fe7d22ae, Mathliba3a10db0e9d66acbebf76c5e6a135066525ac900, official REPL0e9e6e2962ab0a51440513d9ee028c8aa66bb53b, stockKimina fb2393d. Full source references and acquisition receipts are in step0010/literature-20261014T1457/.
Both REPLs use the already qualified author initialOptions autoImplicitfalse/maxHeartbeats800000; file-level maxHeartbeats0 remains unchanged. No proof repair/import normalization.
Candidate uses official Lake Mathlib.Tactic.Linarith dynlib and Lean.loadDynlib before the existing REPL loop. Builder/source/symbols and actual process maps qualify the implementation; loaded symbols do not prove sampled execution.

## Comparison and fairness
Single main baseline: exact stock warm service, a credible prepared-CPU competing answer. Candidate: same warm service with native tactic dependency code loaded.
No remote published ratios can replace the matched comparison. No extra weak cold or proxy checker row.
Three alternating whole-corpus pairs: original/compiled, compiled/original, original/compiled. One separate resource-profile cell for each method. All eight cells useCPU8-11 and four HTTP requests in flight on private loopback8002; stock defaults12GiB address-space perREPL/300s request timeout/maxpool23/maxuses-1 unchanged. Identical input/admission source sequence. Completion order depends on runtime and is retained; this is closed-loop saturated service, not measured real arrivals or fixed offered-load latency.
Current other acquisitions useCPU0-3/8000 andCPU4-7/8001. They remain active; shared memory/cache/I/O and other users are background, not exclusive hardware. No device/quota/Workspace/restart or persistent helper change. CPU affinity is a matched finite benchmark condition, not reservation.

## Metrics and interpretation
Primary: whole corpus wall seconds and returned-attempt throughput, all outcomes. Whole clock includes source-input persistence, server startup/readiness, imports/native-library loading, frontend/tactics/kernel, HTTP transport, logging/raw capture, worker replacement, shutdown and pipe EOF. Software build and postclock lossless ZIP are separately recorded and excluded from steady-state service time.
Secondary: per-source request latency distribution and outcome-class decomposition; separate profiles sample process-tree CPU/PSS and include observer overhead. Sampling is not a replicated peak-memory claim.
Native response objects/basic outcomes compared per proof ID, excluding only the stock adapter-injected measured duration; internal IDs and operational errors remain raw. Independent author statuses are diagnostic reference, not current operational ground truth. Unsupported/resource-limit failures count and are retained.
Report every primary pair and descriptive variation; no significance or confidence claims from setup/preflight.
This comparison bounds this official CPU mechanism/workload, does not alone answer RQ4 or validate GPU acceleration, full native-state branching, all four RQs or OSDI novelty.

## Execution
Build using official Lake target +Mathlib.Tactic.Linarith:dynlib and a private source-copy REPL with one optional loader addition. Original4.9 runtimes and sources untouched.
Preflight: exact published Proof_00000(authorok) andProof_00004(authorerror), through actual HTTP /verify on both methods, preserving error feedback. Existing direct run_checks preflight qualifies producer options only; HTTP/native-load readiness is still required.
Full command: stockKimina .venv/bin/python artifacts/lean-modern-native-compilation-2026-10-14/run.py full.
Completion: all29750 returned outcomes in all8conditions plus normal owned shutdown/EOF, raw source and outcome comparisons; partial cells are never whole-corpus results.
Raw directory: this artifact's full1/; input acquisition retained separately. Per-source append checkpoints and raw responses/logs survive failures. No live same-cell restart or partial-prefix speedup interpretation.
Figure: all paired whole-corpus times vs modern warm CPU; failed/incomplete populations explicitly shown. Full result review required before paper insertion or completed-step publication.

## Review boundary
Human explicitly requires root to implement/run directly and forbids delegation. Root plan review/preflight/result analysis are self-review; fresh independent review and outer audit remain unsatisfied. This does not authorize fabricating independent review or stopping available approved experiments.

## Submission-order clarification before full acquisition
Logical submissions use the fixed sorted source sequence. Thread scheduling may reorder actual HTTP admission; each source admission/response timestamp and completion order are recorded. This does not assert identical physical arrival histories or fixed offered load. Matched width/resources and all original source bytes remain fixed.

## Native4.27 dependency-loader qualification
Unlike old4.9, actual official4.27 module dynlib omits DT_NEEDED links to imported modules on Linux. Load the complete official-built target dependency closure through Lean.loadDynlib, ordered by native symbol dependencies; manifest/build/symbols retained. Source-native proof/options/server policy are unchanged. No single leaf mapped is called evidence of tactic engagement. Full HTTP preflight remains required before acquisition.
