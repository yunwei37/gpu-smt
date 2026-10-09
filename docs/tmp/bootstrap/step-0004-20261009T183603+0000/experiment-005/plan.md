# Experiment005: RQ2 native prepared-context behavior and cancellation

## Research question and admission

Exact RQ2: Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?

Specific uncertainty: can the CLI-owned lazy context qualified in experiment004 retain native behavior across prefix parser EOF, forked suffixes, changed sibling order and a actually killed sibling? Role: supporting. Positive evidence admits this concrete preparation boundary for later resource/service tests; it cannot establish a service contribution by itself. A normalization or split-call discrepancy rejects that interface; a branch/order/post-cancellation discrepancy rejects that particular boundary. Missing kill landing leaves cancellation coverage incomplete. This is not a necessary thesis-wide falsification. The stronger alternative, real equal-resource service comparison, needs a qualified boundary; repeated constructor or coarse module profiles cannot supply these absent events. Real generated Lean attempts remain pending at the existing GPU allocation, independently.

The largest credible story is useful behavior-preserving native preparation and bounded disposable histories beyond established warm/logical/snapshot reuse. Generic fork is prior art. RQ meanings, strongest native snapshot/warm/cache/CPU baseline families and complete heterogeneous scope remain unchanged.

## Expected and competing outcomes

Expected: complete non-statistical native requested responses match the unchanged same-source CLI across the restricted prefixes, with killed children unable to mutate parent memory. Competing explanation: parser boundaries or inherited global/resource/random state change outcomes even with unchanged assertions, or cancellation fails to land. A single complete response, artifact, error or exit difference contradicts exact local response identity; execution validity is distinct from parity. Artifact identity does not prove model validity or semantic equivalence for unobserved inputs. UNKNOWN is preserved, not treated as rejection/acceptance improvement.

## Primary sources and real assets

Reuse pinned official Z3 ddb49568d3520e99799e364fb22f35fc67d887b1, unchanged source-built CLI/static library, official `parse_smt2_commands` and owned `cmd_context`/shell command installation. Source: https://github.com/Z3Prover/z3/tree/ddb49568d3520e99799e364fb22f35fc67d887b1 . Source EOF returns without clearing context; native reuse helper is also available. Prefixes contain no verification, finite timers, parallel tactics, callbacks or input-directed stream replacement. Source timer atfork handling and single-task refusal checks bound this preparation condition; they do not prove arbitrary fork safety. The new wrapper keeps interactive=true, matching qualified stock `-in -smt2`; fresh file input versus original stdin remains an explicit adapter factor.

Published protocol/metric authority: [SMT-LIB commands and responses](https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf); native Verus verification [SOSP2024 artifact](https://verus-lang.github.io/paper-sosp24-artifact/). Reuse prior public VeruSAGE sampled tasks and their actual captured native queries, retained in artifacts/native-branch-2026-10-07/full/inputs. These are 156 captured solver streams/440 checks from a selected published-task run, not full historical agent candidate traffic. Complete ordered native queries and request markers are unchanged. Reuse existing response observer from experiment004; no new SMT parser, inserted commands, oracle or budget.

Retained prior splits are comment/whitespace-normalized. All `.full` bytes equal existing group `.prefix` plus `.suffix`; original bytes remain the independent reference. Group membership comes from existing repeat0 branch provenance, not outcomes. Observed groups:106 streams/108 commands/9464 prefix bytes and50 streams/1 command/30 prefix bytes. Preparation-byte counts do not measure costly shared work.

## Comparisons and fairness

One behavior reference/control: unchanged same-source CLI executes each original input independently. Its competing position is that the native interface only preserves behavior when original bytes run independently. A matched run is essential because no published work settles this exact native state boundary. There is no speed-superiority comparison here.

Controls: fresh owned-lazy driver on retained `.full` (normalization/interface), split calls in one owned context (parser boundary), sequential fork children (proposed boundary), reverse sibling order (history control), cancellation before normal siblings (lifetime control). Six conditions are not six main baselines. Each original suffix/check/resource option/request remains unchanged, no preparation check or warmup, no accepted-only filtering. All are one CPU-affinity core8, sequential normal children, same static library/native budgets. Affinity does not establish isolation. No concurrent siblings or process-tree admission/resource policy is tested. Release compatibility retains experiment004's version-frame difference and is not reasserted by same-source parity.

## Workload, metrics and repetitions

Primary: per-input complete SAT/UNSAT/UNKNOWN response identity, and exact native non-statistical requested response bytes, availability/error/exit identity. Statistics are retained but excluded only from exact byte identity because timing/counters are expected to vary. Native models after UNKNOWN are requested artifacts, not verified satisfying models. No SAT/model-validity/proof/core coverage is claimed where the input lacks it. Preserve every stdout/stderr, error, missing frame, nonzero exit and partial killed output. Original requested-command positions define response framing independent of the proposed method.

Three whole matrix repetitions, condition order forward/reverse/forward; normal index order fixed except explicit reverse siblings. Full normal cells156×6×3=2808, checks440×6×3=7920. Fork modes have2 parents each per repeat:18 prepared parents,1404 normal children. Counts distinguish launcher processes, leaf response cells and canceled controls. Three repeat consistency is not distributional generalization; no tail/service/statistical speed claim.

Cancellation input selection before outputs: maximum check count, then largest retained suffix bytes, then lowest original index in each complete group. This selects58 (25 checks,437926 bytes) and87 (1 check,1179 bytes). Six total full-run cancellation attempts. Parent reads the first native SAT/UNSAT/UNKNOWN response followed by existing native DONE output, records live proc/smaps then sends SIGKILL, drains output and wait4 reaps the exact owned child before normal siblings. Sampling introduces a race; require observed native check decision and marker, kill return0 and actual SIGKILL wait status for landed cancellation. A completed race is reported separately, not retried until favorable. Kill after a check response is a native-progress boundary, not guaranteed interruption inside solving; this limits cancellation inference. Partial output can include multiple completed responses due to read buffering.

Secondary descriptive costs: parent/child raw smaps, wait4 child CPU/RSS/wall, launcher elapsed and affinity/load/topology. Parent CPU includes earlier process initialization while wall starts at parsing, so do not assign identical stage intervals. Summed RSS is not fleet memory/PSS. Sequential branch lifetime removes concurrent memory-density evidence; actual PSS receipts are diagnostic only. These costs are not RQ3 answers.

## Execution

Build only the new wrapper with artifacts/native-prepared-2026-10-09/build-driver.sh, linking unchanged existing source objects/static library. No rebuild or modification of previous release/source/frontend targets. Required runner/analyzer are thin invocation/response inspection glue; native frontend is authoritative.

Real preflight, one original stream46, all six paths once, full group's selected cancellation58:

```sh
python3 -u bench/verus_native_prepared_probe.py artifacts/native-branch-2026-10-07/full --source artifacts/native-frontend-2026-10-09/z3-source --driver artifacts/native-prepared-2026-10-09/native-z3-prepared --cores 8 --repeat 1 --index 46 --out artifacts/native-prepared-2026-10-09/preflight1
python3 tools/analyze_native_prepared_probe.py artifacts/native-prepared-2026-10-09/preflight1
```

Full same command without `--index`, repeat3, output artifacts/native-prepared-2026-10-09/full. All declared normal cells and cancellation attempts must reach terminal status; native parser failure/exit, missing cells/frames and cancellation races remain rows, not exclusions. Expected negative semantic results do not prevent completing the comparison. Runner refuses existing output directories and preserves raw partial runs; recovery uses the actual same valid path and retains interrupted attempts. Own subprocess groups only are cleaned on runner interruption; children have parent-death kill and wrapper-owned signal/reap handling. Do not stop unrelated jobs.

Outputs: raw inputs/outputs, launches and leaf rows, cost.tsv/smaps/proc receipts, jobs/provenance/completion, unchanged executed source snapshots and derived analysis. Plan frozen before preflight; any runner/metric deviation recorded, affected comparisons rerun when required. No experiment-control interface or fabricated runtime evidence.

## Interpretation and intended display

Positive: complete normal response identity supports only the observed native prefix/sibling boundaries; landed cancellations support post-disposal response isolation at recorded native progress points. Negative: preserve concrete changed response/location and distinguish fresh, split and branch effects. Mixed: local parity with races or changed diagnostics limits scope. Inconclusive/invalid: missing native engagement, unmatched input/backend or analysis incompleteness blocks those conclusions. Supporting RQ2 boundary table lists exact coverage, per-condition differences and landed/raced cancellations. No service speed headline, RQ closure, general semantic equivalence or OSDI acceptance follows.
