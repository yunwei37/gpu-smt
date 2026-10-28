# Singleton partition result — root self-review

All7808first native starts and every applicable PID/birth registration/retirement
join. The disjoint totals exactly recompute10,375.984325s singleton time
(45.326784%of its22,891.507755s cell):
* Actual exclusive attempts8924.778203s,86.013798%of singleton time:
  8622.568692s on finalresourcefailures,302.209511s on timeout1885.
* Another native attempt during an inferred pending-retry window1232.447705s,
  11.877887%:996.553879s on eventually resource-failed sources and235.893826s
  on eventualtimeouts.
* End-of-batch tail218.331456s,2.104200%,alltimeout7771.
* Remaining intervals with unstarted native work0.426961s,0.004115%.

The second category is lifecycle-inferred,not a directly logged admission cause;
it includes small backend/engine gaps. Tail means allfirst native starts have
occurred,not independently measured zero queued leases. Exclusive spans are
actual recorded attempts,not predictions. No evidence supports attributing
thousands of singletonseconds to conservative forecasting. No reserved-CPU
fraction or Amdahl saving is inferred,and required exclusive retries are not
removed to improve a ratio.

Separately,source inspection finds a real stale-global-fallback bug for warm
queued batches. That bug is not asserted as the cause of this historical45%.
Its repair and no-native regression are experiment002. Matched warm qualification
remains the next actual native task;rootonly/self-review,not independent audit.
