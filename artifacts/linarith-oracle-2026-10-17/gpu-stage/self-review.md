# GPU attribution implementation boundary — root self-review

2026-10-17T22:16:14.732716+00:00

No delegated work. All source editing/builds/native runs occur in the owning
Workspace on main. Four Python entrypoints parse; separate Lean/Rust diagnostic
build completes. Baseline v2 and oracle v4 raw 24-source native JSON match their
corresponding primary3 responses exactly, 24complete/no operational, normal EOF.
V4 corrects a diagnostic-only acceptance flag with IO.Ref: 110 successful
checks match 110 successful direct rows, 5 direct no-cert and 10 fallback-service
calls; no unmatched source/client IDs. Earlier raw v1-v3 records retained.
The finite 1000-source acquisition is actually running under 48 GiB.
No full result, GPU bound or independent audit is claimed.
Known remaining CPU coverage, fallback-product metadata, tail-wave and
scheduling limitations are stated in progress.md, not silently filled with zero.
