# Incomplete native replay, not population timing
Snapshot2026-10-30~11:09UTC:214 completed invocations.
EPFL136of144:53compiler passes,71ordinary compiler errors,12budget-exceeded.
Completed EPFL cost623.799s;12budget-exceeded requests159.678s(25.60% observed).
The8unreturned requests include one actively blocked candidate. This incomplete
frame cannot estimate population-tail concentration or answer transfer of
the old1.6%/73% finding. Top3of136completed costs10.20% is only a censored
completed-prefix statistic; not an estimate for full EPFL or its missing timeouts.

APRIL78of78startup returns:all invalid -D max_memory,including39references.
These are configuration failures,not invalid proofs or native budget failures.
The original capture statuses are retained in raw_status; derived status
corrects their classification. Do not use their costs as proof-verification time.

EPFL request index214:the authoritative active input is214.lean and source
theorem exercise_2_19a. It contains exact?. Both native threads were sleeping;
CPU~1.85s stayed unchanged,while RSS~4.4GiB stayed stable.
No assertion of deadlock root cause or intrinsic proof-search timeout.
PID13733/birth741054360,SIGINT errno13 despite same observed AppArmor labels.
Existing host SSH also closed without command execution. No security,Pod or
other process changed. The native child remains alive: no second W Lean starts.
The original parent checks1500s only between requests; a blocked call defeats
that batch bound. Heartbeats do not bound time spent waiting.

46budget-diagnostic occurrences belong to12requests; whole-request times
repeat in budget-diagnostics.csv and MUST NOT be added per diagnostic.
Native phases/tactic-time partition are not measured here.
All native source/log/partial/memory records remain on PVC outside Git.
Snapshot:/workspaces/.agent-state/gpu-smt-captures/workloads/
candidate-native-v1-snapshot-1109; original candidate-native-v1 still observed.
APRIL repair prepared,not executed:declare C++ shell max_memory as a Lean
option in a tiny imported module,retaining-M8192 runtime enforcement.
It requires real qualification after the existing child retires.

A separate OS-only self-timer control passed:natural sleep0.1s returned0;
sleep5s armed before exec with1s ITIMER_REAL returnedSIGALRM after1.001s.
No external kill,security change or second Lean invocation. This does not
qualify Lean delivery,does not reclaim the existing blocked process and is
not a new acceleration method. A future replay is prepared with a declared
120s/self-alarm bound plus remaining batch time; wall-budget exhaustion would
be separate from native heartbeat exhaustion and ordinary rejection.
Not enabled in the running capture. Reference:
https://man7.org/linux/man-pages/man2/setitimer.2.html
