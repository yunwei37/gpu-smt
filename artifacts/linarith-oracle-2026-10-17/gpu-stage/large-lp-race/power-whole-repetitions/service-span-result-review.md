# Complete candidate-span reanalysis — root self-review

This reuses all six closed captures; no new timing acquisition or solver variant.

Across the three blocks, median source-service spans change from
2.197/2.119/2.209 s to1.156/1.155/1.187 s. P99 changes from
33.689/32.058/32.949 s to23.165/23.126/23.933 s. The empirical CDF plots
each block's full1000 population separately, including the eight rejected
sources, without pooling proofs into extra whole-run repetitions.
The improvement is not limited to the maximum or one selected tail source.

However, direct spans are longer for131/164/156sources in the respective
blocks. The same70source IDs are longer in all three observations. These are
retained under same_source_slower_in_all_three_observations; no source is
dropped or rerouted using its known answer. They are observations, not a
statistical confidence claim. Span differences include scheduling/waiting and
interference, not isolated per-candidate CPU cost.

Both modes reach eight overlapping source-service intervals. Time with exactly
one source interval active changes from48.84/55.61/60.46 s to
23.52/21.46/25.37 s over each candidate envelope. A source envelope excludes
earlier setup/later retirement. Zero source spans do not prove CPU idleness;
eight source spans do not prove eight simultaneously ready LPs for GPU batching.

The collected self+waited-child CPU ratios are only1.2125/1.1649/1.2028,
versus whole-clock ratios1.7950/1.7636/1.7874. CPU accounting is not exhaustive
for all descendants, so neither utilization nor energy savings are derived.
In particular, do not present1.782x elapsed improvement as1.782x less CPU work
or infer a pure-LP/GPU Amdahl bound from it.

Reproduction: pinned Kimina venv Python analyze-service-spans.py. Raw source
spans and terminals are the prior six captures; service-span-analysis.json
retains all definitions and stable regressions. Matplotlib3.11.2 renders
candidate-service-cdf.pdf/png. The figure's three panels/legend/log axes were
visually checked. This supporting analysis bounds the existing result rather
than creating a new contribution, general workload claim or independent audit.
