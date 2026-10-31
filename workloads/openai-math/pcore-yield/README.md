# W yields the shared P-core lock

The user directed W to cancel every not-yet-started continuation and let M's
profile matrix and O's calibration/replay finish first. At06:28:45UTC,
wrapper38309/birth748045910 received SIGTERM after its actual command, birth
and absent capture-start were checked. It left no native child. The original
launch stays unchanged; queue-cancelled.json is an additive cancellation record.
The active37246 cohort is unchanged and may finish normally.

## Future W submissions

pcore_launch.py inspects /proc/locks arrow-marked waiters using the shared
file's actual device and inode. Existing waiters defer execution. Lock take is
LOCK_EX|LOCK_NB: a busy lock also defers, without joining a kernel wait queue.
It checks waiters again after taking the lock and releases it if one arrived
in the race window. The successful path execs taskset -c0-7 while retaining
the same existing lock descriptor for that command's lifetime. No daemon,
queue, sleep/retry loop, host setting or other lane is modified.

An empty wait queue **does not prove M/O are finished**. W must not submit
again until their profile/calibration/replay completion is actually verified.
During that priority hold, use only E8-23 preparation/analysis. Do not run the
successful launch path merely because a gap appears between their cases.

Read-only inspection (returns75 if somebody waits; acquires nothing):
    taskset -c8-23 python3 workloads/openai-math/pcore_launch.py --inspect

Only after M/O completion has been verified:
    taskset -c8-23 python3 workloads/openai-math/pcore_launch.py -- COMMAND ARGS

A75return means not submitted, not queued, and no native result. Do not
replace it with blocking flock or loop retries. Record that deferred state and
wait for the other lanes' actual take/finish evidence before a later attempt.
Frozen captures already running retain their original source and protocol.

## Controls and input readiness

Six untimed E-core controls passed: exact arrow/identity parsing, different
devices, preexisting waiters, a post-take waiter, exclusion on a free private
fixture and a real owned fixture holder returning busy with no waiter entry.
The fixture child exits naturally; no native Lean, actual P-core lock take or
performance claim. Real-lock inspection returned75 with M PID11027; raw
control/inspection/cancellation evidence is included here and retained on PVC.

Meanwhile the fixed six-draw conditional extension has a prepared native-input
union of2,385not-yet-cached jobs/19,920,109source bytes on PVC
workloads/openai4341-precision-native-prepared. All copied bytes match the
immutable public sources; fixed seed and conditional draw roles remain.
No launch exists. The complete source union is2,403modules; individual closures
overlap, so remaining counts must not be summed. These inputs are not compiled
objects, new cost observations, proof acceptance or a global CI.
