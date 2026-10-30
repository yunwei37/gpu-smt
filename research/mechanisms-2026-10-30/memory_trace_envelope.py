"""Observed RSS traces under counterfactual thresholds; not replayed throughput."""
from pathlib import Path
import gzip,json,datetime
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
POINT=ROOT/"artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z"
def main():
    streams={}
    with gzip.open(POINT/"warm/memory-rss.jsonl.gz","rt") as f:
        streams["warm"]=[(x["time_ns"]/1e9,x["total_rss_bytes"]) for l in f if (x:=json.loads(l))]
    with gzip.open(POINT/"engine.stderr.gz","rt") as f:
        rows=[]
        for line in f:
            x=json.loads(line);fields=x.get("fields",{})
            if fields.get("message")=="owned RSS sample":
                rows.append((datetime.datetime.fromisoformat(x["timestamp"].replace("Z","+00:00")).timestamp(),fields["rss_bytes"]))
        streams["engine"]=rows
    result={"new_native_runs":0,"source":str(POINT.relative_to(ROOT)),"trace_comparison":{}}
    for name,rows in streams.items():
        span=rows[-1][0]-rows[0][0]
        cells=[]
        for percore in [2,4,8,12]:
            budget=percore*4*1024**3
            over=sum(max(0,b[0]-a[0]) for a,b in zip(rows,rows[1:]) if a[1]>budget)
            cells.append({"GiB_per_core":percore,"total_budget_GiB":4*percore,
                "held_sample_seconds_above_threshold":over,"fraction_of_observed_span_above":over/span})
        result["trace_comparison"][name]={"samples":len(rows),"covered_span_seconds":span,
            "sampled_peak_RSS_bytes":max(x[1] for x in rows),"cells":cells}
    result["limits"]=[
      "Each trace uses its own sample timestamps and sampled denominator; clocks are not aligned across runs.",
      "Left-hold integration is descriptive, not new-budget admission, counterfactual outcomes or measured throughput.",
      "A one-second response can overshoot; these are not hard RSS quotas.",
      "The new threshold would change queueing, restarts, failure timing and perhaps terminal coverage.",
      "Use the separate peak-reservation matrix only as a labeled model; no observed 48GiB clock is rescaled to another budget."]
    (HERE/"retained-analysis/observed-memory-thresholds.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
