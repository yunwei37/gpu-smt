# Step 003 — software sampling control and prior-work boundary

2026-10-30 UTC. M branch; self-review.

## Experiment
PMU work remains deferred after EACCES. A process-local ITIMER_PROF sampler
records instruction pointers and phase numbers into a preallocated mapped
capture, without PMU, ptrace, stack unwinding or allocation in the handler.
The C control uses 200 ms of process CPU and exits naturally.

Both standalone and Lean-FFI shared-library builds succeeded. Control exit 0:
100 samples, 0.20635 s whole-process elapsed. The binary capture is retained in
gzip form, together with exact build argv and logs. This qualifies only signal
delivery inside that C process, not external signaling or Lean FFI execution.

PC sampling measures CPU residence. It cannot supply cycles, IPC, cache/TLB
misses, or exact inlined reference-count/allocation costs. No performance or
precompilation benefit has been measured.

## Operational failure
The existing full-Mathlib maps probe exceeded the requested 30-minute collection
limit while importing on WAN-backed storage. At the recorded observation it
was D (disk sleep), with approximately 0.36 GiB owned RSS and only a few CPU
seconds. The previously observed EACCES prevents external termination;
heartbeats do not bound import I/O. This is a failed bounded-run design.
No second Lean process was started and no security setting was changed.
The capture subsequently retired naturally: exit 0, 2442.703 s, sampled
owned RSS peak 3,758,579,712 bytes. Its deadline observation remains a real
bounded-run failure, not a compliant 30-minute experiment. Future probes must arrange a qualified in-process wall
exit before imports, and avoid broad imports during replica rebuild.

## Write/review
prior-work.md maps all requested families to primary sources. Lean.Elab.Parallel
and LeanTree materially constrain novelty: generic independent proof work and
state factorization are already known. A full timed dependency DAG is still
missing; there is no measured mean parallelism and no 1.3 claim.
DigitsCertificate.lean subsequently passed the complete ordinary-kernel check; details below.

## Qualified follow-up control
A process-internal ITIMER_REAL exit was added to the same measurement library.
The 200 ms CPU control still exits 0 naturally (0.20674 s); with its own 20 ms
wall timer it exits 124 in 0.02229 s. No parent signal is used. This validates
only the tiny C control, not an uninterruptible WAN read or a Lean import.

## Numeric reference, not a certificate
Three optimized C runs independently count 100 eligible decimal integers
(sum 544000) and two product-grid solutions (5,401)/(401,5). The 4,016,016-cell
loop takes 2.374--2.390 ms of process CPU; whole processes take 4.03--4.33 ms.
This supports that numeric evaluation itself is cheap on CPU. It does not
estimate Lean kernel time, certificate construction or general IR coverage,
and does not establish a GPU opportunity. Inputs fit machine words; this is
not evidence of GMP big-integer acceleration.

## Native completion and certificate

The FFI symbol control initially failed because the interpreter searches
Lean-mangled wrapper symbols. That failure is preserved; adding correctly
boxed/unboxed wrapper exports qualified the follow-up control, exit 0.
Four core handlers resolve inside libleanshared.so in the actual Lean process.

The digits prototype has four retained versions: missing Omega module import;
a deep-recursion failure for a single 10,000-layer count; a successful block
computation plus a diagnostic-formatting elaborator error; and the fully
successful version. The final version uses 100 blocks of 100 structurally
recursive tests, with proved block/count/Finset equivalence. It exits 0 in
30.5811 s, uses 30.5467 CPU s, and has kernel leader RSS high water
2,369,380,352 bytes. Exact warm declaration-recheck nanoseconds and printed
axioms are in native/phobos-digits-certificate-v4/stdout.txt.

The computation theorem has no axioms. The digits equivalence and theorem
bridge use standard Mathlib propext/Quot.sound/Classical.choice, with no sorryAx
or native_decide. This is an alternative verified proof representation, not
an engine speedup for unmodified generated candidates or a general verified
IR compiler. End-to-end original-candidate parity remains unmeasured.

## Additional retained-data result

The parent RSS scope audit covers 7,808 prepared-leader wait4 observations:
accepted/rejected leader median 470,599,680 bytes, p99 977,809,408 bytes, versus
one observed parent peak 3,614,543,872 bytes. This supports a substantial
shared-parent memory opportunity for ordinary small requests. It does not
supply a complete aggregate RSS upper bound or a new native budget comparison.
The initial script incorrectly required a ready event on each attempt; that
one-row undercoverage is retained separately, and the corrected scope join
uses the explicit native-parent wait4 marker. Full results are under
retained-analysis/parent-rss-scope.json.

Hot-tactic ELF dependencies and actual plain-CLI process maps are distinct
points. See hot-tactics.md: the CLI imports .olean without Mathlib .so, whereas
the historical service explicitly loaded a library with 684 DT_NEEDED entries.
