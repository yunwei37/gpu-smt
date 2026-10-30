# Step0160 — executable API documentation and retained native CI evidence

BUILD_AND_EVALUATE; same-thread self-review. This step closes an OSS validation
gap without enabling failure caching or dispatching a formal capture.

## EXPERIMENT_GATE
E160.1: Installed Cargo help explicitly says that --all-targets does not include
doctests. Existing CI built documentation but did not execute its examples.
Add an explicit workspace doctest invocation to the existing Rust job.

E160.2: Add a compile-checked generic default-off FailureCacheAdapter example,
coerced through the existing VerificationBackend trait object. No speculative
associated-type bounds, new service, CLI option or runtime behavior.

E160.3: The existing native job now retains the authored candidate differential
directory even on failure, excluding rebuildable olean files. This is raw evidence
retention for short finite controls, not a new collection or scheduling layer.
Its actual upload is pending CI; a declared upload is not verified retention.

## WRITE_GATE
CONTRIBUTING documents the explicit doctest command and the scope of the native
fixture artifact. The preceding paper-build report now distinguishes observed
warnings from baseline-attributed warnings: the earlier manuscript was not rebuilt
to establish whether those warnings predated the edit. The successful build is
unchanged. Daily maintenance records the concrete validation gap and fix.

## REVIEW_GATE — self-review
Local G10 CPU6–7 validation: fmt, workspace doctests (2 passed), all-target clippy
with warnings denied and rustdoc with warnings denied all exit0; full raw logs
are in experiment-001. No Lean processes were launched. The full local
signal-dependent integration suite was not run on the known unqualified signal
environment. Local development memory samples are recorded, not a hard quota.
Existing native transition/matrix results remain fixture-only: no production
failure cache, population hit rate, replay performance or broad semantic guarantee.
No CronJob, credentials, security configuration, Workspace or scheduling change.
The code boundary will be committed/pushed before collecting its own CI outcome.
