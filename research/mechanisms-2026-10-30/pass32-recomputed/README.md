# Full-corpus pass@32 recomputation — 自审
Input7808 unique sources,244tasks×32. The exact pass@32 statistic is the fraction of tasks with at least one accepted candidate (k=n=32).
Baseline142/244=58.1967%; repaired144/244=59.0164%, +0.81967percentage points. Accepted candidate count3014→3045; no old accepted ID removed.
New tasks: amc12a_2020_p4 (16native-checked repairs) and mathd_numbertheory_541 (15). new-tasks.csv lists every candidate.
Each new accepted theorem was checked by stock Lean4.9.0-rc1 and has an explicitly printed transitive axiom closure contained in propext,Quot.sound,Classical.choice; zero sorryAx. Full-source errors/nonzero exit are rejected.
The source router changed only already-tested family sources. All other full-corpus source bytes are unchanged and retain their historical native outcome. This is a complete7808 acceptance overlay recomputation, not a new7808-invocation same-hardware experiment.
The baseline3014 sources have no explicit sorry/admit/axiom/native_decide/run_tac/unsafe/skipKernelTC tokens after comment/string masking and no sorry/axiom response diagnostics. That audit is not a fresh transitive-axiom closure check of all3014, and must not be described as one.
No same-resource throughput ratio is inferred by combining historical lab and finite phobos points.
