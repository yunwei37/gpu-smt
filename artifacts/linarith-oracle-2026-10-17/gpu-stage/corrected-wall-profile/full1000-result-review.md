# Complete corrected-family native/oracle wall attribution

2026-10-18 UTC. Implemented, executed and self-reviewed by the owning thread.
No independent audit or paper-acceptance claim.

## Measurements and denominator

The full original1,000 arithmetic-heavy Goedel sources return992 complete and
8 rejected in both methods, with zero operational failure. Native profile
wall is **1774.239197591 s**; oracle profile wall **1342.059889496 s**.
These use corrected arithmetic imports, CPU4--7,width4,48GiB. The historical
2234.689173920 s primary used CPU12--15 without phase instrumentation.
No earlier phase time is divided by that primary. These new own-clock
measurements are diagnostic, not substituted primary performance results.

All1,000 native responses match the corrected primary's complete JSON.
Oracle has the same88 warning-only changes, zero non-message or verdict changes.
All native13230 LP requests and oracle10251 requests have source/call metadata.
All fallback LPs have product-column ancestry and all FP shapes are present.
Oracle's4202 direct requests include3597 checked certificates and605 misses;
6049 fallback requests include5440 certificates and609 misses.

## Conditional zero-cost calculation

Native all-LP summed wall is **856.902708356 s**
(48.2969% of its own wall as a *sum*, not a disjoint
whole-wall partition). The optimistic fixed-work calculation is
1774.239197591 / (1774.239197591 - 856.902708356) =
**1.934120x**.
This deletes only LP work and already does not exclude1.5x.

The native product timer additionally aggregates199.779563353 s, including
Lean-side product-proof construction; it is not all GPU-ready numeric work.
Deleting that entire mixed stage too gives the deliberately generous2.472611x
sensitivity, not a guaranteed GPU ceiling with unchanged proof checking.

The CPU oracle exposes untrusted numeric products directly: products use
3.105376410 CPU s. All LP plus numeric-product summed wall, including fallback
and internal exact LP, is **551.271193961 s**
(41.0765% of oracle wall). Its zero-cost remaining
wall is **790.788695535 s**, or
**2.243632x** relative to this matched native
profile. Pure numeric LP/product observed union occupies39.7247% of oracle
wall; sum and union differ because intervals overlap.

These are optimistic conditional sensitivities: unchanged certificates,
fallback decisions and noneligible work, zero device overhead, and summed
deletions can overcount overlap. They are not measured GPU speedups or a
universal scheduler theorem. In particular they cannot justify negative
route closure. Stronger pooled-native comparison is now separately admitted;
its wall cannot be substituted into this profile's formulas.

## Search, protocol and failure costs

Native numeric-service CPU is860.045862378 s: FP search32.655849593 s,
exact search820.476926237 s, with parsing/build/repair/verification/protocol
reported separately. Its640 no-certificate/error calls include42.368067355 s
exact-search CPU;12590 certificate calls include778.108858882 s exact CPU.

Oracle direct numeric CPU is212.872549835 s (FP12.540350039,exact195.340305069);
native fallback CPU339.443310964 s (FP15.466588260,exact321.093773002).
Numeric products3.105376410 s, linearization0.317961226 s and matrix packing
0.640331799 s are distinct from LP search. Full per-success/miss ledgers,
worker wait4 CPU receipts, protocol/repair costs, row/column/nnz/product
distributions and actual candidate-selected1%/10% component totals remain
in full1000-wall-summary.json and each complete cost-analysis.json.
Parent Lean LP intervals and numeric child CPU must not be added as disjoint
elapsed. A diagnostic CPU percentage is not an end-to-end wall fraction.

## Full-run gate and next decisive comparison

Native FP row median10. The7201 LPs below11 rows total0.021797926 CPU s;
6029 LPs at least11 rows total853.110977904 CPU s. Freeze the full GPU threshold
at11 rows, replacing only the historical small-qualification gate37.
The matched native-pool24-source comparator is40.986507059 s serial versus
30.909538492 s pooled on CPU8--11, with identical outcomes/non-message values.
This strengthens the native baseline; it is not claimed as GPU gain.

The original1000 strong pooled-native versus CPU oracle has launched at
05:24:38Z on CPU0--3,width8,48GiB. Full GPU follows the same CPU allocation
and concurrency after the CPU cells actually retire. All preparation,
pack/transfer, queue, exact repair, Lean checks, fallback, cancellation/rebatch,
proxy retirement and cold Job lifecycle are retained. The best valid CPU/GPU
result determines the final1.5x decision. This record does not close GPU.

## Raw-log recovery and limits

A missed unlocked product-summary emitter concatenated three pairs of complete
JSON objects in the native log and one pair in the oracle log. The original
bytes are retained. Ordered JSON tokenization only moves delimiters; every
derived pair reconstructs the original bytes exactly, with no numeric,
source or timing value synthesized. There are132875 native and76411 oracle
records. Recovery receipts and initial failed-analysis output are preserved.
The future builder now serializes that product emitter as well; the active
capture was never rebuilt or edited. Actually compiled sources are retained.

Single profiling order and the24-source overhead check (about2.6%) limit
precision; no overhead is subtracted. A full corrected CPU0--3 pooled primary
is distinct from this CPU4--7 diagnostic. Results characterize the selected
arithmetic-heavy1,000 sources, not all Lean, SMT, or a complete deployed service.
