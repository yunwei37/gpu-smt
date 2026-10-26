# Task-heldout source-cost ranking — frozen-cost replay,not runtime speed

Uses only the complete original7808native capture at the new fourworker point,
not another native experiment or competitor reproduction.244tasks×32sources;
142tasks have at least one observed checked acceptance,102have none. All
backend faults/resource results/timeouts remain,no easy-subset exclusion.

## Predeclared protocol

Five folds split whole tasks:sort task IDs,fold=index mod5. All32siblings stay
together. Training-only standardization and unit L2regularization. Features are
log source bytes/newlines,semicolon fanout and12fixed tactic-token counts,
including comment text. This is a cheap heuristic,not a semantic parser.
No task/theorem IDs or future outcomes are features. Logistic model predicts
observed checked acceptance;ridge predicts summed physical-attempt seconds.
One declared score:P(accept)/(1+nonnegative predicted seconds),stable original
index ties. No hyperparameter grid,model-selection sweep or deployment.
All5Newton fits converge in6–7iterations. Models/scalers/fold IDs and every
heldout source prediction remain in raw compressed files.

Each task consumes ranked sources until first observed acceptance;unsolved
tasks consume all32. Cost is sum of existing native Attempt.elapsed_seconds,
including preemption/retries/retirement,excluding originalqueue. Reordering
does not magically change the frozen costs/outcomes in this replay.

| Policy | All-task frozen work(s) | Solved-task work(s) | First source accepted(tasks) | Sources consumed |
|---|---:|---:|---:|---:|
|FIFO|50527.116345|2408.034121|92|3631|
|Source bytes|49975.153224|1856.071000|95|3635|
|Heldout source-cost|50740.663170|2621.580945|90|3740|
|Future-outcome oracle|48637.216675|518.134450|142|3406|

Unsolved tasks contribute48119.082225s in every policy,95.2342%of remainingFIFO
work. Even a perfect future-informed within-task order removes only3.7404%of
this frozen work,ratio1.038857. This is NOT an Amdahl/end-to-end/GPU bound.
It does not constrain cross-task response latency,actual parallelism,pressure,
changed native outcomes or other failure-aware mechanisms. Solved-only work
would exaggerate the all-task opportunity.

The one heldout cost-aware model adds0.4226%frozen work versusFIFO;source bytes
saves1.0924%. This model is not worth installing/hardcoding into Rust or tuning
on these test folds. Direction2remains open:existing source-size/task-interleave
policies and more informative workload mechanisms need actual native/service
evidence. No result closes another direction or the whole research objective.

## Interpretation and resource limits

No deployed model,new service/native run,rejection predicate or shortened
timeout. Predictions never certify failure. Native resource/time budget labels
are observed acceptances,not theorem truth;costs are censored and pressure-
affected. FIFO and oracle preserve142observed solvable tasks by construction,
not a new acceptance differential test.

Source analysis2.705859s plus interpreter/controller cost is a one-time offline
analysis,not measured production inference overhead. Reused1s combined monitor
peaks10,566,365,184B with existing42owner443878/birth144092233,no pressure/error.
OnlyCPU11/one numerical thread;current42binary/environment unchanged and no
new proof candidates executed. Default data-analysis libraryalready exists;
no dependency or CLI/public API change. Source/driver/receipts/raw outputs retained.
Same-thread implementer/reviewer,not independent audit or a novelty result.
