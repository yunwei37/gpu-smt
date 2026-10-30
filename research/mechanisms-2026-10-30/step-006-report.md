# Step006 — profiling perturbation and native-timing repair

M branch; self-review,2026-10-30UTC.

## EXPERIMENT
Completed200source x2 diagnostic calls at the restored local-disk point.
Same source/budget does not make trace.profiler transparent:7/200 error flags
change, and observed work is prematurely truncated. This invalidates the naive
work/span inference. Full native evidence and limits are in the methodology note.
The dynamic C hook is inactive (0 callbacks), so no timed-DAG result is claimed.

## WRITE
Added the methodology result,400-row small CSV,7 differences, terminal summary
and raw external capture links. M-generated binaries/raw sample buffers were
moved out of checkout without touching tracked history or other lines.

## REVIEW
Matched-input claims scoped to raw error flags, not full production acceptance.
Raw heartbeat multiplier unknown; warm-order/cache limitation explicit.
C prototype failure retained, not treated as qualified by exit0.
Next necessary action is a minimal link-time wrapper qualification; the original
200-source scope and full research objective remain open.
