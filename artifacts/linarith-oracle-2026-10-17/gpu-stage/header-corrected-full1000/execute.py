import pathlib,subprocess,json,time,os,resource,gzip,shutil
r=pathlib.Path("/workspaces/repository")
q=pathlib.Path("/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle")
a=r/"artifacts/linarith-oracle-2026-10-17/gpu-stage/header-corrected-full1000"
py="/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python"
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{12,13,14,15})
results=[]
for i,methods in enumerate([["fast-hybrid","oracle"],["oracle","fast-hybrid"],["fast-hybrid","oracle"]],1):
 out=q/("header-corrected-full1000-pair"+str(i))
 argv=[py,str(r/"bench/lean-native/linarith-oracle/run-batch.py"),"--out",str(out),"--methods",*methods,"--affinity","12","13","14","15"]
 dest=a/("pair"+str(i));dest.mkdir(exist_ok=True)
 with (q/("header-corrected-full1000-pair"+str(i)+".log")).open("w")as log:
  proc=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT)
  receipt={"utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"pid":proc.pid,"start_ticks":pathlib.Path("/proc",str(proc.pid),"stat").read_text().split()[21],"argv":argv,"RLIMIT_AS":51539607552,"order":methods}
  (dest/"launch.json").write_text(json.dumps(receipt,indent=2)+"\n");print(json.dumps(receipt),flush=True)
  code=proc.wait()
 if code:raise RuntimeError("actual pair collector fault: "+str(code))
 with (dest/"analysis.log").open("w")as log:
  subprocess.run([py,str(r/"bench/lean-native/linarith-oracle/analyze-batch.py"),str(out),"--methods","fast-hybrid","oracle"],stdout=log,stderr=subprocess.STDOUT,check=True)
 for p in out.rglob("*"):
  if p.is_file():
   target=dest/p.relative_to(out);target.parent.mkdir(exist_ok=True,parents=True)
   if p.suffix==".jsonl":target.with_name(target.name+".gz").write_bytes(gzip.compress(p.read_bytes(),mtime=0))
   else:shutil.copy2(p,target)
 data=json.loads((dest/"paired-analysis.json").read_text())
 results.append({"pair":i,"methods":{n:{"whole_seconds":v["whole_seconds"],"counts":v["counts"],"outcome_differences":v["outcome_differences"],"full_native_JSON_differences":v["full_native_JSON_differences"],"non_message_differences":v["non_message_differences"]}for n,v in data["methods"].items()}})
 (a/"completed-pairs.json").write_text(json.dumps(results,indent=2)+"\n")
 print("PAIR_CLOSED "+json.dumps(results[-1]),flush=True)
aggregate={"pairs":len(results),"native_seconds":sum(v["methods"]["fast-hybrid"]["whole_seconds"]for v in results),"oracle_seconds":sum(v["methods"]["oracle"]["whole_seconds"]for v in results)}
aggregate["ratio"]=aggregate["native_seconds"]/aggregate["oracle_seconds"]
(a/"aggregate.json").write_text(json.dumps(aggregate,indent=2)+"\n")
print("ALL_PAIRS_CLOSED "+json.dumps(aggregate),flush=True)
