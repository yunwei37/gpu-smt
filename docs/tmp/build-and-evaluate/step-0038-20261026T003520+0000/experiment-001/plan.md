# Fresh native EOF transport repair and actual four-worker qualification

The first24original-source run exposed four idle REPLs after native work:
all blocked on next stdin read while Rust awaited their buffered stdout.
Pinned REPL4.9 source prints the blank delimiter but never explicitly flushes;
the fresh backend leaves input open. Close stdin after exactly one request:
this matches raw native differential input lifetime and independent-process
backend semantics. No upstream REPL,proofsource,timeout,limit or fallback change.

Retain interrupted24partial records and pre-repair backend source.
Regression:process fixture withholds response until inputEOF. Full ordinary
Rustchecks plus releasebuild,then repeat same24real sources at48GiB actualRSS,
CPU8–11,onecorelease,unlimitedAS. Native/prepared outcomes and accepted IDs
must be compared;capture all failures/RSS/retirement. No performance claim
from this small set. After qualification commit/push,launch whole7808pair.
This is an actual transport-fault repair,not a scientific admission threshold.

No other capture runs. Root alone implements/reviews. Ordinary resource
mechanisms are prior work. Original23/48hotspot diagnostics remain pending;
zero-coverageclosed-tail andexternalCPUoracle stay frozen.
