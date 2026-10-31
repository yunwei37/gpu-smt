# Cost concentration versus failure frequency

## Cross-dataset comparison (W036)

| Data point | Cost numerator | Cost denominator | Share |
|---|---|---|---:|
| miniF2F7808 |126budget-containing sources,38,795.133s|52,992.124historical worker-attempt s, retries included|73.21%|
| ProofNet5952,rep0 |70budget-containing sources,138.011s|1,192.435request s|11.57%|
| AutoVerus3566,3reps |58slowest processes per rep|639.238/631.215/632.607process s|3.315–3.399%|

AutoVerus's third-row metric is the slowest1.6%tail. Its budget-exceeded time
share remains unknown; it must not be relabelled as3.4%. All ratios keep their
own summed request/process denominator, not batch wall or a common hardware
point. Thus miniF2F's concentrated budget exposure is not universal evidence
about program verification or all Lean candidate distributions.

[M's original audit](../research/mechanisms-2026-10-30/generalization/README.md)
reports no whole-source recovery on ProofNet, EPFL or APRIL by the implemented
routes. ProofNet has56recursion/14heartbeat budget sources; the separate
operational source stays separate. The same70sources appear in all3retained
repetitions. EPFL's two checked arithmetic expressions recover0complete
sources; its six training HB cases were reviewed and do not match the proved
numeric fragment. This is observed method coverage, not impossibility proof.

[Exact comparison CSV and scope](candidates/cross-dataset-budget/) preserve all
seven Mpoints plus three AutoVerus repetitions. EPFL136/7/12 and APRIL39+39
remain unequal, stratified, budget-specific samples; none is a population
budget-time estimate. Previous sample/label/retirement limitations below hold.


AutoVerus direct native records contain3,566 candidates per repetition.
Top58 candidates (ceil1.6%) use3.399%,3.338%,3.315% of each repetition's
summed process elapsed. The tiny candidate tail consuming73% of Lean time
does not reproduce at this program-verification point.

This does not mean failed work is cheap in aggregate. Nonzero process exits
use94.99–95.02% of process elapsed:3,376/3,566 candidates exit nonzero.
JSON success=false alone uses91.92–91.97%. High failure frequency can
dominate cost without a concentrated slow-failure tail. None proves a
candidate was doomed before verification.

419 rows per repetition have JSON success=true but process exit1;17 exit101
rows have no native JSON verdict. Keep both axes in
[cross-tabulated cost](candidates/autoverus-outcome-time.csv) and original
receipts. Do not treat the JSON flag as whole-process acceptance or relabel
operational failures as tactic errors.

The denominator sums direct process elapsed per repetition, excluding capture
conditions and model generation; it is not batch wall or a hardware speedup.
No Verus rerun or verdict-changing intervention was performed.

[The earlier scenario gap audit](../docs/workloads-audit.md) remains linked.
This update stays under workloads/ per the latest W ownership restriction.
EPFL excludes timeout/operational failures, APRIL is a mutation distribution,
and successful-proof releases omit failed arrivals. None supplies uncensored
causal costs from labels or tactic tokens alone.


## Versioned native samples and constructed training releases

[EPFL136 native returns](candidates/native-versioned/epfl-completed136/)
have12explicit budget returns,159.68/623.80s (25.60%). This is a completed
prefix, not the full144-source plan; the unresolved exact?-search candidate
is separately censored and excluded from that denominator.
[APRIL39pairs](candidates/native-versioned/april39/) supply78actual returns:
16mutation budget errors consume50.53% of unweighted selected-mutation time.
Budget-text oversampling changes the released-test inverse-inclusion weighted
ratio to11.05%, without a confidence interval. It is not a natural arrival log.

EPFL's4.84million-row training release contains250,000publisher synthetic
pairs, fallback-recovered inputs and explicit exclusions of infrastructure,
missing-declaration and invalid-without-error records.
[Construction audit](candidates/epfl-training-provenance/) attributes those
counters to the publisher. [First-group](candidates/epfl-training-rowgroup0/)
and [three-group](candidates/epfl-training-random3/) static scans have no
per-row native cost. Label/annotation agreement partly follows enforced
filtering, not independent semantic validation.

Native tail ratios cannot be transferred directly between these samples,
Verus and the older Lean1.6%/73% point. Each needs its own runtime denominator,
budget provenance, arrival distribution and censoring analysis.


## A concrete stored-label non-reproduction

[Six fresh controls](candidates/epfl-label-reproducibility/) on
training-rg0-row19776 retain the released program/feedback. Original0HB,
annotated0HB and800kHB all compile; explicit recursion128 fails while256/512
pass. Our smaller heartbeat cap and annotation comments therefore do not
explain fresh success at this point. This does not prove the producer used
a low recursion limit or that its label was a bug. The reported Lean version
matches; exact original Mathlib/recursion/trace/target context is unavailable,
and producer implementation is not yet released. No original per-row timing
exists to attribute this to machine speed. Preserve both native and stored
verdicts. Native-semantic budgets and harness acceptance labels are different
measurement axes, not interchangeable facts about an intrinsically false goal.


### EPFL annotation-artifact follow-up (W028)
The same released amoeba_xor_function source and its feedback-annotated form
also pass in Lean4.15 when .ilean serialization is requested. That alone
does not reproduce LeanInteract's tracing/protocol. The confirmed discrepancy
remains a publisher label versus current native replay discrepancy, not a
proven label error. MaxRecDepth128 causes a native failure; default512 and
256pass. Original trace/options/Mathlib pin and pre-truncation source remain
unknown. No wallclock or machine-only causal explanation has been established.


### Research formalization: source counts and native budget tails (W032)

OpenAI math is a published source/reference workload, not an RL stream with
reliable candidate-validity labels. Full source coverage163,097files does
not establish full project acceptance. Version-matched native sampling is
partial:W02719/42probability costs,13/21cells observed,6complete.
Its later23-endpoint dependency group invoked11modules:7complete,2native
allocation exceptions at the selected-M8192point,1full600s censor and1group
remainder106.12s censor. Four budget events consume61.63%of1399.897s native
wall in this selected group, not1.6%of a population or evidence of falsegoals.
Interpreter is the allocation check tag, not a measured tactic CPU phase.
Each cause and its own denominator are in authored-sample23/time-by-budget-cause.csv.

The frozen sample retains failed/unreached endpoints; replacing them with
easier proofs would bias a cost estimate. Full successful-build CPU/95%CI
is not available from this budget-failed/incomplete subset. Uniform costs
also emit only.olean; normal Lake artifacts/setup are a separate scope.
The exact external Rellich dependency context requires the OAI4.34.1patch,
not the dependency's original4.29.1objects. Source lexical1.35million kernel
sites are not runtime check counts:Jet50shows944sites versus3938retained
shape-matched helpers after branching. Neither type dedup nor static tokens
establishes a timed global reuse opportunity.


### Current research-formalization cost point (W039/W041)

The historical W032 .olean-only/budget-tail numbers above remain frozen.
Current standard .olean/.ilean/.c sampling has26/42random observations,
11/21complete strata at M9216/j8/authored source options.
[Cost tables and assumptions](openai-math/standard-artifact-native-a/)
keep this new point separate from25/42old M8192 .olean-only costs.
Full successful-build CPU/global95%CI remain unknown; per-cell nominal
intervals are fragile normal-cost models, not full-build confidence.
[Six-draw precision extension](openai-math/precision-panel-plan/) is prepared,
not measured. Default OAI-root130,834modules and all-source163,097modules
remain different populations; neither can inherit static size fractions
as runtime fractions.
