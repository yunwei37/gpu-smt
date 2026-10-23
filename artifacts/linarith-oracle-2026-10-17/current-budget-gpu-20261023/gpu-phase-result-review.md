# Original1000 GPU phase closed — root self-review

This is the GPU cell of the predeclared GPU → provider retirement → Power CPU
→ native matrix. The two controls are still pending. No paired speedup,
CPU/GPU response equality, native-ranked tail result or GPU-route closure
can be inferred from this cell alone.

## Result and actual GPU work

All original1000 candidates returned: 992 Lean completions and8 rejections.
The closed Kimina HTTP/SDK trace contains1000 unique source attempts,2 warm
attempts, no retry, missing response or HTTP/SDK payload mismatch. Whole cell
762.439982722s includes preparation
5.793457326s, warm verification
756.120294023s and local process retirement. Separate cold
provider lifecycle797.608028s includes startup13.6264005s, client wrapper
767.1391141s, and provider retirement14.360091s. The provider's JobUID
bd8afbc4-3125-4d4a-946c-abbd912e07d6 is deleted; lab was Ready at retirement.

906 numeric race records cover379 distinct original source IDs. All source/
call joins are known. Native+HiGHS remain actual contenders.721 races have a
GPU child;185 smaller LP races retain CPU-only HiGHS. Winners are390 HiGHS
positive,82 exact-negative HiGHS,186 native positive,238 native no-certificate,
6 GPU positive and4 exact-negative external/GPU. No spawn, wait or kill error
is recorded. GPU-positive source IDs and exact-negative source IDs are
retained in gpu-phase-analysis.json; numeric wins do not themselves measure
candidate or cohort time saved.

Provider logs contain496 launch *events*, of which8 are empty groups cancelled
before any model is built. There are488 nonempty groups/488 actual models,
all singleton. There are zero verified cross-source multi-model launches.
All496 groups retire. Actual model states:404 cancelled,15 phase-I feasible,
42 phase-I no hint and27 numerical no hint. Floating hints alone are not
accepted certificates: the original exact support/negative checks and Lean
proof checking remain. No minimum-batch wait or CPU delay is added.

## Why no true batches were formed

The existing CUDA proxy calls solve_cuda_batch synchronously from gpu_dispatch
and waits through kernel retirement before dispatching another group. The
provider supports concurrent request handlers, but the proxy does not submit
a second group while the first remains active. The closed trace confirms
496 submission/retirement pairs and zero overlapping submitted groups.

This serialization is not by itself a measured large opportunity: among505
decoded proxy inputs, only5 source-owned requests arrive while a previous
group remains unretired;4 finish their CPU race before that prior group
retires. All5 actual source/call IDs and timings are in the canonical analysis.
Another192 proxy connection records have incomplete/undecodable JSON input.
They remain unattributed here; they are neither GPU-solved LPs nor evidence
that all possible batch windows have been enumerated. The906 race records
and actual CUDA launch source joins are a separate, known population.
No zero-cost asynchronous dispatch speedup or strict GPU bound follows.
The healthy frozen matrix is not changed to try another dispatch variant.

## Resource and provenance self-check

Source commit695c2b485b2f7ab32579b0f93e5058195e5a84fb; same original1000/order,
source2/live2, four CPU8–11, per-REPL24GiB AS and aggregate48GiB sampled RSS.
All763 memory samples recompute local own-tree RSS plus exact-owned provider
RSS; stable PID1/startticks117032656. Peak combined RSS
16072593408 bytes
(14.968769GiB), maximum
2 live REPLs,0 kills/monitor errors/attribution issues, no local live
descendants after shutdown. Provider host peak146989056bytes is included.
Largest observed sample gap1.018203s: this is a sampled response, not a
kernel-hard RSS quota. Peak device allocation16777216bytes; final live
allocations and device bytes are zero.

Closed GPU HTTP/results/server/RSS/race bytes are losslessly compressed;
raw-archive.json records original/compressed sizes and byte roundtrip equality.
The reader is rerun against those archived files. Proxy .gz input reading
was corrected in this post-run reader (no running collector change). Original
qualification readiness bytes are preserved separately from the full-phase
provider-ready.json. Active CPU/native files are neither compressed nor staged.

## Next empirical boundary

Complete the already-running Power/native controls once, then compare all
three closed clocks and complete responses, same-native-ranked1%/10% tails,
actual device engagement and full costs. Do not replace missing controls with
historical clocks. Do not launch another capture, change binaries or make a
broad GPU-impossibility conclusion from this singleton outcome. The same4 RQs,
OSDI research goal and better-valid-CPU/GPU1.5× criterion remain. All review
here is self-review; no independent audit or completed contribution is claimed.
