# Native unit result self-review

The generic CnfBridge compiles in pinned4.27. Corrected Positive passes5Boolean
guards,concrete native certificate soundness and generic correspondence proof.
WrongCnf fails specifically at unrelated equality rfl;InvalidCertificate002
fails because native_decide evaluates its certificate assertion false. Merely
observing exit1 is insufficient:the earlier invalid source failed field
notation/metavariable elaboration and is not an intended negative result.

Retain all failed attempts. Positive001's shortened certificate still checks
true for the contradictory formula,so it is not a valid negative control.
Ordinary decide also cannot reduce this opaque native checker;the concrete
proof uses original native reflection instead. Initial support-runner parse
failure starts0Lean processes. Negative002's postcheck searched the wrong
English wording;the already retained native error supplies the intended
false result and is validated without rerun.

6actual Lean compiler invocations check helper/unit modules,not6generated
workload candidates. Highest combined own support+fullcapture sample is
38,852,960,256B,below51,539,607,552B in retained samples,no abort/monitorerror.
CPU11support overlaps the frozen capture and remains a clock confound.
No fixedASlimit,new collection,active binary/import/resource change.

Printed generic bridge axioms are propext,Classical.choice,Quot.sound;the closed
native proof additionally uses existing Lean.ofReduceBool/Lean.trustCompiler.
This matches the stock reflection trust basis,not a new axiom or independent
external kernel checker. The original draft entry and all raw data stay.

The checked correspondence theorem does not demonstrate physical sharing,
tactic integration,parallel LRAT scheduling or end-to-end gain. Next implement
the optional closed-CNF frontend and preserve SAT-model/fallback behavior,
then actual complete-module comparison using existing capture path. No source
feature or theorem alone establishes novelty. Root self-review only.
