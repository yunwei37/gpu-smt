# Applicability boundary — 自审
Certificate-based computational repair is supported only when:
1. The expensive obligation is closed/computable, or symbolic variables admit proved finite bounds. Source-written speculative bounds are insufficient.
2. The original kernel normalization algorithm is pathological for the representation (e.g. well-founded recursion unfolding) or a tactic materializes a huge finite search. A structural/fuel evaluator with a proved equivalence, or compressed checker with a completeness theorem, must reduce actual kernel work.
3. The generated payload is untrusted. Original kernel checks all certificate obligations/bridges; no native_decide or extra axiom is accepted. Source prefix/suffix errors remain errors.
4. Preparation, emission, bridge proof, loading and final checking fit below the cost avoided. A fast final wrapper cannot hide expensive auxiliary checks.
5. New accepted proofs are reported as changed operational acceptance, separately from acceptance-preserving system acceleration.

Negative boundary: Lean4.34.1 decide+kernel is already efficient on the seven tested structurally computable Int/list row goals. Naive chunking adds proof assembly and duplicate reductions; measured serial whole-source wall13.32→23.94s and additional kernel work2.33→5.76s.
Do not generalize that small biased sample to all Lean4.34 goals. Nor infer a benefit merely from a closed goal, a large numeric domain, or a large certificate.
Reflection, verified evaluators, compilation and proof futures are established techniques; the measured pathology/algorithmic repair must supply any new contribution.

Current supported families: digit cardinality with a proved fuel/digits equivalence; product grid compressed to a proved row-division completeness checker.
Next admitted test: cube/fourth coincidence below4096, after proving x<16,t<8 and checking128assignments. It tests whether another pathological enumeration can be repaired while retaining invalid original prefix steps.
