# GPU arithmetic counterexample screening — RQ4

User-directed own-method experiment. Stop extending external SHRED/Kimina/
Farkas comparisons; retain their existing evidence. The existing native
request boundary is reused only to run our method off/on on identical
original candidates, not to integrate another competitor.

Hypothesis: a consequential fraction of failed arithmetic attempts reach a
genuinely false supported goal whose exact counterexample can avoid expensive
native search. Existing failed request time alone does not establish this.

First characterize the full retained miniF2F native outcomes/time and
arithmetic failure messages. Build a native Lean goal/context extractor at
actual tactic entry. Record supported typed arithmetic AST and complete
propositional context; unsupported/metavariable/dependent terms fall back.
Do not use unconstrained linarith atoms as semantic variables or infer false
from numeric solver failure. Candidate failure is distinct from false goal.

For a counterexample, every supported assumption must be true and the goal
false under exact rational/integer evaluation with correct native type/domain
constraints and local definitions. GPU float evaluation only proposes points.
CPU exact verification authorizes early arithmetic-tactic failure, never proof
acceptance. Preserve enclosing first/try/repeat alternative behavior, rather
than kill an entire candidate because one branch has a false goal.

Measure observed supported/falsified goals by final candidate outcome and
historical own request cost, preserving unknown/no-witness/unsupported classes.
If the real opportunity survives this measurement, prototype a batched
point-evaluation kernel on RTX5090 and compare off/on at the same candidate/
resource point. Report complete costs, accepted/rejected/incomplete/resource/
timeout outcomes, failed-source and timeout distributions separately. No
assumed accepted-set invariance or whole-wall speedup from overlapping sums.

All work root-only, main/existingWorkspace. Max2actualREPL24GiBeach,
48GiBaggregate sampled ownRSS includes any GPUprovider. One fullgroup only.
Original workloads/failures/raw remain. No third-party reproduction or solver/
kernel tuning grid. Real qualification precedes any full end-to-end pair.
