# Arithmetic/prefix protocol paper update — root self-review

This is a bounded update while the actual arithmetic and standard-workload
collectors run. It does not close EXPERIMENT, the full WRITE gate, REVIEW,
the four RQs or the user1.5xdecision. Self-review is by the implementation
author in the same thread, not an independent reviewer.

## Source and scientific contract

- Implementation text matches Oracle.lean/oracle.rs and the corrected
  Fast/hybrid/product fallback. Export is Real/Rat only, with Nat/Int and
  unsupported normalization falling back. Weighted contradiction is once
  per solved contradiction branch. Equality may require two branches.
  The enclosing declaration remains natively checked.
- Native polynomial/products/LP code is CPU-only. No new GPU engagement,
  time saving, new-contribution or venue-readiness claim is introduced.
- Farkas source supplies numeric probe/restrict search as the competent
  established comparator. Native compilation and invocation-local product
  application reuse stay baseline engineering, not claimed novelty.
- SHRED's pinned README and prefix.py distinguish rooted-prefix accounting
  and closing-certificate reuse from a complete deployed prefix executor.
  Correct one existing paper sentence to that narrower verified scope.
  The new adapted executor is not labeled upstream service performance.
- Prefix counts are recomputed from published original inputs/native parser
  outputs, with task+statement identity. Exact/unit edges have different
  inter-tactic-trivia treatment. Counts are not weighted savings.
- The original title, abstract, four RQs and contribution scope are unchanged.
  The last admitted1000source protocol and1.5xthreshold are explicit.
  Complete prototype/strong diagnostics/standard-workload timing stay missing.
  The sole complete1000reference has source association and disclosed build
  lineage. No small diagnostic CPU fractions are substituted for its phase mix.

## Writing/style and rendered verification

Use paper-writing-style on the three new paragraph groups. Existing prose is
not broadly polished or shortened. One existing SHRED scope sentence changes
for factual grounding, not wording preference. New text uses concrete actors,
connected paragraphs and scope-bearing qualifications. No new punctuation,
terminology or system-name issue requires a separate rewrite.
No independent full-paper critique or twelve-round WRITE completion is claimed.

Tectonic0.17.0 writes an18page PDF successfully. Existing/nonfatal underfull
box warnings remain, without a fatal error or overfull-box warning.
The changed regions on pages5,8,11and12were rendered with Poppler and visually
inspected: text and tables are readable, with no clipping or overlap.
Source/PDF are retained under docs/paper/. Build and pdfinfo are attached here;
rendered inspection images stay in the owning experiment temp directory.
