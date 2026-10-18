# First real size-gated CPU/GPU race: qualification complete

2026-10-18 UTC; root self-review only.

Width8, CPUs0–3 shared by client and cuOpt, 48 GiB, 24 original sources. Strong
native31.486097491 s; original CPU oracle22.051807059 s; same-large-LP CPU-only
ablation27.780423020 s; GPU race29.371985627 s. All return24 complete and no
operational failures, with no source-verdict or non-message changes.
Full responses and candidate tails are retained in paired-analysis.json.

58 actual large-LP races: CPU certificates45, CPU no-certificate8, GPU exactly
repaired certificate5. There are five **actual two-request GPU batches**;
all five submitted jobs have completed result records before proxy exit.
This confirms working jointly submitted LP batches, not merely
a concurrency flag. It does not establish throughput or end-to-end gain:
the GPU path is slower than the fastest CPU oracle in this qualification.

CPU-only mechanism and GPU race currently spawn native query processes from
the large Lean process on every query. Their waited-child system CPU
(about10–11 s here versus1.57 s for the persistent original oracle) exposes a
substantial integration cost. This cost is included, not subtracted away.
Reuse of the already established native daemon protocol can remove repeated
process creation without reviving the old global serial mutex. That is the
next integration repair, subject to new parity and full-cost qualification.

The finite GPU Job has been deleted after this run. Retained lifecycle receipts
include startup, server log/affinity, native wrapper, and actual deletion.
Lab is Ready and the other GPU Workspace remains Running. No other Workspace
was changed. All race child termination/reaping receipts are retained.

This version is not a best-valid-GPU result above1.5x. It also does not close
the GPU route: the full corrected-family wall profile is still collecting,
and the user requires an applicable ceiling before negative route closure.
