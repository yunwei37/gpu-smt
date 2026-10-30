# Prior mechanisms and applicability — same-thread self-review

Search date:2026-10-30UTC. Claims:reuse of repeated resource-limited verification
work;cost-aware exact first-success ordering;age-based preemption/restarts.
Queries included "SATzilla portfolio based algorithm selection SAT",
"Luby Sinclair Zuckerman optimal speedup Las Vegas algorithms",
"SOAP Gittins heavy tailed jobs","Weitzman Pandora rule",and
"best of N early stopping verification adaptive sampling".

Primary sources inspected:
- Xu,Hutter,Hoos,Leyton-Brown,JAIR32(2008)565–606:
  https://arxiv.org/pdf/1111.2249 .
  Empirical instance features and hardness prediction select among solvers.
  Cheap feature-based cost/ranking models are established technique,not novelty.
- Weitzman,Optimal Search for the Best Alternative,Econometrica47(1979)641–654;
  primary working-paper copy:
  https://dspace.mit.edu/entities/publication/990c36ff-57d4-4d0e-916e-2db6a4e93969 .
  Harvard PDF retrieval timed out;MIT metadata verified. Pandora optimizes
  costly search with random rewards/reservation values,not our exact finite
  accepted-set verification contract. A probability/cost ranking alone is not
  a new mechanism,nor a general Pandora optimality proof for correlated siblings.
- Luby,Sinclair,Zuckerman,IPL47(1993)173–180:
  https://www.cs.utexas.edu/~diz/pubs/speedup.pdf .
  The independent randomized Las Vegas runs are essential to the universal
  restart guarantee. Restarting a deterministic Lean prefix without changed
  search randomization need not escape it;discarded work must be charged.
- Scully,Harchol-Balter,Scheller-Wolf,SOAP(2018):
  https://arxiv.org/html/1712.00790v2 .
  The model is M/G/1 with lossless,penalty-free preempt-resume;Gittins minimizes
  mean response time under its assumptions. Killing and restarting a Lean
  candidate is not such a resume mechanism,or an automatic batch-makespan theorem.
- Kalayci,Raman,Dughmi,Optimal Stopping vs Best-of-N(2025 preprint):
  https://arxiv.org/abs/2510.01394 .
  Reward-based stopping already connects Pandora and LLM inference.
  Predicted reward stopping differs from exact finite pass@k:an observed-unsolved
  problem must finish every candidate in our requested contract.

For two independent Bernoulli candidates with expected complete costs c_i,c_j,
i-before-j costs c_i+(1-p_i)c_j versus c_j+(1-p_j)c_i. Pairwise interchange gives
descending p/c. This stated special-case derivation is ours in this report;
it does not transfer the full Pandora/Gittins guarantees to correlated candidates,
resource-constrained four-worker execution,censored traces or restart overhead.

Novelty disposition:high same-mechanism risk for generic algorithm selection,
ordinary p/c ordering,cancellation and restarts. Possible workload-specific
contribution still requires a sound native transition/resource model plus
nontrivial full-workload benefit. No competing system is reproduced,none of the
four directions/RQs is closed,and no new scope or claim is silently adopted.
