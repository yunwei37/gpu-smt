# Counterexample-screening closest-work and experiment disposition

Root-only literature node, 2026-10-24T06:30–06:44 UTC. Parent: step0011
EXPERIMENT_GATE / RQ4; source entry main3d083d3. This is a bounded search and
self-review, not a new proof run, external-system reproduction, independent
audit, completed RQ, or new performance result.

## Question, authority and coverage boundary

Read the user-directed arithmetic-screening instruction, current author
questions, complete original scientific narrative/evolution and current paper
mechanism/RQs. The latest user prohibits reproducing or integrating other
systems and requires own-method effort at the existing48GiB aggregate point.
All four RQs and the original Lean/SMT systems objective remain. This node
does not change scientific meaning or admit a new numerical baseline.

Claims stated without project names:

1. Sampling values satisfying all hypotheses can expose a false intermediate
   arithmetic goal before expensive proof search.
2. A refuting witness can guide tactic failure/backtracking, while unsuccessful
   testing retains native proof search and never accepts a theorem.
3. GPU evaluation of actual simultaneously available goals may reduce complete
   failed-candidate and timeout cost at matched resources, including export,
   packing, communication, exact checking, fallback and retirement.

Coverage: same problem/mechanism, proof-assistant setting, proof/disproof
communities (FroCoS/ITP/ACL2 and current Lean), and complete verification metric.
Stop this finite node when verified sources determine generic-mechanism overlap
and the next discriminating own experiment. No claim of an exhaustive survey,
first use, or absence of GPU prior art follows from this search.

## Search and verification history

Exact queries used in this node:

- Isabelle Quickcheck random exhaustive counterexamples arithmetic theorem prover
- Nitpick higher order logic counterexample generator rational arithmetic Isabelle
- Lean plausible counterexample tactic testing false goals mathlib
- "The New Quickcheck for Isabelle" Bulwahn
- "GPU" "counterexample" "proof" arithmetic falsification theorem prover
  (arXiv/ACM/Springer source families)
- "GPU" "counterexample" "theorem" testing
- "GPU" "falsification" "proof" arithmetic verification
- "GPU" "counterexample" "theorem prover"
- "GPU" "falsification" "arithmetic" proof
- "Automatic Proof and Disproof in Isabelle/HOL" FroCoS 2011

The first branch found the established proof/disproof and premises-aware
testing literature. The Lean branch found official Plausible documentation
and source. A current counterexample-generation branch exposed the October
2026 revision below. GPU-specific queries did not provide a verified
same-workflow performance result; this remains uncertainty, not novelty proof.
Wikipedia, Reddit, blogs, ResearchGate and secondary citation snippets were
not used to judge mechanisms. No code artifact was downloaded or executed.

Primary-source access distinguishes success from failure. The TUM author PDF
of the2011 overview was opened earlier in this node; later refetches of both
TUM host aliases timed out. Nitpick's author PDF timed out; its VU mirror
returned403. The standalone2012 Quickcheck chapter remains a lead, not a
newly verified citation. One batched tool output overflowed context; only
individually returned/reopened material is relied on below.

## Verified closest sources and claim impact

### Automatic Proof and Disproof in Isabelle/HOL

Jasmin Christian Blanchette, Lukas Bulwahn and Tobias Nipkow; FroCoS2011,
12–27. [Author overview/PDF](https://isabelle.in.tum.de/~nipkow/pubs/frocos11.pdf);
[author metadata](https://www21.in.tum.de/~nipkow/pubs/frocos11.html).

The opened introduction distinguishes invalid conjectures from failed proof
search, describes compiled random/exhaustive evaluation and premises-aware
generation, and describes automatic parallel proof/disproof on conjectures.
This covers the generic motivation and sampling/filtering principle in claims1–2.
It is not our Lean/RTX5090 workload or a matched whole-verification speed result.
No published speed is imported into our measurements.

### Integrating Testing and Interactive Theorem Proving

Harsh Raju Chamarthi, Peter C. Dillinger, Matt Kaufmann and Panagiotis Manolios;
EPTCS70(ACL2 2011),4–19; DOI10.4204/EPTCS.70.1.
[Primary metadata](https://arxiv.org/abs/1105.4394);
[full text v2](https://arxiv.org/html/1105.4394v2).

The abstract and sections1–2 explicitly integrate testing with proof-generated
subgoals, use counterexamples to trigger backtracking, and warn that proof
transformations can strengthen a subgoal even for a true original theorem.
They also explain why random assignments often fail to satisfy hypotheses.
This is strong same-mechanism evidence for claims1–2 and for preserving outer
alternatives. It does not establish our GPU latency claim. Citation-only.

### Plausible, official Lean documentation and pinned tactic source

[Official tactic documentation](https://leanprover.github.io/hex/docs/Plausible/Tactic.html);
[pinned source fb13df72](https://github.com/leanprover-community/plausible/blob/fb13df72ecefd8ddbf9291021d7f33a8673eb57b/Plausible/Tactic.lean),
accessed2026-10-24; access year is not a publication year.

The documentation and source describe reverting local hypotheses into a
testable implication and discarding samples that violate premises. They say
successful testing acts like admit; a found counterexample produces an error.
Thus Lean goal testing itself is established. Our native-fallback-only positive
path differs operationally, but that safety choice alone is not a new systems
contribution. We did not install, adapt, run or benchmark Plausible.

### Learning to Disprove: Formal Counterexample Generation with Large Language Models

Zenan Li, Zhaoyu Li, Kaiyu Yang, Xiaoxing Ma and Zhendong Su.
[arXiv2603.19514v2](https://arxiv.org/abs/2603.19514),
revised2026-10-14; [full text](https://arxiv.org/html/2603.19514v2).
Preprint, no acceptance claimed.

The work generates counterexamples with Lean4 proof obligations, trains on
hypothesis-removal mutations, and evaluates counterexample, reasoning-step
and formalization tasks. This covers formal Lean refutation and reasoning-step
checking, rather than our complete failed-request latency. Our Fraction/AST
CPU witness check is not a generated Lean proof certificate. Its mutated
datasets are not replacements for the user's original candidate traffic.
No training, dataset download or external numerical comparison is admitted.

### Visible but not independently verified here

Nitpick's finite relational model-finding principle is described by the opened
2011 overview; the standalone2010 paper remains a source-access gap in this
node. The2012 New Quickcheck chapter remains a metadata lead. Neither is used
to assert an additional performance or implementation fact.

## Name-free novelty and contradiction review

| Candidate statement | Same-claim risk | Root disposition |
|---|---|---|
| Find sampled counterexamples before wasting proof search | High | Established principle; reject as our novel contribution |
| Refute intermediate goals and backtrack without accepting from finite tests | High for principle | ACL2 source overlaps; retain necessary semantics, not a novelty claim |
| First Lean counterexample mechanism | High / contradicted | Official Plausible and formal Lean counterexample work disallow this claim |
| GPU materially improves complete failed verification at equal resources | Unresolved | Requires actual own complete native/on pair and GPU attribution; not proved by search absence or kernel time |

The primary evidence also supplies a competing explanation for the current
measurement: narrow supported contexts and finite proposals rarely expose
the costly failures, even if point evaluation is fast. In the already-published
immutable snapshot,11 witnessed sources are all Lean errors with0timeouts;
19 observed timeouts split13no arithmetic entry,5unsupported and1supported.
That one supported timeout mostly contains closed inconsistent contexts.
These are partial-cohort facts, not a global impossibility/Amdahl bound.

## Experiment handoff and allowed assets

No new runnable competitor is requested or admitted. Existing native CPU
verification is the numerical comparator; existing external comparisons remain
historical evidence without expansion. Closest systems above are citation-only
precedents. Official-source reading is not reproduction.

Continue the already-launched original7808candidate typed-goal observation
until actual terminal and retirement. Then collect whole outcome/coverage/
cost/resource denominators once, run the existing own native24 off/on
qualification, and only after it passes run the existing complete off/on
pair at the same resource point. Keep original ordering, all outcomes,
failures/timeouts, native acceptance and fixed baseline-ranked1%/10% tails.
Charge preparation/provider startup/export/queue/exact recheck/fallback and
retirement. An own CPU point-provider control is attribution evidence if a
real GPU benefit is found; it is not a new external-system matrix admitted now.

Reusable experimental precedents: test generated subgoals rather than assume
original theorems false; test all premises; retain unknown on unsuccessful
sampling; distinguish proof acceptance from test success. These sources
supply conceptual protocols, not a systems-venue numerical target. The real
asset remains our already-retained original miniF2F7808candidate traffic.
No source-only technique or mutated success benchmark replaces it.

Potential larger opportunity is eliminating costly futile proof search
without replacing native acceptance. It remains a hypothesis, not an adopted
new story or permission to broaden hooks/operators/grids before the complete
approved measurement. The original full Lean/SMT service RQs remain open.

## Gate completion, root self-review and remaining uncertainty

Coverage/contradiction review is sufficient for this declared decision:
generic sampling/backtracking is prior art; the only possible performance
claim remains complete useful-work savings, not GPU arithmetic throughput.
This node is complete at that boundary; GPU closest-work exhaustiveness,
complete false-goal coverage, runtime alias qualification, native/on acceptance,
whole-flow speedup and independent audit remain unresolved.

WRITE_GATE: inspect the current paper's arithmetic-screening paragraph.
It already says intermediate-goal refutation, complete supported context,
outer alternatives, native fallback and missing complete result. No empirical
result or stronger novelty claim is inserted. Paper source/PDF are unchanged;
the previous full12round writing pass/compile remains the latest build.
A future result-bearing manuscript update must cite the verified precedents;
this node's canonical map supplies that obligation without pretending it is
already in the bibliography.

REVIEW_GATE: root self-review only. No Agent, external replication, resource
change, second full run or existing-collector replacement. No RQ is closed.
The next action returns to the actual experiment boundary, not another search
or writing cycle on unchanged material.
