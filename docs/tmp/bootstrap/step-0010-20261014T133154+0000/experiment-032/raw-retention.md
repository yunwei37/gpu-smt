# Native CPU raw retention

The complete E032 recording is now retained at
/workspaces/.agent-state/gpu-smt-deps/native-cpu-perf-20261015/goedel427-compiled-profile/native-1828338-49247006.data
outside Git on the existing owning Workspace PVC. All5,665,548,374bytes match
the original directly, followed by fsync. The original private temporary raw
remains at /tmp/gpu-smt-native-cpu-perf-20261015/raw-profiles/goedel427-compiled-profile/native-1828338-49247006.data.
Earlier raw and failed/partial captures remain retained at their recorded paths.
[Actual copy receipt](full-raw-retention-receipt.json) owns verification evidence.

Raw DWARF stack memory must remain outside Git. Only symbolized statistics and
input/outcome/source metadata enter the repository. No credential, permission,
volume, storage-class or runtime policy changes occur.

The standard perf archive attempt exits1 and reports no buildIDs; that helper
produced no archive. The ordinary buildid-list still exposes recorded DSO paths,
so all95 available ELF paths (526,466,296uncompressed bytes) are retained as
recorded-native-code.tar.gz beside the persistent raw. Archive size157,523,516;
every archived payload matches the current recorded path, followed by direct
compressed-copy comparison and fsync. All original files stay in place.
The recorded temporary /tmp/perf-vdso.so-hL3DCZ is absent and remains a declared
recomputation limitation; it is not silently replaced with a fresh vDSO.
[Failed helper](full-code-retention-receipt.json), [actual code inventory](full-code-path-inventory.json),
[successful path-based archive](full-code-path-retention-receipt.json).

For recomputation on another machine, extract the code tar under a private
symbol root and pass that root with perf report --symfs; member names preserve
original absolute path suffixes. Exact recorded temporary raw paths are not
required when -i names the persistent raw. This is a restoration recipe, not a
claimed fresh-machine replay. Retain recorded failures/missing mapping and
unknown symbols in any new analysis.

Earlier space repair losslessly retained the inactive old4.21 native build cache
on this same PVC. [Implementation and restoration](../../../../implementation.md#retained-historical-native-build-cache)
links the exact archive and verification receipt. No raw data or old source was
deleted for space. Expanded historical generated outputs can be restored.

## Completed inclusive-report retention (2026-10-16T00:09:30.560564+00:00)

The original full raw and95ELFs remain unchanged. The full inclusive report
now completes with perfreturn0. A malformed derived report is preserved at
/workspaces/.agent-state/gpu-smt-deps/native-cpu-perf-20261015/goedel427-compiled-profile/inclusive-flat-subprocess-stdout-original.bin before exact gzip
packaging repair. Its [recovery receipt](full-inclusive-output-recovery-receipt.json)
retains byte counts and lossless comparison. Exact observer transport failure
is private at /workspaces/.agent-state/gpu-smt-deps/native-cpu-perf-20261015/goedel427-compiled-profile/inclusive-observer-transport-failure-20261015.txt; its public receipt separates remote success from
observer failure without publishing infrastructure addresses. No raw replay,
fresh-machine replay validation or missing-vDSO recovery is claimed.
