# Step0144 — correct the native test filter in the contributor command

BUILD_AND_EVALUATE;root only;small OSS documentation bug discovered during
the user's requested G10 maintenance. Formal collection remains unstarted.

## EXPERIMENT_GATE

Entry:read contributor guide and actual Rust native differential declarations.
The documented filter matches zero of the six test functions;the corrected
native_task_memory_accept_reject_and_sorry_match_raw_stock_repl matches one.
Correct only that name;no Rust source,backend behaviour or test body changes.

Installed cargo metadata --no-deps --locked --offline confirms the referenced
integration target exists. No compilation/download/native test ran. Initial
cargo shim could not select a default;metadata used the already installed
1.98.1 toolchain binaries through a per-command PATH,without changing defaults.
Detailed validation is in experiment-001/documentation-validation.json.
PVC free space was about3.1GB;no new large build or cache was created.

## WRITE_GATE

Exactly one contributor command token corrected;all other text retained.
The current instruction remains how to invoke an existing ignored native
contract,not a report that it was executed onG10. No paper change.

## REVIEW_GATE — root self-review

Exact old/new filter match counts and cargo target verified. No redundant
test,helper,dependency,quota or Rust API change. Existing production/native
coverage remains what prior CI established,not a fresh local77-test claim.
One-line docs patch satisfies the open-source maintenance request;no full
research result,independent audit or novelty claim.
Commit/push this complete boundary. Current native resources still await the
existing lab approval;continue only authorized development work meanwhile.
