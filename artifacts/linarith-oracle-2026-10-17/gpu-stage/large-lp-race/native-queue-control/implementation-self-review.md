# Root implementation self-review

The diff against the frozen original Main has only one new FIFO helper (43
lines) and two-line dispatch. Existing static/naive/body/checker/header functions
remain byte-identical. Shared native Command.State and eight IO.asTask workers
match the original static implementation; no fork or cross-process state claim.
The counter is mutex protected, each original index has one promise, returned
results remain input-ordered. Every started candidate uses existing timing,
timeout and runCommandGCAux. Normal IO failures become error responses; unexpected
worker failures yield explicit unfilled-slot errors after all worker tasks join.
The <=8 bound is also checked against actual candidate intervals.

First build invocation treated a trace environment assignment as executable and
failed BEFORE running Lean; no original output was touched. Repair resolves
original trace paths and separates leading environment assignments before
substituting every private Main input/output/executable. First elaboration then
failed on an implicit Promise type argument and a missing Command Inhabited
instance. Its source and compiler diagnostics are retained. Type annotation and
checked array lookup repair those errors, without adding global instances.
Final Lean/clang/link stages succeed, only inherited trim deprecation warnings.
Recorded final commands point all writable outputs into private /tmp control
directory; imports and other objects remain the frozen original read-only inputs.
Private collector only changes one mode literal; original common files remain
unmodified. --help passed with the already-required row11 environment.
This is source review and actual compilation, not independent audit or a claim
of successful full-workload verification.
