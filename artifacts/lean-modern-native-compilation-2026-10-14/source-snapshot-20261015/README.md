# Measured Lean4.27 implementation source snapshot

This saves the currently measured implementation sources before temporary build
directories disappear. It is source preservation, not a new final evaluated
version, research result, independent review or scientific-contract freeze.
Active packages, native libraries, build outputs and running measurements are
unchanged.

## Contents and restore layout

[source-map.json](source-map.json) records the actual original path, relative
source path, repository snapshot path, group and observed mtime for 45 entries.
Every entry is compared directly with the original bytes after copying.
Existing identical artifact snapshots are reused rather than copied again.

- gc-repl/ is the complete REPL Lean/config source base. native-repl,
  farkas-repl and products-repl are overlays on this base; the map explicitly
  lists changed/unchanged paths. Some changed files reuse existing snapshots in
  the parent artifact directory.
- product-farkas contains the measured Products/Instrument plus their
  Telemetry/Native/Fast/Platform source closure and actual Lake configuration.
  products-only maps the separately measured original-oracle ProductsOnly/
  Products/Telemetry closure and its configuration.
- external-support maps the actual Rust oracle sources, Cargo.toml and
  Cargo.lock. Its existing identical oracled snapshot is reused from the parent
  artifact directory; use the map to restore src/bin/farkas-oracled.rs.

To reconstruct a variant in an owning Workspace build directory, start from
gc-repl/ for a REPL variant, then copy each entry's repository_path to that
group's source_relative_path. For non-REPL groups, copy their mapped entries
directly. Do not assume an overlay directory is a standalone package.
Original source/license headers remain. No SDK, Mathlib checkout, .lake/target,
weights, environment values, credentials or private perf stack memory is copied.

## Actual prerequisites and recorded build commands

Lean is leanprover/lean4:v4.27.0; the existing Mathlib source is
a3a10db0e9d66acbebf76c5e6a135066525ac900 with no tracked changes.
Preserve its exact dependency manifest and ordinary sibling mathlib4 layout.
Native library manifests and library paths are retained in the parent artifact
directory, including native-library.json and stock-products-*-native-library.json.

| Component | Recorded build path |
|---|---|
| Mathlib native closure | build.py, mathlib-build.log: lake -v build +Mathlib.Tactic.Linarith:dynlib |
| Existing Fast adaptation | build-farkas-fast427.py, farkas-fast427-build.log |
| Native REPL/header support | build-header-repair.py and retained header-repair build logs/snapshots |
| Original-oracle ProductsOnly | build-stock-products.py, stock-products-build-result.json: lake build +Farkas.ProductsOnly:dynlib, then lake build repl |
| External CPU oracle | build-external-support.py, external-support-build.log: cargo +1.98.1 build --release --bin farkas-oracled |

The runnable collectors and complete input/order/config/outcomes remain in the
parent artifact directory. Restore into a separate build package within the
owning Workspace; current live paths must remain unchanged. No fresh rebuild
or verification run is performed by this snapshot operation, so fresh-machine
reproduction is not claimed validated. SDK/dependency availability and any path
relocation must still be handled by the ordinary build workflow.

This source snapshot is published as a completed-work checkpoint within an
incomplete research step on main. It is not a frozen final system or a
fresh-machine reproduction result.


## Upstream attribution and license retention

The REPL files preserve their existing Scott Morrison/other upstream copyright
and Apache-2.0 headers. The pinned FrederickPu/repl commit has no top-level
LICENSE/NOTICE entry; gc-repl/LICENSE includes the standard Apache-2.0 text
matching those explicit source headers. Farkas Rust/Lean support comes from
lucifer1004/farkas at the recorded 5a38a7e revision; its unmodified upstream
Apache-2.0 license is retained in external-support/LICENSE and product-farkas/LICENSE.
The REPL/native overlays retain their source attribution. The per-file source
map distinguishes copied upstream source from project adaptations.
[Publication provenance](publication-licenses-20261016.json) records the actual
source access, including the missing REPL LICENSE probe. This preserves upstream
notices; it does not select a license for original gpu-smt contributions.
