# Repair CLI termination through existing engine shutdown

FixedRQ2/resource-layer dependency,not new native performance evidence.
Scope:CLI SIGTERM/SIGINT termination and owned-attempt retirement; preserve
backend verification,queue/timeout/RSS/CPU/cache/consumer semantics and current
native fullpair. No new command/flag/dependency/service or native experiment.

The serve branch listens only to ctrl_c;check/measure install no graceful
signal path. SIGTERM therefore uses process default termination,skipping
Engine::shutdown and owned-child retirement. First reproduce the default signal
exit on the actual old executable with an idle service and no backend children.
Do not deliberately orphan a live verifier on the shared host.

Use Tokio's existing Unix SIGTERM/ctrl_c streams for all CLI modes. Serve keeps
graceful HTTP drain plus engine shutdown;interrupted check/measure first retire
owned native attempts then exit nonzero without emitting a complete capture.
Full completed captures and normal input/output stay unchanged. No SIGKILL or
startup-before-handler guarantee is claimed.

A subprocess protocol fixture,not Lean,holds one candidate. Send SIGTERM to
only the CLI PID for serve/check/measure and SIGINT for existingctrl_c path;
assert app exit meaning,owned PID retirement,and interrupted measure lacks a
complete capture. Test HTTP uses loopback ephemeral port only. Cleanup remains
bounded and targets only spawned fixture PIDs. Run ordinary workspace checks
under48GiB combined monitor/CPU10–11;real native tests remain skipped locally
because the preserved fullpair is the sole native collection group.
Document lifecycle behavior in API/architecture. Root self-review and raw
failure/success receipts,then one main commit/push. No full paper edit or new
novelty/performance claim;source implementation dependency only.
