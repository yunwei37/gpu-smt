# Qualified APRIL configuration: four existing reference pairs
Lean4.22.0-rc4,matching release Mathlib928758a,50000HB,-M6144,-j1,CPU0-7.
First four selected pairs without exact?/aesop:all4reference sources compile,
all4mutations produce ordinary Lean errors.8invocations actually complete.
This qualifies this small adapter point,not the entire39pair sample.

v1's78startup errors remain preserved. Root cause observed:CLI-M produces
max_memory,which the frontend rejects as undeclared. Adapter imports one tiny
module declaring this existing C++ runtime option:
~~~lean
import Lean
register_option max_memory : Nat := {
  defValue := 0
  descr := "Declare existing C++ shell memory option"
}
~~~
This adds no proof or tactic implementation. Original proof bytes retained;
replay only prepends this import and official Mathlib preamble,and caps explicit
larger/unlimited heartbeats. Native-M runtime budget stays enabled.
No environment security change. Original dataset Mathlib pin remains unknown.

Each invocation arms an inherited30s ITIMER_REAL before exec as an explicit
wall safety budget,plus50000native heartbeats. No parent kill is needed.
All8finished without wall alarm. Wall timeout is an operational budget outcome,
never a false-goal verdict. This point is separate from v1's200000HB/M8192.
One fresh Lean at a time plus retained stuck v1 process,as newly authorized.
Combined1s tree RSS peak10,343,792,640bytes(9.63GiB),max2Lean processes;
W16GiB budget. Sampling is not a kernel hard quota. Both old tree and new
capture descendants included. New native/controller retired;old retained.
Raw:/workspaces/.agent-state/gpu-smt-captures/workloads/candidate-april-small-v3.
