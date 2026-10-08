# Released AutoVerus candidate acquisition

This is retained primary source material and acquisition/stage analysis, not a complete native-call trace or a verification performance result. Exact publisher revision: `microsoft/verus-proof-synthesis` `cbf9c0c6337b224fd8e5b7cb4e01ae65c0f98bc1`.

`cohort.tar.gz` SHA256: `098c4b4fd332dbf13c69b26f6d5533f30691f6865352363b2e0c1009fcc9a794`. It contains the complete declared acquisition:4,295 selected public files plus official full tree and acquisition metadata. All selected files matched their Git blob SHA1 during fetching; zero missing selected files. Selection includes ALL four main autoverus-generated directories (3,762 files), matching Verus-Bench task context, official generator/verifier Python and README/license files. It excludes other baseline/ablation runs by role, not outcome. It is not the complete1.03GB publisher release. The original unpacked `cohort/` remains on the owning PVC and is ignored by Git; nothing was deleted or replaced.

To inspect a clean repository copy, extract into this directory only when `cohort/` is absent; existing working data are authoritative and must be preserved:

```bash
tar -xzf artifacts/autoverus-source-2026-10-07/cohort.tar.gz -C artifacts/autoverus-source-2026-10-07
python3 tools/analyze_autoverus_candidate_logs.py artifacts/autoverus-source-2026-10-07/cohort/raw /tmp/autoverus-stage-analysis-new
```

Use a new output directory. Acquisition can be reproduced, if needed, through `python3 tools/fetch_autoverus_candidate_artifacts.py /tmp/autoverus-source-new`; it streams the pinned official archive without creating a source checkout. Reading retained results needs no download or verifier execution.

`analysis/` retains the actual original analysis. The196 observed logs contain3,566 saved Rust files,1,005 named inference stages,378 named merge stages,432 named refinement stages and349 Houdini labels. These are logger/file counts, NOT counts of native calls. Some named stages lack saved files, legitimate early returns can skip saving, historical producer version may differ, and debugging/scoring/Houdini invoke internal checks. Saved score/comment-annotated files are not asserted to equal deleted ephemeral native input bytes. The complete released main cohort can be an authentic saved-candidate replay pool under a separately declared protocol; it is not admitted as complete original agent/native traffic.

The earlier `sample/` and original `tree.json` are preserved acquisition history, not additional experimental rows. Scientific decisions and exact limits are in [step0002](../../docs/tmp/bootstrap/step-0002-20261007T224656+0000/step-report.md).
