# Released candidate workloads

Small derived tables from public, already generated sources.
[Catalog](../catalog.csv) records exact pins, license, version, scale and
selection. No source corpus with an unknown license is redistributed here.
Public availability is not permission to relicense data.

## Completed analyses

| Input | Coverage | Original labels / observations |
|---|---:|---|
| EPFL evaluation 0bbf3133 | all 68,932 programs | 28,145 valid; 39,473 failed; 1,314 wrong declaration |
| APRIL test 4e307527 | all 1,835 test tuples | all have recorded errors; 20 contain budget diagnostic text |
| LNSym 5c05220f | all 196 files / 1,887,252 bytes | 62 bv_decide; 153 native_decide; 1 direct ofReduceBool token |
| AutoVerus retained direct | 3,566 candidates × 3 repetitions | top58 use3.315–3.399% of summed process elapsed |

EPFL lexical coverage is 68,930/68,932: two sources have unterminated block
comments; all original labels are retained. Occurrences outside nested
comments and strings are not executed tactic calls or time shares.
norm_num occurs in44,198 programs, linarith34,142, simp32,068, simp_all31,579.
Six model/benchmark groups are separate in epfl-evaluation-0bbf3133/verdicts.csv.

EPFL evaluation excludes timeouts, infrastructure exceptions, not_run and
precheck failures. Labels also check expected-theorem matching and forbidden
constructs. It is neither an uncensored arrival stream nor compiler verdicts
alone. Neither inspected EPFL schema includes native per-program costs.

APRIL consists of publisher-created mutations, not natural prover failures.
april-test-4e307527 retains the first complete analysis; the script-v2 folder
is a complete reproduction using the committed classifier. Both count1,835
rows/20 budget-text records. First matching diagnostic categories are
exclusive, while budget substring flags can overlap another category.
They are not proven causes or new native outcomes. The card's global258,103
count conflicts with its260,103 split sum; training was not fully recounted.

## Larger releases: metadata versus local scan

- EPFL training: publisher full statistics (partial=false) report4,836,380
  programs,2,168,417valid/2,667,963invalid. Its4.46GB compressed corpus was
  not downloaded. validation is feedback text, not a split. Dataset license
  is not explicit in the pinned card.
- OProofs: full publisher info reports6,804,694pairs/73shards,27.50GB
  compressed/153.47GB decoded. Actual fields: formal_statement,formal_proof,
  cot_proof,prompt. Failed steps/status/feedback are not exposed; paper
  descriptions of internal repair traces do not change the released schema.
- Nemotron: raw JSONL29,525,155,225bytes. Card ~900k trajectories is a claim,
  not a recounted result. Viewer243,314rows is partial, not the whole file.
  messages=null in a prefix does not describe all trajectories.
- DeepSeek V2: complete released ZIP contains438 Lean sources, selected
  successful solutions without failed attempts/native timings.
- Goedel V2 repo: all612 JSONL statement/template rows contain sorry; not
  completed generated proofs. Actual V2 outputs in EPFL form19,177rows,
  10,120valid. This subset uses4.15 rather than original4.9.

Publisher service totals are observation snapshots, not local raw scans.
Their provenance is explicit in the catalog.

## Reproduce

Use persistent storage. EPFL analysis requires PyArrow (recorded26.0.0 /
Python3.13). Download the exact pinned input after reviewing license status:
https://huggingface.co/datasets/EPFL-LARA/lean-evaluation-benchmark/resolve/0bbf31331bd1c726f539b311cce8b058a821f15c/data/test-00000-of-00001.parquet

~~~sh
python workloads/candidates/analyze_epfl.py --parquet /persistent/test.parquet --out /persistent/epfl
python workloads/candidates/analyze_april.py --out /persistent/april
python workloads/candidates/analyze_autoverus_tail.py --cells artifacts/autoverus-native-2026-10-09/full/analysis/cells.json.gz --out /persistent/tail.csv
~~~

EPFL batch512 scan:107.44s parser elapsed,198,376KiB peak.
APRIL script-v2:7.21s,26,248KiB peak. These are static processing costs on
the replacement Workspace, not native verification. The interrupted G10
attempt is not merged into these clocks. Original inputs/metadata/logs stayPVC.

## Native budgets and tail

budget-cause-evidence.csv explicitly leaves unmeasured causal costs unknown.
Resource interruptions/timeouts mean exceeded declared native/replay budget,
not false goals or intrinsic dataset properties.

AutoVerus direct receipts use Verus33269ac6...,Rust1.76.0,Z34.12.5,oneCPU
and120s per-process capture timeout. Each repetition has190exit0,
3359exit1,17exit101,zero capture timeouts. Exit101 causes remain unknown.
Tail costs sum individual process elapsed times, excluding capture conditions:
not batch wall, model generation, or a Lean hardware comparison.
The1.6%/73% hypothesis does not reproduce at this AutoVerus point; it cannot
be evaluated on releases without timings or with censored timeout tails.

No new proof, native candidate, agent harness, full build or production
mechanism was launched by W.

## Bounded raw Nemotron inspection

Three deterministic 1 MiB windows at byte 0, midpoint and final 1 MiB yield 202 complete JSONL rows and 119 assistant messages with reasoning_content. This confirms actual released trajectories beyond viewer conversion. Position/row-length bias prevents population rate estimates; no verdict or native cost is inferred. Reads required exact HTTP 206 Content-Range and were capped at 1 MiB each. Result: nemotron-byte-windows.json; 30,340 KiB parser peak, 6.89 s, zero native runs.
