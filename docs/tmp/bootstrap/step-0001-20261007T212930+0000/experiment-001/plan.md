# Native prefix branching: bootstrap behavioral discriminator

Started 2026-10-07. RQ2 exactly as in the current unfrozen paper: Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?

This bootstrap experiment tests one necessary condition, preservation of original SAT/UNSAT/UNKNOWN identities on all 156 retained real VeruSAGE streams, including the 31 differences from added scope/history. It does not answer all of RQ2, test cancellation/artifact fidelity, or constitute final frozen-version evidence.

## Admission and alternatives

Role: supporting feasibility and causal discriminator, not headline service evidence. The consequential story it can unlock is separating native preparation reuse from changed solver mode/history. Closest-work pressure is complete in ../literature-20261007T213700+0000/report.md and docs/background-related-work.md: logical roots, snapshots and bounded warm services already exist. The strongest reject argument is that a stock library driver or branch changes observable native behavior before any useful service optimization.

Prior pooling changes 31 sessions; scope-only and history controls establish their mechanisms but do not test untouched suffixes with independent native histories. This adds independent evidence without repeating that negative pooling run. Positive results admit deeper real-stream/equal-resource work; fresh-driver differences require driver qualification/repair and forbid attributing differences to fork; split-only differences identify call segmentation; branch-only differences contradict the proposed simple boundary. Mixed or inconclusive outcomes preserve failures and keep the contract unfrozen. Profiling dynamic Lean conversion is the strongest sibling alternative; this discriminator wins now because it tests the load-bearing native-isolation premise with fully retained source-native inputs and a binary identical to the prior baseline, without a speculative GPU mapping.

## Hypothesis, precedent and scope

Expectation: fresh native API evaluation, prefix/suffix call segmentation and disposable fork branches recover original decisions when no scope is added and parents execute no checks. Competitor: API manager/defaults, segmentation, native resource counters or inherited runtime state change outcomes despite identical logical commands.

Use original pinned Z3 4.16.0 native command evaluation. Source verifies CLI and eval API use the strategic solver factory but differ in manager ownership/error handling: https://github.com/Z3Prover/z3/blob/z3-4.16.0/src/api/api_parsers.cpp and src/shell/smtlib_frontend.cpp. Official API: https://z3prover.github.io/api/html/group__capi.html. Source-native behavioral comparison is the published-protocol path, with no custom solver or assertion rewriting. Data are the real retained full Verus solver streams, not fabricated query fixtures; they are published proof replay, not generated traffic. Full CAV/NeurIPS/SOSP precedent and final service baseline handoff are linked in the literature report.

## Comparison and fairness

The four paths are controls for native behavior, not four speed baselines: original executable -in -smt2; fresh stock-library driver evaluating complete stream; fresh same driver evaluating prefix then suffix; a single-threaded native parent after the exact prefix, with one disposable child per original untouched suffix. No extra solver check, push/pop, reset or heuristic warmup is introduced. Each option group gets a fresh parent process; its preparation occurs before any candidate evaluation, and candidates never mutate parent state. Prefix is longest exact observed command prefix, stopped before scope or observable operations. Input command parsing uses the existing scope-aware analyzer; split retains order and content. CLI and library use the same official release; the executable hash equals the previous Verus binary.

Resource options and all original checks/output requests are retained. CPU affinity 8 is the measured mask, not isolation. Single-threaded parent is verified in /proc/self/task immediately before fork; failure refuses execution. Original native CLI behavior is the oracle, not proposal outputs. Existing scope/history baseline records remain available for per-input regression intersection. No throughput superiority can be claimed from these adapter/process timings; complete verification, equal-resource service baseline and arrival latency are outside this probe.

## Matrix and measurements

| Group | Conditions | Input coverage | Repeats | Decision |
|---|---|---|---:|---|
| native behavior | executable, fresh API, split API, branch API | All 156 complete streams / 440 checks from retained 100-task sample | 3; middle pass reversed | Qualify or invalidate driver, segmentation and branch boundary independently |

Primary measure is each ordered SAT/UNSAT/UNKNOWN identity per stream/check, including missing responses as failures. Preserve raw stdout/stderr, API errors, all parent/child exit statuses, exact commands, setup and per-process timings and sampled memory. Stats/artifact text is retained but no unsupported claim of universal byte identity or models/proofs validation is made. Three full repeats diagnose reproducibility, not broad universal behavior. No input is filtered by acceptance or prior parity.

## Entry point and completion

Build stock-library adapter (headers/library extracted from official z3-4.16.0-x64-glibc-2.39.zip):

```bash
g++ -O2 -std=c++17 bench/native_z3_branch.cpp \
  -I/workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/include \
  -L/workspaces/.agent-state/gpu-smt-deps/z3-4.16.0 \
  -Wl,-rpath,/workspaces/.agent-state/gpu-smt-deps/z3-4.16.0 -lz3 \
  -o /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/native-z3-branch
python3 bench/verus_native_branch_probe.py \
  /workspaces/.agent-state/gpu-smt-verusage-20261004/mixed100 \
  --z3 /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/z3 \
  --libz3 /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/libz3.so \
  --driver /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/native-z3-branch \
  --cores 8 --repeat 3 --out artifacts/native-branch-2026-10-07/full
```

Real preflight uses same command with --one --repeat 1 and a new preflight directory. At most three repair attempts. Full completion requires all four paths, all 156 streams, three repeats terminal; errors/missing outputs remain in the report. Process-level timeouts are not added to original solver options; an actual hung native process is an incomplete experiment to investigate, not a dropped input. Preserve partial output on interruption, inspect actual process state and resume only missing cells without overwriting files. Runner currently begins a new empty output directory for a full rerun after a recorded repair; any affected comparison is rerun as a whole. Final result review is independent and recomputes per-input identities from raw outputs; no blanket RQ2 closure is allowed.

Raw path: artifacts/native-branch-2026-10-07. Target bootstrap decision table: native-driver, call-split and branch parity, intersection with the earlier 31 regressions. Final service/paper figures require a later frozen complete experiment.

## Plan-review repair before execution

Root accepts both mandatory findings from plan-review.md. CLI now receives original captured bytes, independently of reconstructed API command inputs. Each original stream is copied and hashed; every API full/prefix/suffix remains retained as a derived input. A successful comparison requires the expected number of responses from original check commands, with all process/child exits and API/stderr failures visible separately. Equal incomplete lists never qualify as parity. Error-free complete decision parity is the qualification criterion; raw statistics/artifacts are retained without a universal equivalence claim. Optional repeat-stability and earlier-regression intersections will be reported; analyzer/compiler provenance is retained. No oracle or tested hypothesis changed.

Authoritative retained root has inputs/traces on agent-state PVC, while runs.jsonl is retained in artifacts/verusage-2026-10-04/mixed100. Restore that missing metadata file into the existing agent-state root before preflight, without replacing sources/traces. The archive remains the portable source of the complete corpus. Do not assume mere directory existence establishes complete dependencies.
