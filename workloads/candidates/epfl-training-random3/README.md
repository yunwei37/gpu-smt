# EPFL compiler-training corpus: three sampled physical groups

Same pinned dataset e5ff00a803d6a4a346a53d2116664c184c946bd7, Lean 4.15.
[Official source/card](https://huggingface.co/datasets/EPFL-LARA/lean-compiler-training-corpus/tree/e5ff00a803d6a4a346a53d2116664c184c946bd7).
Dataset license unknown; no raw source/feedback redistributed.

After the purposeful first-group pilot, select three groups uniformly without
replacement from physical groups 1 through 413, Python Random seed 20261030:
113, 280, 287. Per-group inclusion probability 3/413. Each selected group is
decoded completely: 13,593 candidates, 4,822 valid / 8,771 invalid.
This is a cluster sample, not 13,593 independent uniformly sampled rows.
The pooled 64.53% invalid fraction is descriptive and not an unweighted
population estimate; no confidence interval or training/evaluation split
construction is inferred. Group sizes and label fractions are in group-labels.csv:
group 113: 46.97% invalid; 280: 70.18%; 287: 71.49%. This heterogeneity makes
first-group-only extrapolation especially unsuitable.

All 8,771 invalid rows have publisher error blocks; valid rows have none.
First-error buckets: 5,197 tactic failure, 1,799 unsolved goals, 732 typing/
instance, 382 rewrite no-progress, 332 explicit native budget text, 150 unknown
name, 65 reported tactic refutation, 56 no-goals, 29 parser and 29 other.
No publisher MemoryError/restart message occurs as a first-error bucket here.
These are diagnostic text categories, not revalidated failure mechanisms.
Budget-text frequency is not a time share or proof of falsehood. No native
runtime column exists, so the 1.6%/73% tail claim cannot be tested from this
static capture. No goal-state or failure-cache eligibility is established.
13,593 distinct source fingerprints within this combined three-group sample;
no cross-sample/global duplicate claim. Lexical tactic counts exclude unclosed
comments where present, retaining those rows in labels/error/size totals.

Compressed ranges fetched: 3,307,741 + 4,716,322 + 4,802,591 bytes.
Only these column chunks, real header and footer are materialized in a sparse
file outside checkout. Other row groups must not be decoded. No full 4.46GB
download, no synthetic candidates, no original payloads committed.
The frozen analysis log inherited a generic 'not random' scope string from the
first-group analyzer: selection.json and selection.csv define the actual
three-group randomization. The reusable script now says sampling design is
supplied separately; no numeric result or raw capture was altered.

Analysis exited naturally in 12.02s including network fetch; combined W
sampling peak 11,582,566,400 bytes includes the concurrent original-module
native build and legacy censored EPFL. This is not isolated analysis memory
or verification throughput. PVC raw root:
gpu-smt-captures/workloads/epfl-training-random3-static.
