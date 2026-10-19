from pathlib import Path
import subprocess,json,datetime,runpy,sys,gzip
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17"
OUT=A/"shred-closing/memory-recovery-20261019"
PY="/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python"
def run(name,command):
    print(json.dumps(dict(event="start",name=name,command=command,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())),flush=True)
    with(OUT/(name+".log")).open("wb")as stream:
        result=subprocess.run(command,cwd=R,stdout=stream,stderr=subprocess.STDOUT)
    print(json.dumps(dict(event="exit",name=name,code=result.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())),flush=True)
    if result.returncode:raise SystemExit(result.returncode)
command=[PY,"-u",str(A/"shred-closing/run-kimina.py"),"--datasets","minif2f","--concurrency","2"]
run("preflight",command+["--out",str(OUT/"preflight")])
root=OUT/"preflight/http-preflight/minif2f"
mod=runpy.run_path(str(A/"shred-closing/analyze-http.py"))
conditions={}
for name in["native","shred"]:
    term=json.loads((root/("rep1-"+name)/"terminal.json").read_text())
    assert term["state"]=="complete" and term["source_concurrency"]==2
    assert term["returned"]==term["expected"]==50
    assert term["memory_limit_bytes"]==51539607552 and term["affinity"]==[4,5,6,7]
    assert not term["owned_live_descendants_after_shutdown"]
    conditions[name]={x["proof_id"]:mod["verification_outcome"](x)for x in mod["rows"](root/("rep1-"+name)/"results.jsonl")}
assert conditions["native"]==conditions["shred"]
assert list(conditions["native"].values()).count("complete")==28
print(json.dumps(dict(event="real_preflight_closed",original_sources=50,source_concurrency=2,native_complete=28,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())),flush=True)
run("full-minif2f",command+["--out",str(OUT/"full-population"),"--full"])
REC=A/"workspace-interruption-20261019"
for name in["resume-current29750-after-repair.py","resume-formal49-after-repair.py","resume-older29750-after-repair.py"]:
    run(name.removesuffix(".py"),[PY,"-u",str(REC/name)])
