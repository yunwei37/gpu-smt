# Native failure-hotspot diagnostic

The fixed480source cohort is the native-ranked slowest10%of failed requests,
not the slowest10%of all7,808attempts. It contains83timeouts,355Leanerrors and
42resourcefailures. The old78timeouts are a strict subset; cohort.json preserves
the additional5IDs. Baseline-costs.json shows thiscohort accounts for93.5659%of
cumulative failedHTTP envelopes (overlapping, not wholeelapsed time).

- plan.md and plan-review.md: root-only admission/self-review.
- build.json: actual diagnostic link commands and unchanged originalnativebinary.
- build1/2/3 failures: dependency compile/link errors before realqualification.
- official-source/*.lean.gz: lossless copies of actual installed Lean sources.
- c-runtime-boundary-disassembly.txt.gz: native profileitM calls the diagnostic wrapper.
- preflight24: native24complete; original C++diagnostic cancelled after an
  allocation-exception ABI conflict. All original/failedraw retained.
- preflight24-c: repaired C-only instrumentation on the same24, reusing the closed
  nativecontrol; includes the same300stimeout and24GiBallocationfailure. Live data
  is not a final hotspot/performance result.

The diagnostic links existing nativeREPL objects with profileit.c. It observes
actual stock profileit/profileitM categories, including syntax-kind tactic calls,
elaboration, typeclass inference and declaration typechecking. Originalsource/
nativealgorithms are unchanged. Builtinprofiler stderr is not inserted into REPL
responses. A private1sthread snapshots actual named stacks and accumulated costs.
Sourceownership uses the existing benchmark activity file for the actualREPL or
its owning launcher; unmatched ownership is explicit. No external system is added.

Counter arrays are [completedcalls,inclusivewall_ns,inclusivethreadCPU_ns,
child-subtractedexclusivethreadCPU_ns]. Active frames preserve observed unfinished
work up to the lastsample. Multiplethread CPU and nestedinclusivewall are not
removablecriticalpath. Killed/SIGTERM processes may leave gzip streams without
a finaltrailer; analyze.py uses the flushed deflate records and reports closure
and incomplete trailingbytes. It never invents records after the lastsample.

    python3 bench/lean-failure-profile/build.py
    /workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python bench/lean-failure-profile/run.py --phase preflight --out artifacts/lean-failure-profile-2026-10-25/preflight24-c --reuse-native artifacts/lean-failure-profile-2026-10-25/preflight24/native
    python3 bench/lean-failure-profile/analyze.py --run artifacts/lean-failure-profile-2026-10-25/preflight24-c --out artifacts/lean-failure-profile-2026-10-25/preflight24-c-analysis

Fresh runs need a freshoutdirectory; never rerun a live or closed output.
Full480uses --phase full only after actual24review. This is profiler setup,
not a new systemcontribution, GPU speedup or independent audit.


The C-only24qualification is complete with all statuses unchanged, source24/24
timed, zero diagnostic drops/errors and no surviving nativechildren.
[Root qualification review](preflight-result-review.md). Full480 is now active
under the same resourcepoint; full480.launch.json records its exactowner.
Do not stage livefull480logs as finaldata or interpret a partialdistribution.


The final analysis now emits per-source.csv and summary.md with baseline-fixed
timeout/Leanerror/resourcefailure groups, categoryCPU and sampled active-tactic
rankings. [Closed24analysis qualification](preflight24-c-group-analysis/self-review.md)
checks realbodycoverage and missingfailureclocks; it is not full480evidence.
Only closedfull480data will determine the next own-method experiment.
