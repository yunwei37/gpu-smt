# Changelog

## Unreleased — preparing 0.1.0

### Added

- A minimal Python batch client with no runtime dependencies.
- A pinned Lean/Mathlib/REPL Docker recipe and real endpoint smoke test;
  full image qualification is pending.
- Source package metadata, docs.rs settings, and a tag-triggered publishing
  workflow with tests and dry-run verification.
- A Linux binary build artifact in CI. This is not a published release binary.

### Changed

- Rename the four crates and executable to ProofServe. See the
  [migration table](docs/releases/0.1.0.md#source-migration) for breaking imports
  and CLI names. HTTP routes and native response schemas are preserved.
- Present user setup and API examples first; retain research details in
  [research status](docs/research-status.md).
- Detect CPU and memory capacity automatically; explicit research resource
  settings remain optional.
- Exclude research data and reports from Cargo packages and Docker context
  without deleting or relocating them.

### Existing capabilities included in this first release

- Core Kimina compatibility and typed batch/stream APIs.
- Resource admission, exact candidate reuse and all/first-success modes.
- Public Rust extension traits and native differential CI.

### Qualification status

- Complete Rust, packaging dry-run and native differential CI pass.
- Two bounded full-image attempts fail during full Mathlib preparation; raising
  the test budget to 180 seconds does not resolve it. The network-disabled small
  native batch passes acceptance, native rejection and sorry checks.
- Restore the existing fresh-REPL default in the Docker entrypoint. A complete
  image recheck of that correction remains pending; the prepared adapter stays opt-in.

No release, tag, package or image is published by this change. Tactic failure
replay remains off by default and requires backend qualification. Resource and
cache primitives are infrastructure; they are not scientific contributions by
themselves.
