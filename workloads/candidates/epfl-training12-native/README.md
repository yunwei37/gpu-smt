# Existing EPFL training candidates:12-case native diagnostic

Pinned EPFL training e5ff00a8, physical groups0/113/280/287.
After excluding exact?/aesop and unclosed comments, eligible frame16,688valid,
18,508ordinary-invalid,516budget-text-invalid. Reservoir seed20261030 takes
4per stratum.2,807search-text/19unclosed exclusions. This oversamples budget
text and cannot estimate natural arrivals or the1.6%/73% tail.

Native Lean4.15.0 commit11651562caae, matching-release Mathlib
9837ca9d65d9de6fad1ef4381750ca688774e608; publisher exactMathlib unknown.
-j2/LEAN_NUM_THREADS2,CPU0–7,M6144,10kHB,self-wall20s/case,300s/group.
All12sources' maxHeartbeats0 capped10k; no other code edited.
Fresh CLI includes imports, not warm throughput. Full raw inputs/replays/
logs/selection/frozen runner outside checkout in epfl-training12-native.

12actual returns:3compile_ok/no sorry,3ordinaryerror,6explicit10kHB.
No wall alarm, crash, startup or resource failure. Native wall29.39253s,
budget16.17880s=55.04% of selected sample; no population estimate/CI.
Capture30.038s,combined sampled9,317,634,048bytes includes old13733.
Native CPU/RSS per case in CSV;M6144/1Hz sampling not hard RSS guarantees.

Publisher/new-native cross: valid2compile/2HB; invalid1compile/3error/4HB.
training-rg0-row19776, amoeba_xor_function, publisher-invalid with recursion
error feedback, compiles here in1.881s. Source and annotation code text agree
after comments/whitespace/EOT-marker removal. This does not reproduce original
environment/resources/instrumentation: root cause unknown, not an established
label bug or equivalence claim. Two publisher-valid cases hit our smaller HB.
Publisher budget labels are not replayable deterministic failure certificates
at this reconstructed point. First diagnostics whnf/isDefEq/elaborator are
locations, not exclusive CPU phases or inevitable failure. Budget!=falsegoal.
