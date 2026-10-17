# Existing HiGHS CPU comparator qualification — root self-review

The lost pinned highspy1.15.1 interpreter was restored within the owning
Workspace, using the existing pip installer; no system package or service was
changed. Real hello/request responses and numeric telemetry confirm engagement.

Same original first24 heavy-cohort sources, width4, CPUs0–3, 48 GiB, complete
whole clocks: Fast/hybrid36.834322728s; Fast/HiGHS53.655261139s. Both24complete,
no operational failures and normal EOF. HiGHS is45.67%slower in this finite
overlapped observation. Its230numeric calls contain225successful exact support
repairs and no reported adapter errors. No speedup is shown, so no full HiGHS
matrix is started. This does not close the GPU stage or prove global CPU optimality.

Complete native values are retained. Source outcomes match; response differences
are listed in analysis.json, rather than normalized away. These are two finite
development cells overlapped with the separate full attribution and prefix
captures on disjoint CPU affinities, not clean repeated primary measurements.

The original three-pair CPU result remains1.34668x. Final max(CPU,GPU)>1.5
decision remains pending; complete all-call attribution proceeds unchanged.
