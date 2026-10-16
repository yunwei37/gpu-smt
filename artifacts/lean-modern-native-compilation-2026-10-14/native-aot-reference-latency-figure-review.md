# Full-reference latency figure review

Observed 2026-10-15T00:10:45.445461+00:00

Figure purpose: show the latency tail and outcome heterogeneity of one complete native-compilation reference acquisition, supporting the existing full-source characterization. It is not a system speedup or queueing plot.

The Python/matplotlib script reads all29750raw rows from the finalized original ZIP. No latency values or coordinates are hand-entered. Complete, rejected and operational populations are retained; each survival curve is normalized within its named population. Both log axes expose tails; the nonzero y minimum is one request in the full population, not a truncated superiority comparison. Caption states single acquisition/sharedCPU0–3/fouroutstanding requests and distinguishes client duration from CPUtime or whole makespan.

Visual inspection of the actual300dpi PNG confirms readable labels/legend, no clipped ticks or title, separate dash patterns and colorblind-safe colors, and a legend outside data. PDF is vector,239.774×189.28pt. Current main.log reports505.89pt text width with0.25in column gap: target column243.911pt. Converting TeX points to PDF bigpoints gives a243.0bp physical target. Intended column-width inclusion would scale this asset1.0135×; smallest7pt text stays above7pt. Standalone grayscale conversion was also visually inspected: dash patterns distinguish the overlapping all/complete curves and the rejected/operational tails without color. No manuscript float/page-placement validation is claimed: this is a staged analysis figure while EXPERIMENT is active, and LaTeX integration/compiled-page/grayscale checks remain for WRITE.

The exact count/percentile table serves reproducibility lookup; the curve serves distribution shape. No plot of the two separate CPU-reference timings is created, because their different affinities would invite an unfair speedup reading. No selected-caseHiGHS ratio or partial candidate prefix is presented as a full benchmark result.

[Vector figure](native-aot-reference-latency.pdf), [PNG](native-aot-reference-latency.png), [source](plot-native-aot-reference-latency.py), [self-contained caption](native-aot-reference-latency-caption.md). Root direct figure self-review, not independent audit. Full WRITE/REVIEW and completed-step publication remain pending.
