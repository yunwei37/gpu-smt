# Complete diagnostic stream — root self-review

Actual source inspection found the native transport retains only64KiB of stderr
in Capture. Simp/interval structured progress events can exceed that, so a tail
alone cannot support per-request stage attribution. The optional configured Rust
source backend now streams complete stderr to create-new per-attempt PID/birth
files in an explicitly supplied existing directory. Backend events retain path,
native process identity, bytes read and completion/error. The normal response
still retains only its labelled tail. No file/directory is created by default.

ConfiguredLean composes existing argv/original-file builders with a logging
directory, preserving NativeLean public literals and all default identities.
The CLI now consumes --stderr-dir for --lean and rejects it with REPL. Tokio's
filesystem feature supplies asynchronous writes; no service/runner/policy is
added. The logging path participates in configured identity; fresh diagnostic
measurement uses reuse=false. File/setup/I/O faults remain operational and cannot
promote proof acceptance. Native stderr classification is unchanged.

Actual large-stream fixture emits1024 ordered UTF8 JSON events (>64KiB).
Backend integration verifies every event from first through last, exact payloads,
actual PID/birth attribution and raw byte count, bounded response tail, and child
retirement. Missing-directory setup kills/reaps the owned native child. A real
Linux /dev/full write/flush test produces ENOSPC without filling project storage
and preserves explicit incomplete-log status after draining. Existing CLI
file test verifies the option creates a completed empty native log.

Three validation attempts are retained:
- validation-20261026T021414: fmt passes, Clippy rejects a collapsible conditional;
  the old temporary driver returns0 despite command101. The receipt itself
  records101; it is not a successful validation. Preserve driver-before source.
- validation-20261026T021643: Clippy passes, integration catches CLI parsing the
  new option without applying it. Corrected driver returns101. Backend stream/
  setup/real-write-failure tests already pass. Preserve raw failed test output
  and the two known temporary-fixture cleanup records.
- validation-20261026T021956: all fmt/Clippy/workspace tests/docs/help pass,
 44tests total and4explicit local native skips. Actual native configured-file
 logging cases compile for existing CI; local native workload is not started.

The [final raw validation](../../../../../artifacts/rust-engine-2026-10-25/validation-20261026T021956/validation.json)
and all failed receipts/logs remain. RSS for each attempt is separate; final
combined full+development sampled peak19,280,990,208B, no pressure withdrawal or
monitoring error. Initial helper exit bug is repaired for future reuse; no raw
receipt is rewritten to conceal failure. The first observed41+native results
from earlier steps remain their own source versions.

Transport completion means EOF bytes flushed to the file, without fsync/durability
or complete phase/proof guarantee. A killed request may have an open phase.
Logs from failed writes remain partial with error evidence; they are not an
admissible completed profile. Logging setup/write/flush/cleanup enters attempt/
whole lifecycle; do not pool diagnostic clocks with uninstrumented performance.
Structured stderr may remain BackendError under normal strict classification;
derive diagnostic-native summaries separately from full raw bytes, never turn
profiler events into accepted verification responses.

The original23simp/48interval runs and nightly complete module remain pending.
No actual bottleneck fraction, reliable rejection, full parity, speedup, GPU
gain or scientific contribution follows from this transport implementation.
The sole7808fresh/derived release pair remains unchanged at42659a8.
