# Native build-cost estimate: incomplete sample, explicit uncertainty

The estimator uses only42frozen probability targets across21strata of the
163,097-module all-source population. Purposeful targets and dependencies
carry no extra population weight. Input files must share pinned source,
SDK,library,options and resource point. Current tables filter8threads,
100kHB,M8192,unprofiled, retaining the first full matched compile per target.

Only3/42matched cost observations;0/21complete cells. Missing, interrupted
and failed target costs are not zero. Current CPU-hour estimate and95%CI
are unavailable. The earlier45/453/2718CPU-hour planning scenarios remain
assumptions, not newly calibrated forecasts. Capped100k data is also distinct
from the ongoing exact-source/native-default point.

For complete cell h, HT total=N_h*mean(y_h); estimated variance is
N_h^2*(1-n_h/N_h)*s_h^2/n_h. Complete census cells have zero sampling variance.
Totals add across cells. The implemented approximate95%Student-t interval
uses Welch-Satterthwaite degrees of freedom from cell variance contributions.
With only2draws/cell and possible heavy tails it is nominal/assumption-sensitive,
not a guaranteed bound. It excludes run-to-run/systematic/configuration error.
Incomplete cells produce no fabricated finite interval.

Target: conditional internal-module compiler CPU with dependencies prepared.
Current captures emit .olean only; standard Lake also requests .ilean/C
(and backend-dependent artifacts). Those costs and Lake driver/link facets
are not measured here. A full Lake build estimate remains pending matched
artifact emission as well as the missing samples.
This is a partial compiler-component projection, not observed cold-build wall, not proof all source
modules compile, and excludes external-package/cache acquisition and sampling
driver overhead. Plain default OAI130,834-module closure is a different scope.
Censors/retries/setup remain in raw data and are not relabelled as full cost.

Reproduce with estimate_native_build.py --targets phaseA-targets.csv
--strata strata.csv --results CHRONOLOGICAL_RESULT_FILES --out OUTPUT.
The --outputs selector separates artifact scopes; legacy W data is
explicitly .olean-only. Use --heartbeat-budget authored_or_native_default for exact-source/native
default observations; source/SDK comparability still requires the run records.
Python3.13 with NumPy2.5.4/SciPy1.18.1 officialbinary wheels tested outside Git.
Hand-calculated finite-population total8/variance8 and census13/variance0,
missing-cell handling and t(df1)quantile were actually checked. They validate
calculation, not missing workload observations. Raw analysis+dependency record:
gpu-smt-captures/workloads/openai4341-build-estimate-v3 (v1/v2 preserved; v2 driver still pointed to v1 and was not the current-scope calculation) and
build-estimate-analysis-deps. No full build or new acceptance claim.
