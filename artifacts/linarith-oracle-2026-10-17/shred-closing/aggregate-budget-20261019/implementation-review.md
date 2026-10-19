# Root implementation self-review and actual kill-branch evidence

The current user explicitly authorizes a48GiB aggregate point and watchdog.
The earlier finite owner is stopped with exact PID/birth evidence; all partial
bytes remain. No Workspace/container/node quota, permission, other-project
setting or service manifest is touched.

The public capture defaults now use2source/live-worker slots and24GiB native
address-space limits. It rejects configurations whose source count times
worker limit exceeds the aggregate or whose aggregate exceeds48GiB.
The service's existing max_repls2setting bounds retained pool entries.
An actual async lifetime semaphore additionally holds its slot from native
startup until process wait/retirement, covering asynchronous destruction.
Idempotent close also handles a worker already killed by the watchdog.

Parent capture's independent thread samples its owned root/descendants every
second; it tracks previously seen PID/birth pairs through reparenting and
counts RSS for controller/server/backend/lake/native workers, conservatively
including shared RSS multiple times. It does not inspect or select foreign
processes. It chooses the largest actual native REPL in that sample, verifies
its owner group belongs to this exact tree, records candidate/header/body
activity and kill notice, then sendsSIGKILLonly to that group.

The original SDK status remains in sdk_status. A structured top-level native
allocation error or watchdog notice becomes resource_failure in capture
outcomes, never a Lean rejection/proof. Actual stderr and returncode remain.
Unexplained exits and ordinary timeouts are not inferred to be memory failures.
No message/error/proof payload is synthesized as accepted.

Actual fault injection uses two original candidates from the24-source cohort,
with a64MiB test-only RSS threshold to exercise the same code safely. Both
return resource_failure overHTTP200, with no retry-induced acceptance.
The two notices identify minif2f-0/minif2f-1 and their distinct native PID,
owner PID/birth/phase. Each victim equals the largest native RSS in its sample.
The root-wide peak is4099465216bytes (about3.82GiB), below48GiB; at most2native
workers are observed, their real address limits are25769803776bytes.
All processes retire. This validates execution/attribution, not full budget
saturation or any verification speedup. The24-source normal paired runs
are still active and are a separate condition with actual48GiB threshold.

The watchdog is sampled, not a kernel RSS quota: it may react after a transient
overshoot. Worker count/address-space bounds act before allocation; the RSS
guard also counts non-native overhead. This limitation is explicit.
No mock,48GiBallocation stressor, delegated reviewer or independent-audit
claim is used. Fresh full7808acquisition must wait for both normal24-source
terminals and the real kill-branch checks. Unsafe old queues are not restored.
