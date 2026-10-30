"""Read allocation-free C profileit events; report bounded local models, never a full DAG."""
from pathlib import Path
import argparse, collections, json
from analyze_dependency import walk, components, classify

def normalized(kind):
    return kind.replace("«", "").replace("»", "")

def read_rows(path):
    return [json.loads(line[6:]) for line in path.open() if line.startswith("M_DAG ")]

def read_events(path):
    sources = {}
    active = None
    nodes = {}
    for line in path.open():
        event = json.loads(line)
        if event["event"] == "source":
            name, mode = event["name"].rsplit("|", 1)
            if mode == "off":
                if active is not None:
                    sources[active]["open_at_end"] = event["open_frames"]
                active = None
            else:
                active = name
                if active in sources:
                    raise ValueError("Duplicate source boundary: do not join across process segments")
                sources[active] = {"nodes": [], "open_at_start": event["open_frames"]}
        elif event["event"] == "enter":
            if active is None or event["id"] in nodes:
                raise ValueError("Unowned or duplicate C call")
            node = dict(event, children=[], source=active)
            nodes[event["id"]] = node
            if event["parent"]:
                parent = nodes.get(event["parent"])
                if parent is None or parent["source"] != active or "end" in parent:
                    raise ValueError("Invalid C parent lifetime")
                parent["children"].append(node)
            else:
                sources[active]["nodes"].append(node)
        elif event["event"] == "exit":
            node = nodes.get(event["id"])
            if node is None or "end" in node:
                raise ValueError("Unmatched C exit")
            if node["source"] != active or ("thread" in event and node["thread"] != event["thread"]):
                raise ValueError("Cross-source or cross-thread exit")
            if any("end" not in child for child in node["children"]):
                raise ValueError("Parent exited before child")
            if event["cpu_ns"] < node["cpu_ns"] or event["wall_ns"] < node["wall_ns"]:
                raise ValueError("Nonmonotone C clock")
            node["end"] = event
    return sources

def cost(node, clock="cpu_ns"):
    return (node["end"][clock] - node[clock]) / 1e9

def summarize(row, source):
    nodes = list(walk(source["nodes"]))
    complete = (source.get("open_at_start") == 0 and source.get("open_at_end") == 0
                and all("end" in n for n in nodes))
    result = {"id": row["id"], "classification": classify(row),
              "body_wall_s": row["wallNanoseconds"]/1e9,
              "body_cpu_s": row["cpuNanoseconds"]/1e9,
              "C_calls": len(nodes), "complete_C_tree": complete,
              "full_DAG_span_s": None, "full_DAG_parallelism": None,
              "local_allGoals_eligible": False, "local_allGoals_saved_cpu_s": 0.}
    if not complete:
        result["local_reason"] = "Open/incomplete C tree"
        return result
    roots = source["nodes"]
    result["C_root_cpu_s"] = sum(cost(n) for n in roots)
    exclusive = collections.Counter()
    for n in nodes:
        own = cost(n)-sum(cost(c) for c in n["children"])
        if own < -1e-7:
            raise ValueError("Overlapping CPU child intervals")
        exclusive[normalized(n["kind"])] += max(0., own)
    result["exclusive_cpu_by_kind_s"] = dict(exclusive)
    leaves = [n for n in nodes if not n["children"]]
    largest = max((cost(n) for n in leaves), default=0.)
    residual = max(0., result["body_cpu_s"]-result["C_root_cpu_s"])
    result.update(largest_opaque_leaf_cpu_s=largest, untraced_body_cpu_s=residual)
    # This model additionally serializes untraced body work. The leaf-only
    # bound below does not require that extra assumption.
    denom = max(largest, residual)
    result["fixed_atomic_untraced_serial_model_ceiling"] = (
        result["body_cpu_s"]/denom if denom else None)
    result["fixed_atomic_leaf_only_parallelism_ceiling"] = (
        result["body_cpu_s"]/largest if largest else None)
    def project(items):
        output=[]
        for node in items:
            children=project(node.get("children", []))
            if normalized(node.get("kind",""))=="Lean.Parser.Tactic.allGoals":
                output.append((node,children))
            else:output.extend(children)
        return output
    def shape(items):
        return [shape(children) for _,children in items]
    def flatten(items):
        for node,children in items:
            yield node
            yield from flatten(children)
    ip,cp=project(row["infos"]),project(roots)
    infos,calls=list(flatten(ip)),list(flatten(cp))
    result["allGoals_info_count"]=len(infos)
    result["allGoals_C_count"]=len(calls)
    result["eligible_allGoals_nodes"]=0
    if not infos or shape(ip)!=shape(cp):
        result["local_reason"]="AllGoals projection forests are absent or not order/ancestry isomorphic"
        return result
    # Every allGoals callback must be present, completed, successful and in the
    # same ordered ancestry forest. This is NOT a global kind/order-only join.
    if len(infos)!=len(calls) or any(c["end"]["return_tag"]!=1 for c in calls):
        result["local_reason"]="Incomplete or failed allGoals correspondence"
        return result
    qualified={}
    reasons=collections.Counter()
    for info,call in zip(infos,calls):
        goals=info.get("liveBefore",[])
        branches=[n for n in info.get("children",[])
                  if normalized(n.get("kind",""))=="Lean.Parser.Tactic.tacticSeq"]
        timed=[n for n in call["children"]
               if normalized(n["kind"])=="Lean.Parser.Tactic.tacticSeq"]
        if len(goals)<2 or len(branches)!=len(goals) or len(timed)!=len(goals):
            reasons["Unmatched branch counts or no split"]+=1;continue
        if any(len(b.get("liveBefore",[]))!=1 or b["liveBefore"][0][0]!=g[0]
               for b,g in zip(branches,goals)):
            reasons["Branch goal identity/order mismatch"]+=1;continue
        if any(c["end"]["return_tag"]!=1 for c in timed):
            reasons["Failed branch callback"]+=1;continue
        if sum(cost(c) for c in timed)>cost(call)+1e-7:
            raise ValueError("Branch CPU exceeds parent")
        qualified[call["id"]]=(timed,components(goals))
    result["allGoals_node_reasons"]=dict(reasons)
    result["eligible_allGoals_nodes"]=len(qualified)
    if not qualified:
        result["local_reason"]="Isomorphic allGoals forest but no qualified multi-goal split"
        return result
    local=[]
    def span(node):
        childspans={c["id"]:span(c) for c in node["children"]}
        own=max(0.,cost(node)-sum(cost(c) for c in node["children"]))
        value=own+sum(childspans.values())
        if node["id"] in qualified:
            timed,groups=qualified[node["id"]]
            branchspans=[childspans[c["id"]] for c in timed]
            serial=sum(branchspans)
            parallel=max(sum(branchspans[i] for i in group) for group in groups)
            value-=serial-parallel
            local.append({"C_call_id":node["id"],
                          "branch_cpu_s":[cost(c) for c in timed],
                          "nested_branch_model_span_s":branchspans,
                          "live_dependency_components":groups,
                          "incremental_model_saved_cpu_s":serial-parallel})
        return value
    modelspan=result["body_cpu_s"]-result["C_root_cpu_s"]+sum(span(n) for n in roots)
    if modelspan<0 or modelspan>result["body_cpu_s"]+1e-7:
        raise ValueError("Invalid nested local span")
    result.update(local_allGoals_eligible=True,
                  local_reason="Order/ancestry-isomorphic allGoals forest; live-meta local model only",
                  qualified_nodes=local,
                  local_allGoals_saved_cpu_s=result["body_cpu_s"]-modelspan,
                  local_allGoals_model_span_cpu_s=modelspan,
                  local_allGoals_model_parallelism=result["body_cpu_s"]/modelspan)
    return result

def analyze(capture):
    rows = read_rows(capture/"stdout.txt")
    events = read_events(capture/"tactics.jsonl")
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Repeated source ID: do not cross segments")
    output = [summarize(r, events.get(r["id"], {"nodes": []})) for r in rows]
    total = sum(r["body_cpu_s"] for r in output)
    saved = sum(r["local_allGoals_saved_cpu_s"] for r in output)
    kinds=collections.Counter()
    for r in output:kinds.update(r.get("exclusive_cpu_by_kind_s", {}))
    return {"capture":str(capture), "observed_sources":len(rows),
            "complete_C_sources":sum(r["complete_C_tree"] for r in output),
            "body_cpu_s":total, "local_model_saved_cpu_s":saved,
            "local_model_ratio":total/(total-saved) if total>saved else None,
            "full_DAG_average_parallelism":None,
            "exclusive_cpu_by_kind_s":dict(kinds.most_common()),
            "limits":["InfoTree-enabled heartbeat3000 diagnostic point, not production acceptance.",
                      "Ordered ancestry-isomorphic allGoals projection model leaves other constructs and unsupported work serial.",
                      "All local context is conservatively traversed; this is not a dynamic read set.",
                      "Metavariable separation alone does not establish merge/hidden-state safety.",
                      "Atomic ceiling assumes unchanged work and indivisible observed C leaf calls.",
                      "C/libc tracing has CPU and I/O cost; no free instrumentation assumption."],
            "rows":output}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("capture",type=Path);p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();d=analyze(a.capture);a.out.write_text(json.dumps(d,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in d.items() if k not in ["rows","exclusive_cpu_by_kind_s"]},indent=2))
