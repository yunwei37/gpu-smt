# Native candidate scheduling

Original miniF2F32candidate/task scheduling for first checked success.
No prefix/certificate reuse or arithmetic oracle changes. This consumer
does not produce all RL candidate rewards.

[Existing-data opportunity and limitations](../../artifacts/candidate-scheduling-2026-10-25/result-review.md).
[Actual measurement plan](../../artifacts/candidate-scheduling-2026-10-25/plan.md).

Run with the retained Kimina Python environment:
    python bench/lean-candidate-scheduling/analyze.py --out /tmp/a-fresh-analysis --workers 2
    python bench/lean-candidate-scheduling/run.py --phase qualification --out /tmp/a-fresh-native-qualification

[Real native qualification](../../artifacts/candidate-scheduling-2026-10-25/native-qualification-20261025T0715/result-review.md)
is complete; the original7808 all/first-original/first-short matrix is active.
Do not start a second proof-collection group while its launch owner is alive.
Analyze closed groups with analyze-native.py --run <completed-group>. AST parsing and
offline simulation are not performance results. Full uses --phase full and
all7,808originals. Existing48GiB/max2/24each resources and sampled watchdog
remain unchanged. Reviews are root self-review.
