# CLI handled termination and owned process retirement

Root-only implementation/self-review,2026-10-26. Operational resource-layer
repair,not native performance evidence or a failure/timeout detector.

## Actual defect and reproduction

The old executable's serve mode listened only to ctrl_c;SIGTERM used default
termination. check/measure had no graceful signal handling. An actual idle
service reproduction exits-15 instead of graceful0. It launches0backend
children deliberately,so the old defect is not demonstrated by orphaning a real
verifier on a shared machine. The missing cleanup path is established by source
inspection;do not claim a measured old orphan. Repro command/PID/birth/source
and output are in repro-before.json/repro-before.log/repro-source.py.

## Repair

Register SIGTERM before launching candidates and select it alongside SIGINT.
serve drains HTTP handlers through the existing Engine::shutdown. Interrupted
check/measure stop admissions,await owned-attempt retirement and exit nonzero.
Input/output errors also await shutdown before leaving their work branch.
No new command,flag,dependency,service,timeout,CPU/RSS policy or schema.

The first targeted compile failed because an async signal block borrowed a
stream moved into the server's static shutdown future. The retained log/source
show that invalid attempt. Owning the signal stream fixes the borrow.
Held-body process fixtures then pass all3CLI modes and check/SIGINT.

Idle-input testing exposes another real failure:Tokio's blocking stdin reader
keeps Runtime::drop waiting for caller EOF after the engine has shut down.
The failing3s diagnostic is retained. After awaited native retirement,the CLI
uses Runtime::shutdown_background so an idle input reader does not prevent
process exit. This does not skip native cleanup or add a runtime timeout.

The first concurrent CLI-suite run exposes a fixture handshake race:Path.write
creates an empty PID file before filling it. This is test synchronization,not
a production shutdown failure. Publish readiness by atomic rename instead.
The failed source/log are retained. fixture-race-cleanup.json records0still-live
matching fixture processes at containment inspection;do not claim a killed
orphan. The fixture has a bounded60s hold;no real Lean candidate executes.
Clippy then rejects a collapsible test cleanup if;fix without an allow-rule.

## Final executed checks

final/receipt.json and commands/logs retain actual final execution:
7CLItests,fmt,Clippy-Dwarnings,51ordinaryworkspace tests/0failed/4ignored,
and rustdoc-Dwarnings allpass. Four actual native differential cases are locally
ignored to preserve the sole native collection. No Lean proof is run here.

The new tests cover held candidates in serve/check/measure under SIGTERM,
check under SIGINT,HTTP error-response drain,owned PID retirement,nonzero
interrupted CLI status,no fabricated complete measurement,and idle open stdin
in check/measure. They use an explicitly labelled Python protocol fixture,
not native proof responses. SIGKILL,startup before handler installation,and
arbitrary FFI/crash containment remain outside this claim.

## Resources and scope

Final development run uses CPU10–11 and combined own+originalfullpair1s sampling.
Peak14,982,926,336B<51,539,607,552B,0pressure/errors. Old idle repro is0.3s with
no backend child;its own engine logs are retained rather than falsely claiming
a complete external combined interval sample. Sampling is not a kernel quota.
Originalfull PID408739/birth140695363/release/host remains untouched and live;
preserved-fullpair.json records the final snapshot. No restarted or mixed-source
measurement,no population speed/parity claim. Resource and workload research
remain active;the frozen CPU oracle is not touched.

Diff scope is CLI lifecycle,test boundaries,and API/architecture paragraphs.
main.rs net+31lines includes moving existing service/input branches;the
219test lines cover actual cross-processHTTP/input/signal/cleanup coordination,
not a new framework. No README QuickStart,workflow,dependency or paper narrative
is changed. Review is self-review,not independent audit.
