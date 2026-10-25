# Native candidate scheduling

Original miniF2F32candidate/task scheduling for first checked success.
No prefix/certificate reuse or arithmetic oracle changes. This consumer
does not produce all RL candidate rewards.

[Existing-data opportunity and limitations](../../artifacts/candidate-scheduling-2026-10-25/result-review.md).
[Actual measurement plan](../../artifacts/candidate-scheduling-2026-10-25/plan.md).

Run with the retained Kimina Python environment:
    python bench/lean-candidate-scheduling/analyze.py --out /tmp/a-fresh-analysis --workers 2
    python bench/lean-candidate-scheduling/run.py --phase qualification --out /tmp/a-fresh-native-qualification

The native runner preserves the sole active480capture and refuses overlap.
Its real qualification/full measurement remain pending. AST parsing and
offline simulation are not performance results. Full uses --phase full and
all7,808originals. Existing48GiB/max2/24each resources and sampled watchdog
remain unchanged. Reviews are root self-review.
