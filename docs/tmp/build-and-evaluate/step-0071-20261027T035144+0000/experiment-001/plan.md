# Plan — causal measured-sibling memory feedback

Parent step0070 finds that a fixed source model misses the resource tail,
while41 actual resource failures occur in four tasks. Within the continuing
RQ3 resource/workload mechanism,implement an opt-in TaskMemory<P> policy that
uses only already observed actual memory peaks from same-task attempts.
This is a new causal feedback mechanism,not lexical model tuning or a new
collection. No claim of novelty or runtime gain before native qualification.

Extend SchedulingPolicy with default no-op observation and identity-preserving
refresh callbacks. Observation supplies only positive actual peak bytes,not
proof verdicts or source-state handles. Namespace by native backend/resource
context,task ID and timeout. Unknown/anonymous tasks retain the wrapped policy.
Take the maximum observed footprint with any initial/source prediction;
never impose a per-worker cap or propagate acceptance/rejection. Users can
clear retained forecasts,and policy storage itself is counted in owned RSS.

The engine publishes feedback after native retirement and before returning
the lease. Eligible queued jobs refresh before each admission attempt,so a
forecast captured before an earlier sibling completes does not stay stale.
Do not call policy code while holding engine state locks. Keep existing
watchdog,exclusive retries,parent reclamation and all/first-success semantics.
TaskInterleave must forward feedback/refresh; TaskMemory must preserve ranking
and inner policy composition. Different backend/resources/timeouts cannot
silently share observations. Scope the wrapper to an engine/workload lifetime;
heterogeneous siblings can overreserve or serialize,so no safety/speed guarantee.

Validate context/timeout/anonymous/zero/maximum/reset behavior and a deterministic
integration fixture: a queued sibling forecasts before the teacher retires;
the teacher later reports a budget-sized observed peak; only then must the
waiting sibling refresh and take the existing exclusive path,after a peer
retires. Teacher rejection must not become sibling rejection. Compose through
TaskInterleave to test forwarding. These fake-backend/toy-memory tests are
not Lean proofs,full COW qualification or actual admission-performance results.

Run relevant Rust tests,workspace compile/clippy and formatting on CPU11 under
the existing combined-tree support monitor. No native proof collection,
no release/example rebuild that changes the frozen active capture. All
implementation/public API docs and raw tests go in one reviewed commit;
the current full native/prepared pair stays unchanged and must finish first.
Afterwards qualify the opt-in method on native same-resource inputs before any
full comparison. Root self-review only;no independent audit/deadline/gate/closure.
