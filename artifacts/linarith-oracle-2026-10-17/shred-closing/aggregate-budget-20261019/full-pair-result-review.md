# Complete miniF2F native/SHRED pair — root result self-review

The existing closing-certificate reuse integration returns every original
miniF2F candidate, with no measured whole-flow benefit and changed native
verification outcomes. This is the declared as-integrated SHRED module/wrapper
inside patched official Kimina, not a claim about every deployment of SHRED
or prefix reuse. No artifact repair or new cache algorithm is introduced.

## Population, baseline and clocks

All 7,808 original sources (244 tasks, 32 candidates each) remain in original
order. Both conditions use two outstanding sources, at most two live REPLs,
24 GiB address-space limits each, four eligible CPUs (4–7), and the same
48 GiB total owned-tree RSS watchdog. The shared transport/logging/resource
dependency adaptations are preserved in this directory. Native uses Lean
4.9.0-rc1 and the existing module-loaded kernel; reuse adds the unchanged
SHRED closing-certificate module/wrapper. These are different resource points
from the earlier eight-source/per-worker48GiB ProofNet and interrupted miniF2F
runs; no clocks are pooled.

| All-input clock | Native | SHRED integration |
|---|---:|---:|
| Whole including actual input preparation and retirement, seconds |18987.741491|19235.453028|
| Warm verification, seconds |18984.048870|19222.924986|
| Input preparation, seconds |0.092256|8.929986|

Native/SHRED whole time is **0.987122×**: reuse takes **1.304587% more elapsed**.
This is one fixed-order shared-host pair, not a confidence interval, isolated
causal cache effect or global CPU optimum. HTTP preparation, waiting, fallback,
timeouts, resource failures and final retirement are retained.

## Native completion versus SDK valid

| Actual returned outcome | Native | SHRED integration |
|---|---:|---:|
| Genuinely complete |3015|3010|
| Rejected by Lean |4675|4669|
| Sorry-bearing incomplete |0|11|
| Timeout |71|68|
| Resource failure |47|50|

The SDK labels 3,021 SHRED rows valid, but eleven contain “declaration uses
'sorry'” warnings. Those eleven were native rejections. Five previously
complete sources (7333, 7335, 7338, 7340, 7346) instead report kernel unknown
constant '_auxLemma.1'. All sixteen changed verification outcomes carry cache
hits, and the original changed source texts have no literal sorry/admit token.
The 3,010 genuine completions are the same IDs under both methods: no gained
complete proof, five lost. This integration does not preserve native outcomes.
We do not infer a hash collision, unsound kernel or defect in every published
configuration. The full changed IDs, native/SDK outcomes and messages remain
available for reproduction rather than being silently repaired or filtered.

Both methods retain the same 118 operational-failure IDs; five switch between
timeout/resource categories. Actual 47/50 exit134/std::bad_alloc records
corroborate the allocation failures. HTTP status200 is not proof acceptance.
All 7,808 real sources have one matched completed HTTP attempt, plus two warm
requests, with no retries or unanswered attempts. Opaque environment handles
differ on 4,104 rows; no full response transparency is claimed.

Returned cache observations are 635 hits, 5,794 misses, 3,378 captures,
1,006 capture rejections, 120 uncacheable and one application rejection.
Hit outcomes are 522 complete, 102 rejected and 11 incomplete. These returned
messages are not exhaustive cancelled-work accounting or saved CPU.

## Distribution and resources

[All 7,808 paired source latencies](full-pair-source-latencies.csv) and the
[all-input CDF](full-pair-http-cdf.pdf) retain every outcome.
HTTP p50/p90/p99 seconds are native0.212351/1.857351/246.356705 and
SHRED0.212093/1.828421/259.456171. SHRED has a longer HTTP span on3,878IDs.
HTTP spans include service waiting, exclude SDK predispatch/global preparation,
and overlap under concurrency. They are not additive wall/CPU/removable work.

The native-ranked slowest1% (79IDs) have overlapping span sums23594.600/23509.359s;
native has71timeouts. The matched slowest10% (781IDs) sums are35363.963/35856.916s.
Do not reinterpret these failure-dominated tails as LP/Amdahl attribution.

The 18,985/19,224 one-second RSS samples reproduce total-tree peaks
47.535389/47.581348GiB, at most two actual native REPLs, actual24GiB /proc limits,
zero watchdog kills/errors and final zero live descendants. Maximum observed
sampling gaps are1.057852/1.010624s. This is sampled response, not a hard
kernel RSS cap or a guarantee against subsecond overshoot.

## Reproduction and disposition

Run `python3 analyze-full-pair.py` in this directory; it streams the closed
gzip/raw datasets and reproduces [complete analysis](full-pair-analysis.json).
Run `python plot-full-pair.py` with the existing Kimina venv to regenerate
PDF/PNG. The [native](full-population/http-full/minif2f/rep1-native/terminal.json)
and [reuse](full-population/http-full/minif2f/rep1-shred/terminal.json) terminal
records link the preserved actual settings/lifecycle; their raw-archive
receipts preserve lossless compression accounting.

RQ1/RQ3 existing-method evidence now covers both requested full producer
populations, with scoped negative results and visible incompatibilities.
It does not close all RQs, prove a novel state-branching mechanism, establish
a GPU upper bound, or meet the OSDI target. The next decisive open question is
whether the corrected arithmetic composition generalizes beyond the selected
1,000 candidates under a matched official-service point. Finish that actual
comparison rather than adding losing cache/solver parameter variants.
Root self-review only; no independent reviewer was used.
