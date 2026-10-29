# Step0146 — standalone typed tactic-failure cache contract and fixtures

BUILD_AND_EVALUATE;root only on the existing G10 Workspace/PVC. This implements
the direct request for Rust development while the lab-placement answer is
pending. Formal8031 capture remains stopped. No scheduling/permission change.

## EXPERIMENT_GATE
Engineering prerequisite,not a new paper experiment. [Plan](experiment-001/plan.md)
and [result review](experiment-001/result-review.md) distinguish the prototype
from native replay,full-state hit rate and workload benefit.

Core defines FailureReplayBackend/TacticCompletion;engine implements a standalone
FailureCache/FailureInput within the existing four crates. Qualified records
carry complete failed transitions;scope is captured before fresh execution.
Replay yields a typed native exception for original failure/backtracking,
not tactic success or a source verdict. Operational/resource cases do not
produce ordinary entries. Backend replay and opaque record destruction happen
outside the metadata lock. Stock Lean adapters/default verification stay unchanged.

Eight new simulated unit tests pass on final source. Public simulated example,
fmt,all-target clippy and warning-free rustdoc pass. Local workspace check
reaches49passes and2existing Lean lifecycle failures with2explicit process-test
exclusions,then stops before later targets. Earlier unexcluded/exclusion attempts
and raw errors remain. Same-UID signal diagnostic reproduces errno13 TERM/KILL
denial on G10;no test/CI weakening or permission workaround. Full CI is pending.

Nominal1s sampled development tree max535,994,368B across retained commands;
no budget interruption. CPUs6–7,one-job compact development builds,outputs on
PVC;not formal48GiB/CPU8–11 performance. All helpers/processes retired;the
finite validation driver is retained as provenance and its temporary copy removed.
[Exact command/results](experiment-001/validation-summary.json).

## WRITE_GATE
Public API,rustdoc,architecture,README and runnable example explain the optional
standalone boundary,native exception propagation,hidden-state/resource/lifetime
obligations and absence of a stock native adapter. Existing engine CI gains the
example command while retaining full workspace/native checks. No dependency,
crate,service,Cargo feature,CLI/HTTP option or native collector is added.
Paper measurement claims remain unchanged;no full paper writing loop claimed.

## REVIEW_GATE — same-thread self-review
Initial boolean return refined to a typed native exception;extra Clone/Sync
bounds removed where not required. Lint type-complexity fixed with a private
alias,not suppression. Eight fixtures cover state effects,HB debit,budget misses,
scope/input/restart isolation,cancellation/invalidation,fault propagation and
lock lifetime. Raw negative/interim checks retained. No native semantic/throughput
claim,no independent auditor. Production activation remains disabled. Commit/push
the implementation boundary,then record actual CI terminal evidence.
