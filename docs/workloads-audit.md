# Workload representativeness audit

W branch; same-chat self-review. This compares released workloads with their
consumer contracts. Static counts, publisher labels, native outcomes and
budget interruptions are different evidence.

| Scenario | What the retained Lean4.9 /32-candidate batch covers | Remaining gap | Public data / completion route |
|---|---|---|---|
| RL training | Every candidate can receive a native reward; retained failures are useful | Offline completed batch has no true arrivals, model updates or original reward latency; successful-only GoedelWorkbook cannot supply failures | EPFL compiler training corpus supplies4,836,380 labelled programs incl2,667,963invalid; retain invalids and compiler feedback, then collect version-matched native costs |
| pass@k / best-of-n |32siblings and checked-winner cancellation fit this contract | Exhaust all candidates for observed-unsolved tasks; ordering/timeout changes cannot be assumed free; published solved-proof collections censor failures | EPFL evaluation has model/task/sample IDs but excludes timeouts; retain its selection rule and obtain an uncensored budget-aware replay separately |
| Tree search / agent repair | Complete-source acceptance can be checked | No step arrival tree, rollback state or interleaved branch dependencies; arbitrary32 independent sources are not tree search | APRIL gives controlled mutations/feedback, not natural search; OProver paper describes traces but current OProofs schema alone does not expose failed steps |
| Autoformalization | Final Lean source is checkable | Accepted proof need not express intended natural-language statement; placeholder definitions and policy checks matter | NVIDIA release includes formal statements/conversations; inspect actual released rows and faithfulness policy rather than treating every record as a proof attempt |
| Program verification | AutoVerus retained source revisions, original logs and native solver captures exist | rustc/VIR/AIR costs and function/spec dependencies differ from arithmetic tactics; saved revisions are not all verifier invocations | Keep original ordering and frontend timing; do not transfer Lean timing proportions or reopen negative SMT-prefix sharing |
| Research-level formalization | A stock Lean backend can check individual sources | Single-theorem Lean4.9 workloads miss163k-file Lean4.34.1 library DAGs, many dependencies, theorem families and large certificate computations | Pinned openai/math full inventory and content/import audit; stratified per-module replay after a qualified environment is ready |
| Computational certificates | Some native reduction appears in existing candidates | A few failed rfl calls are not representative of verified multi-million-witness certificates or kernel-checked SDP reflection | Erdős647/flag-algebra released artifacts; preserve standard-axiom vs ofReduceBool trust distinctions and publisher resource requirements |
| Industrial binary verification | Existing code-verification examples provide a protocol foothold | Mathematical SFT proofs omit ISA semantics, symbolic simulation and bitvector/SAT workloads | Pin leanprover/LNSym sources, classify bv_decide/reflective checks, then use actual native project/version |

## Data and budget interpretation

The old48GiB watchdog point is an experimental setting, not an intrinsic
property of a proof or dataset. Record resource interruption and timeout as
exceeded declared native/replay budget, with the limit kind and actual toolchain.
Do not relabel them as ordinary rejection or a false theorem.

For a future native attempt retain: dataset revision, source ID, Lean/Mathlib
pins, native options/heartbeats, original budget, replay budget, final outcome,
per-stage wall and CPU, peak RSS and whether a host watchdog intervened.
Cause classes are combinatorial expansion, closed computation, rewrite
nonconvergence, proof-search expansion, frontend/kernel work and unknown.
A profile or diagnostic may support a class; static tactic names alone do not
prove it. A sampled hot stack is not a proof that a tactic never terminates.

Report per-dataset same-run time by supported cause, including unknown and
budget-exceeded work. Do not borrow stage shares from a different resource
point, mix CPU and wall time, or count overlapping phases twice.
The 1.6%-of-candidates/73%-of-time observation remains a hypothesis to test:
a release with no native timings, no failed attempts, or censored timeouts
cannot establish or refute it.

## Native sampling and build cost

No whole openai/math or certificate build is launched by this audit.
Source-tree inventory gives163,097files/1,785,499,363bytes. A hypothetical
mean1s/file would already be45.30CPU-hours;10s/file would be453.05CPU-hours,
excluding dependency builds. These are sensitivity scenarios, not measured
build estimates. Source byte size is not a calibrated CPU-cost predictor.

A small version-matched native pilot should stratify by source size, import
depth, certificate tactics and project, and measure each file independently.
W stays within5GiB and one Lean process; bounded-heartbeat work must end
naturally on the G10 path. Heavy native builds await the agreed machine and a
documented cost estimate. Publisher requirements for flag algebra include
26–43GB single-module peaks; these cases do not fit the current W allocation
and must be reported as out of budget, not invalid source.

## Evidence links

- [Complete OpenAI math inventory](../workloads/openai-math/README.md).
- [EPFL compiler training](https://huggingface.co/datasets/EPFL-LARA/lean-compiler-training-corpus).
- [EPFL evaluation selection policy](https://huggingface.co/datasets/EPFL-LARA/lean-evaluation-benchmark).
- [APRIL](https://huggingface.co/datasets/uw-math-ai/APRIL).
- [OProofs released schema](https://huggingface.co/datasets/OProver/OProofs).
- [NVIDIA released card](https://huggingface.co/datasets/nvidia/Nemotron-Math-Proofs-v1).
- [Erdős647 artifact](https://github.com/ibrahimmian36/decanus).
- [Flag algebra artifact and build requirements](https://github.com/taeyool/lean-flag-algebras-release).
- [LNSym](https://github.com/leanprover/LNSym).

No candidate generation, model inference, competitor-system reproduction or
production mechanism enablement is part of W's static workload acquisition.

## Completed cross-workload check

The [candidate audit](workloads-candidates.md) and [tail CSV](../workloads/candidates/autoverus-tail-direct.csv) add an actual counterexample: AutoVerus top 1.6% candidates use 3.315–3.399% of summed direct native process elapsed, separately per repetition. The denominator is not batch wall or generation. EPFL evaluation censors timeouts; the other new candidate tables lack native time. Their causal cost distributions remain unknown.
