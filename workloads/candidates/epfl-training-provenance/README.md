# EPFL training construction and censoring

Primary [pinned publisher audit](https://huggingface.co/datasets/EPFL-LARA/lean-compiler-training-corpus/blob/e5ff00a803d6a4a346a53d2116664c184c946bd7/answer_data.audit.json).
Exact public JSON: 9,365 bytes, retained on PVC. CSV counters are publisher
reports, not our full recensus or native execution.

This is a constructed compiler-feedback training distribution, not a complete
natural arrival log. Native merge has 3,586,218 rows, including 865,640
fallback-truncated-invalid and 9,571 fallback-complete-valid inputs, with
3,296 corrected legacy labels. Publisher direct source map was not rebuilt;
this summary cannot assign historical source families to our sampled groups.
Publisher adds 250,000 synthetic pairs. We generated no candidates.

Construction arithmetic reconciles:
3,586,218 + 250,000 = 3,836,218;
GRPO appends 142,698 of 223,360 rollout rows -> 3,978,916;
contract filter drops 8,457 invalid-without-error rows -> 3,970,459;
self-distill/inference-train/Qwen-GRPO append 391,120/363,420/111,381
-> 4,836,380, with 2,168,417 valid and 2,667,963 invalid.
Actual Parquet footer independently confirms final rows and414groups,
not historical transformations.

GRPO exclusions include 16,485 lean_infra_failed, 56,926 missing_declaration,
2,564 wrong_declaration, 171 wrong_declaration_name,293 contains_sorry,
17 escape_hatch. These are stage counters, not disjoint global failure rates.
All sampled invalid rows having an error block is partly enforced by
construction: annotation-contract consistency is not independent semantic or
representativeness validation. Source recovery/truncation, alignment and
duplicate filtering affect replay applicability.

Audit merge_seconds/filter_seconds measure data processing, not verification
or generation costs. They cannot supply a native denominator or test1.6%/73%.
Whole-corpus cost concentration and original per-row budgets remain unknown.
Dataset license unknown; no raw source or foreign scratch paths committed.
