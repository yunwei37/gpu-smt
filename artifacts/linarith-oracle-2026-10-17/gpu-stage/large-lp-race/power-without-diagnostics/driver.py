from pathlib import Path
import subprocess,os,resource,json,time,gzip,sys,datetime
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics"
U=Path("/tmp/gpu-smt-linarith-oracle-20261017/power-without-diagnostics")
Q=A.parent/"power-export";P=U.parent/"power-export"
os.sched_setaffinity(0,{8,9,10,11});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
# Await the already-running finite compiler without starting a second build.
while "COMPLETE_LEAN_BUILD_SAME_NUMERIC_BINARIES"not in(A/"build.log").read_text():
 try:
  fields=Path("/proc/484055/stat").read_text().split()
  if fields[2]=="Z":raise RuntimeError("builder exited without final receipt")
 except FileNotFoundError:raise RuntimeError("builder disappeared without final receipt")
 time.sleep(.2)
def cell(root,out,label,n,frontend,method):
 env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(root),GPU_ARITHMETIC_RACE_MIN_ROWS="11",GPU_ARITHMETIC_NEGATIVE_CERTIFICATES="1",GPU_SMT_NATIVE_OMEGA_CONTROL="1",GPU_SMT_OMEGA_CONTROL_LOG=str(out/"omega-calls.jsonl"),GPU_SMT_COST_FRONTEND=frontend)
 env.pop("GPU_ARITHMETIC_NUMERIC_PHASE_LOG",None)
 cmd=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python",str(A/"run-power.py"),"--out",str(out),"--input",str(A.parents[2]/"input-top1000.jsonl"),"--limit",str(n),"--width","8","--affinity","8","9","10","11","--sample-seconds","0","--native-buckets","--repl","/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl","--methods",method]
 print(json.dumps({"condition":label,"argv":cmd,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}),flush=True)
 subprocess.run(cmd,cwd=R,env=env,check=True)
 term=json.loads((out/("rep1-"+method)/"terminal.json").read_text())
 assert term["state"]=="complete"and term["attempts"]==n and term["effective_RLIMIT_AS"]==51539607552 and term["resource_observer_enabled"]is False
 with gzip.open(out/("rep1-"+method)/"responses.jsonl.gz","rt")as f:rows=[json.loads(l)for l in f]
 assert len(rows)==n
 return term,{x["proof_id"]:x for x in rows}
conditions=[("retained-native",P,"native","fast-hybrid"),("reduced-native",U,"native","fast-hybrid"),("reduced-power",U,"power","oracle-highs"),("retained-power",P,"power","oracle-highs")]
results={};responses={}
for label,root,frontend,method in conditions:
 term,rs=cell(root,A/"qualification"/label,label,64,frontend,method);results[label]=term;responses[label]=rs
ref=responses["retained-native"];fidelity={}
for label,rs in responses.items():
 assert rs.keys()==ref.keys()
 fidelity[label]={"verdict":[k for k in ref if ref[k]["outcome"]!=rs[k]["outcome"]],"non_message":[k for k in ref if {a:b for a,b in ref[k]["response"].items()if a!="messages"}!={a:b for a,b in rs[k]["response"].items()if a!="messages"}],"messages":[k for k in ref if ref[k]["response"]!=rs[k]["response"]]}
qualified=all(not v["verdict"]and not v["non_message"]for v in fidelity.values())
(A/"qualification-result.json").write_text(json.dumps({"state":"complete","qualified":qualified,"conditions":results,"fidelity":fidelity},indent=2)+"\n")
if not qualified:raise RuntimeError("qualification native response mismatch retained")
print("QUALIFICATION_COMPLETE",flush=True)
full={}
for label,frontend,method in[("native","native","fast-hybrid"),("power","power","oracle-highs")]:
 term,rs=cell(U,A/"full1000"/label,label,1000,frontend,method);full[label]=term
(A/"full1000-terminal.json").write_text(json.dumps({"state":"complete","conditions":full},indent=2)+"\n")
