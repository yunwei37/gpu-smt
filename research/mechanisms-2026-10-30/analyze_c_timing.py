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
    # Optimistic ceiling only if recorded leaf calls remain indivisible and work fixed.
    denom = max(largest, residual)
    result["fixed_atomic_work_optimistic_parallelism_ceiling"] = (
        result["body_cpu_s"]/denom if denom else None)
    infos = [n for n in walk(row["infos"])
             if normalized(n.get("kind", "")) == "Lean.Parser.Tactic.allGoals"]
    calls = [n for n in nodes if normalized(n["kind"]) == "Lean.Parser.Tactic.allGoals"]
    result["allGoals_info_count"] = len(infos)
    result["allGoals_C_count"] = len(calls)
    if len(infos) != 1 or len(calls) != 1:
        result["local_reason"] = "No unique allGoals correspondence"
        return result
    info, call = infos[0], calls[0]
    goals = info.get("liveBefore", [])
    branches = [n for n in info.get("children", [])
                if normalized(n.get("kind", "")) == "Lean.Parser.Tactic.tacticSeq"]
    timed = [n for n in call["children"]
             if normalized(n["kind"]) == "Lean.Parser.Tactic.tacticSeq"]
    if len(goals)<2 or len(branches)!=len(goals) or len(timed)!=len(goals):
        result["local_reason"] = "Unmatched branch counts or no split"
        return result
    if call["end"]["return_tag"] != 1:
        result["local_reason"] = "C allGoals did not return qualified success tag1"
        return result
    for branch, goal in zip(branches, goals):
        before = branch.get("liveBefore", [])
        if len(before)!=1 or before[0][0]!=goal[0]:
            result["local_reason"] = "Branch goal identity/order mismatch"
            return result
    groups = components(goals)
    costs = [cost(n) for n in timed]
    serial = sum(costs)
    parallel = max(sum(costs[i] for i in group) for group in groups)
    if serial > cost(call)+1e-7:
        raise ValueError("Branch CPU exceeds parent")
    saved = serial-parallel
    result.update(local_allGoals_eligible=True,
                  local_reason="Unique local allGoals; conservative live-meta conflict model only",
                  branch_cpu_s=costs, live_dependency_components=groups,
                  local_allGoals_saved_cpu_s=saved,
                  local_allGoals_model_span_cpu_s=result["body_cpu_s"]-saved,
                  local_allGoals_model_parallelism=result["body_cpu_s"]/(result["body_cpu_s"]-saved))
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
                      "Unique allGoals model leaves other constructs and all unsupported work serial.",
                      "All local context is conservatively traversed; this is not a dynamic read set.",
                      "Metavariable separation alone does not establish merge/hidden-state safety.",
                      "Atomic ceiling assumes unchanged work and indivisible observed C leaf calls.",
                      "C/libc tracing has CPU and I/O cost; no free instrumentation assumption."],
            "rows":output}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("capture",type=Path);p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();d=analyze(a.capture);a.out.write_text(json.dumps(d,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in d.items() if k not in ["rows","exclusive_cpu_by_kind_s"]},indent=2))
