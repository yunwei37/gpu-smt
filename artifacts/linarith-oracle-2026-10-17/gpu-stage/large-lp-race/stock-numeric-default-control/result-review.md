# E1072 — default native engine control

The unchanged native Fast frontend plus official omega runs the same15 original
sources, eight queues on four CPUs4--7,48GiB. Default tiered search takes
88.594756499seconds; the historical hybrid override takes87.767444935seconds.
Both return7complete/8reject/0operational, with **identical full responses**
and no resource-observer read errors. Default is0.9426%more elapsed in this
one fixed-order preflight; neither confidence nor global engine dominance is
established. There is no preflight benefit admitting another full engine matrix.

The upstream native helper selects tiered unless FARKAS_EXTERNAL_CPU_HYBRID=1.
The old collector's raw method label remains fast-hybrid even when the late
wrapper removes the override. See both engine-route.json receipts and
run-stock.py. Receipts capture the inherited parent environment immediately
before worker creation, not an independent child-environment audit. Source and
actual commands are retained. The original collector label is not rewritten.

This control uses the retained upstream native numerical executable, distinct
from the new dual-backend native-frontend component control. It checks a
competing existing baseline, adds no solver algorithm and does not silently
redefine the original whole-system1.5x criterion. No GPU work or new full matrix.

[Reproduce analysis](analyze.py), [all metrics](qualification-result.json),
[default raw](qualification15-default-tiered-raw/),
[hybrid raw](qualification15-hybrid-raw/).
All work/review by root thread alone; self-review only.
