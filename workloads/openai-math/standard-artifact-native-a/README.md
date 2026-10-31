# Standard compiler artifact cost sample A

Pinned openai/math4eaee875, Lean4.34.1/5045d005, Mathlibd13f23b7,
phobos-vt CPU0–7,j8. All26ready original random targets compiled without
sorry or source edits: **26/42observations,11/21complete strata**, covering
93,998/163,097modules. Original16pending targets remain nonresponses.

New point emits .olean/.ilean/.c (actual SDK LLVM backend=false).
NativeCPU sum712.009670s; request wall sum471.717085s; group471.845673s,
including controller472.608103s; output77,581,124bytes.
Scope: internal compiler artifacts, excluding Lake driver, dependency
setup/cache acquisition and linking. Earlier M8192 .olean-only costs are
retained and **not pooled**.

-M9216 is a cooperative RSS check, not AS/kernel hard RSS. Child self-alarm
<=1200s/group1700s; authored HB/recursion unchanged. One current child plus
old censored13733. W owned-tree1s sampled peak13,369,733,120B (12.45GiB),
including old process/CLI parent; sampling can miss short excursions.
Controller/26child PID-birth identities retired/zombie before batchB.

## Statistics
Seed20261030 SRS without replacement,2modules per21size/depth/kernel strata;
two-module strata are censuses. For complete cell h: total=N_h*mean(y_h),
variance=N_h^2*(1-n_h/N_h)*s_h^2/n_h; y=user+systemCPU.
estimate_native_build.py uses nominal95%t intervals with Welch–Satterthwaite
degrees of freedom. n=2/heavy tails make normal-cost intervals fragile;
they exclude systematic/runtime variation, hard nonresponse/model error.
Largest complete-cell variance:45,251small non-kernel/depth11–100 modules,
74.1775CPUh, nominal **cell-only**95%[0,623.1803].
This is not full-buildCPU/CI. Full totals remain blank until missing random
draws are resolved, rather than treating them as zero.

Reproduction:Python3.13,NumPy2.3.5/SciPy1.16.3 official cp313 Linux wheels
unpacked on PVC outsideGit. MissingSciPy analysis failures then qualified
dependency-path rerun; no Lean rerun. Raw/logs/source/memory/terminals:
PVC workloads/openai4341-standard-artifacts-a. Analysis:standard-cost-v1.
Next batchB:original Dihedral/Ramsey pair,LowBlock15_1,Moments.Tail at
same M9216/artifact point. Dependency work carries no random-sample weight.
