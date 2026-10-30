# OpenAI math — W001 static inventory

Pinned source: openai/math commit4eaee87548250b2682affda7d05d947c05554bae,
upstream commit2026-10-30T00:35:35Z. Root and lean LICENSE are Apache-2.0;
dependency licenses remain separate. Exact dependency revisions are in the CSV.

Complete tree enumeration finds163,097 .lean files /1,785,499,363 source bytes.
A recursive OAI tree was truncated. Its returned partial entries were discarded,
then all direct discipline subtrees were enumerated without truncation.
inventory.json records every response's completeness. No source build occurred.
The old53,554file/474MB observation was a lower bound, not corpus size.

files.csv.gz retains every source path, Git blob ID, size and source group.
projects.csv groups by OAI/discipline/component, not independent Lake projects.
The publisher organizes a single large Lean library; dependency graph and
content statistics follow in the next stage. There is one observed workflow,
lock-prs.yml; no public build CI was found in this pinned tree.

Toolchain: leanprover/lean4:v4.34.1. This source release is not the historical
Lean4.9 candidate replay. Successful release artifacts alone cannot characterize
RL rejected candidates or per-proof search histories. Current counts establish
neither kernel acceptance nor native cost or causal timeout classes.

## Reproduce

Run inventory.py with --pin4eaee87548250b2682affda7d05d947c05554bae
and --out pointing to an output directory. It reads upstream Git trees and
metadata, not solver/generator output. It does not generate new candidates.

## Self-review / resource boundary

All work is by the W chat. Only workloads/ and docs/workloads*.md are owned.
No Lean process, security/configuration change, Workspace migration or other
agent is launched. W's ceiling is5GiB within the shared12GiB; this tree audit
uses small metadata only. Source contents are not yet counted in tactic stats.
Preserve all original records and other branches' dirty paths.
