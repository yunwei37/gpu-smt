# Independent E038 native-batch preflight result review

Reviewed 2026-10-16. This is a result audit of the three retained native-batch preflight attempts, not a second plan-review round or a whole-paper verdict. I read the human instruction log, intact Initial Narrative and RQ3 promise, current evaluation/closest-work map, E038 plan including its frozen native-batch contract and inherited-address-space repair, the prior protocol review, current Lean/C++ implementation and runtime patch, actual build/relink receipts, executed preflight drivers and raw terminal/stdout/stderr/resource files. I independently recomputed input identity, full native JSON equality, engagement counts and sampled resource maxima. Only this report is written; no implementation, runner, canonical document or Git operation is changed.

## Five judgments

| Judgment | Result |
|---|---|
| Protocol validity / run status | Third preflight is valid executable dependency evidence for the stated trusted-source native-batch boundary. Attempts 1 and 2 are invalid performance comparisons and remain separately retained. The full corpus matrix is not completed or certified by this review. |
| Hypothesis outcome | Inconclusive for RQ3 and the planned full comparison. The one successful 24-source setup is adverse to the current private implementation, with no observed memory advantage or acceleration. It cannot establish a replicated corpus-level effect. |
| Evidence value | Dependency-only preflight inside the admitted E038 comparison. It establishes a real source/native baseline/interface/measurement path, not a separate scientific contribution. |
| Contribution risk / paper impact | Mechanism/workload boundary only. Stock native naive batching already shares the prepared command state. Ordinary co-location, compilation or immutable-root reuse therefore supplies no new contribution. The candidate currently adds expensive runtime version/lifetime work, whose benefit must survive this real competitor and full costs. Arbitrary FFI isolation and complete interactive API semantics remain unqualified. |
| Next decisive work | Inspect the actual OMP-delivered runner, freeze its command and bookkeeping, then execute the already declared complete original-order comparison under the repaired common policy. Preserve all outcomes and adverse costs. No extra correctness campaign, baseline grid, quota, GPU kernel or new experiment is needed to admit that work. |

The user's request is timely real performance evidence, followed by honest negative-route disposition and complete paper evidence. This preflight resolves executability; it should not become another extended cycle of tiny controls or healthy-process polling.

## Input and native comparison independently checked

The authoritative input has 29,750 JSONL records. The retained preflight-original-inputs.jsonl is exactly the first 24 records of that file, not a selected-success subset: Proof_00000 through Proof_00023, 24 distinct original identifiers. Each original code begins with exactly `import Mathlib\nimport Aesop\n`. The driver sends those imports once and replaces just those two original import lines by two newline characters in each candidate body. All subsequent source characters and line positions are retained. Batch width is the observed affinity count, 24; no proof/thread flag or source rewrite obtains the result.

The strong competitor is the actual retained same-toolchain QGC/header-repaired native REPL, not the earlier non-GC producer or a process-per-proof strawman. Its `runBatchVerify` with `mode:"naive"` obtains env 0's prepared Command.State and invokes `runCommandGCAux` in native IO.asTask tasks, with ordered result collection. That helper performs the same processInput options, message/sorry/tactic/tree extraction and returns env none. The candidate calls this same implementation through runCommand with gc=true and env=0, drops returned StateT state, and exposes the same native result array. The passed BatchCommand has no internal timeout. The native stock and candidate paths therefore genuinely engage the intended full candidate parser/elaborator/tactics/checker/result extraction in this setup. The branch-off executable is a component control, not another main baseline.

I parsed all three raw preflight3 batch.stdout files, required each to be a list of exactly 24 entries, compared their complete parsed JSON values without removing fields or normalizing environments, and compared each with its terminal.json responses. All comparisons are exactly equal. Array elements include native empty objects and native messages; equality is not merely equal accepted counts. Stock uses pretty output and the candidate compact output, so this is exact JSON-value equality, not identical raw byte formatting. Header env=0, complete_array=true, normal_eof=true and exit_code=0 are recorded for all methods.

The successful preflight validates this public trusted input prefix only. It does not cover the other 29,726 original attempts, all supported artifacts/history/cancellation cases, unknown native extensions or arbitrary programs. That scope is sufficient to proceed to the actual comparison without demanding a separate broad correctness project.

## Failed preflights are not successful outcome evidence

### Attempt 1: bytes-capture defect

All three native workers returned far enough for the driver's header read, then Path.write_text received the bytes returned by original Repl._read_response and raised TypeError. No proof batch ran. The driver used native failure close, producing -9 exits. Its printed ALL_NATIVE_OUTCOMES_EQUAL true compared three absent responses (None==None==None). That is explicitly invalid equality evidence. Root's subsequent byte-safe write and complete-array predicate repair are appropriate. These failed captures must never be pooled with successful timings or counted as verified attempts.

### Attempt 2: common actual native thread failure under 12 GiB AS

After byte capture was repaired, all three workers returned a header, then aborted with exit 134 and native stderr `failed to create thread`, before a complete proof array. The JSONDecodeError is a consequence of empty response output, not proof that source parsing or JSON framing was the primary fault.

The retained stock core observation has 43 threads and 12,879,224,832 mapped virtual bytes, only 5,677,056 bytes below the 12,884,901,888-byte address-space limit. The distant cgroup pid ceiling and available host memory do not support claiming a process-count or physical-memory exhaustion. The generic native exception does not retain pthread errno, so address-space reservation is strongly supported rather than a fully diagnosed errno-level proof. This is enough evidence for the recorded common benchmark-local repair; another diagnostic campaign is unnecessary.

### Attempt 3: recorded common inherited-AS repair

Before unchanged original Repl.start, each method's max_memory_bytes is set to the parent's observed RLIMIT_AS soft limit, -1. The actual Repl.start still creates lake env in its own process group and sets both native child AS limits to that passed value. The third receipts explicitly retain nominal settings 12288 MiB and effective_RLIMIT_AS=-1. This removes the same demonstrated obstruction for every method without tuning thread count, affinity width or source.

This is a real comparison-policy deviation from default Kimina's 12 GiB per-worker virtual-address limit. It must remain visible in final methods, commands and result interpretation. The experiment is matched native-batch verification under inherited Workspace AS, not a result under deployed default Kimina memory policy, and not an equal aggregate-memory-cap result. No persistent default is changed by this finite repair.

## Native implementation, executable provenance and engagement

The frozen-paths receipt identifies batch-frozen-v1/plain/repl and private/repl and their separate library directories. Current NativeBranchBackend.lean is byte-identical to the frozen Lean source inspected. Actual successful build receipts cover Lean-to-C, C/backend entry, helper DSO, private/plain shared runtimes and executable links. Both shared runtimes include the same upstream util/shell.cpp object needed by original lake env. Relink uses the actual directory-encoded generated initializer after the initial link error. The plain path replaces the three modified runtime objects with upstream counterparts; the private executable includes the branch helper and modified runtime. Original producer binaries are not substituted or overwritten. These are build receipts and source evidence, not performance wins.

Private stderr has exactly one gpu_smt_batch record containing 24 ordered metadata entries. Independently summed:
- 62,678,594 reference operations, 1,061 private reference versions;
- 24 private thunk versions and 5,616 admitted descendant tasks;
- zero marked fallbacks, zero non-null discarded responses and zero fallback child results;
- internal_ready_ns <= released_ns <= completed_ns in every entry.

Branch-off has exactly 24 metadata entries, zero ref operations/versions/thunk versions and 2,287 descendant tasks. It still executes branch bookkeeping and modified-runtime allocation/free/task hooks; it is not identical to the plain stock runtime and should not be relabeled as such.

Source inspection confirms the private route resolves prepared refs into private versions on first *access*, including reads, rather than only on writes. Its owned_here path locks the one global registry mutex for every enabled ref operation, and ref_ops itself adds a hot atomic increment. The large operation count plus native system-CPU increase makes hot-path synchronization a plausible substantial cost. The present preflight is not a profiler or causal proof of a unique bottleneck; the report must not assert that all slowdown is mutex time.

endBranch waits admitted tasks/scopes, destroys held versions/original ownership and returns before released_ns is observed. Its drain_seconds counter is formatted before clone destruction and therefore is not complete cleanup time. The recorded released/completed intervals and complete EOF wall boundary avoid that mistake. Listed filesystem/process guards and cold native fallback remain in the implementation; this preflight happens not to exercise replay. Prior actual fallback control is separate setup evidence, not a fallback-frequency result for the full corpus. In-flight-thunk/process-exit worker termination remains an operational batch failure, not successful replay.

## Costs recomputed and their limits

The following are single preflight observations, preserved to expose actual cost rather than to advertise a corpus speedup or a statistical result.

| Method | Header s | Batch response s | Whole start-through-EOF s | Waited child-tree user+system CPU s | Sampled tree PSS MiB |
|---|---:|---:|---:|---:|---:|
| stock native naive | 3.816255041 | 13.894735747 | 18.187631345 | 36.834280 | 1888.827 |
| private branch | 3.831148437 | 22.560584338 | 26.865098890 | 136.825640 | 1898.390 |
| branch-off control | 3.753769201 | 14.431149537 | 18.596853699 | 39.198602 | 1897.988 |

Private whole wall is 1.4771x stock (47.7% longer) in this one prefix observation. Its user/system split is 55.618291/81.207349 CPU seconds versus stock 34.882652/1.951628. No speedup exists in this setup; no useful PSS reduction is demonstrated. Order/load/warm-state effects and this small source prefix prevent treating those ratios as the final full-workload result.

The driver begins wall time immediately before original Repl.start, records header and complete ordered-array response, closes stdin, waits actual normal process termination, drains stderr to EOF and records exit status. This includes preparation, native verification, branch/replay work if present and normal release. It does not equate a frontend response with all retirement. The 300-second batch request deadline is a common external array deadline, not an independently enforced 300 seconds per proof. All members share their batch's observed emission; eventual latency percentiles are grouped offline native-batch latency, not a live offered-load/interactive service frontier.

RUSAGE_CHILDREN deltas are taken in the isolated sequential preflight Python process around each method and only after waiting for its launcher. On Linux, waited descendant usage can propagate through the launcher. This is more credible than summing only surviving psutil process CPU counters, and no competing benchmark child is created by this driver. It remains a waited-child-tree counter: the Python collector/sampler's own CPU is not included, and escaping/unwaited descendants on failure are not magically accounted for. Do not label it exhaustive whole-system CPU. The whole wall interval includes sampler/transport interference.

I recomputed each PSS and RSS maximum from resources.json; all equal their terminal receipts. There are 17/25/17 sample rows for stock/private/off, nominally one second apart plus sampling overhead. Visible PID sets consist of launcher plus native worker; no fallback child is observed. These sampled maxima are not exact peak bounds. Short-lived descendants/read failures can be missed, PSS depends on simultaneous external sharing, and summed RSS double-counts shared pages. Report sample interval/timestamps and qualified tree PSS, do not promote the roughly 10 MiB single-run difference to a memory claim. Full matrix repetitions remain required for uncertainty.

## Minimal remaining work and disposition

The OMP-owned run-native-batch-comparison.py did not yet exist when checked during this audit. This review cannot certify an undelivered collector's restart/partial-capture behavior. Root should inspect the actual delivered file for the already agreed properties: every original record in original order, the common actual native batch contract and effective AS policy, continuous stdout/stderr handling, explicit operational rows for failed arrays, no silent retries replacing outcomes, charged restart/preparation/replay and final EOF, same sampled resource method, gzip output on existing /tmp, and exact complete native JSON comparisons.

No new workload or baseline is requested. Once that implementation is inspected, the successful third preflight resolves the previously blocking path. Proceed to the declared rotated complete-corpus runs; do substantive mainline integration/writing while they execute and gather terminal records rather than spending goal turns polling healthy row counts. Keep binary/library variants frozen throughout a capture. If implementation is changed to reduce the observed hot-path overhead, record a new concrete method version and do not pool it with v1 as a repetition.

The full comparison should decide whether this native-state isolation constructor delivers any useful joint outcome/time/CPU/PSS tradeoff beyond stock native batching. A complete adverse result should be recorded and the constructor closed without another narrow GPU kernel or unrelated tuning grid. A positive or mixed result still needs a defensible differentiation from existing services, caches and snapshots; ordinary native compilation is not that differentiation. All four RQs, broader Lean/SMT/GPU scope and full paper gates remain open.
