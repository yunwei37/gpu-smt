from pathlib import Path
import subprocess,os,json,gzip,shutil,resource,datetime
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-full29750-recovery-20261019"
Q=A.parent/"power-without-diagnostics"
U=Path("/tmp/gpu-smt-linarith-oracle-20261017/power-without-diagnostics")
INPUT=R/"artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl"
PYTHON="/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python"
os.sched_setaffinity(0,{8,9,10,11});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def archive(out):
 for p in out.rglob("*"):
  if not p.is_file()or p.suffix not in[".jsonl",".log",".phases"]:continue
  q=p.with_name(p.name+".gz")
  with p.open("rb")as f,gzip.open(q,"wb",compresslevel=6)as g:shutil.copyfileobj(f,g,1024*1024)
  with p.open("rb")as f,gzip.open(q,"rb")as g:
   while True:
    x=f.read(1024*1024);y=g.read(1024*1024)
    assert x==y
    if not x:break
  p.unlink()
def cell(label,frontend,profile=False):
 out=A/label;method="fast-hybrid"if frontend=="native"else"oracle-highs"
 env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS="11",GPU_ARITHMETIC_NEGATIVE_CERTIFICATES="1",GPU_SMT_NATIVE_OMEGA_CONTROL="1",GPU_SMT_OMEGA_CONTROL_LOG=str(out/"omega-calls.jsonl"),GPU_SMT_COST_FRONTEND=frontend)
 env.pop("GPU_ARITHMETIC_NUMERIC_PHASE_LOG",None)
 cmd=[PYTHON,str(Q/"run-power.py"),"--out",str(out),"--input",str(INPUT),"--limit","0","--width","8","--affinity","8","9","10","11","--sample-seconds","1"if profile else"0","--native-buckets","--repl","/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl","--methods",method]
 print(json.dumps({"event":"launch","condition":label,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"argv":cmd}),flush=True)
 subprocess.run(cmd,cwd=R,env=env,check=True)
 term=json.loads((out/("rep1-"+method)/"terminal.json").read_text())
 assert term["state"]=="complete"and term["attempts"]==29750 and term["effective_RLIMIT_AS"]==51539607552
 archive(out)
 print(json.dumps({"event":"closed","condition":label,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"whole_ns":term["whole_ns"],"counts":term["counts"]}),flush=True)
 return{"label":label,"profile":profile,"terminal":term}
closed=[]
for rep,order in[(1,["native","power"]),(2,["power","native"]),(3,["native","power"])]:
 for frontend in order:closed.append(cell("rep"+str(rep)+"-"+frontend,frontend))
for frontend in["native","power"]:closed.append(cell("profile-"+frontend,frontend,True))
(A/"terminal.json").write_text(json.dumps({"state":"complete","cells":closed},indent=2)+"\n")
