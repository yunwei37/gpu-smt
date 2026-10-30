# Native retained-type inventory of363compiled objects

Same pinned OAI4eaee875/Lean4.34.1. Native readModuleData reads actual checked
objects, retaining compacted regions; all363MODULE records and DONE363363.
89,268retained theorem declarations;47,989auxiliary-name matches.
45,661auxiliary-name declarations have direct of_decide_eq_true proof head.
Their serialized types form42,610global nativeExpr-equality groups, or
44,164groups when distinct counts are summed separately per module.
Observed source decide+kernel token count in these files is42,886.

This matching shape is not an exact source-call attribution: auxiliary names
and proof heads can arise through other elaboration paths; tactics can run
over multiple goals, cached calls create no new retained helper, abandoned
branches may disappear, and names/metadata affect keys. The source/helper
counts are not one-to-one. Global type equality also cannot erase repeated
checks across modules or environment branches.
The1,497within-module repeated-type helper declarations and1,554cross-module
type repetitions are inventory differences, not proved avoidable CPU costs.

UMoments9:1,164matching helpers/1,164native types; Barrier50:641/641;
Canonical240:600/600. This is a convenience/dependency prefix, not a random
sample of all1,354,379source occurrences. No global cache-miss estimate,
kernel-compute seconds, speedup or Amdahl bound follows. Transitive axiom/
ofReduceBool dependencies remain unknown. Private declaration-name flags are
not direct observations of producer exporting/cache/defeq context.

Reader natural-exit0,1.762s,wait4peak2,410,512KiB; it reads artifacts rather
than re-verifying proofs. Separate1Hz sampling can miss brief peaks.
Full native log/input list/helper/failure history remains outside Git in
gpu-smt-captures/workloads/openai4341-olean-types-363.
