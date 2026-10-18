from pathlib import Path
import os,sys,subprocess,resource,json,time,gzip,importlib.util,collections,traceback
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9"
F=A/"full-populations"
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
for k in["FARKAS_CORPUS_FILE","GPU_ARITHMETIC_NUMERIC_PHASE_LOG","GPU_SMT_NATIVE_OMEGA_CONTROL","GPU_SMT_FORMAL_ORACLE_LOG"]:os.environ.pop(k,None)
p=Path("/tmp/gpu-smt-primary-opportunities-20261017/shred/src/lean_prefix/repl.py")
spec=importlib.util.spec_from_file_location("formal_native_repl",p)
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def outcome(ans):
 if not isinstance(ans,dict)or ans.get("message")or ans.get("error"):return"operational"
 if any(x.get("severity")=="error"for x in ans.get("messages",[])):return"rejected"
 if ans.get("sorries")or any("sorry"in x.get("data","")for x in ans.get("messages",[])if x.get("severity")=="warning"):return"incomplete"
 return"complete"
def usage():
 return[resource.getrusage(k)for k in[resource.RUSAGE_SELF,resource.RUSAGE_CHILDREN]]
def run(ds,mode,items):
 out=F/ds/mode;out.mkdir(parents=True,exist_ok=False)
 start=time.monotonic_ns();ru0=usage();counts=collections.Counter();returned=0;failure=None;normal=False;proxy=None;forced=0
 log=gzip.open(out/"requests-responses.jsonl.gz","wt",compresslevel=1)
 rows=gzip.open(out/"results.jsonl.gz","wt",compresslevel=1)
 os.environ["GPU_SMT_FORMAL_MODE"]=mode
 os.environ["GPU_ARITHMETIC_RACE_LOG"]=str(out/"lp-races.jsonl")
 sock=U/("support-full-"+str(os.getpid())+"-"+ds+"-"+mode+".sock");assert not sock.exists()
 os.environ["GPU_ARITHMETIC_SUPPORT_SOCKET"]=str(sock)
 proxylog=open(out/"support-proxy.log","w")
 client=mod.LeanRepl(M,executable=U.parent/"prefix/repl-kernel/.lake/build/bin/repl",timeout_seconds=300)
 headers={}
 def request(data):
  nonlocal forced
  if client._process is None:client.start()
  t=time.monotonic_ns()
  log.write(json.dumps({"event":"request","request":data,"start_ns":t},ensure_ascii=False)+"\n");log.flush()
  try:res=client.request(data)
  except mod.ReplError as e:
   log.write(json.dumps({"event":"request_failure","request":data,"wall_ns":time.monotonic_ns()-t,"error":str(e),"kind":type(e).__name__,"stderr":getattr(e,"stderr","")},ensure_ascii=False)+"\n");log.flush()
   client.close();headers.clear();forced+=1;raise
  log.write(json.dumps({"event":"response","request":data,"response":res.response,"wall_ns":time.monotonic_ns()-t,"native_cpu_seconds":res.cpu_seconds,"stderr":res.stderr},ensure_ascii=False)+"\n");log.flush()
  return res.response
 def env_for(h):
  if h not in headers:
   ans=request({"cmd":"import FormalOracle49\n"+h,"allTactics":False,"ast":False,"tactics":False,"premises":False})
   if outcome(ans)!="complete"or not isinstance(ans.get("env"),int):raise RuntimeError("header failure "+str(ans))
   headers[h]=ans["env"]
  return headers[h]
 try:
  proxy=subprocess.Popen(["/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python",str(R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-export/support-proxy.py"),"--backend","highs","--socket",str(sock),"--log",str(out/"support-calls.jsonl.gz")],stdout=proxylog,stderr=subprocess.STDOUT)
  while not sock.exists():
   if proxy.poll()is not None:raise RuntimeError("HiGHS startup")
   time.sleep(.01)
  client.start()
  for offset in range(0,len(items),32):
   group=items[offset:offset+32];byheader=collections.defaultdict(list);answers={}
   for x in group:byheader[x["header"]].append(x)
   for h,xs in byheader.items():
    for at in range(0,len(xs),4):
     chunk=xs[at:at+4]
     try:
      env=env_for(h);bodies=[]
      for x in chunk:
       assert x["code"].startswith(h)
       bodies.append("".join(c if c in"\r\n"else" "for c in h)+x["code"][len(h):])
      ans=request({"env":env,"cmds":bodies,"allTactics":False,"ast":False,"tactics":False,"premises":False})
      values=ans.get("results")
      if not isinstance(values,list)or len(values)!=len(chunk):raise RuntimeError("batch response")
      answers.update((x["index"],value)for x,value in zip(chunk,values))
     except mod.ReplError as e:
      answers.update((x["index"],{"message":str(e),"transport_failure":type(e).__name__})for x in chunk)
   for x in group:
    ans=answers[x["index"]];status=outcome(ans);counts[status]+=1;returned+=1
    rows.write(json.dumps({"dataset":ds,"index":x["index"],"outcome":status,"response":ans},ensure_ascii=False)+"\n")
   rows.flush()
   print(json.dumps({"dataset":ds,"mode":mode,"returned":returned,"counts":dict(counts)}),flush=True)
  if client._process is not None and client._process.poll()is None:
   try:
    bye=request({"quit":True});code=client._process.wait(timeout=300)
    normal=bye.get("bye")is True and code==0
   except mod.ReplError:pass
   except subprocess.TimeoutExpired:
    client.close();headers.clear();forced+=1
 except BaseException as e:
  failure=repr(e);traceback.print_exc()
 finally:
  if client._stderr is not None:
   (out/"repl.stderr").write_bytes(os.pread(client._stderr.fileno(),os.fstat(client._stderr.fileno()).st_size,0))
  client.close()
  if proxy is not None:
   proxy.terminate();proxy.wait()
  sock.unlink(missing_ok=True);proxylog.close();log.close();rows.close()
  ru1=usage()
  cpu={"collector":(ru1[0].ru_utime+ru1[0].ru_stime)-(ru0[0].ru_utime+ru0[0].ru_stime),"waited_children":(ru1[1].ru_utime+ru1[1].ru_stime)-(ru0[1].ru_utime+ru0[1].ru_stime)}
  terminal={"state":"complete"if returned==len(items)and failure is None else"failed","dataset":ds,"mode":mode,"expected":len(items),"returned":returned,"counts":dict(counts),"whole_seconds":(time.monotonic_ns()-start)/1e9,"normal_native_exit":normal,"forced_native_retirements":forced,"CPU":cpu,"CPU_scope":"self+waited children, not exhaustive descendant CPU; forced retirements may censor tails","error":failure,"affinity":sorted(os.sched_getaffinity(0)),"memory_limit_bytes":client.memory_limit_bytes,"scope":"full original population, selected extra module in all modes, one fixed-order shared-host block, no GPU work"}
  (out/"terminal.json").write_text(json.dumps(terminal,indent=2)+"\n");print(json.dumps(terminal),flush=True)
 if terminal["state"]!="complete":raise RuntimeError("incomplete full cell")
 return terminal
qualified=json.loads((A/"qualification-result.json").read_text());assert qualified["qualified"]
results=[]
for ds in["proofnet","minif2f"]:
 with gzip.open(A.parent/("prefix-opportunity/"+ds+"-input.jsonl.gz"),"rt")as f:items=[json.loads(l)for l in f]
 assert len(items)==(5952 if ds=="proofnet" else 7808)
 for mode in["stock","native","direct"]:results.append(run(ds,mode,items))
(F/"terminal.json").write_text(json.dumps({"state":"complete","cells":results},indent=2)+"\n")
