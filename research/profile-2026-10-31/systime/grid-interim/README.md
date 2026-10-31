# Grid interim attribution: most kernel cycles serve the memory guard

Self-review (自审), generated UTC 2026-10-31T09:05:53.172250+00:00. All Grid baseline cells now complete:
3plain +3stat +3record +3trace, all accepted, exact native diagnostic and .olean
bytes equal. Raw perf.data stays PVC. This is a selected Grid module result,
not a whole OpenAI/math estimate or a completed90-cell matrix.

## Main result and confidence

The unprofiled baseline is53.065%system CPU (range52.917–53.081%),
621.936s wall and436.151s system CPU medians. In three recorded runs,
**resource-accounting callchains occupy74.98%[74.92,75.26]%of kernel sampled
cycle periods**; futex paths20.42%[20.33,20.72]%. Mapping/advice0.14%,
page faults0.78%; large allocation syscalls do not explain this kernel majority.

The decisive observed chain is:
getrusage → libc getrusage → lean::check_memory → lean::check_system →
lean::type_checker::whnf_core / reduce_recursor.
Upstream Lean4.34.1 and actual SDK disassembly confirm the guard's200-call
counter and getrusage(RUSAGE_SELF). Among accounting samples with resolved
Lean callers, the first two repetitions attribute~93%to the C++type checker
and~7%to the IR interpreter. The third record reaches libc but lacks the
application caller for this path: it stays unresolved, **not zero guard work**.
All three still independently show the same kernel accounting symbols.

Confidence is high that native memory-accounting checks are the main systemCPU
source at this -M8192point. The exact removable unprofiled fraction still needs
the three no-M counterfactual repetitions; sampled-cycle fractions are not
multiplied into another run's elapsed denominator.

The prioritized first no-M/unprofiled run has already returned0:
wall320.612s,user391.521s,system107.412s, compared descriptively with the
three-run baseline medians621.936/385.525/436.151s. All84,076,976.olean bytes
and exact diagnostics match. Outer native cgroup15GiB and M16GiB tree budget
remain; only -M is removed (plus output destination). It is **one exploratory
control**, not the requested final three-run gain claim. Its~75%systemCPU
reduction independently supports the sampled accounting-path attribution.

## Hardware counters — n=3, median[min,max]

| Metric | User | Kernel |
|---|---:|---:|
| Cycles (10^12) | 1.169 [1.159, 1.174] | 1.455 [1.401, 1.717] |
| Instructions (10^12) | 2.318 [2.318, 2.319] | 0.785 [0.780, 0.791] |
| IPC | 1.984 [1.974, 2.001] | 0.540 [0.454, 0.565] |
| Cache misses (10^6) | 5,160.279 [5,014.777, 5,262.973] | 4,049.079 [3,608.318, 4,740.794] |
| LLC load misses (10^6) | 698.244 [678.014, 727.825] | 999.600 [714.525, 1,388.437] |
| dTLB load misses (10^6) | 522.270 [470.769, 801.263] | 169.489 [157.881, 209.321] |

| Inherited process event | Median[min,max] |
|---|---:|
| Page faults (10^6) | 2.439 [2.206, 3.238] |
| Context switches (10^6) | 39.223 [34.623, 39.305] |
| CPU migrations (10^6) | 17.634 [15.520, 17.651] |

These are cpu_core(P0–7) events, scaled by perf with89–90%running ratios;
software events run100%. Counters include the constant short Python launcher
and native descendants. Stack tables exclude the launcher and retain native
lean commands only. dTLB/LLC are **load misses**, not all-access miss rates.
IPC is calculated per repetition before taking the median.

## Syscall summaries — n=3 observed counts and elapsed sums

| Syscall | Observed calls median[min,max] | Cumulative elapsed seconds median[min,max] |
|---|---:|---:|
| getrusage | 4,010,856 [4,010,848, 4,010,865] | 309.265670 [306.654945, 327.540189] |
| futex | 52,366,009 [51,753,963, 52,717,904] | 874,905.585335 [874,369.218563, 904,104.681846] |
| mmap | 20,579 [20,577, 20,588] | 0.073995 [0.073327, 0.074813] |
| munmap | 204 [139, 204] | 0.007547 [0.007465, 0.007568] |
| madvise | 53,094 [49,409, 56,115] | 0.511239 [0.495931, 0.552241] |
| brk | 7 [7, 7] | 0.000050 [0.000048, 0.000051] |
| read | 18,966 [18,966, 18,967] | 0.023541 [0.023470, 0.023894] |
| clone3 | 2,252 [2,247, 2,282] | 0.632510 [0.632159, 0.635328] |

Trace loss events by repetition: 16749,7348,0. These summaries are observations,
not a loss-free exact census; no error bound is inferred from the loss count.
The thread-summary filter is comm=lean; helper-Python calls are excluded.
Around1454–1455Lean thread summaries and~2250clone3calls are cumulative
observations, **not simultaneous thread count** or a claim that -j8runs only
eight OS threads. Linux RUSAGE_SELF accounts the entire thread group; this
makes thread-count amplification a plausible mechanism to test with the
already queued one-worker control.

Futex elapsed sums include sleeping across many threads and overlap enormously;
hundreds of thousands of elapsed seconds are not hundreds of thousands of
kernelCPU seconds. Syscall elapsed totals cannot answer the on-CPU partition;
the kernel stacks above do. getrusage elapsed also includes preemption/waiting.
The exact syscall table and trace-quality.csv retain all losses.

## Runtime-operation and top20 tables

For every repetition, top20 user and kernel symbols (full demangled names,
periods and within-domain fractions) are in top20-per-repeat.csv and the
Grid-baseline-record-rN-top20.csv files; top20-summary.csv ranks per-domain median fractions with three-run ranges. Periods and native sample totals from
the streaming decoder exactly equal an independent perf-report flat histogram.

| Domain | Visible operation | %within domain median[min,max] |
|---|---|---:|
| kernel | PMU_observer_path | 0.07 [0.07, 0.07] |
| kernel | futex_synchronization | 20.42 [20.33, 20.72] |
| kernel | kernel_other | 3.35 [3.29, 3.47] |
| kernel | mapping_advice | 0.14 [0.11, 0.15] |
| kernel | page_fault | 0.78 [0.66, 0.85] |
| kernel | resource_accounting | 74.98 [74.92, 75.26] |
| kernel | scheduler_wakeup | 0.12 [0.11, 0.13] |
| user | IR_interpreter_leaf | 2.56 [2.51, 2.59] |
| user | allocation_release | 9.47 [9.06, 9.62] |
| user | hash_table | 37.08 [36.73, 37.10] |
| user | import_other | 0.11 [0.10, 0.11] |
| user | interpreted_other | 1.64 [1.54, 1.74] |
| user | kernel_type_check_other | 28.14 [28.02, 28.24] |
| user | native_memory_check | 0.34 [0.34, 0.40] |
| user | reference_count | 10.33 [10.26, 10.37] |
| user | tactic_other | 1.14 [1.10, 1.17] |
| user | task_pool_synchronization | 2.43 [0.22, 2.77] |
| user | unclassified | 6.59 [6.57, 9.59] |

User categories are an ordered, exclusive visible-operation attribution:
allocation/RC/hash work is assigned before residual type-checking/tactic
ancestry. Thus kernel_type_check_other is **remaining** checker work, not
the total semantic checking share; source phases are not additive with runtime
operations. Inlined RC and missing/truncated callers stay unresolved.
Kernel categories use kernel callchains directly and do not label a generic
task-manager worker ancestor as synchronization. Third-run application-caller
loss explains its user task-pool/unclassified variation. It does not invalidate
kernel flat symbols, OS callchains, native decisions or artifact equality.

Raw decode caches/excerpts and the superseded broad-worker classifier are
preserved on PVC; the latter's operation labels were excluded. Current decoder
uses48native frames, no addr2line inline expansion. Raw perf.data is unchanged.

## Profiler overhead is material and kept separate

| Mode | n | Native wall seconds | User CPU seconds | System CPU seconds |
|---|---:|---:|---:|---:|
| plain | 3 | 621.936 [612.777, 633.650] | 385.525 [381.749, 396.113] | 436.151 [431.615, 445.192] |
| stat | 3 | 631.057 [627.441, 641.163] | 386.238 [384.965, 390.450] | 580.505 [564.290, 643.739] |
| record | 3 | 631.688 [629.731, 633.348] | 386.095 [384.572, 388.604] | 486.194 [484.871, 488.997] |
| trace | 3 | 616.584 [616.536, 636.247] | 375.757 [373.631, 376.203] | 515.744 [510.242, 533.572] |

perf stat adds~1.47%wall but~33.10%systemCPU in this ordered triplet comparison;
record adds~1.57%wall/~11.47%systemCPU; trace~−0.86%wall/~18.25%systemCPU.
Ranges, cache/scheduler variation and deterministic ordering are retained;
these are not randomized causal CIs. A small wall delta does not make the
profile free, and a profile's60%systemCPU is not the plain baseline's53%.
No groups are pooled. Offline decoding on E8–15 overlaps allowed native
collection; shared memory/I/O effects are not claimed isolated.

## Next comparison and actual safe reorder

No-M is the highest-priority test, followed by one-worker execution. A separate
finite priority driver reorders12EXISTING Grid cells (no-M plain/stat/trace
triplets, then one-worker plain triplet) through the SAME pcore.lock.
It was submitted during record-r3 and started only after that run retired.
The original frozen matrix and active source were not modified or interrupted.
Later matrix entries retain those exact completed result paths rather than
running them again; unique planned cell count remains90. Both drivers are
serial on P0–7, each native self<=1200s, owned temporary cgroup15GiB,
M tree budget16GiB. No parent cgroup/host/sysctl/other Pod change.
First priority no-M source returned identically; remaining repetitions/counts
and all other matrix cells remain pending/running rather than inferred.

GLIBC thresholds remain useful negative controls but rank behind these:
the SDK uses mimalloc for Lean objects, and measured VM syscall costs are tiny.
No production memory policy or engine setting is changed by this experiment.

## Reproduce and primary-source interpretation

Run analyze_grid.py and aggregate_grid.py on the retained Workspace to rebuild
small tables; completed raw flat reports and normalized callchain caches are
in the recorded persistent raw root. decode_grid_stacks.py derives the caches
from each retired perf.data using48frames; no live file is decoded.
All raw first/failed/partial data remain. Files/captures are under
/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/.

- [Lean4.34.1 memory guard](https://github.com/leanprover/lean4/blob/v4.34.1/src/runtime/memory.cpp)
- [RUSAGE_SELF semantics](https://man7.org/linux/man-pages/man2/getrusage.2.html):
  process-wide thread aggregation.
- [Upstream Linux7.0 getrusage implementation](https://github.com/torvalds/linux/blob/v7.0/kernel/sys.c):
  scans thread-group statistics and obtains adjusted group CPU time.
  This explains the observed symbol path; the Ubuntu7.0.0-29build may have
  downstream changes, so it is not presented as an exact distribution-source audit.

This evidence characterizes the **guarded benchmark configuration**, not an
intrinsic rule that stock Lean proof checking naturally spends half itsCPU
in the OS. The unguarded counterfactual still runs the original kernel; resource
failure semantics beyond these accepted modules are outside this intermediate
correctness/performance result. No GPU/Amdahl/global speedup claim follows.
