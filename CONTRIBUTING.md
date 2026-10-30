# Contributing

The reusable Rust engine lives in crates/. Raw research inputs, failed runs
and one-off scripts stay in artifacts/, results/ and bench/. Read
[architecture](docs/architecture.md) before changing the layer boundaries.

## Build and check

Use Rust1.98 or newer on Linux and Python3 for subprocess fixtures:

    cargo fmt --all -- --check
    cargo clippy --workspace --all-targets -- -D warnings
    cargo test --workspace --all-targets
    cargo test --workspace --doc --locked
    RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps
    cargo bench -p gpu-smt-engine --bench exact_cache

Cargo excludes doctests from --all-targets; run both test commands above. CI also
retains the short native candidate differential artifact, including raw JSON,
stdout/stderr and fixture sources, while excluding rebuilt olean files. These
authored controls check fixture semantics, not population reuse or performance.

The owned-RSS process integration test needs at least two eligible Linux CPUs.
Use an allowed two-core affinity when running that full suite; a single-core
mask cannot exercise its concurrent preemption/retry case.

Lifecycle fixtures also need permission to signal their own child processes and
process groups. A container that denies TERM/KILL cannot exercise the full
watchdog/cancellation/retirement contract; report that environment limitation
separately from fixture-only successes. The standalone failure-replay example
uses no subprocess or Lean and is described in [examples](examples/README.md#tactic-failure-replay-skeleton).

The protocol fixture is deliberately not Lean. Real native differential tests
require a stock REPL and its pinned project, and must not overlap an owning
Workspace's existing full collection:

    LEAN_REPL=/absolute/path/to/repl LEAN_PROJECT=/absolute/path/to/project \
      cargo test -p gpu-smt-lean --test native_differential \
        native_task_memory_accept_reject_and_sorry_match_raw_stock_repl -- --ignored

CI runs the native contract against pinned official Lean4.18/REPL sources.
The separate optional prepared-parent test also requires LEAN_PREPARED_HOST
and LEAN_SYSROOT, set after building [the native adapter](native/lean/README.md):

    LEAN_REPL=/absolute/path/to/repl LEAN_PROJECT=/absolute/path/to/project \
      LEAN_PREPARED_HOST=/tmp/prepared-build/prepared-host \
      LEAN_SYSROOT=/absolute/path/to/matching-lean-sdk \
      cargo test -p gpu-smt-lean --test native_differential \
        native_import_parent_isolates_children_and_matches_raw_responses -- --ignored

This tests the declared pinned-context transport/lifecycle contract, not
complete Mathlib performance or arbitrary-FFI-safe COW. State the exact version, resource point, source
population, retries and accepted-ID differences in performance submissions.

## Public APIs and extensions

Core owns requests/verdicts/traits. Engine depends only on these contracts;
native backends implement them without importing HTTP. Protocol adapters
must reject unsupported options rather than silently changing semantics.
0.1 APIs are experimental: document changes and migration implications.
Add tests for a real behavioral boundary, especially native rejection,
admission, watchdog preemption/requeue, cancellation subscribers and cleanup.

A prediction may change order or reservation. It must never become a native
verdict without a sufficient validated witness. Cancelled pass@k candidates
are unavailable RL rewards. Operational failures are not cacheable proofs.

## Review and research records

Keep changes focused; preserve other authors' work and all original failed
results. Verify code and docs together. The current maintainer workflow uses
main and forward-only commits. Research self-reviews are labelled as such;
tests/CI are not independent audit, novelty or venue acceptance. CPU oracle
experiments remain frozen. Do not add a competing runner or scheduler.

## Licensing

New engine code is Apache-2.0. Preserve third-party notices; dataset/source
snapshots retain their upstream licenses. Do not place credentials, model
weights or private data in examples or tests.
