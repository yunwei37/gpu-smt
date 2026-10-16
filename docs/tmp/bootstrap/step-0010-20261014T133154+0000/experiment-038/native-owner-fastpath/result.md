# E038 prospective native ownership-cache implementation

Root,2026-10-16. Same open RQ3 mechanism. This is implemented and natively exercised supporting engineering while the original full comparison continues; it is neither a new scientific contribution nor an accelerated full-corpus result.

## Why this change

The actual matched24-source preflight found private26.865s versus stock18.188s with no PSS advantage. Private performs62.68M resolver reference operations and consumes81.207systemCPU seconds versusstock1.952s. The resolver unconditionally took a global mutex/map lookup even for refs created within the current candidate. That is a concrete avoidable implementation cost; the previous preflight does not prove every excess CPU second was spent there.

## Implementation and support boundary

Use the existing native LeanRef m_other byte as an immutable owner-cache tag initialized before publication. Reserve a tag for its context and every tagged live ref; only release the context reservation after descendants/scopes and held clone cleanup. A surviving ref prevents its tag being reused by a new context. Keep the complete64bit owner registry, and use its original lookup whenever no cache slot is available. Cache capacity therefore does not reject, wait or cap branches.

Native object size, value position, RC representation and task ownership remain unchanged. Creation/free and foreign/prepared-ref version lookup still synchronize; existing hot ref_ops counter remains, so there is no claim to remove all synchronization. Tags created in a copied/serialized ref cannot carry ownership: both compact insertion and loading clear that byte. The new static and shared runtimes must include those compact.cpp hunks, not only the helper.

Independent source inspection confirms those ordinary native lifecycle paths and explicitly identifies a limitation: direct unsafe ShareCommon.Object.eq/hash on refs observes m_other, although normal sharing excludes refs and ordinary ref pointer identity is unchanged. Manual header manipulation/copying/external allocation and arbitrary FFI remain unqualified. Root accepts this stated experimental boundary rather than opening a separate unsafe-program correctness project or claiming transparent arbitrary-process equivalence.

## Actual validation and provenance

Syntax checks pass for helper and compact. Actual helper, static/shared compact objects, runtime archive, shared runtime and existing native backend executable build/link all exit0. Both link compositions contain the new compact object. The entire prospective method lives at /tmp/gpu-smt-native-ref-branches-20261016/owner-cache-v2; active batch-frozen-v1 artifacts remain unchanged. Source snapshots, actual commands/stdout/stderr/exit/CPU/UTC and reverse-patch qualification are retained. Current helper source equals the actual compiled snapshot byte-for-byte.

One untouched original Proof_00000 is run through the same actual native start/header/BatchCommand/gc path with the new method. Complete original JSON input is retained. Native header env0 and response array[{}] match the earlier same-source stock JSON exactly, without normalization. Native metadata reports owner_cache_tag1,8,905,059ref accesses,43versions,245descendant tasks,one thunk version,zero fallback. Worker exits0 with normalEOF. An independent reviewer reads both actual native raw responses and original input, and confirms the new compact objects were linked. One sampling read error remains recorded.

This single-case check establishes executable engagement only. It does not cover cache exhaustion/reuse across the full corpus, arbitrary source isolation, unknown unsafe code or all native artifacts. Native completion is not inferred from response-ready or drain_seconds alone.

## Measurement disposition

The finite development compiler work totals5.941406CPU seconds, and the one native verification overlaps the original full capture's rep1-stock. Exact UTC/CPU/wall provenance is in development-overlap.json. Sampled PSS/RSS and waited native/collector CPU remain raw evidence, with the sampling error retained. These simultaneous runs supply NO valid v2-versus-v1/stock latency or memory comparison; do not reuse their durations as a claimed improvement or silently pool v2 into v1 repetitions.

The9-cell267750-attempt full capture remains fixed to v1. Later evidence must retain method identity and original outcomes. No extra GPU kernel, baseline grid, thread setting, cache admission quota, model/service/Workspace change or complete-paper claim follows. A source cache is ordinary implementation engineering; contribution and the useful outcome/time/CPU/PSS frontier still need the full experiment and prior-work comparison.
