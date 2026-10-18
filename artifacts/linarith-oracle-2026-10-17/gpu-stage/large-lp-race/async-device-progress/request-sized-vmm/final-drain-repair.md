# Final-result read repair

The first successful VMM run has40launchedmodels but39device-state samples and
one generic no_hint. Source order polls model states before testing completion;
a kernel can finish between those observations. Preserve that first source and
raw result. The repaired loop performs exactly one final scan after a positive
completion observation, then exits. It does not add a timeout, numerical change,
retry budget or polling-frequency adjustment. Native checks/fallback stay intact.
Qualification must show actual complete model/timer coverage; do not retroactively
label the first acquisition fully attributed.
