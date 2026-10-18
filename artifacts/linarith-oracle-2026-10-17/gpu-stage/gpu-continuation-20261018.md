# GPU continuation: corrected wall profile, racing and real batching

Updated 2026-10-18 UTC. Author/executor/reviewer: owning Codex thread; self-review only.

The single-request PDLP failures remain unchanged and retained. The earlier statement in 033a418 that GPU work would stop was too broad. The current route is open. The final result uses the better valid CPU/GPU oracle, compared against the strongest matched native baseline. Only an applicable measured optimistic ceiling below 1.5x can close GPU without testing the admitted racing/batching mechanism.

The 2,234.689173920 s native primary did not enable all-call phase profiling. There is no way to recover its missing phase timestamps from source response times. A separate corrected-family diagnostic must run with its own wall denominator and an uninstrumented matched check; it cannot reuse old header-stacked phase durations as if they belonged to this run.

The decisive measurement records all product expansion and all LP searches, including failed direct calls and native fallback, with source/call identity, wall intervals, shape and outcomes. It retains preprocessing, exact repair, certificate validation, queue and retirement costs. Instrumentation cost and missing coverage must be reported. A union of LP occupancy intervals or sum of thread CPU is not automatically a removable critical path; the counterfactual must respect candidate sequencing and batch barriers.

If the bound does not rule out 1.5x, test large-LP racing and real cross-candidate batches. A CPU solution remains live until a GPU support set has passed exact repair; a floating hint alone cannot win. Cancel and reap the losing work, including its cost. Speculation, IPC, cancellation and contention can make racing slower, so 'no slower than CPU' is a hypothesis to measure, not a guarantee.

Use data-derived LP shape eligibility, preserve tiny LPs on CPU, and compare native, CPU oracle and GPU oracle at identical candidate concurrency and total CPU eligibility. Keep 48 GiB, unchanged source outcomes and full costs. Do not change or stop the active corrected CPU or original prefix captures. No subagents or other executors are used.

Self-review: this boundary corrects a research decision, not a performance result. No new bound, speedup or batching claim has been fabricated. Full paper writing/review gates and independent audit remain incomplete.
