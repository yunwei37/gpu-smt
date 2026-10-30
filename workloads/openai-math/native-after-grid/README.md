# Incremental native continuation after actual Grid completion

Same original batch3 targets/171-module closure.109 prior compiled objects
explicitly reused (including Grid);62 planned fresh modules. Lean4.34.1,
exact lockedMathlib, -j8/LEAN_NUM_THREADS8,CPU0–7,100kHB/M8192,
unprofiled, nominal120s native self-wall and1400s group bound.
Actual bounded group terminates cleanly; native/controller identities retired.

24rows:12native compiles,2self-wall censored,10dependency-blocked uninvoked.
38fresh modules were not started before the group boundary. Thus14actual
native invocations,48uninvoked across these two categories. This is not a
complete62-module attempt or full target/corpus build; absent rows are not
ordinary failures. Twelve successful original modules now have real objects,
including10Powers modules and TransformedPowers10.

Amplitudes self-censors at120.115s. Last KernelValues10 self-censors at41.935s
because only the group remainder remained. Its row's self_wall_limit_s=120 is
the nominal configured per-file cap, not the effective remaining wall budget;
do not classify it as having failed a full120s opportunity. All unsuccessful,
uninvoked and successful records retained. No censored source is proved false.
No original source budget value was changed in these14invocations.

Per-module native wall/CPU/RSS and exact own group sums in CSV. Captured total
1406.549s includes graph setup and monitoring, not cold fresh-backend throughput.
Combined1Hz sampled peak12,292,308,992bytes includes legacy censored13733.
M8192 and sampling are not hard kernel RSS quotas. Distinct earlier budget/
worker/profile points are not concatenated or reweighted as one full run.
This purposeful dependency-heavy stratum cannot estimate all163,097modules.

TableDensityValues and HighHeaders0 still lack compiled objects; the16real
Planar annotation-type query remains blocked. No axioms/sorry substitutes.
Raw selection/source-replay/logs/terminal/memory preserved outside Git:
PVC gpu-smt-captures/workloads/openai4341-native-after-grid.
