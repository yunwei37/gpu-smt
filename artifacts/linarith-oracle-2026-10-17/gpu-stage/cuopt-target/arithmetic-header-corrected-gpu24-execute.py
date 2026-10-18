import os,sys,json,time,pathlib,subprocess,resource,grpc
q=pathlib.Path("/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle")
a=pathlib.Path("/workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target")
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.sched_setaffinity(0,{0,1,2,3})
host=sys.argv[1]
channel=grpc.insecure_channel(host+":5001")
grpc.channel_ready_future(channel).result(timeout=60)
channel.close()
env=os.environ.copy();env["GPU_SMT_CUOPT_HOST"]=host
cmd=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python","/workspaces/repository/bench/lean-native/linarith-oracle/run-batch.py","--out",str(q/"header-clean-gpu24"),"--input",str(q/"direct-feasibility-native24-input.jsonl"),"--methods","oracle-gpu","--affinity","0","1","2","3","--reuse-reference",str(q/"header-clean24/rep1-fast-hybrid")]
start=time.monotonic_ns()
with (q/"header-clean-gpu24.log").open("w") as log:
 p=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env)
 receipt={"utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"pid":p.pid,"start_ticks":pathlib.Path("/proc",str(p.pid),"stat").read_text().split()[21],"argv":cmd,"host":host,"RLIMIT_AS":51539607552,"scope":"real24sources, corrected arithmetic import family, phase-I PDLP/crossover plus owner cancellation, no numerical warmup"}
 (a/"arithmetic-header-corrected-gpu24-launch.json").write_text(json.dumps(receipt,indent=2)+"\n")
 print(json.dumps(receipt),flush=True)
 code=p.wait()
result={"exit":code,"wrapper_whole_ns":time.monotonic_ns()-start,"utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
(a/"arithmetic-header-corrected-gpu24-return.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result),flush=True)
sys.exit(code)
