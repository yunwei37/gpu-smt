# Two workload mechanisms:primary prior art and research disposition

Root only;2026-10-29UTC. Finite scoped follow-up to step0123,not an exhaustive
novelty survey. Current latest verbatim user request is appended unchanged in
user-instruction.md. No other agent or competitor reproduction is used.

## Plain claims and branches

C1:idle verifier cores can execute independent work inside one request without
changing native results/resources. Check proof futures,asynchronous elaboration,
goal-dependency factorization and full accounting/cancellation.
C2:identical tactic states can avoid expensive reexecution,including failures,
without changing proof or resource-budget semantics. Check state/tactic learning,
certificate reuse,simplifier memoization and heartbeat replay.

Queries in order:
- Isabelle parallel proof checking futures Wenzel proof parallelism
- Lean4parallel tactics independent goals heartbeats
- Tactician tactic proof state cache failed tactics
- SHRED Lean theorem proof prefix caching verification
- site.arxiv.org Tactician Seamless Interactive Tactic Learner Prover Coq
- site.github.com/leanprover/lean4 simp cache memoize Simp.State cache Expr
- Lean parallel tactic all_goals par_iter independent metavariables heartbeats
- Parallel Proof Checking in Isabelle/Isar2009doi
- SHRED Closing-certificate
Primary source branches are followed below. Secondary wiki/Reddit/DeepWiki/
aggregator search leads are not used as evidence. Individual request seconds
are not retained;this dated pass is the verification window.

## Verified precedents

[Wenzel2013](https://arxiv.org/abs/1307.1944),EPTCS118pp57–71,
doi10.4204/EPTCS.118.4:read primary PDFintroduction and managed evaluation/
output sections. Proof promises/futures organize parallel work;regular values
and exceptions are memoized,environmental cancellation is distinct;task
dependencies/groups and ordered output are explicit. Parallel proof execution
and exception memoization are prior techniques. The2009authorPDFfetch times
out;do not claim its full reread. The2013primary text supplies the relevant
direct precedent and cites earlier work.

[Lean2021systempaper](https://lean-lang.org/papers/lean4.pdf) and
[official parallel tactic-monad source](https://github.com/leanprover/lean4/blob/master/src/Lean/Elab/Parallel.lean):
current ordered/greedy iterators retain states and cancellation hooks. This
current APIis not silently inserted into measured4.9. The retained4.27SDKhas
Elab/Parallel.lean;4.9does not. The original4.9isIndependentOf exists and is a
conservative assignment-dependency test. It does not establish arbitrary
tactic/state/diagnostic commutation.

[LeanTree2507.14722v1](https://arxiv.org/html/2507.14722v1) explicitly factorizes
states and handles metavariable coupling for parallel proof search/reuse.
Its workshop status and existing bibentry remain. Factorization is therefore
not our discovery. Additional idle-resource adaptation with complete native
accounting would need its own real evidence;this is a candidate question,
not an accepted new claim.

[Tactician2008.00120v1](https://arxiv.org/abs/2008.00120):primary PDFSections2.2
and4describe recording state/tactic transitions and a reconstruction sequence
cache with search fallback. Its learning interface abstracts away some shelf/
unification-map complexity. This is adjacent state-aware reuse,not proof that
a displayed state alone is our complete operational key.

[SHRED0.2.1officialsource](https://github.com/memo-ozdincer/shred/blob/d23598b04065bda07027a6ed1f20d3a1ee263623/README.md):
exact environment,tactic,target and ordered context select closing proofs;
hashes only locate buckets,structural checks/native typechecking/fallback
remain. Its prior recorded revision is not upgraded or rerun. Generic checked
closing-certificate reuse directly overlaps C2. The inspected source does not
establish our desired failure-cache/heartbeat guarantee;that is unresolved,
not a claim that no other work supplies it.

[Lean4.9CoreM](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/CoreM.lean)
matches installed source. withRestoreOrSaveFull restores saved state and adds
recorded heartbeats. Its own comment explicitly excludes some reuse overhead
and calls the accounting approximate. Heartbeat replay itself is existing
work. Pinned SimpTypes has context-sensitive cache rules;[official4.22notes](https://lean-lang.org/doc/reference/latest/releases/v4.22.0/)
document further cache reuse. Plain memoization is not a new contribution.

## Contrary evidence and exact disposition

Resource/caching/ordinary futures primitives have substantial direct overlap.
No novelty is inferred from a negative search or renamed implementation.
No new numeric competitor run is admitted;native/own equal-resource comparisons
and cited prior mechanisms suffice for current opportunity work.

The completed source reanalysis corrects18%to ProofNetrooted count;its expensive
outer repeats are82of3957. miniF2Fhas461of3987. Full key equality/cost is absent.
Current42resource-tail IDs map to old profileCPUdominated byeqRefl,not the
83-timeoutinterval_casesdistribution. Old CPUand new wall remain separate.
These contradictions change the next observation,not the original four RQs.

Need actual runtime independent-goal/dependency/cost and full-state equality/
heartbeat records after current42retires. Success caching,failed tactic
exceptions,operational resource failures and cancellation must stay distinct.
Successful cached terms still need kernel checking. Shared metavariables require
serial execution. Mere diagnostic hashes do not certify equal states/cycles.
Parallelism's physical work and the required native heartbeat/timeout behavior
must be checked;neither standard futures nor approximate replay proves them.

Coverage:all five user-named prior families plus direct LeanTreeand pinned
heartbeat primitive are addressed with primary assets. No exhaustive formal
equivalence/negative-cache literature survey is claimed. Root accepts only this
positioning/opportunity update;the two method questions remain open. Targeted
paper changes are explicitly requested by the user and do not replace thesis,
fourRQs,workload,consumer contract or OSDIobjective.
