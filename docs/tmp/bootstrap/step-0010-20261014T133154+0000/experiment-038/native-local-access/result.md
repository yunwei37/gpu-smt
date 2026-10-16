# Native local-access implementation result

Observed 2026-10-16 UTC. Supporting implementation work within E038; not a new standalone paper experiment or completed RQ. Root authors Lean/GPU/runtime code, while existing OMP owners retain README/docs/paper/reusable experiment scripts. Main before this delta is 7b97c20.

## Reason and implementation

The unchanged v1 full comparison remains active on frozen binaries. Its setup observation showed substantial private-path overhead, but no profile causally attributes it. Source inspection identifies two avoidable operations in the resolver: shared atomic instrumentation at every ref/thunk access and repeated locking of a context's stable original-to-version mapping. This source finding motivates an algorithm-detail optimization, not a claim that either cost explains the measured slowdown.

Root changes only bench/lean-native/native-ref-branches.cpp:
- Thread-local ref/thunk counts are flushed to the branch totals before task context entry, restoration and root branch end. Normal terminal totals retain the resolver-entry meaning. Mid-scope shared totals can now lag; they must not be used as instantaneous progress.
- Each thread retains one last ref version and one last thunk version, keyed by full live context ID and original pointer. Only mappings whose original and clone are already held until the context drains can populate the cache. A hit skips the repeated map mutex; misses keep the existing locked authoritative map.
- No adjustable capacity, admission cap, service policy, namespace, scheduler, model or persistent runtime setting is introduced. Native primitive ref atomics, ownership/tag rules, task registration and supported-effect limits remain.

The before source, actual build command, native command and raw results are retained here. Independent source-review.md evaluates the actual control paths and lifetime assumptions. Ordinary caching is supporting engineering, not scientific novelty.

## Actual separately versioned build

build.executed.py reuses the recorded exact native toolchain and link composition. All three commands return zero: helper DSO, shared runtime, native REPL. New outputs are under /tmp/gpu-smt-native-ref-branches-20261016/local-access-v3/private. The existing owner-cache-v2 static archive and compiled shared compact object are reused, including the ref identity/tag-clear behavior.

The executed helper source is /tmp/gpu-smt-native-ref-branches-20261016/local-access-v3/native-ref-branches.executed.cpp and byte-matches the current repository source. No frozen-v1 or v2 binary/DSO is overwritten. candidate-paths.json and per-command JSON/stdout/stderr give exact paths, flags, UTC, compiler CPU and exit status. This is native runtime engagement, not an LD_PRELOAD claim.

## Actual original-source validation

native-check.executed.py is the previously executed one-source native check with only prospective candidate/report paths changed. It uses the original Kimina Repl.start/_read_response, same native library manifest and original Lean4.27 Mathlib source, inherited Workspace AS policy and original native thread environment. PID2047132 started at 2026-10-16T15:41:23.377729Z and completed at 15:41:33.132259Z.

native-check1/ preserves complete original input, launch/terminal/cell records, raw gzip stdout/stderr, decoded response, events and resource samples. The archived original input dictionary exactly matches the first untouched record of artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl, Proof_00000. No generated fixture or normalized replacement input is used.

Native stdout contains the prepared header response env0 followed by [{}]. The one candidate result is exactly {}, with complete outcome, normal EOF and exit0. Branch metadata records owner_cache_tag1, ref_ops8905059, ref_versions43, thunk_ops1, thunk_versions1, descendant_tasks244 and fallback=false. The exact ref/thunk totals agree with the earlier v2 original-source observation; the descendant task count is scheduler-dependent (v2 recorded245), not asserted invariant. This finite agreement supports source-path engagement and proportional validation, not general correctness or proof of exact counters for every execution.

## Costs, limitations and disposition

The command retains whole/request/resource data and reports zero sampling-read errors. It runs during frozen-v1 capture and therefore supplies NO comparative performance result. The finite compiler and this native validation are competing CPU load for the active full run; development-overlap.json links their actual UTC and CPU receipts. Do not claim exclusive resources, silently remove affected baseline data, pool candidate versions or infer a speedup from either co-run duration.

Unsafe ShareCommon.Object.eq/hash header observation from v2 remains an experimental limitation. General globals/FFI/interactive continuation support remains unqualified. TLS counters rely on the existing admitted root/task/scope drain lifetime, full context IDs and no abnormal-exit terminal claim; old cached pointer representations are not dereferenced for a different context. Source review is not an isolation theorem.

Disposition: retain this separately built prospective candidate and original evidence. Continue the existing complete frozen-v1 comparison, collect terminal results once, and use the full native outcome/cost evidence to decide subsequent comparison value. Do not replace its running artifacts or start an overlapping formal matrix. No GPU backend, new paper contribution, closed RQ or completed writing/review gate follows from this implementation checkpoint.
