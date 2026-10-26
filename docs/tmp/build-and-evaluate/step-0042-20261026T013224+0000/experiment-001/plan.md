# Preserve original file context for the real code workload

The pinned lean-mlir complete module has not run. A stdin-only frontend cannot
prove original filename/module-context equivalence. Add optional NativeLean
original-file execution using the same engine admission, ownership, timeout,
cancellation, output and reaping lifecycle. Verify original file bytes against
Candidate.code before spawn. Do not edit/normalize/copy the original module
into another source path. Include file path and declared argv in backend/cache
identity, preserving all old defaults and public struct fields.

Transport fixtures exercise original file selection, source mismatch refusal,
exact argv, accepted/rejected diagnostics and retirement. Extend the existing
pinned-native CI source test to raw/file backend accepted and rejected Init
sources. Local ordinary checks only compile native tests: the active7808 pair
remains the sole Workspace native acquisition and retains its release binary.
New source API support is not full project qualification or a scientific result.
