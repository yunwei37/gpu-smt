from pathlib import Path
import os,sys,subprocess,resource,json,time,gzip,importlib.util,collections
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9"
U=Path("/tmp/gpu-smt-linarith-oracle-20261017/formal-oracle-4.9")
P=U.parent/"power-export"
D=Path("/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture")
SDK=D/"lean-4.9.0-rc1-linux";M=D/"mathlib4"
N=Path("/tmp/gpu-smt-native-mathlib-20261014")
os.sched_setaffinity(0,{12,13,14,15})
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.environ["PATH"]=str(SDK/"bin")+":"+os.environ["PATH"]
os.environ["LEAN_PATH"]=str(U)+":"+os.environ.get("LEAN_PATH","")
os.environ["LEAN_SERVER_NATIVE_DYNLIB"]=str(U/"libFormalOracle49.so")
os.environ["LD_LIBRARY_PATH"]=":".join([str(N/".lake/build/lib")]+[str(x/".lake/build/lib")for x in(N/".lake/packages").iterdir()if x.is_dir()])
os.environ["GPU_ARITHMETIC_ORACLE"]=str(P/"arithmetic-batchd")
os.environ["FARKAS_NATIVE_BIN"]=str(P/"farkas-batchd")
os.environ["GPU_ARITHMETIC_RACE_WORKER"]=str(P/"farkas-race-worker")
os.environ["GPU_ARITHMETIC_RACE_MIN_ROWS"]="11"
os.environ["GPU_ARITHMETIC_NEGATIVE_CERTIFICATES"]="1"
os.environ["FARKAS_EXTERNAL_CPU_HYBRID"]="1"
for k in ["FARKAS_CORPUS_FILE","GPU_ARITHMETIC_NUMERIC_PHASE_LOG","GPU_SMT_NATIVE_OMEGA_CONTROL"]:os.environ.pop(k,None)
p=Path("/tmp/gpu-smt-primary-opportunities-20261017/shred/src/lean_prefix/repl.py")
spec=importlib.util.spec_from_file_location("formal_native_repl",p)
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
items=[json.loads(l)for l in(A/"qualification-input.jsonl").read_text().splitlines()]
def outcome(ans):
 if not isinstance(ans,dict)or ans.get("message")or ans.get("error"):return"operational"
 if any(x.get("severity")=="error"for x in ans.get("messages",[])):return"rejected"
 if ans.get("sorries")or any("sorry"in x.get("data","")for x in ans.get("messages",[])if x.get("severity")=="warning"):return"incomplete"
 return"complete"
for mode in ["stock","native","direct"]:
 out=A/("qualify-"+mode);out.mkdir(exist_ok=False)
 start=time.monotonic_ns();counts=collections.Counter();answers=[];failure=None;normal=False;proxy=None
 log=gzip.open(out/"requests-responses.jsonl.gz","wt",compresslevel=1)
 os.environ["GPU_SMT_FORMAL_MODE"]=mode
 os.environ["GPU_SMT_FORMAL_ORACLE_LOG"]=str(out/"oracle-trace.jsonl")
 os.environ["GPU_ARITHMETIC_RACE_LOG"]=str(out/"lp-races.jsonl")
 sock=U/("support-"+str(os.getpid())+"-"+mode+".sock");assert not sock.exists()
 os.environ["GPU_ARITHMETIC_SUPPORT_SOCKET"]=str(sock)
 proxylog=open(out/"support-proxy.log","w")
 client=mod.LeanRepl(M,executable=U.parent/"prefix/repl-kernel/.lake/build/bin/repl",timeout_seconds=300)
 def request(data):
  t=time.monotonic_ns()
  log.write(json.dumps({"event":"request","request":data,"start_ns":t},ensure_ascii=False)+"\n");log.flush()
  res=client.request(data)
  log.write(json.dumps({"event":"response","request":data,"response":res.response,"wall_ns":time.monotonic_ns()-t,"stderr":res.stderr},ensure_ascii=False)+"\n");log.flush()
  return res.response
 try:
  proxy=subprocess.Popen(["/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python",str(R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-export/support-proxy.py"),"--backend","highs","--socket",str(sock),"--log",str(out/"support-calls.jsonl.gz")],stdout=proxylog,stderr=subprocess.STDOUT)
  while not sock.exists():
   if proxy.poll()is not None:raise RuntimeError("HiGHS startup")
   time.sleep(.01)
  client.start();headers={}
  for offset in range(0,len(items),4):
   chunk=items[offset:offset+4];h=chunk[0]["header"];assert all(x["header"]==h for x in chunk)
   if h not in headers:
    ans=request({"cmd":"import FormalOracle49\n"+h,"allTactics":False,"ast":False,"tactics":False,"premises":False})
    if outcome(ans)!="complete"or not isinstance(ans.get("env"),int):raise RuntimeError("header failure "+str(ans))
    headers[h]=ans["env"]
   bodies=[]
   for x in chunk:
    assert x["code"].startswith(h)
    bodies.append("".join(c if c in"\r\n"else" "for c in h)+x["code"][len(h):])
   ans=request({"env":headers[h],"cmds":bodies,"allTactics":False,"ast":False,"tactics":False,"premises":False})
   values=ans.get("results")
   if not isinstance(values,list)or len(values)!=len(chunk):raise RuntimeError("batch response")
   for x,value in zip(chunk,values):
    status=outcome(value);counts[status]+=1
    answers.append({"dataset":x["dataset"],"index":x["index"],"outcome":status,"response":value})
   print(json.dumps({"mode":mode,"returned":len(answers),"counts":dict(counts)}),flush=True)
  bye=request({"quit":True})
  code=client._process.wait(timeout=300)
  normal=bye.get("bye")is True and code==0
 except BaseException as e:
  failure=repr(e);print("ERROR",failure,flush=True)
 finally:
  if client._stderr is not None:
   (out/"repl.stderr").write_bytes(os.pread(client._stderr.fileno(),os.fstat(client._stderr.fileno()).st_size,0))
  client.close()
  if proxy is not None:
   proxy.terminate();proxy.wait()
  sock.unlink(missing_ok=True);proxylog.close();log.close()
  with gzip.open(out/"results.jsonl.gz","wt")as f:
   for row in answers:f.write(json.dumps(row,ensure_ascii=False)+"\n")
  terminal={"state":"complete"if len(answers)==len(items)and normal and failure is None else"failed","mode":mode,"expected":len(items),"returned":len(answers),"counts":dict(counts),"whole_seconds":(time.monotonic_ns()-start)/1e9,"normal_native_exit":normal,"error":failure,"affinity":sorted(os.sched_getaffinity(0)),"memory_limit_bytes":client.memory_limit_bytes,"scope":"selected actual formal64; technical engagement only; includes trace and CPU support setup"}
  (out/"terminal.json").write_text(json.dumps(terminal,indent=2)+"\n");print(json.dumps(terminal),flush=True)
 if terminal["state"]!="complete":raise SystemExit(1)
(A/"qualification-terminal.json").write_text(json.dumps({"state":"complete"})+"\n")
