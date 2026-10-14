# Independent real-group dependency qualification review

Reviewer: `/root/lean49_real_group_qualification_review`, gpt-6.1-sol. Reviewed 2026-10-10. This reviewer had no execution or implementation role and did not rerun the workload, modify root code/canonical documents, or perform Git operations. `docs/user-instruction.md` was read first; the actual complete `research-experiment-design/SKILL.md` was consulted. This is a finite dependency review, not the experiment008 result review or step outer audit.

## Judgment

- Run status: **valid for this bounded dependency qualification**.
- Tested hypothesis: **supported locally**: the executed stock-native full-snapshot adapter supplies prior trees, engages unchanged-command reuse, and preserves each producer response on this one actual 32-candidate task group under the three recorded histories.
- Research value: **dependency-only**. No complete-corpus result, system superiority, RQ answer, or new reuse algorithm is established.
- Paper impact: a baseline implementation boundary is now qualified beyond two unrelated inputs. The next decision is to retain this as readiness for the properly admitted, matched full-corpus comparison; do not turn it into a headline speed or isolation result.
- No material issue invalidates these retained 32-input comparisons.

## Independently recomputed evidence

The reviewed directory is `artifacts/lean49-native-snapshots-2026-10-10/actual-group-20261010T075309+0000/`. I read its runner, analyzer, input receipt, commands and terminal exits, all fresh result/stdin/stdout records, and all three native output streams. My independent Python inspection did not import or execute the retained analyzer. It checked every raw response and each input, rather than relying on the existing summary.

The copied original first completed model-task record is byte-identical to the first line of the retained miniF2F full-capture stream, including its newline. Its SHA-256 with newline is `b1c1b91a602aea2ffe5facfac98fdddaba7aeae30a7bd78180ec5ea6f48aeab1`; the receipt's `d5d034ac5ac2c4d61ac5400fb5912a087a8a471de5124ae5c4b94894f9674c1c` hashes that same line without its trailing newline. The receipt therefore does not identify different candidate bytes. It is task row 0, `mathd_algebra_478`, with 32 model outputs and 32 distinct full candidate strings.

All 32 `{name, code}` rows equal the original task's ordered `full_code` entries. The fresh archived codes file is byte-identical to `codes.json`; every fresh stdin command equals its corresponding candidate string. Every forward input contains the exact recorded header and code at its declared index. Reverse input is exactly the forward list reversed. No candidate replacement, trimming, deduplication, or preflight insertion was found.

All four wrapper commands have start/finish receipts and exit 0. Fresh capture has exactly 32 admitted/launched/result entries and a shutdown listing all indices with no missing result. Every fresh request is `status=exited`, returncode 0, error null; all recorded stdin/stdout/stderr byte counts and SHA-256 values match. The native streams each contain exactly 32 unique indices covering 0–31, with no adapter errors, fallback, missing response, or nonempty import diagnostics.

| Native order / retirement | Responses matching fresh | Old snapshots supplied | Observed consecutive reused task prefix |
|---|---:|---:|---|
| Forward / 256 | 32/32 | 31 | 0 once; 2 on 31 rows |
| Reverse / 256 | 32/32 | 31 | 0 once; 2 on 31 rows |
| Forward / 16 | 32/32 | 30 | 0 twice; 2 on 30 rows |

All **96 full response JSON objects are exactly equal** to the corresponding fresh object, even before handle normalization: fresh and adapter env IDs are all 0. This preserves ordered diagnostics, positions, text, default AST and field presence; no sorry records occur here. Independently applying the original producer interpretation gives **28 complete and 4 rejected**, at sample indices **5, 10, 13, 28**. These rejections remain rejections in every native variant. Recorded local declaration fingerprints also agree across all three histories, but they are only additional structural observations.

The no-old-tree observations occur at index 0 for forward, index 31 for reverse, and indices 0 and 16 for retirement. This matches the declared retirement boundary. Each complete diagnostic list equals recorded import diagnostics concatenated with response messages; the final-command-state observation is true for all 96 rows.

## Executed implementation and mechanism

I reviewed the **archived executed-build13 source**, not any later streaming extension. Its SHA-256 is `eb4b573eda12de93c0cd9206d82f3d798bfa2c9b2cb4871d265480177063871a`; the executed-build13 binary is `7e3a95470667785849b30662b575ed1a2350cb223ce6c12b219eafe2830855d2`. All seven source/helper/generated-C/current-binary/REPL-library/toolchain/manifest hashes in `build-13.json` matched at inspection. The qualification runner pins the separate executed-build13 binary and asserts its digest.

The pinned Lean4.9rc1 `IO.processCommandsIncrementally` source consumes the same initial command state and optional prior incremental state, waits through the command chain, collects snapshot messages/trees, and returns the final command state. The adapter passes the original post-import state for each candidate, not the previous candidate's final declaration environment. The pinned producer's `processInput` uses the normal nonincremental command frontend and its `runCommand` serializer supplies the compared response. Local package revisions are represented by retained source archives/path manifests rather than live `.git` repositories; the original setup records and binary/library hashes remain the version evidence.

The observed pointer count is a direct engagement discriminator for the stock unchanged-command path: the source explicitly reuses `old.data.finishedSnap` for unchanged command syntax. The candidates share the `set_option` and `open` command prefix before a changed theorem proof. A count of 2 establishes reuse of that prefix; it does **not** establish unchanged theorem checking, reuse inside the changed proof, two reused expensive checks, or saved CPU time.

## Limits and nonblocking cautions

This group is one actual formal-benchmark task, not the full 430-task/13,760-attempt workload and not a feedback-driven online stream. Two fixed permutations and one retirement setting provide local predecessor/rejection/retirement evidence, not arbitrary branching or a history-isolation theorem. Retirement drops roots in the same process; it does not establish memory reclamation, cancellation, cross-request security, or bounded service memory.

Native failure responses can still leave a declaration fingerprint, as these four rejected inputs do. Their fingerprints cannot be read as acceptance or kernel proof equivalence. Response parity also does not independently prove original-statement preservation or audit all axioms/imports.

Timing and GNUtime records are diagnostic. Fresh launches one process per request whereas the adapter retains native roots; cold-launch savings do not establish novelty. All commands use CPU1/one Lean thread and overlap ongoing CPU/GPU research; affinity does not establish isolation. No speed, memory or per-request latency conclusion is warranted here.

The retained analyzer's `unknown` enumeration is narrower than the complete fresh interpreter's possible error statuses. That does not alter this result: independent inspection found only valid terminal responses and explicitly checked adapter-error absence, coverage and all fresh result statuses. A later broader corpus analysis must classify **every** non-complete/non-rejected/non-incomplete transport/native/adapter outcome as unknown rather than relying on this short list. This is a future analysis caution, not a reason to rerun these unchanged valid records.

## Changed boundary follow-up: build14 streaming transport

Root requested review of a new execution boundary, not rereview of the unchanged build13 scientific result. I reread the direct instruction log, then independently examined `build-14.json`, the archived `executed-build14-Lean49NativeSnapshots.lean`, the recorded `streaming-build14/executed-capture.py`, all 32 streaming request artifacts and the 70 lifecycle events. No workload was rerun.

Build14 changes only file/stream acquisition and loop handling: the native adapter now reads one line at a time from a file or persistent stdin. The stock per-candidate processing/root/oracle implementation is unchanged. Archived source SHA-256 is `704c9602c41207690848fe6134b5e73c5a7523c5ed9a72441d95946d59d45560`; executed native binary is `2a96e011a5f36ec01dbc86fa34717ce121988a4f9f519d98ae4a5ca0d8d0c553`. The recorded generated-C/library/toolchain/manifest/binary identities match retained files. Executed transport SHA-256 is `2ef72989dcb04de9b76fcdc4bbbe13de1bfd8f3cbb1539ece71790b3371a5ff9`, matching the archived script and original run event. This is distinct from any subsequent root edits to the current transport source.

The streaming capture uses exactly the same 32 code bytes and unchanged task metadata/header (the metadata task row omits model output fields; it does not alter the input). All per-request stdin payloads map to their exact original index/header/code. Input archive hashes match run provenance. All 32 result records are `status=response`, error null, and report every stdin byte written. Every saved `response.bin` equals its native observation and the fresh producer object **without normalization**. The original 28 complete/4 rejected identity is unchanged, and declaration fingerprints match the build13 forward observations.

There are exactly two launched owned sessions, with 16 candidate responses in each. Session stdout equals the concatenation of its 16 per-request raw native frames byte-for-byte. Native old trees are supplied 30 times; prefix count 2 occurs on those 30 rows and 0 on indices 0 and 16. Both import diagnostic lists remain empty, complete diagnostics equal response diagnostics, and no adapter/fallback/transport unknown occurred.

Event sequence is contiguous, clocks are monotonic, all 32 `whole_job_begin` entries have corresponding `whole_job_end` entries, and shutdown lists all 32 completed indices with no supervisor signals. Each deadline equals its admission begin plus 300 seconds within float-to-nanosecond rounding. Each recorded invocation duration exactly equals end minus begin, and each native operation duration equals its frame's native clock and is no greater than the whole invocation duration. All observed responses arrive before their deadlines.

The session replacement records report returncode **-9** for `retire_limit` and final `shutdown`. The archived supervisor deliberately kills only the new-session owned process group after its completed responses. These two codes are lifecycle disposal receipts, **not** failed proof responses or evidence of OOM. The per-candidate clock starts before persistence/setup/possible prior-process retirement and ends after response or synchronous owned error cleanup. Corpus clocks also include input/event persistence, startup and final shutdown. This is a serial closed-loop transport, not offered-load latency or a concurrency experiment. It provides no CPU or memory accounting by itself.

Source inspection shows that timeout/interruption/EOF/parse/index failures are retained as distinct transport statuses and the owned process is discarded; native adapter errors remain `adapter_error`, never proof rejection. These branches were not exercised by this successful run. Deadline polling governs response acquisition; synchronous persistence/setup/cleanup is not a proven hard wall-clock cancellation bound. SIGKILL ownership also does not establish behavior of children that deliberately escape the process group.

The executed transport has two future failure-handling deficiencies: a malformed non-object frame/record can escape later persistence code after the receive exception is caught, and stream handles opened before a failed launch are not covered by the `proc is None` cleanup path. Neither occurred in this complete run, so neither invalidates its local response qualification. Root reports fixes in the **current** source, plus provenance for the imported warm helper; those fixes are not retroactively attributed to the archived executed script and were not independently executed here. A later formal run should pin its actual corrected transport, retain all malformed/launch-failure/timeout outcomes as unknown, and record the imported helper version.

The actual streaming event records `XDG_CACHE_HOME=/workspaces/.agent-state/cache`, whereas the earlier fresh group records the Lean4.9 capture cache path. This does not alter these exact response checks; it prevents treating the diagnostic durations as a fully matched numerical comparison. Future baseline timing must explicitly match or disclose environment/cache/retirement policies, including the intentional fresh versus persistent process distinction.

Follow-up judgment: **valid dependency-only qualification for build14's successful serial streaming path and two-session retirement on this actual group**. No material invalidating issue was found for these retained records. Complete-corpus fidelity, error-path behavior, cancellation, general isolation, memory reclamation and superiority remain unestablished. The prior limits and required properly admitted comparison remain unchanged.
