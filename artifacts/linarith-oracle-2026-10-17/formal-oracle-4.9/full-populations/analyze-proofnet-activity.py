"""Read closed ProofNet race/support logs without treating them as Amdahl input."""
from pathlib import Path
import collections,gzip,json
A=Path(__file__).resolve().parent
result={}
for mode in ["native","direct"]:
    root=A/"proofnet"/mode
    races=[json.loads(s)for s in(root/"lp-races.jsonl").open()if s.strip()]
    with gzip.open(root/"support-calls.jsonl.gz","rt")as f:
        records=[json.loads(s)for s in f if s.strip()]
    children=[]
    for row in races:
        for role in ["cpu","gpu","strong_cpu"]:
            e=row.get(role+"_exit")
            if isinstance(e,dict):
                children.append(dict(role=role,signal=e["signal"],
                    cpu_ns=e["wait4_user_cpu_ns"]+e["wait4_system_cpu_ns"],
                    wait_error=e.get("wait_error"),kill_error=e.get("kill_error")))
    result[mode]=dict(logged_eligible_races=len(races),
        winner_labels=dict(collections.Counter(x["winner"]for x in races)),
        summed_decision_and_retirement_seconds=sum(x["decision_ns"]+x["retirement_ns"]for x in races)/1e9,
        summed_reaped_child_cpu_seconds=sum(x["cpu_ns"]for x in children)/1e9,
        killed_support_children=sum(x["role"]=="gpu"and x["signal"]==9 for x in children),
        backend_connections=len(records),
        fully_parsed_models=sum(isinstance(x.get("rows"),int)for x in records),
        JSON_decode_error_records=sum(str(x.get("reply",{}).get("error","")).startswith("JSONDecodeError")for x in records),
        child_wait_or_kill_errors=[x for x in children if x["wait_error"]or x["kill_error"]])
result["scope"]="Observed race-eligible LPs (row threshold11), legacy gpu label is CPU HiGHS. Excludes small direct problems, Lean export/check and unprofiled native fallback. Summed overlapping spans are not fractions of whole wall or Amdahl bounds. A killed writer can leave truncated JSON; individual malformed connections lack IDs, so no exact cause join is claimed."
(A/"proofnet-numeric-activity.json").write_text(json.dumps(result,indent=2)+"\n")
