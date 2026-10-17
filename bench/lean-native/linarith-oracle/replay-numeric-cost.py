"""Replay a closed numeric request stream for exact worker CPU accounting.
This is NOT end-to-end Lean performance and does not replace source-native runs.
"""
from pathlib import Path
import argparse,collections,gzip,importlib.util,json,os,resource,subprocess,time,sys,datetime

def rows(p):
    with (gzip.open(p,"rt") if p.suffix==".gz" else p.open()) as f:
        for line in f:yield json.loads(line)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-log",type=Path,required=True)
    p.add_argument("--build-root",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--affinity",type=int,nargs="+",default=[8,9,10,11])
    a=p.parse_args();resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    os.sched_setaffinity(0,set(a.affinity));a.out.mkdir(parents=True,exist_ok=False)
    groups=collections.OrderedDict()
    for x in rows(a.input_log):
        if x.get("kind") in ["direct","fallback"]:groups.setdefault((x["kind"],x["pid"]),[]).append(x)
    env=dict(os.environ);env["FARKAS_COST_FILE"]=str(a.out/"solver-costs.jsonl")
    env["FARKAS_EXTERNAL_CPU_HYBRID"]="1"
    env.pop("FARKAS_COST_WORKER",None)
    launch={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pid":os.getpid(),"argv":sys.argv,
            "input_log":str(a.input_log),"process_streams":len(groups),"source_records":sum(map(len,groups.values())),
            "native_engine":"same hybrid as closed oracle/fast-hybrid inputs","RLIMIT_AS":resource.getrlimit(resource.RLIMIT_AS),
            "scope":"same per-process numeric request order, no Lean work; numeric CPU composition only, not whole-verification/GPU speedup"}
    (a.out/"launch.json").write_text(json.dumps(launch,indent=2)+"\n")
    start=time.monotonic_ns();compared=0;diff=[];children=[];state="failed"
    with gzip.open(a.out/"responses.jsonl.gz","wt",compresslevel=1) as out:
        try:
            for (kind,old_pid),xs in groups.items():
                binary=a.build_root/("arithmetic-costd" if kind=="direct" else "farkas-costd")
                with (a.out/f"stderr-{kind}-{old_pid}.log").open("w") as err:
                    child=subprocess.Popen([str(binary)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True,env=env)
                    children.append(child.pid)
                    try:
                        for n,x in enumerate(xs):
                            child.stdin.write(json.dumps(x["request"],separators=(",",":"))+"\n");child.stdin.flush()
                            line=child.stdout.readline()
                            if not line:raise RuntimeError("numeric replay EOF before response")
                            answer=json.loads(line);old=x.get("answer") or {}
                            equal=answer.get("cert")==old.get("cert") and answer.get("error")==old.get("error")
                            compared+=1
                            if not equal:diff.append({"old_pid":old_pid,"record":n,"kind":kind,"old":old,"new":answer})
                            out.write(json.dumps({"old_pid":old_pid,"record":n,"kind":kind,"cert_and_error_equal":equal,"response":answer})+"\n")
                    finally:
                        child.stdin.close()
                        tail=child.stdout.read();rc=child.wait()
                        if rc!=0 or tail:raise RuntimeError(f"numeric worker terminal {rc}, extra stdout={tail[:200]}")
            state="complete"
        finally:
            terminal={"state":state,"compared":compared,"certificate_or_error_differences":len(diff),"elapsed_ns":time.monotonic_ns()-start,
                      "children":children,"scope":launch["scope"]}
            (a.out/"terminal.json").write_text(json.dumps(terminal,indent=2)+"\n")
            (a.out/"certificate-differences.json").write_text(json.dumps(diff,indent=2)+"\n")
    spec=importlib.util.spec_from_file_location("cost_analysis",Path(__file__).with_name("analyze-cost.py"))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    ledger=module.cpu_ledger(list(rows(a.out/"solver-costs.jsonl")))
    (a.out/"numeric-cpu-ledger.json").write_text(json.dumps(ledger,indent=2)+"\n")
    print(json.dumps({"terminal":terminal,"ledger":ledger},indent=2),flush=True)
if __name__=="__main__":main()
