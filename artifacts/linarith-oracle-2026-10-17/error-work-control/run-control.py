"""Real fixed ProofNet error-work preflight; no recovery/cache/solver mutation."""
from pathlib import Path
import argparse
import asyncio
import gzip
import importlib.util
import json
import os
import re
import resource
import runpy
import subprocess
import sys
import time
from types import SimpleNamespace

R=Path("/workspaces/repository")
SOURCE=Path(__file__).resolve().parent
PRIOR=SOURCE.parent/"shred-closing"
control=PRIOR/"full-populations/http-full/proofnet/rep1-native"
prior_terminal=json.loads((control/"terminal.json").read_text())
assert prior_terminal["state"]=="complete"
own=json.loads((SOURCE/"build-receipt.json").read_text())
build=json.loads((PRIOR/"http-build-receipt.json").read_text())
build["lean_path"]=own["lean_path"]
build["lean_src_path"]=str(SOURCE)+":"+":".join(build["lean_src_path"].split(":")[1:])
SDK=Path(build["sdk"])
M=Path(build["mathlib"])
origin=json.loads((PRIOR/"full-launch.json").read_text())
K=Path(origin["command"][0]).parents[2]
upstream=json.loads((PRIOR/"build-receipt.json").read_text())
S=Path(upstream["upstream"])
sys.path[:0]=[str(S/"src"),str(K),str(K/"client")]
from lean_prefix.certificate_prevalence import wrap_final_tactic
outcome=runpy.run_path(str(PRIOR/"analyze-http.py"))["verification_outcome"]
spec=importlib.util.spec_from_file_location("error_work_http",R/"bench/lean-native/linarith-oracle/kimina-http.py")
capture=importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)
args=SimpleNamespace(kimina=K,build=Path(own["build"]),
    repl=Path(prior_terminal["effective_test_settings"]["LEAN_SERVER_REPL_PATH"]),
    reference=Path(prior_terminal["native_helper"]))

def load_rows(path):
    with gzip.open(path,"rt") as stream:
        return [json.loads(line) for line in stream]

def choose():
    measured=load_rows(control/"results.jsonl.gz")
    selected={int(row["proof_id"].split("-")[1]) for row in measured
        if outcome(row) in ("complete","incomplete","operational")}
    selected.update(range(32))
    rejected=sorted([row for row in measured if outcome(row)=="rejected"],
        key=lambda row:row["result"].get("time") or 0,reverse=True)[:3]
    selected.update(int(row["proof_id"].split("-")[1]) for row in rejected)
    originals=load_rows(SOURCE.parent/"prefix-opportunity/proofnet-input.jsonl.gz")
    selected.update(row["index"] for row in originals if row["code"]=="None")
    picked=[row for row in originals if row["index"] in selected]
    assert len(picked)==len(selected)
    return picked,dict(selection="All prior genuine complete/incomplete/operational IDs, first32, all None placeholders, three longest prior rejected bodies; original order. No new-result speed selection.",
        prior_native_counts={label:sum(outcome(row)==label for row in measured)
            for label in ("complete","incomplete","rejected","operational")},
        selected_sources=len(picked),selected_indices=[row["index"] for row in picked],
        slow_rejected_IDs=[row["proof_id"] for row in rejected])

def guarded(rows,out):
    mapped={}
    requests=[]
    for row in rows:
        match=re.search(r":=\s*by\b",row["code"])
        if match and row["code"].startswith(row["header"]):
            proof=row["code"][match.end():]
            mapped[str(row["index"])]=(match,proof)
            requests.append(json.dumps(dict(proposalId=str(row["index"]),proof=proof),ensure_ascii=False))
    env=dict(os.environ)
    env["PATH"]=str(SDK/"bin")+":"+env["PATH"]
    env["LEAN_PATH"]=own["lean_path"]
    result=subprocess.run([str(SDK/"bin/lake"),"env","lean","--run",str(S/"lean/LeanPrefix/Extract.lean")],
        cwd=M,env=env,input="\n".join(requests)+"\n",capture_output=True,text=True)
    (out/"parser.stderr").write_text(result.stderr)
    with gzip.open(out/"parser.jsonl.gz","wt",compresslevel=1) as stream:
        stream.write(result.stdout)
    assert result.returncode==0
    parsed={row["proposalId"]:row for row in (json.loads(line) for line in result.stdout.splitlines())}
    assert set(parsed)==set(mapped)
    snippets=[]
    coverage=[]
    for row in rows:
        code=row["code"]
        info=parsed.get(str(row["index"]))
        changed=False
        reason=info.get("error") if info else "unsupported source boundary"
        if info and info.get("eligible") and info.get("units"):
            match,proof=mapped[str(row["index"])]
            try:
                wrapped=wrap_final_tactic(proof,info["units"])
                if wrapped is not None:
                    start=info["units"][-1]["startByte"]
                    raw=wrapped.encode()
                    marker=b"reuse_closing in\n"
                    assert raw[start:].startswith(marker)
                    wrapped=(raw[:start]+b"error_work_control in\n"+raw[start+len(marker):]).decode()
                    code=code[:match.end()]+wrapped
                    changed=True
            except Exception as error:
                reason=repr(error)
        coverage.append(dict(proof_id="proofnet-"+str(row["index"]),guard_wrapped=changed,fallback_reason=None if changed else reason))
        if code.startswith(row["header"]):
            code=code.replace("import Mathlib\n","import Mathlib\nimport ErrorWorkControl\n",1)
        snippets.append(dict(proof_id="proofnet-"+str(row["index"]),code=code))
    (out/"coverage.json").write_text(json.dumps(coverage,indent=2)+"\n")
    return snippets

async def main(destination):
    destination.mkdir(parents=True,exist_ok=False)
    picked,selection=choose()
    (destination/"selection.json").write_text(json.dumps(selection,indent=2)+"\n")
    with gzip.open(destination/"selected-originals.jsonl.gz","wt",compresslevel=1) as stream:
        for row in picked:
            stream.write(json.dumps(row,ensure_ascii=False)+"\n")
    for method in ("native","guard"):
        started=time.monotonic_ns()
        rows=load_rows(destination/"selected-originals.jsonl.gz")
        prep=destination/(method+"-preparation")
        prep.mkdir(exist_ok=False)
        snippets=guarded(rows,prep) if method=="guard" else [
            dict(proof_id="proofnet-"+str(row["index"]),code=row["code"]) for row in rows]
        prep_seconds=(time.monotonic_ns()-started)/1e9
        directory=destination/("rep1-"+method)
        result=await capture.cell(args,"stock",directory,snippets,build)
        result.update(condition=method,input_preparation_seconds=prep_seconds,
            whole_with_input_preparation_seconds=(time.monotonic_ns()-started)/1e9,
            scope="Error-work preflight only; all preparation and retirement charged, no recovery/cache mutation, opaque env/messages differ. Root self-review.")
        (directory/"terminal.json").write_text(json.dumps(result,indent=2)+"\n")
        if result["state"]!="complete":
            return 1
    return 0

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    options=parser.parse_args()
    os.sched_setaffinity(0,{16,17,18,19})
    resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    raise SystemExit(asyncio.run(main(options.out)))
