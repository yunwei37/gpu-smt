# Native simp call patterns and diagnostic cadence

Exploratory reuse of the completed480 real native diagnostic;no new candidate
execution. analyze-existing.py reconstructs the complete fixed23 selected
simp_all-dominant timeouts from primary open-frame/call records. See
existing23/result.json and per-source.csv.gz. All23have one HTTP attempt and zero
diagnostic flags. Each selected body-open simp frame has matching PID/TID/
snapshot ancestry under simpAll. Non-atomic clocks and killed open frames stay
censored;durations do not become completed phase costs.

| Last observed inner simp | Sources | Observed open-call wall | Cumulative completed simp calls |
| --- | ---: | --- | --- |
| Long | 9 | 143.822307–299.859294s | See retained individual rows |
| Short | 14 | 0.000009–0.048869s | 3,194–178,417 |

Eight of the short-call sources also have 2,208–36,206 cumulative completed
outer simpAll calls. These are whole-source completed-call counters,which can
include earlier invocations;they are neither exact loop rounds nor counters
isolated to the final call. A last-open short frame alone would hide repeated
work. A long call requires observation within that action. No claim about
which hypothesis,lemma,fallback or enclosing combinator caused the timeout
follows. No cycle or reliable early rejection is established. One second is
the existing diagnostic cadence,used only to describe this table. This is
not population prevalence,Amdahl input or a speedup.

## Source repair

The previous diagnostic allocated a fresh zero progress timestamp on every
observedSimp call and serialized all entry hashes at every phase end. Repeated
calls create potential observer amplification;the native counters are not a
measurement of old progress event counts or its overhead.
The new source shares only its timestamp in an IO.Mutex. It releases the lock
before native work,hashing or output. Expensive progress JSON now follows the
process-wide one-second cadence. Full entry hashes move from each phase end
to the sampled progress record;they describe current-call entry state only.
Every lightweight begin/end,subject,completion/exception distinction and
native call/order remains. Per-phase logging can still be expensive and must
be charged to the future diagnostic denominator. Analyzer behavior is unchanged.

## Actual validation and retained failed attempts

compile-001 compiles production definitions but same-file clock execution
reports unreachable code. compile-002 stops on the analysis script's deliberate
fresh-output protection. compile-003 compiles definitions/control but its
driver redeclares imported main. compile-004 imports the control but still
reports unreachable code:the new state used builtin_initialize rather than
the ordinary imported user-module initializer. These failures are preserved,
including source versions;none touched the live capture.
With initialize,compile-005 executes the imported control successfully.
compile-006 is final:production and control definitions compile;two fresh
importing processes each verify initial zero state,178,417 dense callbacks
produce one emission,cadence boundaries/cross-caller sharing work and a
backward timestamp is suppressed. This executes clock-only IO,zero candidate
proofs. It is not native differential qualification,thread stress testing,
COW qualification or performance evidence.

Raw command logs/source snapshots/receipts and combined1second memory samples
are retained. Final combined peak is recorded in compile-006/receipt.json
under48GiB;no pressure abort or monitor error. These sums include the existing
full acquisition,not incremental observer memory. CPU11only. The original
fullgroup PID408739/birth140695363/release and prepared host are unchanged.
Old qualification007/oleans remain:their seven matched native pairs do not
qualify this new observer. Actual original23/native phase comparison remains
queued behind the sole healthy full acquisition.
