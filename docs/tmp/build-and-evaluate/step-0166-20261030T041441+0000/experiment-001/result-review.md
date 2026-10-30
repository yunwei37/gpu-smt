# Cross-proof expensive-call audit — same-thread self-review

This implements the user's corrected unit:the expensive call inside different
proofs,not equality of whole successful/candidate sources. Source predictor
training/ablation is frozen;do not rerun step0164's source model.

All41resource-failed sources have eligible retained native Syntax. Final byte
mapping checks every unit against the original proof bytes:offsets are
proof-relative,as in the original extractor. An initial source-absolute span
assertion failed and is retained,then corrected without a native invocation.

There are4cross-proof standalone call-text groups and1rooted native-unit-text
group. Textual equality is not goal equality. A deliberately narrow three-unit
template,have : S=E := by ...;rw [that];rfl,matches19sources. Extra simp/norm_num/
other steps are excluded instead of assuming they preserve the same goal.
The original statement S.card=100 is explicitly checked.

One repeated source-derived rewritten-target group has5distinct proofs:
minif2f-3687,3691,3700,3706,3709. All explicitly replace S with:
Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧
  (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
  (Finset.range 10000)
and then invoke rfl. This is stronger evidence than same task/final line or
full-source repetition. It remains a source projection,not the elaborated
target/local context/hidden effect state. Lemma names/proofs/source coordinates
and retained heap may differ even when the closed computation looks identical.

In chronological exclusive order,the4later proof envelopes total889.819596s.
This is conditional whole-candidate exposure,not measured time inside the
matching call or a certified saving. Separate historical profiles observe
442.045817rfl CPU seconds over the5proofs. These values have different runs,
libraries/resource conditions and clock scopes and are never multiplied or
renormalized into one speedup. Per-source Syntax,spans,CPU and envelope fields
are all retained. Exact full-state match count remains unknown.

Budget51539607552B here is the recorded aggregate RSS cap,not remaining
allocation space at the call. Same expression/rfl/global cap is not an exact
allocator/GC/heap state or monotone budget-failure witness. No failure verdict
cache is enabled. The positive source-template cohort is a focused candidate
for native state/effect qualification when such capture is safe.
