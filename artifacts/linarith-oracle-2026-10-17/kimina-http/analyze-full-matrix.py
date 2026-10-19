"""Reproduce all nine original Goedel HTTP cells, exposing restart epochs."""
from pathlib import Path
import argparse,collections,csv,gzip,json,math,runpy

def rows(path):
    if not path.exists():path=path.with_name(path.name+".gz")
    with(gzip.open(path,"rt")if path.suffix==".gz"else path.open())as stream:
        return[json.loads(line)for line in stream if line.strip()]

def nonmsg(row):
    return{k:v for k,v in row["result"].get("response",{}).items()if k!="messages"}

def analyze(root):
    ids=json.loads((root/"full1000/source-ids.json").read_text())
    assert len(ids)==len(set(ids))==1000
    boundary=runpy.run_path(str(root.parents[2]/"bench/lean-native/linarith-oracle/analyze-http-boundaries.py"))
    cells={};mapped={};projection=[]
    for rep in[1,2,3]:
        for method in["stock","native","power"]:
            name=f"rep{rep}-{method}"
            recovered=rep==3 and method!="power"
            directory=root/("full1000-recovery2-20261019"if recovered else"full1000")/name
            terminal=json.loads((directory/"terminal.json").read_text())
            data=rows(directory/"results.jsonl")
            assert terminal["state"]=="complete"
            assert terminal["expected"]==terminal["returned"]==len(data)==1000
            assert[x["proof_id"]for x in data]==ids
            assert dict(collections.Counter(x["status"]for x in data))==terminal["counts"]=={"valid":992,"lean_error":8}
            native_incomplete=[x["proof_id"]for x in data if x["result"].get("response",{}).get("sorries")or any("sorry"in m.get("data","")for m in x["result"].get("response",{}).get("messages",[])if m.get("severity")=="warning")]
            assert not native_incomplete,"SDK-valid must not mask incomplete sources"
            derived=[]
            for row in data:
                response=row["result"].get("response",{})
                assert isinstance(response,dict)and not response.get("message")and not response.get("error")
                derived.append("rejected"if any(m.get("severity")=="error"for m in response.get("messages",[]))else"complete")
            assert dict(collections.Counter(derived))=={"complete":992,"rejected":8}
            assert terminal["affinity"]==[20,21,22,23] and terminal["memory_limit_bytes"]==51539607552
            assert not terminal["owned_live_descendants_after_shutdown"]
            mapped[name]={x["proof_id"]:x for x in data}
            detail=boundary["analyze_cell"](directory,ids)
            assert detail["exactly_one_recorded_request_per_source"]
            assert detail["exactly_one_matching_final_attempt_per_source"]
            assert not detail["non_200_attempts"]and not detail["unanswered_recorded_requests"]
            cells[name]=dict(directory=str(directory.relative_to(root)),epoch="after-container-OOM"if recovered else"original-Pod",analysis=detail)
            for item in detail["completed_attempts"]:
                projection.append(dict(rep=rep,method=method,epoch=cells[name]["epoch"],proof_id=item["proof_id"],
                    status=mapped[name][item["proof_id"]]["status"],HTTP_attempt_seconds=item["HTTP_attempt_seconds"],
                    SDK_body_seconds=item["reported_body_seconds"]))
    pairs=[]
    for rep in[1,2,3]:
        n,p=mapped[f"rep{rep}-native"],mapped[f"rep{rep}-power"]
        changes=dict(status_difference_IDs=[i for i in ids if n[i]["status"]!=p[i]["status"]],
            non_message_difference_IDs=[i for i in ids if nonmsg(n[i])!=nonmsg(p[i])],
            raw_response_difference_IDs=[i for i in ids if n[i]["result"].get("response")!=p[i]["result"].get("response")])
        ranked=sorted(ids,key=lambda i:n[i]["result"]["time"],reverse=True)
        tails={}
        for label,count in[("slowest_1_percent",10),("slowest_10_percent",100)]:
            subset=ranked[:count]
            tails[label]=dict(source_IDs=subset,
                native_SDK_body_seconds_sum_NOT_whole=sum(n[i]["result"]["time"]for i in subset),
                power_SDK_body_seconds_sum_NOT_whole=sum(p[i]["result"]["time"]for i in subset))
        nt,pt=[cells[f"rep{rep}-{method}"]["analysis"]["terminal"]for method in["native","power"]]
        pairs.append(dict(rep=rep,mixed_restart_epochs=rep==3,native_whole_seconds=nt["whole_lifecycle_seconds"],
            power_whole_seconds=pt["whole_lifecycle_seconds"],native_warm_seconds=nt["warm_verify_seconds"],power_warm_seconds=pt["warm_verify_seconds"],
            native_over_power_whole=nt["whole_lifecycle_seconds"]/pt["whole_lifecycle_seconds"],
            native_over_power_warm=nt["warm_verify_seconds"]/pt["warm_verify_seconds"],fidelity=changes,native_ranked_tails=tails,
            sources_with_longer_power_body=sum(p[i]["result"]["time"]>n[i]["result"]["time"]for i in ids)))
    same_epoch=pairs[:2]
    sums={name:sum(x[name]for x in same_epoch)for name in["native_whole_seconds","power_whole_seconds","native_warm_seconds","power_warm_seconds"]}
    out=dict(source_runs=9000,unique_sources=1000,closed_cells=9,cells=cells,pairs=pairs,
        first_two_original_epoch_pairs=dict(**sums,native_over_power_whole=sums["native_whole_seconds"]/sums["power_whole_seconds"],
            native_over_power_warm=sums["native_warm_seconds"]/sums["power_warm_seconds"]),
        scope="All nine declared original1000source cells completed, all native fields/messages retained. Seven cells precede container replacement/OOM; rep3stock/native are recovered, so rep3 is mixed epoch. No uninterrupted three-repeat aggregate, causal CPU/LP fraction, GPU gain, confidence interval, global CPU optimum or systems novelty. Source HTTP/body spans overlap and exclude pre-dispatch SDK wait; whole clocks charge full lifecycle. Root self-review.")
    (root/"full-matrix-analysis.json").write_text(json.dumps(out,indent=2)+"\n")
    with(root/"full-matrix-source-latencies.csv").open("w",newline="")as stream:
        writer=csv.DictWriter(stream,fieldnames=list(projection[0]));writer.writeheader();writer.writerows(projection)
    return out

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("root",type=Path);args=parser.parse_args()
    out=analyze(args.root)
    print(json.dumps(dict(source_runs=out["source_runs"],pairs=[{k:v for k,v in x.items()if k not in["native_ranked_tails","fidelity"]}for x in out["pairs"]],
        differences=[dict(rep=x["rep"],**{k:len(v)for k,v in x["fidelity"].items()})for x in out["pairs"]],
        original_epoch=out["first_two_original_epoch_pairs"]),indent=2))
