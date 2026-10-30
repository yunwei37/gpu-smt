# Native sampling environment on phobos-vt

Same gpu-smt-dev Workspace/PVC, now128GiB. All SDKs, datasets, originals,
replay copies, generated olean files, raw logs and scripts are outside this
checkout under /workspaces/.agent-state/{gpu-smt-workloads,gpu-smt-captures}.

Official Lean4.34.1 release executable reports commit5045d0056413266e57c625dcd7c365b10e377c52.
ZIP904,280,152bytes,unpacked3,290,453,049bytes,installation38.43s.
No Lean source compiler build or additional download hash gate.

Mathlibd13f23b723b8a846827a245b89c10fc7d3f11612 has exactly the same8
dependency revisions as openai/math's lock. Cache executable prerequisites
were built dependency-first and serially, then the actual upstream
lake exe cache get command downloaded/decompressed8908cache entries.
Exit0;65.34s excluding clone/SDK; one-second sampled own-tree peak
2,019,532,800bytes; maximum simultaneously observed Lean compilers1.
Mathlib was not compiled from source and no source-build fallback enabled.

Short self-child signal tests both failed with errno13(permission denied);
children exited naturally after2s. The raw cache helper used the colloquial
label EPERM, but the actual recorded errno is13(EACCES). No permissions,
AppArmor/seccomp,Workspace/node settings or credentials were changed.
Native samples therefore use finite Lean resource budgets and natural exit.
A native allocation limit is not a kernel hard RSS quota.

PhaseA source extraction retained exactly12,785original files/
252,627,947bytes,68.98s,178,140KiB Python peak. No public archive preprints
or unrelated projects were extracted. Current native samples use exact
Mathlib pins; additional external packages must be qualified separately.

Management SSH handshakes became intermittent over a~3.5s DERP link.
A command-local connection timeout increase8->30s restored observation.
No persistent SSH/cluster setting changed. The local Coder CLI's existing
session was expired; no UI/login/credential mutation attempted.
