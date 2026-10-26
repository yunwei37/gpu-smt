# Prevent backend admission after shutdown returns

A deterministic non-native regression holds the admission resource snapshot
after its initial health check. While it is held,shutdown sees no active lease
and returns. The snapshot then completes. On old code,a stale admission creates
a lease and invokes the backend after shutdown;the red assertion observes one
backend call instead of zero. The final result still says backend_error,so
checking only final verdicts would miss this lifecycle violation.

The fix rechecks fatal/shutdown state inside the active-state lock immediately
after sampling. If shutdown already returned,the new lease is prevented. If
shutdown races after that check,it must acquire the same state lock and sees
the inserted lease,then cancels/awaits it. The check also covers fatal watchdog
state set while admission sampled. No queue policy,budget,timeout or publicAPI
change. Existing engine tests still exercise cancellation/retirement.

## Actual validation

- red-001:inherited helper expected LEAN_PATH in the parent controller;it lives
  only in native children. KeyError before any cargo command. Preserve failure
  and remove that unused dependency for non-native Rust tests.
- red-002:old implementation plus regression compiles;test fails as expected,
  one backend invocation after shutdown returns (cargo101).
- green-001:fixed implementation passes the new regression and20existing engine
  integration tests (21total,cargo0).
- clippy-001:engine lib/tests with warnings denied passes0. Rustfmt check passes.
  Formatting after green is whitespace-only;clippy compiles the final format.

No additional native proof or second capture group ran. Existing combined1s
monitor covers the native71controller/descendants plus new compiler/test tree;
CPU11/one cargo job. Observed combined peaks30,671,077,376B(red),36,089,413,632B
(green),46,033,952,768B(clippy),all below48GiB at sampled points,no pressure kill
or monitor errors. These samples are not a hardquota/no-global-OOM proof.
The short support compilation competes forCPU11during native71reference timing;
this confound is recorded in its artifact. Do not call that clock isolated.

The running CLI binary remains72,263,456B,mtime1792994229.5977643,matching its
actual launch manifest. No rebuild/replacement of the collecting CLI or pinned
Lean modules;current71conditions retain theiroriginalbinary. Apply source fix
on a future fresh build after the group retires,not halfway through conditions.

Full failed/passed logs,exact engine and reused monitor helper snapshots,command/
resource receipts are preserved as losslessgzip. Fixture proof is about lease
ownership,not nativeLean accepted-set parity,MathlibCOW safety or speedup.
All execution/review is same-thread self-review,not independent audit.
