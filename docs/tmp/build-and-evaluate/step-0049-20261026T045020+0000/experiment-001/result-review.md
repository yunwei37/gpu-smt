# Result review — sensitivity of previously associated memory

Root self-review; the executor and reviewer are this same thread, not independent.
The earlier Step0016 primary477-source attribution remains authoritative and
unchanged. This step initially duplicated that analysis, then corrected its
scope to a single full-read-window/body-active sensitivity control. It does not
acquire a new dataset or answer the full equal-resource RQ3.

## Completed declared scope

All480 original failure-selected sources are retained, including null fields.
The final join assigns33,039 native-worker samples to435sources:310/355 ordinary
errors,83/83timeouts and42/42resource failures. The primary body-only subset had
34,130samples/463sources. Every new sample key(source,time,PID,birth) exists in
that subset; same-key RSS mismatches are0. All125timeout/resource per-source
sampled maxima match the original primary result exactly.137ordinary maxima
decrease;0increase. Boundary trimming loses fast-error observations rather than
changing the cohort or verdicts.

Nearest-rank p50 observed per-worker maxima:ordinary3.67686GiB,timeout14.70888GiB,
resource23.27201GiB; observed maxima12.64094/22.59550/23.45602GiB respectively.
These are sampled maxima of history-dependent occupancy, not true peaks,
incremental source demand or counterfactual uncapped requirements.

126first/changed-process windows and1,350other outside-body windows remain
unassigned. Source-byte mismatches0. All126native gzip streams lack trailers:
the existing reader retains complete-line prefixes, with no tail extrapolation.
Observed prior selected-source history exists for324sources, not complete
allocator/import/cache history.

## Method and verification

Same PID/birth must occur in adjacent watchdog rows and have a singleton
observed birth index. The entire sequential RSS read window must fall within
agreeing active-body snapshots and matching HTTP envelope. Any source boundary,
unknown/conflicting frame or existing2.5s observation gap breaks continuity.
Native boundary snapshots precede ownership updates. No aggregate/peer memory
is substituted. Four one-off tests pass for these boundaries and truncated
streams. Confirmed/final summary invariance and exact primary-subset comparison
are executed, not inferred.

One-off code/tests live under the artifact, not a second core analysis/CI
pipeline. Initial paths and sources remain in receipts. Final analysis has
0native executions,combined sampled peak29,601,259,520B; comparison8,888,807,424B;
the earlier confirmation47,333,916,672B reflects the contemporaneous live native
state. Each uses CPU11,aggregate48GiB1s monitoring,0pressure/monitor errors.
Sampling is not a hard kernel RSS quota. The original fullpair is never signalled.

## Interpretation and limits

The critical high-memory observations survive this stricter association choice.
This is supporting robustness evidence only. Old2worker/24GiB-AS, instrumented,
failure-selected data do not train a current uncapped resource-point predictor,
show per-tactic causal memory,or produce a native throughput result. No further
variant of this unchanged cohort is selected absent a concrete attribution fault
or different captured resource point.

Paper edits are one local result paragraph. Pinned Tectonic exits0; all4RQ lines
are byte-identical. PDF509096bytes;70underfull warning mentions,0overfull and0
unresolved-reference mentions. Compilation is not visual QA or paper readiness.
Raw logs/PDF/commands/samples are retained in the linked artifact.

Current fullpair remains source42659a8,PID408739,birth140695363;05:40UTC it has
a growing attempts journal and no native terminal capture. Physical attempts
are not final consumer results. No partial speedup or acceptance-set claim.
Continue original queue and four directions; CPU oracle and rejected routes stay
frozen. All scientific claims/RQs remain unchanged.
