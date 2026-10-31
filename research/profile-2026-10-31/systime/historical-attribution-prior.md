# Historical CPU concentration and next causal comparison

Self-review. Read-only recomputation of the completed W26-module standard-artifact
point, not a new profile and not a population estimate.

Total user510.822757s/system201.186913s; system share28.256%.
The two largest system-CPU consumers, UMoments9 and Transonic BarrierData41,
contribute84.113%of that systemCPU; adding Barrier50
gives89.388%. They are the actual module names,
not an inferred operational classification. EnvelopePsiB uses a comparable
8.1GiB RSS yet has~4%systemCPU, so high memory occupancy alone is insufficient
to explain the difference.

All26peak RSS/native-M ratios are below1 (maximum
0.9003). This does NOT rule out the
stock getrusage checks: the fast path executes regardless of distance from
the cap. It also does NOT prove /proc/self/statm is absent throughout, because
peak accounting and observation boundaries differ. The linked check_memory
code has a thread-local200-call counter and direct getrusage on its fast path.

The installed Lean allocator configuration is mimalloc; glibc tuning therefore
is a scoped control rather than a presumed fix. The requested no-M control is
a strong candidate to separate runtime measurement overhead from unavoidable
kernel checking. Native stacks/syscall counts and repeated whole-source runs
must establish or refute that causal explanation. No amount of this historical
correlation replaces that measurement, and no speedup has been claimed.

Exact per-module numbers and original scope are in historical-system-cost.csv.
The original W sources/captures are unchanged; new P-lock/cgroup results will
have distinct denominators and instrumentation labels.
