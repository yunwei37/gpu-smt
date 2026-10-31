# Native phase-profile matrix: four real reference files

**Prepared, not launched.** This supports the user-directed characterization
question: where does native reference compilation spend CPU, and does a
computational-looking proof actually spend most CPU in trusted kernel reduction?
Root owns paper framing/RQs. This is not an acceleration or population estimate.

## Selection and scope

Three highest native-CPU files among the26standard-artifact observed original
draws, plus the mathematical InteriorH1Derivative comparator without lexical
decide+kernel. Their earlier CPU values are selection evidence only, not the
denominator for a new profile or a cross-platform speedup.
cases.csv retains original strata and sampling weight0for **profile fractions**.
The source identities also belong to the fixed42random frame: a fresh
unprofiled baseline may supply one matched per-file cost, never another draw.
No-kernel-token does not mean absence of trusted kernel checking.

Public source4eaee875/Lean4.34.1/Mathlibd13f23b7, original source/options,
j8/M9216 and .olean/.ilean/.c. Native compiler acceptance/no-sorry/artifact
completion checked in every mode; budget/instrumentation failures remain
separate and are not mathematical falsehoods or automatic profile wins.

## Integrated matrix and bounds

Each file: baseline_before ->perf stat ->perf record ->baseline_after.
Fresh native processes, unchanged imports/source, distinct preserved outputs.
The bracketing baselines expose drift and instrumentation overhead, not a
precise repeated-trial CI. Four files x4modes=16planned invocations.
Earlier unprofiled standard-artifact wall predicts roughly22minutes for4passes, not a
guarantee; native self-limit<=600s and finite group1700s, parent cleanup1760s.
Failed/missing units are retained and the16unit plan is not declared complete
from an easy prefix.

All timing/profile work: taskset0–7/flock global pcore.lock; preparation and
postprocessing8–23. W owned-tree actual RSS16GiB/1s sampling and largest-native
termination; sampled response can overshoot and is not a kernel hard quota.
No full-project build, host sysctl/module or other-Pod access.

## Counters, sampling and honest attribution

Hardware stat group: cpu_core cycles/instructions/cache-misses, plus page-faults
and context-switches. Preserve enabled/running fractions, not-counted values
and wrapper overhead. Use only this run's counts; unavailable is not zero.

Record cpu_core/cycles/u at99Hz, DWARF8192byte stack, process descendants only
(no system-wide capture). This controls expected PVC sample growth; it is
not an unprofiled speed result. No default build-ID cache writes to container
root: the pinned SDK/binary and raw perf data already live on PVC.
ELF inspection found symbols and .eh_frame in libleanshared.so, but source-line
debug info is minimal; symbol availability is not successful unwinding.
Actual unwind depth/unknown symbols/lost events must be inspected.

Phase fractions use sample **period weights**, not event counts alone or
historical wall denominators. Label trusted Lean kernel, Meta/Elab, compiler,
serialization/import, runtime and unresolved only where actual symbols/
stacks justify them; do not force ambiguous malloc/GC samples into the kernel.
Cycles:u omits kernel-mode OS work and is not full-request wall/CPU.
No lexical tactic frequency, helper count or subset profile becomes a global
Amdahl fraction or claim that all published proofs have this bottleneck.

A Python leaf waits for native Lean directly and preserves native rusage,
while outer perf/wrapper rusage and wall are separate. Counter attachment and
recording overhead never enter the original unprofiled cost estimator.
All raw leaf logs/results/perf/tool failures stay outside Git on PVC at
workloads/openai4341-perf-case4-plan. perf6.12.113 binary is pinned on PVC.
