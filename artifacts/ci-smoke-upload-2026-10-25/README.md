# Bound smoke uploads to their own outputs

The existing benchmark-smoke workflow passed all test/benchmark/validation
steps but remained uploading the complete artifacts/ tree:13417tracked files,
2956568979bytes. Those are retained original research inputs/results, unrelated
to this CI smoke job. No new benchmark or third-party system is introduced.

Change only upload-artifact path to the four JSON outputs and generated traces
already produced by this job. artifacts/traces has0tracked files before smoke
execution. No research files are removed, reclassified or relocated. No new CI
job, schedule, timeout, retention override, dependency or execution limit.
The existing in-flight upload is preserved; new pushes use the scoped outputs.

Root self-review checks every selected output against the same workflow's
actual producer and validation paths. Native implementationd376bddalready
passes real3testCI; this change affects only artifact upload contents.
