"""Full-coverage companion to the retained instantaneous-peak stress model.
No measured throughput claim: peak trajectories, counterfactual outcomes and COW
savings are not identifiable. Retried jobs retain frozen labels by assumption.
"""
import collections, gzip, heapq, json
from pathlib import Path
from retained_analysis import PAIR, HERE, gz

def retry_model(rows, budget, cleanup_s=0.):
    waiting=collections.deque(rows)
    active=[]; deferred=[]; done=[]; killed=[]; now=0.; seq=0
    while waiting or active:
        while waiting and len(active)<4:
            row=waiting.popleft();seq+=1
            heapq.heappush(active,(now+row["cost"],seq,row))
        # Instantaneous peak pressure: retirement is free at cleanup_s=0.
        while sum(a[2]["peak"] for a in active)>budget:
            victim=max(active,key=lambda a:a[2]["peak"])
            active.remove(victim);heapq.heapify(active)
            killed.append(victim[2]);deferred.append(victim[2])
            # Charge the chosen scenario's serialized retirement delay while
            # other active jobs are suspended. No unmeasured overlap is free.
            now+=cleanup_s
            active=[(end+cleanup_s,i,row) for end,i,row in active]
            heapq.heapify(active)
        if active:
            now,_,row=heapq.heappop(active);done.append(row)
    # Reattempt each preempted job once, alone, full original recorded work.
    for row in deferred:
        assert row["peak"]<=budget
        now+=row["cost"];done.append(row)
    assert len(done)==len(rows)
    assert len({r["id"] for r in done})==len(rows)
    return {"makespan_proxy_s":now,"terminal_coverage":len(done),
            "original_accepted_retained_by_assumption":sum(r["accepted"] for r in done),
            "preemptions":len(killed),"serialized_retry_work_s":sum(r["cost"] for r in deferred),
            "cleanup_s_per_preemption_scenario":cleanup_s,
            "lost_results":0,"post_victim_reservation_never_over_budget":True}

def main():
    d=gz(PAIR/"engine.stdout.gz");rows=[]
    for r in d["results"]:
        rows.append({"id":r["id"],"cost":sum(a["elapsed_seconds"] for a in r["attempts"]),
                     "peak":max(a["peak_rss_bytes"] for a in r["attempts"]),
                     "accepted":r["outcome"]["status"]=="accepted"})
    result=[]
    for core in [2,4,8,12]:
        b=core*4*1024**3;fit=[r for r in rows if 0<r["peak"]<=b]
        result.append({"GiB_per_core":core,"cores":4,"budget_bytes":b,
                       "fit":len(fit),"excluded":len(rows)-len(fit),
                       "scenarios":[retry_model(fit,b,c) for c in [0.,1.,5.]]})
    pairs=collections.Counter();examples=[]
    for r in d["results"]:
        if len(r["attempts"])>1:
            a=r["attempts"];pairs[(a[0]["status"],a[-1]["status"])]+=1
            examples.append({"id":r["id"],"initial_status":a[0]["status"],
                             "exclusive_status":a[-1]["status"],
                             "initial_peak":a[0]["peak_rss_bytes"],
                             "exclusive_peak":a[-1]["peak_rss_bytes"]})
    warm=collections.defaultdict(list)
    with gzip.open(PAIR/"warm/attempts.jsonl.gz","rt") as f:
        for l in f:
            r=json.loads(l);warm[r["id"]].append(r)
    warm_pairs=collections.Counter((a[0]["status"],a[-1]["status"])
                                   for a in warm.values() if len(a)>1)
    output={"matrix":result,"engine_retry_transitions":[{"from":a,"to":b,"count":n}for (a,b),n in pairs.items()],
            "warm_retry_transitions":[{"from":a,"to":b,"count":n}for (a,b),n in warm_pairs.items()],
            "engine_retry_rows":examples,
            "limits":["Companion model, not a new native run or measured throughput.",
                      "Same budget-fit subsets as memory-matrix.json; excluded jobs are unknown under new budgets.",
                      "Frozen physical-attempt work includes historical retry overhead; no queue elapsed used.",
                      "Instantaneous full peaks omit within-job growth and victim work before detection.",
                      "0/1/5s are declared cleanup sensitivity scenarios, not measured cancellation latency.",
                      "Retries finish with frozen labels by assumption; native parity is NOT established.",
                      "No COW discount, per-worker import baseline, allocator retention or new memory trajectory invented.",
                      "Initial pressure is a modeled watchdog event, not a kernel hard RSS quota.",
                      "Warm aggregate resource_failure can become timeout under exclusive retry at the same48GiB total budget."]}
    out=HERE/"retained-analysis/memory-full-coverage-retry.json"
    out.write_text(json.dumps(output,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in output.items() if k!="engine_retry_rows"},indent=2))
if __name__=="__main__":main()
