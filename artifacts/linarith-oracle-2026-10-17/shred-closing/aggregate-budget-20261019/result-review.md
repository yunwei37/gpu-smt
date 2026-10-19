# Root result self-review: actual24-source aggregate-memory qualification

The user-requested resource qualification is complete. This is dependency
evidence, not a new performance result or independent audit.

## Exact requested resource point

Both native and SHRED use at most2live native workers,24GiB address space each
(25769803776bytes), within48GiB total owned-process RSS budget. Both
terminals and actual native /proc limit lines agree; max sampled live
native count is2, including warm/preparation/destruction transitions.
The root RSS includes controller/server/lake/native workers, not just the
active request's heap. No Workspace quota, permission or other project changes.

Normal native sampling has169samples, peak49804845056bytes=46.384377GiB;
SHRED has164samples, peak49578123264bytes=46.173225GiB. Both stay below48GiB;
neither needs an aggregate watchdog kill. Maximum observed sample gaps are
1.000886/1.000954seconds. These are actual sampled maxima, not an
unconditional kernel-enforced RSS ceiling or proof about every subsecond.
Both method lifecycles finish with no owned live descendants.

## Real candidate outcomes and per-process resource enforcement

The same24original miniF2F sources are first20 plus579/663/664/2518. Each
arm returns17genuinecomplete,4Lean rejections,3resource_failure. Actual native
message/sorry classification confirms complete counts; there are zero
per-ID status/native-outcome differences. Twenty-one native responses differ
in opaque handles/cache messages; original raw responses remain exposed,
and no snapshot/API transparency is claimed. Top-level errors match.

579/663/664each exit with actual returncode134 and stderr containing
libc++abi/std::bad_alloc under the real24GiB limit. Those are reported as
resource_failure, retaining original SDKserver_error and full stderr/exit.
They are not normal Lean rejections or inexplicable HTTP500retries, and no
system-level OOM is inferred from the single-process exit. Source2518remains
an ordinary Lean rejection. All failures remain in the denominator/data.

The whole selected-cohort clocks are168.248511/174.116743s including input
preparation. They are qualification observations, not a speed ratio, original
7808population result or a comparison against old48GiB-per-worker data.

## Actual watchdog intervention without risky48GiB allocation

A separate actual two-candidate run uses original candidates0/1from that
same24, no warm-only substitute, with a64MiB test threshold. Root sampled
peak is4099465216bytes=3.817924GiB, below the actual48GiB budget.
At two successive one-second samples the watchdog records the largest
native REPL in that exact owned tree and kills only its verified group:
owner/victim PIDs7767/7770and7768/7769, source0/1header phases, distinct
births. Both return explicit resource_failure overHTTP200; all retire.
The preserved samples independently show each victim's RSS equals the
maximum native RSS in its sample. No other process is selected.

This proves real selection/signal/attribution/reply handling, not actual
48GiB saturation. Fault-injection runs are excluded from performance data.
The unchanged whole-tree48GiB threshold is recorded in both normal arms.

## Continuation and publication

At07:31:31Zthe real24qualification finishes and the same finite root starts
one fresh full7808-source miniF2F native/SHRED pair. Actual current native
HTTP/RSS files and the sole root/server/twoREPLtree establish startup.
Full outputs remain incomplete, active and unstaged. Unsafe old all-matrix
continuation is stopped; other Lean runs must adopt aggregate accounting
before they may restart. No Agent/subagent/OMP or extra scheduler is used.

The existing hourly task retains frequency/goal and now names this latest
user resource requirement, so a future wake cannot restore the obsolete
48GiB-per-worker instruction. Historical resource points and partial data
remain separately reported.

Reproduce the closed qualification analysis:

    python3 artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/analyze-budget.py

All raw RSS samples, candidate results, HTTP, exits, source snapshots and
kill/retirement records are retained. Exact before/executed sources and the
MIT dependency patch make the mutation reviewable. Root self-review only;
all four paper RQs, GPU/Amdahl limits and systems novelty stay unchanged.
