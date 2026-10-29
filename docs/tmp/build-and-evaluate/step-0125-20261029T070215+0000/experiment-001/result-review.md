# Source-process retirement repair — root self-review

Old source regression actually fails after3.02s:resource lease waits for the
background stderr holder. The bounded fixture child exits on its own after3s,
so this failure does not leave a permanent helper. Old source is retained.
The first fix fails compilation because siginfo_t crosses await;scope the
native struct before awaiting,without unsafe Send. A second test observes a
transient Rstate during kernel SIGKILL exit;it now waits for actual absent/Z
state rather than assuming synchronous kernel retirement. Neither failed
qualification is discarded.

The final implementation observes exit without reaping,stops the existing owned
group under PID/birth validation,reaps leader and drains/joins both pipes.
Stdout completion remains inside request_io's original late-decode deadline
check. It adds no polling interval,cleanup timeout,dependency,publicmode,
monitor,runner or process-discovery layer. Escaping groups are outside the
unchanged existing boundary;this is not a sandbox/security guarantee.

Final local workspace alltargets:74passed/0failed/6native tests ignored.
Doctests pass. Focused stdout/stderr control passes in~0.05s on a qualified
pre-final-IOboundary version,and the final source passes focused plus whole
workspace. Do not treat the fixture clock as Lean throughput.
Clippy and fmt pass on the final source.

The initial single-CPUprocess suite has8passes/1failure because its existing
RSSwatchdog fixture requires two visible CPUs. Full workspace is correctly
run on10–11;no test prerequisite is removed. A later clippy pass is killed
by the combined-budget guard at51555725312B;only the new support tree is
killed. Retained exit-9 is not a pass or a systemOOM. Retry succeeds at
20749570048Bsampled peak. No live native42binary,request,input or timeout changes.
All support overlap/resources remain disclosed for that continuing collection.

Code-growth review:production57additions/7deletions (+50);test70lines and
fixture9additions/2deletions (+77);APIparagraph7lines. The single exit helper
is necessary to authorize group retirement before PIDreuse. Concurrent reader
and conditional join are necessary to retain large-output/deadline/error
behavior. Tests exercise both inherited pipes and actual child retirement;
no reusable fixture framework or unrelated refactor is introduced.

Run status:valid engine dependency repair;not new Lean or full workload evidence.
Research value:dependency-only;no new scientific claim/RQanswer.
Independent audit remains absent. Current source is committed/pushed after
validation;source CIwill be checked on that exact revision separately.
