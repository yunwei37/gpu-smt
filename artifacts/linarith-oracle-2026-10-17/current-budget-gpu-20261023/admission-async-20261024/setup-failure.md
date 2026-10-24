# First setup attempt — root-caused path error, no measurement

The new runner still selected the parent qualification24-gpu-ready output.
Existing exist_ok=False refused it with FileExistsError before starting any
REPL/candidate, so historical output was not overwritten. Root's incomplete
path rewrite caused this setup error. Preserve the failing source and lifecycle/
provider/readiness records with setup-failure prefixes. Actual JobUID
42b2a022-139e-4338-a024-ef02df98ea7e was deleted, labReady, devicepeak0 and
no allocations. The32.0242314sfailed cold lifecycle is not performance.

Repair changes only the artifact output path in this new runner. Retry the
same original24 qualification once through the same lifecycle; no numerical
algorithm, candidate ordering or resource change.
