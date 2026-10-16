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


## Supplement: actual finite full execution command and opportunity correction

This is an execution-source supplement to the same result audit, not a new plan-review round or experiment. Root supplied native-batch-integration/full-command.executed.py because the actual OMP reusable CLI delivery remains delayed. I read that entire command and the appended E038 ownership/protocol note. Root owns this one-off native command receipt while OMP retains its exclusive bench runner file; no OMP file is changed by this substitution.

The source explicitly loads and asserts all 29,750 distinct original records and import headers; discovers actual affinity width; loops the three predeclared rotated method blocks; runs methods sequentially; preserves full parsed native payloads without normalization; and labels branch-off separately. It reuses original native Repl.start/_read_response with the recorded inherited-AS repair, the same frozen binaries/library composition, 60-second header/300-second array deadlines and no thread setting. Each failed current batch becomes operational rows; it is not silently retried, and the next original batch gets a fresh worker with preparation/replacement cost inside that cell's wall time. Normal completion closes stdin, drains remaining stdout and waits actual exit, while abnormal retirement uses the native owned-process failure close. Raw outputs and process/resource events use gzip in the caller's existing /tmp output directory. All nine complete cells are required for the full-matrix terminal receipt; an exception leaves explicit failed-terminal and completed-cell records.

The resource differences from preflight are explicit rather than silently pooled: self RUSAGE is labeled collector; RUSAGE_CHILDREN is labeled waited_children; sampled fleet totals include the collector and each PID/create-time/PSS/RSS/VMS/CPU observation is retained. One-second sampled totals are not exact peak bounds. The command does not perform cross-method equality analysis itself; it preserves complete indexed responses for that analysis after terminal collection. Per-case classifications are secondary labels; claims must use the retained native payloads and operational losses, not count equivalence alone.

Two related immediate source defects were sent directly to root before launch:
1. exchange writes stdout.gz only after original _read_response returns a complete frame. That native function holds consumed lines locally; timeout/read exceptions lose those partial lines from the retained raw file, and abnormal retire initially did not drain stdout. Thus the initial source did not implement its promised partial-output preservation.
2. original _read_response wraps readline errors in LeanError("Failed to read from REPL stdout"). The driver's outer string checks for underlying separator/line-limit text therefore do not detect that concrete framing obstruction, and could incorrectly continue predictable invalid batches instead of following the plan's common repair path.

The minimal correction is on the same one-off command: tee bytes as the underlying native line reader consumes them, retain/drain the failure tail after owned cleanup, and retain/examine the underlying read exception rather than only the wrapper's text. No new preflight, quota, transport tuning, schema or correctness project is requested. Until the actual correction is inspected, the original finite-command source cannot be certified for all promised failure/raw-output handling; its successful normal path otherwise follows the fixed comparison. Root may implement this small execution repair immediately and then run the already admitted full comparison. This is not permission to change OMP ownership or silently pool changed method builds.

### Corrected Meta denominator independently verified

I also read E038/opportunity-denominator-correction.md/.json, the original E033/full-observed-category-groups-20261016.json and artifacts/lean-modern-native-compilation-2026-10-14/meta-inventory/meta-observer.c. Independent arithmetic gives:

- outer no-metavariable CPU: 3,078,852,745,407 ns;
- total observed outer CPU: 13,041,048,187,034 ns;
- fraction: 0.23608936193243535 (23.60893619%);
- no-metavariable outer entries: 208,151,681 / 293,112,273 = 0.7101431777986315 (71.01431778%).

The actual wrapper clocks outer calls using CLOCK_THREAD_CPUTIME_ID and accumulates outer_cpu_ns only for timed completed outer returns; entered counters have a different denominator. The root forward correction is right: 23.61% is an instrumented observed outer calling-path thread-CPU descriptor, not a count fraction. Earlier wording in the project/this thread calling it a count fraction was incorrect and should be corrected forward without rewriting the raw evidence.

The correction also correctly declines to multiply that observed denominator by another run's sampled inclusive defeq share as a measured end-to-end bound. It does not identify independent arguments, all native defeq work, full-wall critical-path cost, transfers or GPU readiness. The conditional no-mvar time budget is only inside this observed wrapped path. No new GPU implementation is justified by this denominator alone. This fixes a material explanation error while leaving raw data and the full research objective intact.


### Execution-command correction inspected and closed

I inspected the actual diff from retained, unexecuted full-command-before-raw-tee.py to full-command.executed.py and independently parsed the corrected source with Python ast.parse. The two reported execution defects are repaired on this same command:

- Immediately after original Repl.start returns, already-buffered native stdout bytes are copied once, and the existing StreamReader.feed_data is wrapped to gzip-write every arriving raw byte before the original reader receives it. There is no await between initial-buffer capture and installing the wrapper. Original _read_response, blank-frame parsing and its actual line-buffer policy remain unchanged. Successful exchange no longer writes parsed frames a second time.
- Normal and failure retirement start a stdout drain concurrently with process wait/native close. Bytes are already preserved at feed_data, including bytes a parser later consumes/discards; draining permits remaining output to reach EOF. An already-dead native process's ProcessLookupError is handled by awaiting its terminal process status.
- The actual failure receipt now traverses cause/context links, with cycle protection, and persists their repr strings. A native readline line-limit failure wrapped by LeanError remains visible to the existing fatal-transport condition. Failed arrays remain operational and are not silently replaced by retries.

No changed native method binary, input population, resource limit, timeout, outcome comparator or OMP-owned file is introduced by this repair. This is source inspection, not another empirical preflight and not a claim that every future operational fault is impossible. The remaining observed-path limitations and sampled resource caveats above still hold.

**Execution-source disposition: no remaining immediate result-invalidating source blocker identified. The successful third native preflight and this corrected actual finite command support proceeding now to the already declared complete 29,750-source, three-method, three-rotated-block comparison.** Preserve this command/frozen v1 identity and its eventual raw/terminal records; do not spend another round repeating the same preflight or broadening correctness work. Full-run completion, native-value comparison and scientific outcome still depend on those real terminal results.
