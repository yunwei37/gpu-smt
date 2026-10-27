# Native shared-CNF contract controls

Pinned4.27nightly compilation actually checks CnfBridge.lean. Positive.lean
passes5Boolean controls (valid certificate,wrong empty/satisfiable formulas,
empty/malformed certificates) and a concrete native certificate soundness
theorem,plus generic correspondence transfer. WrongCnf.lean and
InvalidCertificate.lean intentionally fail:the first cannot provide unrelated-
CNF equality;the second native_decide evaluates the certificate claim false.

These are build/unit checks,not a second fullpopulation collection or generated-
candidate experiment.6Lean compiler invocations include the retained failed
development attempts. The first positive control wrongly treated a shortened
yet accepted certificate as invalid and ordinary decide could not reduce the
computation. The first invalid-proof source had a field-notation error;that
exit alone is not counted as the intended certificate rejection. Both original
sources/logs remain in the linked step. A postcheck wording assertion was
corrected against the same already correct negative compiler log,without rerun.

The generic bridge's printed axiom set is propext/Classical.choice/Quot.sound.
The concrete native proof also uses the stock Lean.ofReduceBool/trustCompiler
basis,as the original bv_decide does. No new axiom or bypass is introduced;
this is not a claim of independence from Lean's existing native reflection.

All new Lean support processes useCPU11 under existing combined own-tree48GiB
monitoring. Highest recorded combined sample38,852,960,256B,no pressure abort or
monitor error. Sampling remains1s,not a hard quota. Support CPU overlap remains
a clock confound for the preserved full capture. No original generated
candidate executes here and no full collection is restarted/reconfigured.

[Exact sources,raw outputs,commands,failures and self-review](../../../docs/tmp/build-and-evaluate/step-0077-20261027T085610+0000/step-report.md)
separate actual native theorem qualification from runtime implementation.
These contract controls do not establish a tactic,runtime value sharing,
GPU implementation,whole-module speedup or original accepted-set conclusion.
The later [opt-in frontend and its separate native controls](../../../bench/lean-bv-shared-cnf/README.md)
now live in the bench source tree;physical reuse and full performance remain
open. This record preserves the earlier contract-only qualification.
