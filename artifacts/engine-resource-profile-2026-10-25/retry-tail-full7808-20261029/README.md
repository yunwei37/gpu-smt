# Complete full7808 retry-tail decomposition

Recompute with python3 artifacts/engine-resource-profile-2026-10-25/retry-tail-full7808-20261029/analyze.py from the existing frozen13d4606
warm/engine archive. No native request is executed. The existing queue-frontier
implementation is db8ecbf;source regressions and actual CI are retained in
[step0094](../../../docs/tmp/build-and-evaluate/step-0094-20261028T102232+0000/step-report.md).

All7850attempts have attributed native roots;all7869registered birth identities
have matching ownership releases. Exclude the persistent import parent538705,
then sweep registration-to-release envelopes against20322.829859s whole time:

| Candidate processes active | Envelope seconds |
|---|---:|
|0|3.786428|
|1|9379.564924|
|2|63.035755|
|3|224.689630|
|4|10651.753121|

The ordinary frontier ends22:31:12.985277UTC. First exclusive native registration
is22:31:13.163526UTC:all7808ordinary attempts precede42exclusive attempts.
The ordinary span is11176.649277s;four active candidate-process envelopes
cover95.3036% of it. This point does not support conservative ordinary
admission as the dominant remaining source of low concurrency.

Exclusive native envelopes cover9145.231930s,
44.9998%of whole time and
97.5017%of single-candidate
time. Only234.332993s of single-candidate
envelopes belong to ordinary attempts. This is the repaired point,not the
historical86%at another point. Exclusive results:41resource exhausted/1timeout.

The42reported attempt sums9146.153409s versus9145.231930s registered envelopes
have different boundaries. Warm52immediate exclusive attempt envelopes sum
12106.916135s;do not subtract these from engine envelopes as an isolated
mechanism gain. The complete clocks remain25176.487277versus20323.007642s.

Unused core slots during solo work are not automatically available memory.
A watchdog-truncated peak is a lower bound;41solo resource failures give no
safe ceiling for mixing small work. Finite ordinary-frontier-first is already
implemented/tested;retain it rather than reopen censored-peak overlap.
This is engagement evidence,not a new speedup or novelty claim.

Analysis uses CPU11for0.916s during the ongoing separate fixed42collection.
The output duration is per invocation,not a native performance datum. Raw pair
is unchanged. The analyzer asserts identity completeness,nonnegative sweep,
no >4candidate overlap,no overlapping exclusive candidate,and total time
conservation. No new logger,runner,control schema,policy or native job is added.
