# Prepared isolated rerun of the42historical resource failures

This is original input preparation, not an executed experiment or changed result.
All42source IDs come from the completed fixed native full480 failure profile;
each complete code string is preserved from the original miniF2F input.
Every JSONL line submits exactly one candidate, all-mode, unchanged300s timeout,
reuse=false. CLI processing is sequential across lines.

After the existing full7808collection retires, run the built Rust engine through
the matching pinned Lean4.9project's lake env. Use total48GiB, no finite inherited
RLIMIT_AS, CPUs8–11, worker-cores4 to reserve the entire four-core point for a
single native attempt. This is the isolated point, separate from four workers
with one core each in the subsequent throughput comparison.

Decompress requests.jsonl.gz into a stream, pass it to gpu-smt check, and retain
stdout, JSON resource-event stderr, actual commands/environment/start/exit and
external cold controller wall time. Each native outcome/attempt retains PID
birth, resource preemption and sampled peak. Collect and compress the raw event
stream after retirement. No source/backend/dataset/model may be substituted.

Compare every native result to the old42AS-limited failures, reporting changed
acceptances, rejections, timeouts and actual total-budget failures separately.
These changes are resource-point effects, not transparent proof acceleration.
Then compare against fresh uncapped native execution at the same isolated point
before claiming per-candidate parity. Do not pool with old24GiB or concurrency2
clocks. No new full population starts until the healthy existing group retires.
CPUoracle remains frozen. This thread executes/reviews; no delegated agent.
