# Step0156 — native ordinary-failure transition implementation

BUILD_AND_EVALUATE;root only. This is native implementation/semantic evidence,
not completed workload measurement or scientific novelty.

## EXPERIMENT_GATE
E156.1:Implemented native/lean/failure-replay/FailureTransition.lean. Importing it
registers no interceptor/store;capture and replay default off. Qualified capture
uses pinned upstream Tactic.withRestoreOrSaveFull around runtime-aware exception
capture,retaining full failed state and action heartbeat charge. Normal returns
do not become failed records;known limit/interrupt/runtime/internal exceptions
are rethrown. The caller must rethrow captured/replayed ordinary exceptions
through the original native handler,not return tactic success or a source verdict.

The retained input holds all four reader contexts,the full Core/Meta/Term/Tactic
state and exact Syntax. Strict object identity is an intentionally conservative
same-process guard,not a semantic equivalence proof. Strong references prevent
recycled-address aliases;mutable referents/ambientIO/opaque effects still need
backend qualification. Cancellation and original remaining heartbeat budget are
checked before installing the recorded state/debit. Upstream overhead accounting
is approximate,so exact wall/timeout parity is NOT established. No production
Rust/REPL/HTTP hook or cross-candidate remapping is enabled.

E156.2:Finite pinnedLean4.9.0-rc1 native development checks onG10 CPUs6–7,PVC,
one natural-retiring compiler at a time,noMathlib population or signals.
The final module and control theorem compile exit0. Controls exercise original
default-off behavior;full failed goal,fresh-scope,pending-mvar and diagnostic
sequence restoration;exception propagation;recorded action debit;state/options/
syntax/budget mismatches;real assumption and simp_all no-progress failures;
logged simp_all unresolved-name errors;normal-open return;heartbeat,interrupt
and internal exclusions;final checkedTrue withoutsorry.

A custom finite action adds50000heartbeats so debit loss is observable without
slow search. This is not a timing measurement. Two separately compiled mutations
exit1 at the intended final-source assertions:omitting installation loses failed
post-state;restoring post-state with zero debit loses recorded action charge.
Final-results.json preserves exact commands,PID/birth,expected/actual exit and
natural retirement. Own-tree sampled max593956864B;host available min21598019584B.
Other development attempt logs and failed sources remain under experiment-001.
These are samples,not a hard quota or formal12GiB load qualification.

E156.3:Initial native fixture errors were corrected with evidence:
reserved syntax identifier prevented module compile;256recursion depth could
not elaborate the long finite declaration(raised to1024);unknown-lemma simp_all
logs an error but can return normally;default no-progress simp_all throws while
failIfUnchanged=false returns an open goal;unsupported-syntax dispatch differs
from a propagated abort internal exception. Final controls distinguish these,
rather than silently grouping them into ordinary failures. No population rate
is inferred from these custom cases.

E156.4:Windows direct management SSH timed out before the mutation batch began;
the batch directory did not exist when access returned. Pi's existingCloudflare
path reported G10Ready and Lease2026-10-30T00:51:55.729439Z. End-to-end Windows
key SSH via that existingPi path returned G10boot
a1bb482b-a7b7-4d15-bb6b-8db1dac37dd7,/readyz=ok,MemAvailable21180952KiB.
No evidence required or justified a host reboot. Same dev container retained.
No agent forwarding or saved proxy configuration was added.
Read-only ordinaryCoderSSH attempt used its existing client/keyring but returned
401expiredAPIkey;no credential/login/security change. Process1's label is base,
runtime-exec callers stacked. Normal-channel comparison remains unqualified.

## WRITE_GATE
Native README/API,existing native README and existing CI job now describe the
component and pin its separate4.9control SDK. Four-crate architecture unchanged.
Daily note records real implementation and remaining science. Paper related-work
already identifies full snapshot/HB primitives as upstream and population
failure reuse as unmeasured;those statements remain accurate,no benefit invented.
Source/API docs don't turn a pointer match into full replay eligibility.

## REVIEW_GATE — same-thread self-review
Reviewed default-off fast path,full post-state lifetime,source exception path,
resource exclusions,remaining-budget miss,reader/state/syntax guards and native
mutation failures. No cache admission from observed-input keys. No new logger,
collection,service,credential,permission,security setting,Workspace target or
clusterCronJob action. Hosted existingCI gets one pinned native control step;
full native/Rust CI is pending at publication. Production cache remains off.
The goal is not complete and is not marked blocked:substantive source/native
progress occurred,while full workload and access qualification remain open.
