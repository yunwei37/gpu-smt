# Five native compiler profiles

All 20/20 planned native invocations completed without sorry, with exact original source bytes and identical native diagnostic bytes in all four modes of each file. This is a purposeful mechanism-characterization panel, with no population phase weights. The first two files are both original random pilots in the 45,251-module high-variance mathematical stratum; the other three are heavy original sample identities. The panel was revised from four to five cases before any execution; the previous plan remains on PVC.

| Original source (short name) | C++ checker family | Lean Meta | Import | Unresolved or runtime without phase anchor | IPC | Cache misses / 1,000 instructions |
|---|---:|---:|---:|---:|---:|---:|
| InteriorH1Derivative | 1.92% | 64.38% | 16.02% | 11.44% | 2.189 | 2.003 |
| ReindexSingle | 2.06% | 50.58% | 34.60% | 3.17% | 1.928 | 3.503 |
| UMoments9 | 81.52% | 5.93% | 0.66% | 3.68% | 1.450 | 1.737 |
| BarrierData41 | 74.93% | 5.37% | 0.80% | 7.55% | 1.495 | 1.379 |
| EnvelopePsiB | 94.01% | 1.11% | 2.07% | 0.72% | 1.638 | 6.101 |

These percentages partition **decoded native-PID user-cycle sample periods**, not wall time, all-mode CPU, whole-library work or a GPU speedup bound. Each sample uses the nearest recognized caller symbol. The C++ family includes reduction, inference/equality and state cleanup; it is not solely final theorem validation. Runtime-primitive leaf shares (19.5–29.9%) are a different, overlapping axis and must not be added to caller shares. The observed heterogeneity supports keeping computational and ordinary mathematical files separate in characterization.

## Native point and raw evidence

Pinned Lean 4.34.1 commit 5045d0056413266e57c625dcd7c365b10e377c52; Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612; public source 4eaee87548250b2682affda7d05d947c05554bae. On phobos-vt/i9-14900K, every unit holds the shared pcore.lock and uses taskset CPU0–7, j8, cooperative M9216, authored/default heartbeats, and standard .olean/.ilean/.c outputs. One native at a time; 16GiB W-owned-tree RSS watchdog sampled every second, not a kernel hard quota. Untimed preparation/decoding uses CPU8–23.

Original evidence: /workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-perf-case4-plan. Its historical case4 name contains the frozen revision-2 five-case plan. Final offline derivatives: sibling openai4341-perf-final-analysis. All raw perf.data, counters, stdout, usage, PID/birth, lifecycle, sampling, earlier/partial decodes and control sources remain on PVC outside Git.

Native group 1,280.714450s, capture 1,281.667573s; summed native wall 1,273.268909s and CPU 1,895.034937s include all four modes, not one build. W sampled tree peak 8,676,712,448 bytes; maximum native concurrency one. Raw perf.data totals 437,217,656 bytes. All native PID/birth identities retired before collection.

## Instruments and overhead

Per case: baseline_before, perf_stat, perf_record, baseline_after. Frozen PVC perf 6.12.113. Stat counts cpu_core cycles, instructions, cache-misses, page-faults and context-switches for the leaf launcher plus native descendants; all reported running percentages are 100.00. IPC/MPKI retain that tool scope. Record uses cpu_core/cycles/u at 99Hz with DWARF8192 stacks; native-PID filtering removes launcher periods.

All five decoded period totals exactly match stock perf report, with zero reported lost samples and 46,882 native samples. sampling-quality.csv reports unknown-leaf periods, depth and incomplete root-marker reachability. No lost samples does not establish perfect unwinding. Padic's shorter recording has only 215 native samples. Root markers are rarely reached, so nearest-family attribution remains explicitly approximate.

Default inline/source address resolution invoked addr2line on the release Lean library and stalled during **offline** decoding. No DEBUGINFOD_URLS or sockets were observed. Only our verified owned decoder/addr2line children were terminated; native captures were already complete. postprocess-repair.json preserves the repair evidence, and original raw/earlier partial derivatives remain unchanged. Final decoding uses --no-inline --max-stack1024, changes no host setting, and does not rerun native compilation.

case-summary.csv keeps native rusage separate from instrument wrapper costs. Baseline-after/before CPU drift is -9.91%, -2.41%, +5.62%, +0.11%, +6.38%. A negative instrument/baseline ratio is not an acceleration result. One bracket per file cannot give a reliable overhead CI; drift, cache state, sample noise and instrumentation remain confounded. System CPU is present in invocation metrics but outside the user-cycle phase denominator.

## Attribution refinement

Revision 2 recognizes the actual native private-name prefix l___private_Lean (the initial permissive anchor missed private functions and left them unresolved). Explicit private environment/module-reader symbols are included in import. Changing the nearest anchor can move a period from a more distant public import to nearer private Meta/Compiler code; this is a classification change, not a new measurement. The initial analyzer/tables remain under final-analysis/v1-classification on PVC.

checker-subfamilies.csv splits the same checker-family periods: normalization anchors account for 71.43%, 65.71%, 80.61% of all native user-cycle periods in UMoments9, BarrierData41 and EnvelopePsiB, respectively; checker-state cleanup accounts for 9.30%, 8.87%, 13.34%. These are nearest symbol subfamilies, not disjoint semantic phases inside the evaluator. Their sum exactly equals the prior broader checker family. Every decoded category partition and stock-report period check still passes. No native rerun was needed.

## Cost-frame update and limits

The original 42 draws and 21 strata are unchanged. Repeated baselines/profiles do not create new random draws. Matching old native compiler settings still gives 27/42 costs and 11 complete cells; **strict shared-lock observations give 6/42 and two complete cells**. Profiled stat/record units do not contribute to cost estimates. Missing hard strata prevent a full CPU-hour estimate or finite global CI. The two complete locked cells can be interpreted separately under the documented SRS estimator, not as a total.

Use ../analyze_native_perf.py --capture RAW_POINT --out OUTPUT to reproduce period/counter tables; default decoding paths are stored with the capture. The existing estimate_native_build.py produces both cost-policy tables. Nearest-family source interpretation was checked against the pinned public [C++ checker](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/kernel/type_checker.cpp), including whnf_core and reduce_recursor. It does not assign source-level tactics from a C++ symbol alone.

CSV run-summary/invocations retain every mode; caller-families/top-native-leaves/top-caller-anchors retain both classification and unresolved mass; raw-counters retain original event values. Same-thread self-review, not independent review.
