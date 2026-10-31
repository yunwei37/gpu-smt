# Native timing after the privileged-mode restart

User-directed protocol change, not an acceleration method or baseline win.
Same phobos-vt i9-14900K and128GiB PVC. Actual PMU cpus files report
cpu_core0–7 /cpu_atom8–23. Untimed preparation runs on8–23.
Every timing/profile capture is launched as:

    taskset -c 0-7 flock /workspaces/.agent-state/gpu-smt-captures/pcore.lock python3 -u CAPTURE/capture.py

The shared exclusive lock covers the finite capture and native cleanup,
so M/O/root timing cannot overlap W timing. Queue wait is recorded separately;
the1700s capture deadline starts after lock acquisition. One native compiler
at a time, j8, .olean/.ilean/.c, original source/HB options. W actual RSS16GiB
is sampled by the independent parent every1s. Largest owned native PID/birth/
candidate is recorded and killed on excess. This is sampled response, not a
kernel RSS quota. -M9216 remains an additional cooperative native RSS check.
Self-alarm≤600s per dependency/1200s per selected target, constrained by the
remaining1700s capture budget. No host sysctl/module/pod changes.

## Data continuity and compatibility

Old B's61successful returned compiles remain cached. The interrupted
CertificatesK14Part003 is forced through a fresh compiler invocation even
if an incomplete old artifact exists. Old raws are never overwritten.
The new recovery has6original random endpoints/659initial jobs, including
the remaining B endpoints and paired kernel/deep cells.
Large dependency jobs are setup for target measurements, not additional
weighted random observations. Full42-draw cost/CI is still incomplete.

The per-file CPU/core/native guard/output settings remain labelled explicitly.
The scheduling policy now has a separate pcore_lock field: earlier observations
did not have this exclusion guarantee, and old13733no longer occupies memory.
Future analyses can use estimate_native_build.py --locked-only to reject
pre-lock observations entirely; do not silently present mixed measurements
as a clean matched capture. Old native costs remain accessible.

## Analysis checks on actual retained records

On frozen A+B: CPU values, stratum estimates and nominal cell intervals remain
exactly unchanged (26costs/11cells). A dependency-not-compiled target is now
recorded as not invoked rather than falsely tagged as another resource point.
The new locked-only filter admits0of those old26costs. This is a data-analysis
qualification, not native semantic validation or a performance result.
CSV records these exact checks; complete logs/scripts on PVC
workloads/openai4341-locked-analysis-qualification.

Native capture/scripts/source/outputs/lifecycle/memory remain on PVC
workloads/openai4341-locked-b-recovery. Source is byte-for-byte public release.
Installed perf6.12.113 binary is copied outside Git to
gpu-smt-workloads/tools/perf-6.12.113; tool availability alone is not a profile.
No perf attachment changes this currently frozen unprofiled cost capture.
