# Step0016 outer audit — root self-review

The proposed analysis addresses source-cost/admission labels for the user's
resource/workload engine. It uses completed original data and does not repeat
a native collection or expand a frozen oracle/GPU baseline. Strict attribution
and coverage limits must decide whether labels are usable; no classifier is
trained from bad_alloc labels or aggregate concurrency by assumption.

The read-only current-state check finds only two live native workers belonging
to the existing original group. The resource memory note is historical and
superseded by the user's new dynamic point for the next collection. Current
foreign dirty paths stay untouched.

## Observed diagnostic and implementation result

477/480sources have inferred process-RSS samples;3ordinary-error sources remain
missing.34284/34515native-worker sample rows satisfy the birth/source/HTTP rule.
All126profile gzip streams lack trailers but have0partial trailing bytes;
existing reader retains complete frames and all flags remain explicit/zero.
All480old source statuses match. The median per-source sampled worker maxima
are23.27GiB(resource42),14.71GiB(timeout83),3.67GiB(error352observed).
These are old AS-censored/instrumented process occupancy, not new RSS peak
labels or removable critical-path memory.

The new engine audit found its conservative peak mixes registered-tree samples
with backend supplements. Source signatures are unchanged; backend events now
retain current-leader versus wait4-leader-HWM kinds with PID/birth/bytes, and the
fresh observation checks birth in the same proc record. The combined admission
estimate is unchanged. The report keeps its old key as a clearly scoped alias.
Local33ordinary tests/format/Clippy/docs/help pass:
artifacts/rust-engine-2026-10-25/validation-20261025T121329. Exact-head native CI
still must run. This makes future source-cost labels interpretable, not a
runtime acceleration or a trained predictor. Missing old provenance stays unknown.

The stale Current frontier in docs/idea-story.md is replaced with completed
profile/four-direction/scoped implementation links. Its entire preceding
Initial Narrative is byte-identical; previous frontier is archived. No historical
evolution is rewritten. Foreign dirty files and the live original group remain.
