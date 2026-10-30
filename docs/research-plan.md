# Research plan

ProofServe studies verification workloads and systems mechanisms around native
Lean verification. The four research questions and retained evidence remain in
[idea-story](idea-story.md), [evaluation](evaluation.md), and [the paper](paper/main.tex).
This document does not decide a replacement paper thesis.

## Current conclusions

- The retained strong pass@k schedule is close to its measured ideal ordering:
  only about1.8% of consumed work remains in that offline ordering gap. This is
  a frozen-work proxy, not a wall-time guarantee under memory/arrival effects.
  Do not repeat the source-feature cost predictor.
- Resource management, warm preparation, ordinary caching and scheduling are
  infrastructure. Their engineering value is not by itself research novelty.
- Workload representativeness comes first. W is checking public mathematical and
  program-verification workloads; selected slow tactics are not representative
  by assertion.
- Analyze native semantics and deterministic budgets directly. Do not assume
  a watchdog or kill signal as a semantic failure oracle. The existing service
  resource watchdog is separate from this research question.

## Asymmetric trust

A proof is accepted only through the original Lean kernel under declared native
semantics; rejection may use any fast path. Fast rejection does not add an axiom
to accepted proofs. It can affect completeness and workload quality, which must
be measured separately. Rejecting a proof attempt does not disprove its target.

Only modifying the trusted kernel changes that proof-checking boundary. Faster
tactics, extracted computation and external certificates still have to produce
proofs/certificates checked by the original kernel. Budget/heartbeat changes
are semantic/resource changes to report, not hidden speedups.
[Architecture](architecture.md) records the same boundary.

## Candidate mechanisms

1. **Computation extraction and certificates.** Batch finite enumeration outside
   proof search, produce a reflection certificate, split it into chunks checked
   in parallel by the original kernel. Include construction, transfer,
   reconstruction and checking costs.
2. **Precompilation.** Native tactic compilation; investigate what csimp actually
   affects in kernel-checked computations; investigate Expr runtime
   representation. A compiler rewrite is not a kernel reduction rule.
   Feasibility and TCB effects require evidence.
3. **Early failure and deterministic budgets.** Analyze native failure and
   exhausted computation under declared budgets. Keep tactic failure, resource
   failure, timeout and unknown distinct.
4. **Out-of-order speculative execution with fine-grained CPU/memory scheduling.**
   Explore independent work and commit ordering, charging rollback, wasted work,
   actual memory and retirement.
5. **Generation/verification co-design.** Later, after workload and feasibility
   evidence for the preceding mechanisms.

M owns feasibility experiments. These are candidates, not completed methods.
CPU oracle work stays frozen; retain failed/partial results.

## Paper decision

The OSDI standard is one clear thesis supported by two or three mechanisms,
representative workloads, generality and strongest relevant baselines. Do not
assemble a contribution from unrelated engineering optimizations.

W and M provide workload/feasibility results. The main thread integrates the
paper/evidence; the user decides its thesis. O prepares the extensible open-source
system and interfaces. No agents beyond the four authorized lines are introduced.

## Engineering and current limits

Contracts, engine resources/scheduling, native Lean backends and service adapters
are separate crates. Crate packages and Docker context exclude research data;
the existing repository and history retain it.

The operator-approved migration keeps the same Workspace/PVC on phobos-vt.
The four lines now share40GiB actual RSS: W≤16GiB, M≤16GiB, O≤4GiB,
main≤4GiB; each line uses at most8cores. O uses one compiler job on CPUs16–19,
without a Lean process, and preserves the interrupted G10 validation separately.

Full Lean/Mathlib Docker construction waits for Longhorn's WAN replica rebuild
to complete, then must stay within O's4GiB allowance. The current short signal
control on the Kubernetes-exec path still returns errno13 for same-UID TERM;
do not assume watchdog delivery from the node change. Native work uses bounded
heartbeats/natural termination until its own execution path is qualified.
The migration is an explicit operator exception; O makes no scheduling/security
or credential changes. No publication token is read or created.

Historical plans remain [archived](tmp/bootstrap/step-0004-20261009T183603+0000/archived-research-plan-20261009T193900+0000.md).
