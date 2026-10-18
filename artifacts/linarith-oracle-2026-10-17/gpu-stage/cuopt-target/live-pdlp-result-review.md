# PDLP convergence and expired-owner evidence
Observed2026-10-18; root-only self-review. This is an intermediate execution diagnosis, not a successful end-to-end GPU result.

## Real evidence
Native wave756--759 enters00:31:00.909Z and times out00:36:01.153Z. The GPU job submitted00:33:33.441Z subsequently logs22,864,800 PDLP iterations at443.789 solver seconds and crossover0.00seconds. Submission during a native wave establishes association with that wave; exact request-to-job IDs were not captured in this version, so no individual candidate attribution is invented. The native wave has four operational outcomes, all retained.

[Trace](active-job-95ea9ac5-8a34-448e-b763-40df487d6e7e-solver-log.jsonl.gz), [extracted loop summary](live-pdlp-stagnation-summary.json), [partial wave clocks](partial-timeout-groups-at-stagnation.json). The generic returned nb_iterations field of other jobs cannot identify their PDLP loop count. Correct the earlier inference forward rather than rewrite raw records.

## Implementation diagnosis and authorized repair
The phase-I formulation is feasible but waits for optimality; feasibility does not imply fast dual convergence. An expired native client does not currently cancel its optional numeric request, so a dead owner's search can block live requests. The current full trial remains frozen, including failures, and its already-admitted CPU controls continue automatically; no hot parameter changes or new full grid.

Prepare a single necessary algorithm/lifecycle repair: directly solve the original equality feasibility system, enable upstream infeasibility detection, stop at first primal feasibility, use default crossover=false, and accept finite support hints only through unchanged exact repair and Lean checking. Never enable first-primal-feasible on the artificial-slack model, where trivial slack is feasible. Cancel a GPU job only when all clients of its joint batch have disconnected; retain other live batch owners. Log actual job IDs and original matrices for reproducibility. No tolerance, buffer, thread, time-budget or kernel grid.

Qualify on actual archived difficult LPs including negative systems, then matched native24-source preflight. No new full1000 run is admitted unless that preflight shows real benefit and unchanged verdicts. The original CPU result1.34668x is interim; broad goal/hourly automation remain active. GPU currently supplies untrusted LP support search, while numeric product expansion, exact repair and proof checking remain CPU/Lean. No claim of GPU product acceleration.

## Self-review and scope
The evidence falsifies crossover-dominance for this job, not all GPU use. One complete fixed1000 GPU variant is still in progress and has operational failures; final best(CPU,GPU)>1.5x remains unresolved. This is a self-review by the implementing thread, not an independent audit. Original source cohort,48GiB limit, matching baseline family and four RQs are unchanged.
