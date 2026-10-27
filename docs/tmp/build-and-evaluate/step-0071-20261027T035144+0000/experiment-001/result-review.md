# Result self-review — measured sibling memory

Root self-review, not independent audit. This is a reusable implementation
boundary supporting RQ3, not a new real-workload performance experiment.

TaskMemory<P> is opt-in and keeps wrapped ranking. The engine serializes its
immutable backend identity and Config into the callback context. Task ID and
timeout complete the history key. Positive physical-attempt observed peaks
are published after retirement, before lease release; no cache hit or extra
coalesced subscriber invents another observation. An eligible queued job
refreshes outside engine locks on each admission attempt. TaskInterleave
forwards observation/refresh and preserves ranking. A maximum never reduces
an initial reservation. Unknown/empty task IDs do not share memory.

The causal regression deliberately removes only publication of observed RSS.
It fails with exclusive-reclamation count0 versus expected1, not a compile
failure. Restoring publication passes: an already-queued sibling sees the
teacher's measured peak and uses existing exclusive admission after its peer
retires. Teacher is rejected; sibling is accepted. No verdict is borrowed.
The other new test covers namespace/timeout/anonymous/zero/max/reset behavior
and both wrapper compositions. These are fake backend/toy memory fixtures,
not proof validation or a claim of native parity/performance.

Green:22engine integration tests,1engine unit test and1compiled public doc
example pass. Core library has0tests; do not add it to the passing-test count.
Workspace all-target check,Clippy -Dwarnings and all formatting pass. No new
native test runs while the sole frozen7808pair is active. Existing process/
native tests outside these named targets were not rerun or silently called
complete. The entire workspace was compiled, not fully runtime-tested.

All support processes are restricted toCPU11 with one Cargo job and combined
own-tree1s RSS sampling against the existing48GiB budget. Red peak is
50,934,038,528B below51,539,607,552B;green39,330,553,856B;doc18,697,375,744B.
No support abort or monitor error. This is sampled evidence, not a hard limit.
Support CPU overlap can confound the ongoing full pair's clocks and remains
in its record. No active binary, native environment, input or policy changes.

Observed preemption peaks are lower bounds. A costly teacher can overreserve
or serialize small siblings. History grows with distinct context/task/timeout
and itself consumes RSS; scope to a workload lifetime or clear explicitly.
Existing watchdog/exclusive retry/parent reclamation are still mandatory.
Default scheduling remains unchanged. Native matched qualification and then
end-to-end resource/throughput/accepted-set comparison remain pending, after
the current group actually retires. No novelty or acceleration is claimed.
