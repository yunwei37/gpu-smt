# EPFL compiler-training corpus: one complete physical row group

Source: [pinned dataset/card](https://huggingface.co/datasets/EPFL-LARA/lean-compiler-training-corpus/tree/e5ff00a803d6a4a346a53d2116664c184c946bd7),
Lean4.15.0. Explicit dataset license remains unknown: no license declared in the
observed card. Raw source/annotations are not redistributed here.

The actual Parquet footer reports4,836,380rows,414rowgroups,3columns and
4,460,281,081bytes. Publisher card reports2,168,417valid/2,667,963invalid.
Only rowgroup0 was fully fetched/decoded here:24,945rows,13,064valid and
11,881invalid (47.63%). This physical first group is not a random sample;
its label ratio is not an estimate of the whole corpus. No whole-file scan or
complete publisher-label recount is claimed.

source_code is evaluator input. validation is source annotated with goal
states and compiler messages, the feedback model's supervised target; it is
not a validation split or a timing column. All11,881invalid rows have at least
one error block; all13,064valid rows have none. Ordinary diagnostics are
first-error keyword buckets, not independently revalidated semantic causes:
6,178tactic_failure,2,282unsolved_goals,1,383typing_or_instance,
804rewrite_no_progress,381unknown_name,305explicit_native_budget_text,
192no_goals,182parser,115other,51tactic_reported_refutation and
8publisher_memory_or_restart_diagnostic. The8publisher MemoryError/restart
messages are kept separate from native Lean budget messages. No budget-failed
candidate is treated as a false target. First-error precedence can hide later
errors. A reported tactic refutation alone is not a replay certificate.

tactics.csv counts lexical tokens in source after nested-comment/string
masking, both occurrences and row incidence by label. It does not measure
runtime calls or executed branches.18invalid sources have unclosed block
comments and are excluded only from tactic counting; labels/errors/size counts
retain them. Exact source-byte fingerprints find24,945distinct inputs, zero
extra duplicates in this group; no goal-state/strategy-result reuse claim.

Sources total45,588,215UTF8bytes. Valid median1,309B; see source-sizes.csv
for exact interpolated quantiles (valid p99 = 8,428.22B; invalid p99 = 14,556.60B).
No native elapsed time exists in these three columns: the fraction of compute
spent on budget-exceeded rows and the1.6%/73% tail hypothesis remain unknown
for this corpus.

Reproduce with PyArrow installed:
python workloads/candidates/training_rowgroup.py answer_data.parquet --row-group 0 --out OUTPUT
For a sparse range capture, decode only explicitly materialized groups.
Actual range capture outside Git preserves header, complete rowgroup0 column
chunks and footer; its apparent4.46GB sparse length is not a full download.
Allocated disk roughly25MB, compressed group range23,139,799bytes.
Raw metadata, pinned card, partial file and frozen analysis are on PVC under
gpu-smt-captures/workloads/epfl-training-{static,rowgroup0-static-v3}.
All row counts match native Parquet metadata. Analysis natural-exit0;
W combined1Hz sampled peak10,358,792,192B includes concurrent native build
and old censored EPFL process, not this analysis's isolated memory.
Earlier v1 coarse buckets and v2 missing-import failure remain in raw captures.
