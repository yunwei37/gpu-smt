"""Qualify the public build on the same first64 real selected sources."""
from pathlib import Path
import collections,gzip,json,os,resource,select,subprocess
R=Path("/workspaces/repository")
A=R/"docs/tmp/bootstrap/step-0010-20261014T133154+0000/portable-source-20261018"
D=R/"bench/lean-native/linarith-oracle/reproduction"
U=Path("/tmp/gpu-smt-linarith-oracle-20261017/portable-source-build")
os.sched_setaffinity(0,{20,21,22,23})
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
if not(A/"native-build-terminal.json").exists():
    try:
        fd=os.pidfd_open(533102)
        select.select([fd],[],[])
        os.close(fd)
    except ProcessLookupError:
        pass
build=json.loads((A/"native-build-terminal.json").read_text())
if build["returncode"]:
    raise RuntimeError("Build failed; no proof results fabricated")
inputs=[json.loads(line)for line in(R/"artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl").open()][:64]
ref=R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics/full1000/power/rep1-oracle-highs/responses.jsonl.gz"
with gzip.open(ref,"rt")as f:expected={x["proof_id"]:x["outcome"]for x in map(json.loads,f)}
sources=A/"sources";sources.mkdir(exist_ok=True)
results=[]
for row in inputs:
    source=sources/(row["proof_id"]+".lean")
    code=row["code"]
    header="import Mathlib\nimport Aesop\n"
    assert code.startswith(header)
    source.write_text(header+"import GpuArithmetic.IntegerPowerOracle\n"+code[len(header):])
    target=A/"proofs"/row["proof_id"]
    cmd=["/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python",str(D/"check.py"),"--build",str(U),"--log-dir",str(target),str(source)]
    p=subprocess.run(cmd,cwd=R)
    output=(target/"lean.jsonl").read_text()if(target/"lean.jsonl").exists()else""
    diagnostics=[]
    for line in output.splitlines():
        try:diagnostics.append(json.loads(line))
        except json.JSONDecodeError:pass
    result={"proof_id":row["proof_id"],"index":row["index"],"returncode":p.returncode,"expected":expected[row["proof_id"]],"outcome":"complete"if p.returncode==0 else"rejected","error_messages":[x for x in diagnostics if x.get("severity")=="error"]}
    if p.returncode and not diagnostics:
        result["outcome"]="operational"
    results.append(result)
    print(json.dumps(result),flush=True)
    if result["outcome"]=="operational":
        break
record={"scope":"Standard CLI functional reproduction on real selected sources, not the warm performance harness; root self-review","expected_sources":64,"returned":len(results),"counts":dict(collections.Counter(x["outcome"]for x in results)),"verdict_differences":[x["proof_id"]for x in results if x["outcome"]!=x["expected"]],"rows":results}
(A/"proof-qualification.json").write_text(json.dumps(record,indent=2)+"\n")
