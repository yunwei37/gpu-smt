# Strong-baseline stage qualification — root self-review

The same four mixed Real/Nat source ids produce exactly the same full native
JSON as the completed Fast/hybrid preflight. The native diagnostic covers
515 arithmetic invocations and exits normally. Its 53.854 s whole time was
captured on logical CPUs0–3 rather than12–15: this is stage qualification,
not an acceleration comparison with the77.304 s preflight.

Counters instrument the existing Fast/hybrid selection, product reuse and
restricted/fallback reconstruction. Separate exported native diagnostic code
leaves the running primary implementation/library unchanged. All stages use
sequential calling-thread CPU; LP-caller CPU omits external solver CPU.
The remainder is explicitly unattributed, not allocated to a proposed mechanism.
Summed invocation wall times overlap across sources and cannot be presented
as fractions of whole elapsed time. Four-source composition is not the
1000-source distribution. The full strong diagnostic is queued after primary
timing; the old stock-stage pilot remains historical evidence only.

See stage-analysis.json for exact counters and scope. Prefix32 result analysis
also preserves the distinction between valid small-pilot behavior and pending
full original-population timing. All reviews here are self-review.
