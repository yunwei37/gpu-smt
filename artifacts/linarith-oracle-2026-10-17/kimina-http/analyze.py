"""Summarize only complete official Kimina cells, retaining all failures."""
from pathlib import Path
import collections,gzip,json,math
A=Path(__file__).resolve().parent

def load_rows(path):
    if not path.exists() and path.with_name(path.name+".gz").exists():
        path=path.with_name(path.name+".gz")
    with(gzip.open(path,"rt")if path.suffix==".gz"else path.open())as f:
        return[json.loads(s)for s in f if s.strip()]

def quantiles(xs):
    xs=sorted(xs)
    return dict(n=len(xs),**{name:xs[max(0,math.ceil(q*len(xs))-1)]for name,q in[
        ("p50",.5),("p90",.9),("p99",.99),("max",1)]})if xs else dict(n=0)

def analyze(root, extra_roots=(), expected_affinity=(20,21,22,23)):
    roots=[root,*extra_roots]
    ids=json.loads((root/"source-ids.json").read_text())
    for other in roots:
        assert json.loads((other/"source-ids.json").read_text())==ids
    result=dict(scope="Official HTTP/SDK, original source IDs, shared-host closed-loop replay; no GPU or per-tactic CPU claim; root self-review.",state="partial",conditions={},comparisons={})
    indexed={}
    role_paths={}
    directories=sorted(p for base in roots for p in base.glob("rep*-*"))
    for directory in directories:
        label=directory.parent.name+"/"+directory.name
        terminal=directory/"terminal.json"
        if not terminal.exists():continue
        t=json.loads(terminal.read_text())
        if t["state"]!="complete":
            result["conditions"][label]=dict(terminal=t);continue
        data=load_rows(directory/"results.jsonl")
        assert len(data)==len(ids)and[x["proof_id"]for x in data]==ids
        assert dict(collections.Counter(x["status"]for x in data))==t["counts"]
        assert t["memory_limit_bytes"]==51539607552 and t["affinity"]==list(expected_affinity)
        events=load_rows(directory/"http.jsonl");spans=[];failed_http=[]
        for event in events:
            if event["event"]!="response":continue
            request=json.loads(event["request"])
            ident=request["snippets"][0]["id"]
            if ident.startswith("warm-"):continue
            spans.append((event["end_ns"]-event["start_ns"])/1e9)
            if event["status"]!=200:failed_http.append(dict(id=ident,status=event["status"]))
        result["conditions"][label]=dict(terminal=t,completed_HTTP_attempt_latency_seconds=quantiles(spans),
            failed_HTTP_attempts=failed_http,latency_scope="Completed HTTP attempt spans only, includes service queue/native work; excludes SDK semaphore waiting and unobserved failed network tails. Whole clocks charge them.")
        indexed[label]={x["proof_id"]:x for x in data}
        assert directory.name not in role_paths,"Explicitly choose one valid cell per repetition/method"
        role_paths[directory.name]=label
    for name,power in indexed.items():
        if not name.endswith("-power"):continue
        rep=Path(name).name.rsplit("-",1)[0]
        for method in["stock","native"]:
            role=rep+"-"+method
            if role not in role_paths:continue
            control_name=role_paths[role]
            control=indexed[control_name]
            changes=[dict(proof_id=i,control=control[i]["status"],power=power[i]["status"])for i in ids if control[i]["status"]!=power[i]["status"]]
            non_messages=[i for i in ids if {k:v for k,v in control[i]["result"].get("response",{}).items()if k!="messages"}!={k:v for k,v in power[i]["result"].get("response",{}).items()if k!="messages"}]
            messages=[i for i in ids if control[i]["result"].get("response")!=power[i]["result"].get("response")]
            operational=[dict(proof_id=i,control=control[i]["status"],power=power[i]["status"])for i in ids if control[i]["status"]not in["valid","lean_error","sorry"]or power[i]["status"]not in["valid","lean_error","sorry"]]
            v=dict(control_cell=control_name,power_cell=name,status_differences=changes,non_message_differences=non_messages,
                   raw_response_difference_IDs=messages,operational=operational)
            if not changes and not non_messages and not operational:
                c=result["conditions"][control_name]["terminal"];p=result["conditions"][name]["terminal"]
                v["whole_control_over_power"]=c["whole_lifecycle_seconds"]/p["whole_lifecycle_seconds"]
                v["warm_control_over_power"]=c["warm_verify_seconds"]/p["warm_verify_seconds"]
            else:v["disposition"]="Preserve clocks/counts; no matched-response speed claim."
            result["comparisons"][control_name+"-vs-power"]=v
    if len(result["conditions"])==len(directories)and result["comparisons"]:
        result["state"]="closed-observed-cells"
    (root/"analysis.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(dict(state=result["state"],conditions={k:{"state":v["terminal"]["state"],"counts":v["terminal"].get("counts"),"whole":v["terminal"]["whole_lifecycle_seconds"]}for k,v in result["conditions"].items()},comparisons=result["comparisons"]),indent=2))

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("extra_roots", nargs="*", type=Path)
    parser.add_argument("--affinity", type=int, nargs="+", default=[20,21,22,23])
    args=parser.parse_args()
    analyze(args.root, args.extra_roots, args.affinity)
