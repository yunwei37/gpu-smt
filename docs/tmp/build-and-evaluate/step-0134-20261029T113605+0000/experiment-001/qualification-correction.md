# Correction of retained preflight reachability

Raw source: artifacts/hotspot-mechanisms-2026-10-25/state-reuse-native-20261029/
qualification/real-preflight/segment-0000/raw.log.gz.

Native original/import-control/observe:6returned source cells,all rejection,
unchanged equal raw diagnostic/status comparisons. Actual observer calls:
897simp_all returned;911simp_all returned,norm_num returned,nlinarith native_error.
The step0130report and qualification README incorrectly said both sources reject
before nlinarith. Correct the current README and append a dated correction to
the historical report,retaining the old text and unmodified raw data.
A regression now executes offline analysis against this actual record.
This is a qualification-accounting correction,not a new proof execution,
population match,hidden-state replay qualification or speedup result.
