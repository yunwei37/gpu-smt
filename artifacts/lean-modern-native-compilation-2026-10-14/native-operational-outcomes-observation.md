# Native operational outcomes in the full producer workload

Observed 2026-10-14T23:29:48.293768+00:00

The ongoing full matrices preserve operational outcomes. At the observed native-AOT prefix26961/29750,49 outcomes were operational:38 stock300second timeouts and11 HTTP JSON-decode errors. This is a partial-population failure characterization, never a whole-performance estimate or exclusion rule.

The stock Python service starts Lean with stderr=PIPE but never reads that pipe; its error_file is a different unused TemporaryFile. After stdout EOF, _read_response returns empty bytes and json.loads raises before the later error-file handling. This explains the generic decode label, but source inspection alone does not prove a stall or memory failure for every source.

Root directly replays original published Proof_02269 (author statusok, elapsed34.88s) through the same SDK/native-GC executable, native DSO manifest, import/body protocol,12GiB virtual-address allowance andCPU0–3 eligibility. Native stderr is captured to a file rather than left unread. The process exits1 normally after23.04s, header emits env0 and body produces no JSON; stderr is exactly "INTERNAL PANIC: out of memory". Thus this one decoder failure is a native allocation failure under the existing service allowance, not a response-parser correctness issue. This diagnostic time is not a performance comparison; background and stderr transport differ.

The12GiB allowance and300s timeout are inherited stock-service defaults, not new experiment limits. Alloriginals, including author-accepted sources that fail under those defaults, remain in complete acquisition and outcome counts. No removal, relaxed memory setting, retry-to-success, response normalization, or active-code mutation is applied. Do not classify every decode error as OOM from this single replay, infer hardware exhaustion from RLIMIT_AS, or blame sharedGPU use.

The current full comparisons answer version/default-service-scoped complete verification performance. They cannot establish unlimited-native success for allreleased proofs or exact published-author parity. Negative OOM/timeout outcomes and any method-dependent differences must be shown alongside whole walltime/throughput. The pre-existing source-level stderr handling defect is documented; changing the running service or its reporting during a matched acquisition would change its protocol, so it is not silently patched.

Raw evidence: [original source and receipt](native-eof-original02269/receipt.json), [stderr](native-eof-original02269/stderr.raw), [stdout](native-eof-original02269/stdout.raw), [replay command](native-eof-original02269.py). This is folded-in execution diagnosis, not an additional paper experiment, contribution or independent audit.
