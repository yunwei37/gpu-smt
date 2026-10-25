# Exact duplicate coverage — existing miniF2F records

Root self-review. No new Lean, LP or GPU run was started.

Of 7,808 complete original candidate sources, 7,791 are distinct byte strings.
The sole duplicate group is 18 literal None sources, all originally Lean errors.
It accounts for 17 redundant submissions; there are no byte-identical substantive
proof candidates in this population. Source bytes are compared directly, with
no hash, whitespace normalization, theorem renaming or prefix reuse.

After keeping the first occurrence, repeated observed native HTTP intervals sum
to 13.337753652s of 43,121.2401169s cumulative HTTP intervals: 0.0309308211%.
This is overlapping request-work accounting under the historical resource point,
not whole lifecycle savings, a new-resource prediction or a measured speedup.

The engine's exact cache/coalescing remains a reusable component for workloads
with duplicates, but this population supplies essentially no performance case
for it. Do not attribute expected full-population acceleration to deduplication.
Continue the actual resource/multi-candidate/failure/code-workload work without
turning ordinary exact caching into a novelty claim.

result.json preserves every duplicate ID/status and the immutable source paths;
command.json and source-analyze.py retain the actual executed analysis.
