# E038 native batch protocol review — substantive follow-up 1

Observed 2026-10-16. This is the first substantive follow-up to E038's original round-1 plan review, not a new experiment, RQ or reset review round. Read the actual current plan's “Frozen executable native batch comparison”, frozen paths/build/relink/compatibility receipts, current NativeBranchBackend/native ref implementation, exact retained QGC REPL/Main.lean and JSON.lean, installed Kimina Repl/settings/models/header policy sources, preflight1/2 drivers and terminal/raw outputs. No native run, source edit, OMP change or Git action was performed. Only this protocol review is authored.

## Admission decision

**Admit the native-batch comparison as a valuable, substantially better matched test of the same RQ3 mechanism. Full-run execution is not yet admitted: the actual preflight fails for all three methods and the sole full runner has not yet been delivered/inspected.**

The primary scientific comparison is now credible: actual ordinary native BatchCommand naive already shares the prepared command state and imported heap, so it tests whether runtime reference versions/lifetime handling add benefit beyond competent native reuse. It is stronger than attributing fewer processes or ordinary native task execution to the candidate. Matching gc=true and ordered batch-array emission removes two concrete sources of unfairness. No additional main baseline is needed.

The present defect is executability, not a demand for an ideal experiment. Preflight2 stock/private/off all abort with “failed to create thread”, before any complete native response array. Launching the nine full conditions now would collect repetitions of an unresolved common native failure, not test the intended service frontier. Repair that actual condition through the existing path, or revise the same protocol to a justified runnable resource regime applied equally to all methods. Do not interpret stock's avoidable startup/worker failure as a private-branch win. No extra correctness-only program, broad baseline matrix, performance tuning grid, user-author wait, agent budget or persistent resource change is required.

The comparison remains one fixed offline batch regime, not the full service load/concurrency frontier or the entire four-RQ paper. That supporting scope is honest and does not make its complete original-source measurement low value.

## Actual source contract and baseline audit

Frozen paths name /tmp/gpu-smt-native-ref-branches-20261016/batch-frozen-v1/plain/repl and private/repl, with the same underlying retained QGC source /tmp/gpu-smt-goedel427-20261014/repl-kimina-native-gc-header-repair. The actual build script replaces only the candidate entry/backend and its private runtime path; the stock entry retains QGC native batch execution. Plain/private shared runtime linking includes the same shell.cpp integration, and both actual lake env compatibility calls succeed. Earlier generated-initializer relink failure is a build repair, not a benchmark result.

Native source evidence:

- REPL/Main.lean:216–243 implements runCommandGCAux with ordinary processInput, messages, sorriesGC, optional tactics/infotrees and no retained candidate snapshot.
- runCommand:291–299 selects exactly that auxiliary path when gc=true.
- runBatchVerify:367–390 retrieves the requested saved command state, constructs commands from the batch options and calls batchVerifyParrallelNaive for mode naive.
- The naive path:330–343 launches native IO.asTask per command, then returns results in input order, catching per-task IO errors.
- Current candidate batch constructs commands with the same batch options, env0 and gc=true, runs independent StateT results from the saved base, and returns the ordered response array after joining all tasks.
- The external payload is therefore a common native ordered array. Private branch/replay counters remain separately captured stderr metadata; internal ready/released clocks are not substituted for actual array-emission latency.

This makes stock the main competing answer, “ordinary native reuse already suffices.” Off is an implementation/component control and cannot replace stock. The candidate still has extra input parsing, runCommand snapshot lookup, branch setup/release, metadata and possible replay costs. Those belong in the proposed complete method; private-minus-off is a branch-component comparison, not a CPU compilation contribution. A small direct ref lookup comparison would not answer this question.

The version-aligned native batch is runnable source prior art on this exact compiler, unlike an unverified Beam upgrade. A positive still must distinguish its runtime mechanism from existing snapshots, native parallelism, Beam/leagent and generic state versioning. Nothing here proves novelty or OSDI readiness.

## Workload and comparison boundary

All29,750 input.jsonl rows, original order/IDs/source/options and rejected/incomplete/operational cases remain the right source population. Import-line blanking preserves original line positions, and the real common Mathlib/Aesop root remains one context. No selected retry, filtered hard input, cached verdict or fabricated multi-context workload is permitted.

Native header preparation once per worker, reused ordered batches and one final partial batch give a concrete offline contract. Width derived from actual24-CPU affinity is a stated experimental choice, not an upstream native BatchCommand default or proof that24 simultaneous commands fit the existing policy. Native thread default is a separate variable: the inspected runtime get_lean_num_threads returns LEAN_NUM_THREADS if set, otherwise std::thread::hardware_concurrency. Affinity width alone does not establish that scheduler default.

Applying300seconds to the whole batch gives every array the same external deadline. It is not the previous per-proof HTTP300second policy, even though it reuses that numerical default, and this experiment must stay separately identified. All members sharing a batch's emission timestamp is the correct consequence of this chosen contract. Their latency percentile is a grouped offline-batch response metric, not an independent proof-completion distribution, interactive response advantage or production arrival trace.

The common order and three rotated blocks stock/private/off, private/off/stock, off/stock/private provide a reasonable first complete method comparison. They do not erase load drift or make29,750 requests independent timing replications. Report whole-run observations/paired ratios and uncertainty at the whole-run level. Do not choose the winning repetition or use another CPU experiment as a denominator.

## Actual native policies and resource accounting

Installed Kimina Repl.start sets RLIMIT_AS from max_repl_mem and starts lake env in a fresh process group. Settings parsing produces12288MiB from the default12GiB value; preflight records confirm that value. The native policy provides no CPU quota. Header60seconds and VerifyRequestBody300seconds are present in the actual sources. Reusing these existing policies is supported; this is not a newly introduced8GiB cap.

A fallback subprocess inherits the same per-process address-space bound. That is **not** a12GiB fleet-memory bound: a candidate with multiple children can use more aggregate memory than one stock worker. Report the complete observed fleet cost, including replay children. A speed/memory tradeoff can be valid, but cannot be labeled equal aggregate memory or a joint dominance result if the candidate consumes more resources. There is no need to invent an aggregate hard cap to conceal that difference.

The plan correctly distinguishes normal EOF/finalization from native Repl.close's SIGKILL behavior. Actual Repl.close closes stdin then kills the process group; it cannot prove graceful retirement. On success the driver must close stdin, drain output, wait for native finalization and record exit status. On timeout/crash/invalid array, retain the failed current batch and owned-process cleanup, then restart for the next original batch; do not silently replace the failed batch's outcome. A finalization failure remains an operational result, with its cost.

Tree CPU and PSS/RSS require honest coverage. The existing Kimina CPU monitor sums currently visible processes; it can miss already-exited children. The preflight also records RUSAGE_CHILDREN waited totals. That improves accounting but is not automatic evidence that every descendant contributed exactly once under every exit path. Publish the actual waited-tree counter and sampling method/limitations unless exhaustive coverage is established. Sampled PSS/RSS maxima with timestamps/incomplete reads are useful but are not exact peak bounds or replicated memory evidence. Match sampling and compression work across methods.

The collector itself, gzip writes, startup/restart/preparation, fallback, stderr draining, response transport and final cleanup must stay inside the same whole-run boundary where they actually affect execution. Private-only metadata output is an actual method cost. Stable staging in existing /tmp avoids filling the project PVC; it creates no storage entity or justification to delete original/active evidence.

## Actual preflight evidence

### Preflight1: capture defect, no candidate comparison

The original driver returns bytes from _read_response but writes header.stdout using Path.write_text(raw). All three methods reach the header and then raise TypeError(data must be str, not bytes); native close terminates them with-9. No proof batch or complete array is returned.

The driver's printed ALL_NATIVE_OUTCOMES_EQUAL True compares absent response values. It is explicitly invalid evidence. Preserve the raw failure, but do not count it as successful verification, equivalence, native EOF or performance.

Root corrected the byte write in preflight2 and strengthened equality to require every complete_array first. That is a minimal same-boundary driver repair.

### Preflight2: real common native failure

The corrected source sends the same24 original proofs, prepares env0 and uses the same existing policies. All three methods terminate134 without a complete batch array:

| Method | Observed whole seconds | Native stderr |
|---|---:|---|
| stock |4.450827504|failed to create thread|
| private |4.857997547|failed to create thread|
| off |4.366103513|failed to create thread|

The JSONDecodeError is downstream of empty native output; it does not identify a JSON protocol bug as the root cause. These times are failure observations, not speed or capacity results. The candidate and baseline agree only in failing this setup condition, not in proving the requested sources.

Read-only current cgroup inspection shows pids.max142882/pids.current469, memory.max=max and cpu.max=max100000. This provides no evidence that the cgroup pids ceiling caused the past failures. Native pthread creation throws a generic exception without preserving its errno in the printed text. Native stack source defaults to8MiB per lthread, while pending task dependencies may grow workers. RLIMIT_AS, actual virtual mappings, stack/TLS reservations, native worker discovery and actual system error remain plausible investigation points, not established causes.

The minimal next action is to resolve this common thread-creation failure and demonstrate the intended native batch at the same comparison boundary. If a policy-compatible batch/resource choice must change, record the substantive protocol deviation and apply it to all methods before the complete run. Do not choose a smaller workload population, change source/proof checking, filter failing cases or weaken the question. This does not require a tuning sweep.

### Framing and output handling

Preflight already drains stderr continuously; the full runner must do the same, because private metadata/fallback logs can otherwise block the native process. Native _read_response uses stdout.readline and blank-line/EOF framing. The underlying default StreamReader has a finite line buffer, so large ordered arrays may expose a transport limit. That is a concrete implementation risk to inspect if encountered, not a reason to invent a speculative new limit or block an otherwise valid preflight. Keep and repair any actual framing failure equally rather than count it as a method outcome win.

The full runner is still absent at review time. The plan says OMP owns its single experiment-script file, so it would be false to certify its exact failure retention, grouping, tree accounting, normalization or normal EOF behavior now. Inspect the actual delivered script before launch. This is a remaining executable dependency inside the same experiment, not an additional scientific project or demand for another author.

## Supported effects and interpretation

The implemented listed filesystem/process guards precede their respective actions; marked results are discarded and replayed through the matched plain native path, with replay inputs/raw output/errors/costs retained. Preflight configuration points fallback to frozen plain/repl, preserving the same QGC response semantics rather than reintroducing the earlier non-GC producer.

In-flight thunk/process-exit cases can end the whole private worker; the plan explicitly turns the current array into operational outcomes rather than silently replaying failed candidates. That failure handling must remain distinguishable from a successful native fallback. Source and helper comments still disclaim arbitrary native globals, uninstrumented FFI/extensions, interactive handles and general process equivalence. The formal result can qualify the unchanged public trusted source regime only.

Exact native outcome comparisons remain essential to the meaning of faster verification, but a separate broad correctness campaign is unnecessary. Preserve all differences, distinguish operational losses from complete/rejected changes, and interpret service speed together with outcomes/resources. A candidate that returns fewer real verifier results by aborting batches has not established useful acceleration.

## Required minimal completion of this same protocol

1. Repair/resolve the actual common native thread-creation condition and retain the failed preflights. This is the current result-invalidating executability defect.
2. Inspect the delivered single runner and freeze its actual command, output path, grouping/failure/EOF/accounting behavior alongside the already frozen binary/library paths. No new control framework or scheduler is needed.
3. Use the real native preflight to establish complete ordered responses, engagement, existing policies, graceful release and resource capture. It is dependency evidence, not a reduced benchmark or a new performance conclusion.
4. Then execute the already declared complete original-source rotated matrix, preserving every outcome and qualified resource limit. Do not pool changed builds or regimes as repetitions.

The method/resource table can report all nine whole-run rows with makespan, grouped latency, outcome classes, observed CPU and sampled fleet PSS; compare private/stock for practical benefit and private/off for component cost. If ordinary native batch matches the useful frontier or the private mechanism costs more, record that outcome and close this constructor rather than restart a table/worker/GPU tuning series. A mixed frontier is reported honestly. Invalid or incomplete output is not promoted to a negative theorem about all native state branching.

This first substantive follow-up strengthens the experiment's competitor and fixes the common interface, but does not yet pass real preflight or authorize a full collector. Root retains implementation and scientific disposition. All four RQs and the complete Lean-first/SMT/RTX5090/paper objective remain unchanged.

## Same follow-up: actual address-space repair reviewed

Root's native-default-thread-failure-observation.json and appended plan revision now provide concrete evidence: the stock failure core has43 threads and12,879,224,832 mapped virtual bytes, only5,677,056bytes below the12GiB RLIMIT_AS value12,884,901,888. The current Workspace parent has RLIMIT_AS(-1,-1), ample observed MemAvailable and a distant cgroup pid ceiling. This strongly supports the address-space-reservation explanation for the common pthread-creation failure; the unreported pthread errno itself remains unknown.

**Accept the proposed common finite benchmark repair for the third preflight:** before the unchanged Repl.start, use its parent's observed RLIMIT_AS soft limit as max_memory_bytes for stock/private/off. With the recorded parent limit-1, all three methods and their native replay children inherit the Workspace's existing unrestricted address-space policy. This preserves native thread defaults and the discovered batch width, adds no persistent setting/quota/entity and removes the demonstrated common setup obstruction without rewarding an avoidably failing baseline.

This is a real protocol deviation from the default12GiB worker policy, now explicitly recorded in the same plan. The resulting experiment can compare matched native-batch methods under inherited address space; it cannot claim equivalence to default-policy Kimina deployment or a fixed aggregate-memory budget. Actual launch/terminal provenance must distinguish Settings.max_repl_mem=12288MiB from the **effective** inherited RLIMIT_AS. All replay-child costs and observed memory remain charged.

The repaired protocol retains paper decision value and does not require a new review round, unrelated correctness project, resource tuning grid or user wait. Actual complete native response arrays, normal EOF and the delivered full runner still need inspection before full collection; the previously failed preflights remain failed and are not pooled as performance repetitions. Root can dispose the demonstrated repair and executable dependencies from their actual evidence within this same reviewed experiment.
