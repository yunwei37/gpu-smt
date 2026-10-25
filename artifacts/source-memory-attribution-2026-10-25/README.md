# Existing source-memory diagnostic

[Result/self-review](result-review.md) · [raw result](result.json) ·
[per-source observations](per-source.csv) · [retained inferred samples](attributed-samples.jsonl.gz).

analyze.py reads the completed480profile only. It never starts Lean/solver
execution or mutates old raw data. It uses the existing partial-gzip reader
and same-run process/HTTP timelines, retains missingness and scopes old AS
limits separately from actual RSS. Exact commands/resource receipts remain.
New kind-tagged Rust RSS events are implementation prerequisites for reliable
future cost labels; they do not train a model or establish speedup.
