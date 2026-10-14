# Direct pre-packet native-head refusal implementation

Root directly implements this candidate in the owning Workspace/main.
Native5 three complete ProofNet blocks reject speedup (4.41–5.84% slower
than fastest matched native CPU). Recomputed original provider logs show
about15.1–15.3 cumulative seconds of packet construction and about2.38M
host refusals, versus2214 actual device launches per run. Counter sums are
censored per-PID maxima, not exact uncensored work or exclusive wall time.

closure-native-provider-v5.cpp invokes a borrowed-native-Expr conservative
head walk before packet construction in GPU mode. It rejects only a
demanded unsupported head, traversing metadata/let/app/lambda bodies and
stopping undecided on demanded bound variables or the original step bound.
It performs no argument evaluation, substitution, successful reduction or
device-result substitution. It matches the existing packed-head predicate's
support boundary with pinned Lean constructor fields from the actual packet
builder. CPU control, original packer, device kernel, readback, fallback and
final native checker are unchanged. Remaining uncertain cases still use
the original packed admission. New prepacking_declined counts distinguish
the changed placement from old packet-stage refusal.

Actual compiler and linker exit0/0; build receipt and command retained.
No GPU execution or gain is claimed. The existing native5 full acquisition
continues through all resource profiles; this candidate will receive fresh
matched full baselines after that acquisition closes, not stitched clocks.
No AI delegate, SDK mutation, new scheduler, resource quota or model change.
Basic full-input checks stay necessary, but no unrelated correctness campaign
or test-derived timing is substituted for the full performance comparison.
Root self-review is not an independent result audit.
