# Actual full-corpus timeout and collector repair

Root self-review,2026-10-17. Native miniF2F full batch stopped at160persisted
source rows (85complete/75rejected). Additional successful responses through
index171remain in the raw request log; the172–175batch exceeded the unchanged
300srequest timeout. The old collector aborted before writing the32source task
group, so this is an incomplete run, not a complete benchmark or rejected proof.

The repaired collector logs requests before sending them, records transport/
timeout outcomes, restarts the native worker, invalidates all saved environment
and proof-state ids, and continues original later inputs. Prefix-state failures
fall back the whole affected task group to original native commands. No native
deadline, source, solver, selection rule or resource setting changed.
Forced retirements explicitly censor waited-child CPU; whole wall still
includes the original timeout/restart/fallback costs.

A real replay of indices172–179is running to exercise the failed batch and its
successor. The finite full-population driver waits for that qualification,
then replays complete original populations into fresh recovered output paths.
All first-run failure/partial data are retained. Main heavy-cohort comparison
is an independent live process and was not interrupted.
