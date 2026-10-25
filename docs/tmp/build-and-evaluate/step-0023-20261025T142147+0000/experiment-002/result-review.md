# Completed original root prerequisites — root self-review

All 60 requested native targets returned exit0 and all 60 preceding native
Lake no-build dependency checks passed: 57 mixed LeanMLIR/SSA prerequisites
plus three Cli modules at the original root55c3729 revision. The root workload
was explicitly excluded. Total setup 196.887s; all logs, exact
run-source and commands are retained. Earlier library-only/source-resolution
failures remain intact. No upstream imports, proof bodies, package manifests
or compiler versions were changed. The original root manifest/lakefile and
82,628-byte workload file were compared byte-for-byte to the pinned source
archive; source revision is b8c4a771319a044854a4bbb49b8821381ef86ff8.

197 one-second combined old-owner/setup samples peak at
41299742720bytes (38.46GiB),
with no monitor/pressure error. This is sampled response, not a hard kernel
RSS bound. Source compilation ran on CPU11; overlapping collection/setup is
retained as shared-host interference, not pristine timing.

The candidate workload itself has not been executed. Dependency setup does
not establish bv_decide/SAT/LRAT timing, verified theorem coverage, GPU benefit,
fullMathlib COW-child parity or throughput. Actual workload execution remains
in the single candidate collection slot after the retained native group retires.
All review here is root self-review, not independent audit.
