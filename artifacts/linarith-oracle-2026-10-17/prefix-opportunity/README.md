# Native proof-prefix opportunity

Original populations: miniF2F7808 and ProofNet5952, groups of32 in preserved
source order. Public source bytes are preserved in the two input gzip files.
SHRED revision a6616e99534ce777dcebfd56566eaaffb63997a8 supplies
LeanPrefix/Extract.lean and the exact rooted-trie accounting in
src/lean_prefix/prefix.py. The official parser ran under the retained matching
Lean4.9.0-rc1/Mathlib environment; raw native responses, errors and task counts
are retained. The192sources without a :=by delimiter remain fallbacks.

| Native-unit scope | miniF2F | ProofNet |
|---|---:|---:|
| Eligible candidates |7672/7808|5717/5952|
| Reusable exact rooted edge occurrences / parsed steps |8/29669|45/21530|
| Same, excluding inter-tactic trivia from edge key |3987/29669|3957/21530|

Exact edges preserve comments/whitespace as upstream SHRED specifies; syntax-unit
text excludes inter-tactic trivia but preserves internal tactic text. Neither
scope normalizes tactics semantically. Groups also require identical original
statement text; ProofNet has259eligible statement-specific groups over its186
tasks, so task labels alone must not authorize state sharing.

These are occurrence/byte opportunities, not CPU fractions or saved verification
time. Native execution and end-to-end comparison to Kimina batch remain pending.
Upstream SHRED's profile recommendation is not itself a generic deployed prefix
executor: its own README says to benchmark an exact prefix executor before
deployment. Distinguish our native trie adaptation from an upstream measured
whole-service result. Closed-root native kernel checking is included in the
private REPL used for the execution experiment.
