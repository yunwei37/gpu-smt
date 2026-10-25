# Real Verina native/profile qualification — root self-review

Pinned official Lean 4.18 executes three original files. Basic 1 and Basic 2
return native exit 0 without explicit admissions; Advanced 1 contains sorry
and is classified incomplete_reference, never a validated reference proof.
The diagnostic returns the same three classifications and produces all three
actual structured profiles. Complete native/profile group clocks are
3.839019142/2.978973431 seconds; this is not an acceleration measurement.

The slowest qualification trace spends about 2.527 seconds in Elab.lint.
This is real reference-file frontend work, not SAT/LRAT or arithmetic search.
The other two traces contain only the top runFrontend span above default
thresholds. Missing subthreshold tactic spans do not mean zero tactic cost.

Peak sampled owned RSS 5,132,300,288 bytes, max one CLI Lean observed,
24 GiB AS inherited, zero watchdog kills/errors, all descendants retired.
An earlier attempt failed before starting Lean because the driver created the
watchdog-owned activity directory twice; attempt1/error/source/log retained,
and the duplicate mkdir was removed before this successful run.
The two original basic files are checked as-is, without injecting proofs or
claiming the full source corpus has completed proofs.

This qualification validates actual CLI and profiler artifact formats.
Next measure all 189 reference files; separate explicit-admission stubs and
real completion before attributing any tactic costs. Root self-review only.
