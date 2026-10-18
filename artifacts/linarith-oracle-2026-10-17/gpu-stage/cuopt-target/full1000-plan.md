# Full fixed-cohort robust CPU/GPU oracle trial
2026-10-17. CPU stage1.34668x; final decision remains best(CPU oracle,GPU oracle)>1.5x against strongest matched native fast/hybrid baseline. Do not close from CPU alone.

## Admission
Valid24-source preflight: native50.576581135s; HiGHS direct-support control collector41.008518123s plus recorded host lifecycle; GPU46.497715329s including0.114865852s host lifecycle.24 complete in each, zero verification-outcome differences. Full native JSON differs from reference at indices16,19,23; classify/preserve diagnostics rather than normalizing away.25 actual GPU requests/25 singleton batches/no backend errors, shared solver time6.519s. Synthetic convenience batching is not claimed on this native preflight. Earlier finite numeric8-request qualification produced actual1/3/1/3 batches and4/5 exact-repaired positive supports; a miss correctly requires fallback.

GPU is slower than the robust CPU control on24 but beats the native reference; full population has costly exact LP tails absent from this first24. Therefore one complete fixed1000 comparison is admitted; no new tuning grid. The result must compare all three paths and existing original CPU oracle1.34668x, including negative/partial results.

## Workload and methods
Use unchanged input-top1000.jsonl, original source bodies/order, native Lean4.27/Mathlib pinned, Kimina warm batch width4, one worker, CPUs12–15,48GiB RLIMIT_AS and zero core. Existing Lean4.9 prefix remains on20–23. Numeric diagnostic replay has finished, so no further CPU replay competes.
Order, fixed before launch: oracle-gpu phase-I cuOpt PDLP support, oracle-highs robust CPU support, fast-hybrid native baseline. GPU runs first so its finite device allocation can be removed while CPU controls finish, and the requested GPU data arrives first. This replaces the unlaunched baseline-first ordering; no measured full-cell result has been selected or omitted. A winning/threshold-ambiguous result requires reverse-order confirmation; do not promote a single order as robust improvement.

The original cheap CPU FP filter remains. Robust CPU uses HiGHS1.15.1 on the original scaled equality LP. GPU uses an always-feasible phase-I extension with nonnegative +/- artificial slack per row and minimum total slack. Ready queued independent LPs form a block-diagonal GPU problem; no artificial waiting timer. Both are untrusted support hints, repaired/verified exactly on CPU and checked by Lean. Direct misses use strong native fallback; native fallback misses still use exact tiered search. Do not weaken CPU control by forcing artificial-slack work.

## Cost and evidence
Whole source-native clocks include header/startup, export, all pack/IPC, queue/transfer/solve, repair, selected proof checking, native fallback and retirement. Add per-cell host proxy import/start/retirement explicitly. The upstream GPU target is a warm private server; its cold startup and initial82s image pull are separate deployment costs. A warm-serving speedup cannot be called cold-system acceleration.

Retain full native responses and verdict differences, per-source actual job intervals, every numeric backend response and batch membership, actual GPU solver state/iterations, source/candidate tails and full-cohort throughput. Rank actual candidate service intervals for top1% and10%; report their union/makespan and both endpoint clock costs, never sum overlapping job wall as total wall. Do not double-count shared batch solver time per member.
No sampled-CPU sum becomes a wall fraction. Full native result equality is stricter than outcome equality; report both.
Memory samples have process-exit read gaps in the new short-lived child path; preserve them and do not claim exact peaks.

## Finite lifecycle
All code/builds/Lean/test clients remain in original source Workspace/main; only upstream numeric cuOpt server consumes the second existing shared RTX5090 resource. Other GPU Workspace and prefix preserved. Parent collector owns host proxy startup and shutdown; cancellation cancels its own pending GPU job. On completed/failed finite GPU evaluation delete gpu-smt-cuopt-20261017 Job and verify restoration. Hourly automation and goal remain active until real result/valid bound resolves final criterion.
Root-only self-review; no subagent/OMP or independent-audit claim.
