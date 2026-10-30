# M step019 — complete reflected grid, preliminary chunk recheck

Self-review (自审), 2026-10-30. User-directed extension of the already checked digits family. Supporting experiment for the computational-certificate opportunity; no claim of generic novelty.

The prototype now proves the **original** mathd_numbertheory_541 statement for arbitrary natural m,n>1 with mn=2005. The checker covers every m=2..2005, and a proved division lemma accounts for every n=2..2005; input bounds follow from the original hypotheses. This is full logical coverage of 4,016,016 cells, **not** 4,016,016 kernel cell evaluations. Division compresses each row to its only possible quotient. Two in-range solution pairs form the untrusted payload. This is an algorithm/representation change, not a same-checker GPU acceleration.

Stock Lean4.9.0-rc1 checked row_sound, block_sound, block_append, 16 concrete blocks, their assembly, and the final theorem. Axiom output contains only standard propext/Quot.sound, no sorryAx or native_decide. The untrusted numeric generator and payload have no authority to accept an incomplete proof: the kernel checks all rows and the soundness bridge.

Actual v4 process: 6.929171s including imports, initial proof construction/checking, axiom reporting and 320 additional chunk rechecks. Sampled own-tree peak572,776,448B; receipt preserves native RSS high water, finite200000 source heartbeats, explicit finite kernel recheck limits, 300s internal alarm, -M8192 and eight allowed CPUs8–15. One native process; retired, exit0. This is a new phobos-vt point, not a matched comparison with the historical48GiB resource failure.

Each group rechecks the same16 existing independent proof values against the same immutable environment. Returned environments are discarded; original declarations were initially checked sequentially, and the final theorem uses those original declarations. This measures **parallel kernel recheck only**, not a production parallel elaborator or environment merge.

| requested tasks | five group wall seconds | median |
|---|---|---|
|1|.282871,.275030,.274810,.276333,.276747|.276333|
|2|.273040,.275972,.274099,.273243,.274145|.274099|
|4|.274919,.274581,.274745,.273694,.274439|.274581|
|8|.274403,.274654,.084742,.086735,.085056|.086735|

The first groups remain close to serial; later8-task groups are faster. Cause has not been established. Do not discard startup repetitions or label this8× scaling. Next integrated run will record absolute chunk intervals and reverse-order groups and time the final theorem recheck; it will also derive the payload from the batch numeric scan rather than merely using the previously observed two pairs.

Failures retained: v1 used an unavailable Mathlib.Data.Nat.Basic import; v2 hit deep recursion during eager tactic assembly; v3 had an unavailable Bool.and_eq_true.mpr projection. Forward fixes use existing SDK imports and a proved compositional block_join; v4 has neither errors nor sorryAx.

Coverage audit is ongoing and uses the current complete same-resource pair: **85timeout+41resource_exhausted=126**, not historical83/42 counts. No coverage count or saved-time claim is inferred from the mere presence of rfl/interval_cases. In particular a false intermediate assertion is proof repair, even when the final problem has a true computational solution.

Raw failed and successful captures remain on PVC under mechanisms-2026-10-30/captures/reflected-grid-v1..v4; small native outputs/source/receipts are retained here. No running source was modified. Next: complete individual coverage audit and generator/end-to-end/checking measurements, separate operational timeout-to-pass from unchanged-verdict semantics.
