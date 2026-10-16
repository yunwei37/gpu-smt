# Root correction: Meta opportunity denominator

Observed2026-10-16. The earlier E038 root-disposition incorrectly called23.61% an entry count fraction. That statement is wrong and is corrected forward; raw source/data and earlier reports remain intact.

Actual experiment-033/full-observed-category-groups-20261016.json records:
- no-metavariable outer_cpu_ns3,078,852,745,407;
- any-metavariable outer_cpu_ns9,962,195,441,627;
- total observed wrapped completed outer thread CPU13,041,048,187,034ns;
- no-metavariable observed outer CPU fraction23.60893619%;
- no-metavariable outer-entered208,151,681 / total293,112,273 =71.01431778%.

The actual meta-observer.c uses CLOCK_THREAD_CPUTIME_ID at the observed outer wrapper entry/exit. Thus23.61% is a measured instrumented calling-path CPU-time descriptor. It is not the share of counts, all verification CPU, total dynamic Meta cost, fullwall, state-independent argument work or parallel/GPU-ready work. Private/same-object/loaded-DSO calls can bypass the wrapper; timing adds overhead and excludes clock-failed/incomplete calls. Outer no-mvar flags also do not prove every inner operation is state-free.

For the user's requested opportunity calculation, write the actual target as alpha × beta × gamma: alpha is paid end-to-end defeq critical-path fraction, beta is the target no-mvar portion under the SAME covered timing denominator, and gamma is the independent argument-comparison portion inside that work. Existing data provides beta=0.236089 only for this observed wrapped outer-thread-CPU denominator. It supplies neither the same-run end-to-end alpha nor gamma. E032's35% inclusive sampled CPU and E033's23.61% cannot yield a measured strict end-to-end ceiling by multiplication. The previous1.067–1.090 values remain sensitivity scenarios, not predicted speedups.

A coarse conditional budget inside the observed wrapped path is at most3,078.853thread-CPU seconds if every no-mvar outer call were removable; actual independent arguments are a subset of it. That is not a fullwall savings bound or GPU result: coverage, observer overhead, multithreaded overlap/critical path, transfers/packing/fallback and unobserved calls prevent that interpretation. No new GPU backend is admitted from these quantities. Current E038 instead directly tests native end-to-end method costs against actual batch prior art, and its24-input preflight is adverse. Preserve those failed routes and complete the declared real corpus comparison before proposing more narrow device work.

This correction changes a mistaken explanation, not raw measurements, the original broad Lean/SMT/RTX5090 goal, RQs or research contract. No new observation program, correctness campaign, model/service or experimental quota is added.
