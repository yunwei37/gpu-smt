# E038 native service integration: independent result review

Observed 2026-10-16, after the concurrent3, stock-native-batch1 and fallback-native2 terminal records. This is one fresh review of the new service integration evidence, not a reopening of the earlier single-source setup review or a paper review. I read docs/user-instruction.md in full, the current E038 plan and root-disposition.md, the current native implementation/patch, the preserved backend versions, actual compiler/link commands, and the raw inputs, transport and outputs. I independently recomputed the checks and timings below rather than accepting setup-analysis.json as an oracle.

The four RQs, complete Lean/SMT verification scope, RTX5090 restriction and OSDI research target remain unchanged. This CPU-native dependency setup does not satisfy those goals. No implementation, paper, experiment script, active writer, Git state or service was changed by this reviewer; this report is the sole written path.

## Five judgments

- **Run status: valid as the finite integration setup; incomplete as the E038 service/performance experiment.** concurrent3 private/control and stock-native-batch1 all exit zero with all four requested original candidates represented. fallback-native2 also exits zero with a real native child response. Earlier failed/partial versions remain material evidence and are not repetitions of the repaired version.
- **Tested hypothesis: inconclusive for the RQ3 better joint latency/throughput/memory frontier.** Supported narrower observation: a genuinely patched native backend can pipeline these four original commands, engage per-candidate runtime versions/tasks, preserve their observed native payloads, and replay the separate listed filesystem-effect control after refusing its shared-worker operation. Neither general isolation nor service acceleration follows.
- **Research value: dependency-only.** This is executable setup inside the admitted mechanism experiment; it is not an additional paper contribution, a complete formal-benchmark result or a new GPU result.
- **Paper impact: mechanism/workload boundary.** Ordinary native parallel verification and shared prepared command state are already an actually runnable competitor on this exact 4.27 toolchain. The proposed runtime versions must earn their cost through a useful supported service boundary; avoiding multiple processes alone cannot establish novelty or causal benefit.
- **Next paper decision:** proceed directly to the one consequential matched service comparison after specifying the actual request grouping and matching the existing memory/deadline behavior and pending-request handling. Use the existing Kimina naive native-batch path as the strong competing mechanism where that contract matches, plus branch-off as a causal control. Do not launch a full cohort under a changed or still undefined policy, claim superiority from this setup, build a baseline-count/tuning grid, or move this constructor onto GPU on these observations.

## What I independently verified

All paths below are relative to this service-integration directory unless explicitly absolute.

1. The four rows in each concurrent3 input.jsonl and stock-native-batch1/input.jsonl equal the first four original dictionaries in artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl, including original code and metadata. They are Proof_00000 through Proof_00003, from the preserved real Goedel4.27 producer; they are not a complete 29,750-attempt cohort or a new representative sampled benchmark.
2. For every input, the transmitted cmd equals the original code with only each import line replaced by an empty line. All other source text and line counts remain equal (20,23,20,55 lines). The prepared header is import Mathlib plus import Aesop. The stock batch cmds exactly equal the four candidate cmd strings of the two streaming groups. No rewritten proof or renamed import root supplies the result.
3. Independently parsed stdout equals observed-responses.json's payload sequence for both concurrent3 groups. Independently parsed stock stdout equals parsed-frames.json. After deleting only the top-level env metadata from each streaming native response, every remaining field equals the corresponding stock response. This compares complete payload dictionaries, including exact diagnostic text, severity, positions and order: warning counts are 0,5,4,0. All four private rows report fallback=false. This is actual payload agreement for these requests, not proof that all possible native artifacts or stateful interactions are equivalent.
4. Private version/task engagement is real in these outputs: ref_versions 43–45, one private thunk version each, and descendant task counts 222,333,224,245 in completion order. Branch-off reports zero ref/thunk version operations. These counts are mechanism receipts, not sampled paid-work fractions or performance benefits.
5. plain-runtime/io.cpp, object.cpp and process.cpp byte-equal their entries in the preserved official lean4-v4.27.0 source archive and contain no gpu_smt hooks. The plain archive actually replaces all three corresponding runtime members. It is not merely the instrumented build with an environment switch.

## Native build and comparator fairness

I read the successful static/shared compile records, archive/link records, plain-build.py, the actual private Main.setup.c entry and the native producer/Kimina sources. The backend links real native REPL producer objects and calls runCommand on a private StateT result using the prepared base; it does not replace checking with an accept cache. The generated C main calls initialize_NativeBranchBackend then gpu_smt_native_backend, and invokes lean_finalize_task_manager before process exit.

The current native-ref-branches.patch also passes reverse --dry-run against the actual private Lean4.27 io.cpp, object.cpp and process.cpp sources (all three checked, exit0; no source mutation).

The candidate actually links the rebuilt libleanrt.a and needs libgpu_smt_ref_branches.so. Its rebuilt libleanshared.so also needs that same helper and retains SYMBOLIC/STATIC_TLS, addressing the earlier static/SYMBOLIC binding problem. Independent readelf inspection confirms those dependencies. The plain rebuilt shared runtime and repl-kimina-gc have no helper dependency. The native runtime patch hooks reference operations, unresolved thunk evaluation, task admission/execution/cleanup and the listed effects. This is stronger evidence than successful compilation or LD_PRELOAD intent. No per-run mapped-library capture was supplied for these new streaming runs, so do not claim those particular dynamic mappings were newly observed at runtime merely from the ELF/launch-path evidence.

The matching runtime builds use the same bundled clang, O3, SDK headers/archives, libc++19.1.7 header family and common shared-runtime composition; the exact original compiler header patch version remains different from the SDK's original build and was already disclosed. The strong baseline is the existing GC/header-repaired Kimina4.27 native REPL objects relinked against the plain runtime. Its actual runBatchVerify mode naive uses one prepared Command.State and IO.asTask for every member, then returns an ordered array. It truly engages the intended competing parallel reuse mechanism; newer Beam incompatibility does not excuse omitting it.

The comparison still has material contract/cost differences: the candidate uses producer runCommand with returned snapshots while the GC batch path uses runCommandGCAux without retaining result environments. Ignoring env metadata for diagnostic agreement is appropriate for this stateless setup but is not a license to claim reusable handles or arbitrary stateful API equivalence. The candidate drops the returned StateT state; emitted env=1 does not expose an independently retained reusable environment for later requests. This is a complete-source candidate verifier prototype, not the complete REPL API.

Branch-off remains instrumented: task accounting and the helper/runtime hooks remain, and prepareRefs still runs. It is an appropriate versions-off causal control, not an uninstrumented fastest baseline. The separate plain rebuilt native comparator is consequently necessary and already present; no additional baseline list is requested.

The terminal environments match the original sysroot, Lean path and native Mathlib manifest and distinguish private/control/plain library paths. At review time the owning Workspace had 24 CPU affinity entries, cpu.max=max 100000 and memory.max=max. Those are current observations, not retrospective measurements of every launch or dedicated CPU reservations. These records contain no new CPU-time/PSS measurements or matched service-level deadlines, so equal-resource memory or policy conclusions remain unproven.

## Timing recomputation and complete-cost limits

From raw terminal.json, the single whole-process observations, including preparation and EOF, are:

| Setup path | Whole seconds |
|---|---:|
| concurrent3 native private | 7.181928293 |
| concurrent3 versions-off control | 6.433317800 |
| stock native batch1 | 6.531248666 |

These are single integration observations with different result handling and emission contracts, not superiority/inferiority estimates. No confidence interval, throughput headline, P95 or speedup is justified.

From private raw stdout, internal-ready to released differences are respectively 1.689215ms (Proof_00001),4.159050ms (00002),4.173197ms (00003),28.794997ms (00000). Control differences are 0.041353,0.017446,0.020937,0.021753ms. The helper's drain_seconds covers its condition wait and counter serialization before most held-object destruction; it is not total cleanup. The released_ns difference includes endBranch release. Actual observed output from the header is 434.932730,893.217632,1258.922049,3410.828515ms private; 194.398813,428.056116,764.737282,2782.995533ms control. These actual emission timestamps must not be replaced by internal_ready_ns.

Version separation matters. NativeBranchBackend-concurrent1-3.lean is the relevant preserved backend for the concurrent3 observations: it has no native replay or completed_ns fields and emits the prepared header before prepareRefs. The current backend contains replay and moves prepareRefs before the header; its source cannot be presented as byte-identical to that earlier run. The old warm-header clock therefore includes promotion after header acknowledgement, while internal per-command clocks begin later. Whole-process cost retains that work. Stock naive emits one array only after the slowest member; comparing its array arrival to individual streaming arrivals would conflate contracts. A common grouping/emission contract is necessary before actual service latency interpretation.

## Fallback: real but bounded evidence

fallback-native2-native-private is one generated #eval IO.FS.writeFile control, separate from the official workload. Its native branch identifies lean_io_prim_handle_mk, preserves the discarded shared-worker error, and reports a child exit0 with two native frames (header env0 and candidate env1), empty stderr and final env1. The expected /tmp/.../original-fallback-effect.txt exists with exact text original-native-fallback followed by newline.

The actual current patch refuses the listed native handle opening before it opens the file. The backend waits for branch release, discards its provisional result, then uses IO.Process.output to run the original command in the plain native child, capture stdout/stderr/exit and wait for its EOF. Thus this evidence supports an actual before-open fallback route for this control. It does not qualify arbitrary FFI, process-global C++ extensions, uninstrumented effects, or worker-death replay. In-flight thunk and process-exit guards terminate the experimental worker; outstanding requests currently have no replay implementation.

Costs are explicitly substantial: internal_ready_ns=265982393, released_ns=266034718, completed_ns=4302417807; actual output after the header=4.302485522s and whole process=8.036315395s. The replay adds about4.036383089s after branch release, including the cold native child. completed_ns stops before outer JSON serialization/output; whole-process and observed emission retain those costs. No fallback-free speedup may be inferred by omitting this work.

The earlier fallback-native1 is a failure even though the parent exits zero: the child exits1 after an extra blank transport frame, returns only the header, and the old backend mistakenly presents env0 as the response. Its raw error is preserved; it must never count as verification success. The current backend trims the outer transport framing and rejects a nonzero child or fewer than two JSON frames. The subsequent native2 result is the repaired control, not a performance repetition.

The fallback terminal explicit_env originally omits GPU_SMT_FALLBACK_REPL and GPU_SMT_FALLBACK_LIBRARY_PATH. I flagged this provenance gap to root. Successful child output establishes that a replay occurred but does not alone reconstruct its exact executable/library selection; a clearly labeled reconstruction from the actual launching command can repair the record without rerunning. General native-output framing/worker death and memory/deadline behavior remain integration work, not reasons to demand an unbounded correctness-only investigation.

## Required next boundary, without expanding this setup

The consequential continuation is the complete supported service comparison already named in the plan: define the common stateless source-verification/request grouping contract, retain exact original workload outcomes and all fallback/failed attempts, finish the actual memory/deadline and pending-request behavior needed for that contract, and measure whole-service makespan/throughput, emitted latency, complete release/EOF and full process/fleet PSS/CPU against the engaged strong native comparator. Then the declared repetitions and original cohort can decide whether runtime versions buy a useful joint frontier. Use existing controls and official/native paths; no extra tuning grid, new quotas, renamed RQ or GPU constructor is warranted here.

This report accepts the new finite setup evidence at its actual scope. It does not reopen the earlier setup audit, qualify general process isolation, establish novel concurrent verification, answer RQ3, close the other three RQs or claim OSDI readiness.
