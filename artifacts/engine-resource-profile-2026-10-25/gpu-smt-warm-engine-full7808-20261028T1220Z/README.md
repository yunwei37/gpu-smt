# Full7808 four-warm resource baseline — complete first leg

The installed Kimina fb2393d Manager/run_checks returned all7,808original
candidates on2026-10-28T19:24:55UTC. The existing finite controller then retired
this leg and launched the frozen engine side. This archive is a complete warm
leg receipt,now followed by the complete engine cell at2026-10-29T01:03:39UTC.
The [complete result review](result-review.md) reports the full pair and limits.

| Final native status | Count |
| --- | ---: |
| valid | 3014 |
| lean_error | 4668 |
| timeout_error | 85 |
| resource_failure | 41 |

Internal whole elapsed is25175.270356s;external launch-to-exit25176.487277s.
Preparation3.026921s is already within internal whole elapsed,not added again.
[Warm terminal](warm/terminal.json),[external exit](warm-exit.json),the complete
[raw responses](warm/results.json.gz) and[physical attempts](warm/attempts.jsonl.gz)
preserve all outcomes and diagnostics. Original input bytes are in
[input7808.json.gz](input7808.json.gz).

There are7860physical attempts:7808ordinary plus52exclusive retries.
Ordinary outcomes:3014valid,4668lean_error,74timeouts,52watchdog preemptions.
Retries:41watchdog resource failures and11timeouts;all native results remain.
Serial exclusive envelopes sum12106.916135s;all physical envelopes sum
55651.175699s. The latter overlaps and is not whole wall. Neither is a
guaranteed saving from backfill. All41final resource errors explicitly identify
the aggregate-RSS watchdog,source,PID,birth and measured memory. They are
budget-limited failures,not41new allocator exceptions.

Same resource point:CPUs8–11,four warm REPLs,48GiB sampled aggregate actual
owned RSS,no fixed per-process AS cap,ordinary compiled Mathlib library,
300s per admitted attempt,unchanged sources and no completed-result reuse.
Four mapped native libraries and observed unlimited address limits are retained.
Across25167samples,the aggregate sampled peak is52365074432B(48.768776GiB),
with93over-budget observations and93largest-own-REPL kill records.
This explicitly includes watchdog overshoot;it is not a hard RSS quota.
The process-count samples include idle warm workers and cannot establish
active-candidate utilization. Full[RSS samples](warm/memory-rss.jsonl.gz),
[process exits](warm/process-exits.jsonl.gz),activity and kill records remain.
All209observed native PID/birth identities are no longer live at root review.

The frozen[adapter source](warm-run.py) drains/retries immediately. The frozen
engine13d4606defers retries behind its registered ordinary frontier.
This disclosed difference remains part of the resource-path comparison;do not
attribute any future ratio wholly to COW. The future adapter6252a78has the
matching frontier order but was never substituted into this running pair.

The historical fixed42subset inside this full warm run ends41resource failures
and1timeout,all on exclusive attempts. That is retrospective subset analysis,
not the separately planned fresh-native42experiment or a new independent run.
Failures and differences must remain in the final pair review.

All329closed raw/source files were preserved losslessly,including activity
and kill records;large files are gzip-compressed without source modification.
Original161355255B becomes10512696B before this index. Per-file byte
comparisons and all recomputed counts are retained in the
[step analysis](../../../docs/tmp/build-and-evaluate/step-0116-20261028T193629+0000/warm-result-review.json).
At the earlier step0116closure,only the complete warm leg was archived.
The subsequently completed engine leg and full comparison are added below;
the original warm raw receipts remain unchanged.


## Full pair completed — 2026-10-29UTC

Engine external20323.007642s versus warm25176.487277s is1.238816996x and
19.2778269%less elapsed on this one ordered shared-host resource comparison.
All7808final statuses and3014accepted IDs match. Raw payload/operational
wording differences remain;this is not universal artifact transparency or
a COW-only causal claim. Immediate-warm versus frontier-engine retry order
and CPU affinity differ. No workload-layer/GPU contribution follows.

The additional engine stdout/stderr,launch/exit,controller logs,terminal and
[complete comparison](comparison.json.gz) are now retained losslessly.
Only the original raw-log filename changes when recomputing through gzip.
The archived input,adapter and source definition are not replaced.

## Post-run response attribution

[Selected23source/model attribution](../native-response-origin-20261029/README.md)
explains optional-field serialization and embedded source-line boundaries using
the actual installed service and historical fresh corroboration. It does not
rewrite any raw/comparison data or replace the cross-context native limitation.
The resource pair remains a composite single-order result,not exact wire
transparency or a COW-only causal estimate.
