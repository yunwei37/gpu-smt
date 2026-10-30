# Retained strong-order control — self-review

This adds no source model,feature extraction or predictor retraining. The
already-completed first-short scheduler ledger supplies all32original candidate
IDs per task,including queued cancellations. Its static per-task order is replayed
only as the existing strong reference. All adaptive policies still use runtime
observations alone. Replaying the retained order at each point reproduces3724
completed sources and142observed-solved tasks,an independent control from the
native consumer ledger. Whole-task runtime priors are unchanged.

|Current-point policy|Frozen work seconds|CPU-slot batch proxy|Mean task finish proxy|
|---|---:|---:|---:|
|Retained short-order reference|36498.245764|9248.759524|3894.304778|
|LAS lossless resume|38487.248192|10746.647743|1190.922669|
|Runtime-index lossless resume|38726.608345|11157.271265|1187.641427|
|LAS charged restart|96486.222253|26975.678217|2387.195069|
|Runtime-index charged restart|54747.316462|17063.831033|1596.579331|

The reference's frozen cost exceeds the exact first-success minimum35838.016728
by660.229036s,or1.8089%of reference work. In the old point,reference29363.916962
versus minimum28923.681945leaves440.235017s,1.4992%. These are summed-work gaps,
not wall-time upper bounds and not ratios multiplied into measured1.439031x.

Age-only restart reduces the model's mean task completion versus this retained
reference,but raises work and batch completion. This remains a conditional
latency/work tradeoff,not useful equal-RSS throughput or new algorithmic novelty.
Resume keeps progress at zero cost;restart discards it. Neither retains the
original native budget/timeout guarantee without further qualification. RSS
and exclusive serialization are omitted,so all CPU-slot times are nonphysical
at the current resource point. Keep original traces,censored resource outcomes
and the historical measured consumer clocks separate. No production feature
or proof verdict was installed from this model.
