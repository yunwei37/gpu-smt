# Candidate scheduling: existing-data opportunity — root self-review

## Question and consumer
For each public miniF2F task, obtain one fully checked valid candidate from its
32released candidates. After success, cancel pending siblings. This is
pass@k/best-of-n inference, not every-candidate verification or RL reward
collection. No prefix or certificate sharing is introduced. Ordinary
first-success scheduling is not itself claimed as novel.

## Evidence and identity
All7,808native results from the completed corrected pair remain, including
3,014valid/4,669Leanerror/83timeout/42resourcefailure.244task identities come
from existing task metadata and the producer32-record layout, checked against
every available theorem declaration.18literalNone failed candidates are
retained in their task, not dropped. The initial strict declaration parser
stopped on723; its error and command remain as offline.log/command.json.
The corrected offline-v2 analysis makes that source boundary explicit.

Of244tasks,142have at least one valid candidate and102have none. Only17of83
timeouts belong to solvable tasks;66remain in unsolvable groups, so another
method is still necessary for that cost. Native timeout HTTP spans sum
24,966.405942s of43,121.240117s total cumulative HTTPspans. Both are overlapping
request clocks, not additive machine CPU or whole elapsed.

## Offline scheduling model

Each candidate reuses its observed HTTPspan as an independent fixed service
cost. Two workers run; cancellation/prediction/setup costs are zero. Actual
request costs may change with ordering, warm state, replacement and overlap.
The all-candidate model21687.482849s happens to be close to observed native
whole21693.761299s; that fit does not validate the changed policies.

| Policy | Model seconds | Ratio versus same all-candidate model | Model completed candidates | Cancelled observed timeouts |
|---|---:|---:|---:|---:|
| all_candidates_original_order | 21687.482849 | 1.000000 | 7808 | 0 |
| stop_first_original_order | 14926.195717 | 1.452981 | 3639 | 17 |
| stop_first_short_code | 14693.324702 | 1.476009 | 3725 | 17 |
| round_robin_original_order | 14803.176432 | 1.465056 | 3631 | 17 |
| round_robin_short_code | 14659.452074 | 1.479420 | 3724 | 17 |
| hindsight_valid_fastest_first | 14446.829113 | 1.501193 | 3406 | 17 |

Every modeled policy retains the same142solved task IDs. This is a consequence
of replaying already-known labels, not a new native correctness result.
A deployable short-code order uses only comment-stripped source size.
It solves96tasks with the first candidate versus92for original order, but
only108at first2versus112and118at first4versus125: shorter code is not uniformly
a better success predictor. The full ordered first-k curves are in result.json.

The hindsight valid-fastest order reads unavailable outcome/time knowledge;
it is an opportunity control, not a deployable algorithm. Its cumulative
span-work minimum is28,830.779821s, giving1.495667relative to all observed
span-work. The ideal two-worker fixed-cost lower bound is14,415.389911s.
Neither value is a physical end-to-end Amdahl bound or an actual acceleration.

## Implementation and next actual measurement
bench/lean-candidate-scheduling/run.py reuses the frozen native HTTP transport
without changing oracle code. It gives at most one active candidate per task
and two active requests globally, skipping pending siblings only after a
native checked success. Thus the first implementation has no in-flight sibling
to kill; no speculative process cancellation is claimed. A later extension
can measure paid in-flight cancellation if useful.

The paired group contains all-candidate native, original first-success, and
short-code first-success. All use unchanged sources/native binary/300s/
CPU8–11/max2REPL/24GiBeach/48GiBtotal, common warm preparation and complete
retirement. Preparation, queueing, result handling and final cleanup are
inside each wholeclock. Source slots explicitly distinguish unexecuted
cancellations (missing proof time) from native rejections. Model costs/labels
are not inputs to runtime ranking.

Before the full7,808group, the real8-source qualification covers checked
success with queued cancellation and unsolved task exhaustion. It has not
run while the sole480profile is live. Syntax parse is implementation evidence,
not a real qualification or speed result. Compare actual solved task IDs with
the all-candidate control, retain all raw native and consumer/cancellation
records, resource failures, tails and actual retirement. No second collection
or agent starts; no performance threshold or deadline is imposed.

## Recompute
Use the retained Kimina Python environment:
python bench/lean-candidate-scheduling/analyze.py --out /tmp/a-fresh-scheduling-analysis --workers 2
The actual invocation uses separate '--workers','2'; see offline-v2-command.json.
Raw paths and scope are in the script. Self-review independently checks
244task count,142solvable, per-task total spans and hindsight minima.
This is root self-review, not independent audit. Existing watchdog covers
the short analysis plus live profile root; its memory summary stays separate.

The generated per-task CSV used standard CSV CRLF endings; it is preserved
byte-for-byte as offline-v2/tasks.csv.gz. The executed analyzer source is
retained beside it; the current writer explicitly selects LF for future
analyses. No source input/result or numerical value is normalized away.
The real8source qualification uses0–3and64–67: one solvable task and one
baseline-unsolved task, rather than mistakenly using32–35from another
solvable task. This correction precedes any runtime execution.

The task-held-out source-only learned ranker is recorded in
crossfit/result-review.md. It does not improve the existing-data model;
retain its negative result without adding a redundant full cell.
The planned actual group still compares all-candidate native, original
first-success and short-code first-success. This is implementation selection,
not a performance gate, deadline or route closure. Runtime consumer lifecycle
now includes model/source sorting and postprocessing/closed-log compression;
offline training and shared input materialization are reported separately.
