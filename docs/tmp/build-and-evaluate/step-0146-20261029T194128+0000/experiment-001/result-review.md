# Development result review — same-thread self-review

This is the user's requested G10 Rust implementation boundary, not a paper
experiment or formal state-reuse activation. No native replay adapter is
implemented, no stock Lean adapter opts in, and Engine.verify/CLI/HTTP do not
construct the store. Full-state match rate and benefit remain unknown.

## Implemented boundary
Keep four workspace crates. Core owns the optional backend contract and typed
ordinary/nonreplayable completion. Engine owns the standalone scoped store;
Lean adapters stay unchanged. Key compatibility includes strategy, complete
goal/context, options and hidden dependencies; an observer match is not a
replay qualification. Scope is captured before a native producer runs.

Ordinary records preserve the backend-owned failed transition, diagnostics,
fresh-identity effects and action heartbeat accounting. The backend must
revalidate at commit. Return Some(native exception) requires the original
failure/backtracking path; it is not tactic success or source rejection.
None leaves effects/charges unchanged and requests original execution.
Operational Err must not become a rejection or unsafe fallback.

Metadata lock covers Hash/Eq/store operations, never backend replay or opaque
record destruction. Immutable records use Arc, without requiring Clone.
Keys must have nonblocking metadata methods. Scope retirement/clear drops
retained entries; there is no automatic native-memory bound or replay claim.

## Meaningful fixture coverage
Eight explicitly simulated unit tests cover failed post-state and exact native
exception, one action heartbeat debit, unchanged miss/unsupported inputs,
insufficient budget, backend rejection, ineligible completion invalidation,
environment/input/generation separation, producer-scope capture before restart,
cancellation at lookup/commit, live-scope revalidation, operational error
propagation, and lock-free backend replay/record destruction. These are Rust
contract fixtures, not eight native differential tests.

A runnable public example uses the same traits and asserts toy state/exception;
existing CI now executes it. README/API/architecture/example docs state the
disabled boundary and obligations. No dependency, new crate, service, CLI flag,
Cargo feature or collection is added.

## Failures preserved
Initial clippy rejected a complex type. The private Entries alias repairs that
without suppressing the lint. Interim boolean-contract source and checks remain
as development history; final interface uses typed native exceptions.

Initial full local workspace validation failed the existing owned-process
retirement test on errno13 PermissionDenied when killing its own child. A
two-second same-UID Python diagnostic reproduced denied TERM/KILL, with signal0
allowed and normal natural retirement. A subsequent exact-exclusion run passed
15 engine unit tests but failed the existing idle-preparation integration test
at its own kill call (same errno13). No process-test body, permission, security
profile or CI exclusion is changed. Final local check labels/JSON retain exact
commands, exclusions, resource samples and results; CI retains the full suite.

## Final local verification limits
Final source passed fmt and all-target clippy. The workspace test invocation
with the two explicitly recorded local exclusions passed 15 engine unit tests
(including all eight new tests), 25 engine integrations and nine Lean-adapter
unit tests, but failed two existing Lean lifecycle controls: late/cancelled/
malformed retirement and owned-group preemption. The latter observed no
interruption; the former reached a non-error outcome instead of malformed
retirement under the signal-denied environment. Do not equate this local
result with a full-suite pass or independently prove every failure's cause.
Remaining integration/server/native targets were not reached by that command.
The initial non-excluded run and both later commands/exclusions are retained.
CI is required to check the unchanged full suite; no local signal workaround,
native adapter modification or test relaxation is part of this patch.

The all-target command also executes the pre-existing exact-cache microbench;
its printed number is not a result of this skeleton or a formal workload
measurement. The example executes separately and asserts only toy semantics.
