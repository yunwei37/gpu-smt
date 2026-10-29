# Step0153 — default-off failure cache in admitted engine verification

BUILD_AND_EVALUATE;root only;engineering dependency,not native replay evidence.

## EXPERIMENT_GATE
Implemented FailureCacheVerificationBackend and FailureCacheAdapter within the
existing engine crate. A generic associated-type store supports a dynamic bridge
backend. Default construction allocates no store and calls original verification.
Explicit enablement passes a typed store to the qualified backend's whole-source
continuation after normal Engine admission. No CLI/HTTP flag or stock Lean hook.

The hook must capture input before a fresh producer, revalidate live native
state/heartbeats and propagate the ordinary exception through original
backtracking. It must finish the remaining native source check; a failure hit is
never a source verdict. Source reuse=false still runs each source and does not
silently disable this separately opted-in tactic store. Enabled backend identity
is separate from default-off whole-source cache identity.
Resource-exclusive execution clears old references and delegates the ORIGINAL
retry/reclamation hook, without tactic replay. Prepared readiness and immediate
resource interruption forward unchanged. Engine waits for active retirement;
shutdown clears retained records before delegated native teardown. No metadata
lock spans backend execution or cleanup. No eviction/memory bound is claimed.

Five new actual Engine pipeline tests cover default-off, dynamic opt-in with
two accepted sources and a rejected one after the same tactic exception,
ordinary/operational separation, exclusive retry cleanup and shared source-cache
identity separation. Fixture final-check counts equal source counts. These use
a simulator,not native state,proof checking or workload performance.

### Validation and retained failure
G10,own Workspace,PVC logs,CPU6–7,single build job. Initial focused5 and public
store3 passed. A broader existing engine suite inadvertently included
owned_idle_preparation_is_included_in_total_rss;its child.kill() again received
errno13/EACCES at engine.rs:489.25other tests passed. The finite8MiB Python
child naturally exits after5s;no security/config change or retry of that kill.
This was a test-selection mistake,not a native long collection or cache defect.
The complete failure log and command remain in experiment-001/check-2.log.

Remaining checks exclude that known signalling-dependent fixture:25engine
integration tests,9selected library tests(including8store cases),1doctest pass.
Together with new5 and public3,this is43successful local cases,one known
environment-dependent failed case preserved separately. cargo fmt,clippy
all-targets with-Dwarnings and rustdoc-Dwarnings pass. No permission bypass or
ignored-test source change. Full existing CI remains authoritative for its own
environment and is pending at publication.

Initial sampled own tree max300449792B;remaining max326348800B. Corresponding
sampled host available minima20099407872/20899790848B. Compiler/test processes
retired;development samples are not the12GiB native point or hard quotas.
No Lean invocation or formal measurement;no missing8031data recovered.

## WRITE_GATE
README,API,architecture and existing daily note now distinguish actual optional
Engine integration from still-unimplemented stock native replay. No scientific
claim,RQ,denominator or paper performance result changes. No new crate,
dependency,daemon,service,config switch or control-plane mutation.

## REVIEW_GATE — same-thread self-review
Reviewed enabled and disabled routing,whole-source identity,backend-owned
exception continuation,resource-specific hook preservation,destruction order,
dynamic associated types and all altered docs. Default remains off. Native
state mapping,post-error/diagnostic replay,heartbeat parity,coverage and benefit
remain unqualified. Native long collection stays off under failed signalling.
All existing CronJobs and security/scheduling configuration remain untouched.
No delegation or independent-review claim. Next:close existing CI and continue
only useful authorized work without relabelling fixtures as native evidence.

Raw tool logs retain trailing blank lines verbatim;source/document diff checks pass.
