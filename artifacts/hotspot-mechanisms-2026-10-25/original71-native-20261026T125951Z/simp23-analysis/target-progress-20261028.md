# What continues the six observed inner-round simplifications

This analyzes already retained2026-10-26native4.9instrumented traces. It adds no
observer,native run or engine rule. Step0066already reported the possibility
of a proof-bearing rewrite creating a fresh target goal;that source reading
is prior project knowledge,not today's new empirical result.

## Actual continuing-round attribution

| Source | Completed round followed by next round | No hypothesis-type update in that round | Historical observer outcome |
|---|---:|---:|---|
|175|2631|2631|runtime fault|
|1816|2603|2603|runtime fault|
|5913|965|964|timeout|
|5919|1786|1785|timeout|
|6807|2639|2639|runtime fault|
|7771|1480|1480|timeout|
|Total|12104|12102|3runtime faults/3timeouts|

A counted round has a target-end record and an actual subsequent round-begin
inside the same wrapper invocation. Compare its cumulative hypothesis_updates
with the preceding round's value,or zero initially. At unchanged count,the
pinned loop has only target goal-ID change left as its modified trigger.
5913contains2wrapper invocations at the same source byte;they are separated,
rather than treated as one recursion. First incomplete/final censored rounds
do not enter the continuing-round denominator. The emitted false
action_completed field is not used. All tagged event counts match the retained
per-source analysis exactly. [Raw-derived values](target-progress-20261028.json)
retain source log paths,call counts/ranges and historical fault classifications.

This does NOT show that the target expression is identical across rounds.
The earlier expression_hash_hint samples a subexpression passed to the pre
callback,not an exact whole-target snapshot. It also omits Meta context,
proof assignments,configuration and simplification procedure state. These
observations therefore identify where progress is being reported;they are
neither cycle certificates nor new0/6proofs of impossibility. Coverage of a
validated early-failure rule remains0. They are not23source or7808source wall
fractions,and cannot be multiplied by the old timeout CPU percentages.

## Native mechanism and the unfulfilled proof obligation

Pinned [SimpAll](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Meta/Tactic/Simp/SimpAll.lean)
sets modified when a hypothesis type changes or target simplification returns a
different goal ID. [Target result application](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Meta/Tactic/Simp/Types.lean#L655)
uses equality-proof replacement when a rewrite result has a proof.
[Replacement](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Meta/Tactic/Replace.lean#L22)
creates a fresh goal even if the resulting target expression is unchanged.
Thus a changed goal ID alone is not evidence of a smaller semantic problem.
The traces above do not record which replacement case actually occurred.

The step limit is per individual simplifier invocation.
[Simp.main](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Meta/Tactic/Simp/Main.lean#L658)
constructs a new Simp.State using only retained Stats fields. In
[State versus Stats](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Meta/Tactic/Simp/Types.lean#L123),
the latter carries theorem-use/diagnostics but no numSteps/cache. A subsequent
hypothesis/target call starts its own counter;the per-call maxSteps guard does
not itself cap the number of outer simp_all rounds. Other native heartbeat,
recursion and runtime resource limits remain. This is not an infinite-execution
proof or justification for changing those limits.

A useful sufficient witness still has to establish the exact target/context
transition,exclude relevant metavariable/procedure-state changes,and show that
the enclosing candidate cannot recover/continue to acceptance. Returning early
from a saturated tactic could otherwise make its later norm_num/omega path
reachable within the request budget and change the accepted set. Nothing in
these records establishes those obligations. No no-op suppression,shorter
timeout,withoutRecover switch or generic loop detector is enabled.

## Existing upstream work is citation-only here

At inspected upstream commit
[18fd0d63a8d69613](https://github.com/leanprover/lean4/blob/18fd0d63a8d696139cfc49869f1c4fd3a4faf0f9/src/Lean/Meta/Tactic/Simp/LoopProtection.lean),
Lean already offers looping-simp-argument warnings. Its optional linter is off
by default;the wrapper can force a check after recursion-depth failure.
It simplifies a supplied theorem's right side and warns on failure,skipping
theorems with local free variables. The original failure is rethrown by the
[wrapper](https://github.com/leanprover/lean4/blob/18fd0d63a8d696139cfc49869f1c4fd3a4faf0f9/src/Lean/Elab/Tactic/Simp.lean).
It does not certify early rejection of arbitrary full candidates. Generic
loop warnings therefore cannot be our contribution. No upstream version was
installed or benchmarked;the resource comparison's native4.9remains unchanged.
[Source observations](target-progress-source-observation-20261028.json) record
actual byte equality with pinned official4.9sources and the inspected newer
revision. No field-wide novelty decision or accepted-paper claim is made.

## Reconstruct the counts from the original logs

The following is a calculation over existing JSON fields,not a new runtime
observer or a maintained parser tool. Run from the repository root:

    import collections, gzip, json
    from pathlib import Path
    root = Path.cwd()
    path = root / "artifacts/hotspot-mechanisms-2026-10-25/original71-native-20261026T125951Z/simp23-analysis/target-progress-20261028.json"
    expected = json.loads(path.read_text())
    for row in expected["sources"]:
        instances = collections.defaultdict(int)
        rounds = collections.defaultdict(dict)
        tagged = 0
        with gzip.open(root / row["raw_diagnostic"], "rt") as stream:
            for line in stream:
                prefix = "[gpu-smt-simp-stage] "
                if not line.startswith(prefix):
                    continue
                event = json.loads(line[len(prefix):])
                tagged += 1
                pos = event.get("invocation_byte")
                if event.get("phase") == "elaborate-arguments" and event.get("event") == "begin":
                    instances[pos] += 1
                rd = event.get("round")
                if not isinstance(rd, int) or rd == 0:
                    continue
                item = rounds[(pos, instances[pos])].setdefault(rd, {"began": False, "target_end": None})
                if event.get("event") == "begin":
                    item["began"] = True
                if event.get("event") == "end" and event.get("phase") == "target":
                    assert item["target_end"] is None
                    item["target_end"] = event
        total = unchanged = 0
        for observed in rounds.values():
            previous = 0
            for rd, item in sorted(observed.items()):
                end = item["target_end"]
                if end is None:
                    continue
                updates = end["hypothesis_updates"]
                assert isinstance(updates, int) and updates >= previous
                if observed.get(rd + 1, {}).get("began", False):
                    total += 1
                    unchanged += updates == previous
                previous = updates
        assert tagged == row["recorded_events"]
        assert total == row["counts"]["continued_completed_rounds"]
        assert unchanged == row["counts"]["continued_without_hypothesis_type_update_rounds"]
        print(row["id"], total, unchanged)

Root self-review only. No independent auditor or new native acquisition.
