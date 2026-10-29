# Standalone failure-cache skeleton

Direct user request:implement the Rust failure-cache skeleton and unit tests on
G10;formal activation/measurement waits for lab. Scope may touch additive core
contracts,standalone engine module,focused tests/example/API docs;must not touch
Engine verification,CLI/HTTP schemas/defaults,existing native adapters or frozen
collector/native sources. Keep four existing crates and existing CI discovery.

Backend owns opaque scope,input key,state and failure-transition payload. The
captured input binds scope before original execution,so a restart cannot label
an old record as new. Only qualified ordinary failure payloads enter the store;
ineligible completions evict a previous entry for that input. Unsupported/miss/
cancelled requests fall through unchanged. On a hit,the backend must revalidate
scope/current state and budget before applying post-state,diagnostics and original
action heartbeat charge. False must not commit effects;errors stay operational.
No whole-source Outcome is manufactured. Store locks cover metadata only.

Tests use an explicit non-Lean adapter to exercise ordinary state effects,
heartbeat debit,insufficient budget,scope/input changes,unsupported inputs,
cancellation,ineligible invalidation,backend fault propagation and reentrant
cache access. Compile/run an explicitly simulated public example;no native
certificate/replay guarantee or performance claim.

All target/registry/log outputs use existing PVC. Current free space is~3GB:
use single-job validation with incremental compilation/debug symbols disabled
for test builds only,not a measured engine runtime setting. G10 CPU6–7;no formal
Lean collection. Run relevant tests first,then documented fmt/clippy/workspace
tests/rustdoc and existing CI. Preserve unrelated dirty paths and all raw results.
Root self-review only under the explicit no-agent requirement.

## Self-review refinement before publication
The initial boolean return could be confused with a successful tactic return.
Replace it with Option<backend-native Exception>: Some requires propagation
through the original native failure/backtracking path; None has no effects and
falls through. Keep operational Err distinct. Remove unnecessary Clone bound
on backend keys and Sync on exclusively owned state; retain Send/Sync where
the async storage actually needs them. Explicitly include tactic/options/hidden
state in compatibility and constrain key methods to nonblocking metadata.

Local full-suite attempt hit errno13 killing an owned same-UID child on G10;
an exact local exclusion exposed a second existing signal-dependent regression.
Do not weaken those tests or CI. Retain both failures, complete feasible
non-signal checks locally and use unchanged full CI for Linux process coverage.
