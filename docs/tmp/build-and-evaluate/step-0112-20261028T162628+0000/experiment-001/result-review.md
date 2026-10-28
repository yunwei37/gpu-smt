# Result review — pending source CI,self-review

Source replaces the co-scheduled async sampler with an owned parent thread.
Existing watchdog implementation still selects the largest active owned
attempt,retains PID/birth/source attribution and marks preemption/requeues.
Independent sampling does not make memory growth bounded between samples;
monitor/syscall/lock/OS delays remain possible.

Rustfmt parses/formats the two changed source files. No local compilation,
new native cohort or active binary change is performed. Existing source CI
must compile and run the two new controls plus required workspace/native
contract checks before qualification may be claimed.

The current full capture remains the older source point. No throughput,
accepted-set equality,48GiB hard quota or OSDI novelty is inferred.


First source80c271dCI40726840855fails Rust compilation(E0063):the existing
private paused-admission fixture initializes Inner directly and lacked the new
watchdog_workerfield. Add its default,unstarted guard. The production constructor
was initialized. No native benchmark/executable was changed. Full failed log
job122952278167and run/jobs metadata are retained. Pinned4.18native job
122952277663passes all5explicit controls;that does not override the Rust failure.
Qualification stays incomplete until corrected source checks actually pass.


Corrected-sourcef15197fCI40727967801passes fmt/clippy,all8engine unit controls,
all26engine integration controls(including both new regressions),all8Lean unit/
8process controls and5explicit pinned-native contracts. It then fails existing
CLI structured_resource_logs_do_not_corrupt_jsonl_results:an empty short request
exits before the new delayed first sample. Root had changed the old immediate
interval phase. Restore an immediate first sample with Duration::ZERO,then
retain the same nominal1s period. Do not weaken the existing log assertion,
insert fixture sleeps or call the partial workspace pass complete.
Failed job122956253072and successful native job122956253593full logs are retained.
