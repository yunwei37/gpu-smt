"""Finite official Kimina HTTP/SDK arithmetic comparison; no upstream patch."""
import argparse, asyncio, collections, json, os, resource, socket, subprocess, sys, time, traceback, tempfile
from pathlib import Path
import psutil

async def cell(args, method, out, items, build):
    from kimina_client import AsyncKiminaClient, Snippet
    from server.split import split_snippet
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic_ns()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    env = dict(os.environ)
    for key in ["GPU_ARITHMETIC_ORACLE", "GPU_ARITHMETIC_PROFILE", "GPU_ARITHMETIC_BASELINE",
                "GPU_ARITHMETIC_STRONG_PROFILE", "FARKAS_CORPUS_FILE", "FARKAS_COST_FILE",
                "GPU_ARITHMETIC_NUMERIC_PHASE_LOG", "GPU_ARITHMETIC_RACE_CPU_ONLY",
                "GPU_ARITHMETIC_STRONG_CPU_SOCKET", "GPU_SMT_CANDIDATE_TIMING"]:
        env.pop(key, None)
    env.update(PATH=str(Path(build["sdk"])/"bin")+os.pathsep+env["PATH"],
        LEAN_PATH=build["lean_path"], LEAN_SRC_PATH=build["lean_src_path"],
        LD_LIBRARY_PATH=os.pathsep.join(build["library_paths"]+[env.get("LD_LIBRARY_PATH","")]),
        LEAN_SERVER_NATIVE_DYNLIB=str(args.build/"native-load.txt"),
        LEAN_SERVER_PROJECT_DIR=build["mathlib"], LEAN_SERVER_REPL_PATH=str(args.repl),
        LEAN_SERVER_LEAN_VERSION="v4.27.0", LEAN_SERVER_MAX_REPL_MEM="48G",
        LEAN_SERVER_HOST="127.0.0.1", FARKAS_NATIVE_BIN=str(args.reference))
    original = "import Mathlib\nimport Aesop\n"
    target = {"stock":"", "native":"GpuArithmetic.IntegerCostControl",
              "power":"GpuArithmetic.IntegerPowerOracle"}[method]
    snippets=[]
    for row in items:
        code=row["code"]; assert code.startswith(original)
        if target: code=original+"import "+target+"\n"+code[len(original):]
        snippets.append(Snippet(id=row["proof_id"],code=code))
    headers={split_snippet(s.code).header for s in snippets}; assert len(headers)==1
    header=next(iter(headers))
    if method!="stock":
        env.update(FARKAS_EXTERNAL_CPU_HYBRID="1", GPU_ARITHMETIC_STRONG_PROFILE="1",
                   GPU_SMT_NATIVE_OMEGA_CONTROL="1")
    if method=="power":
        env.update(FARKAS_NATIVE_BIN=str(args.build/"farkas-batchd"),
            GPU_ARITHMETIC_BATCH="1", GPU_ARITHMETIC_ORACLE=str(args.build/"arithmetic-batchd"),
            GPU_ARITHMETIC_RACE_WORKER=str(args.build/"farkas-race-worker"),
            GPU_ARITHMETIC_RACE_MIN_ROWS="11", GPU_ARITHMETIC_NEGATIVE_CERTIFICATES="1",
            GPU_ARITHMETIC_RACE_LOG=str(out/"lp-races.jsonl"))
    with socket.socket() as address:
        address.bind(("127.0.0.1",0)); port=address.getsockname()[1]
    env["LEAN_SERVER_PORT"]=str(port)
    events=(out/"http.jsonl").open("w")
    def record(row):
        events.write(json.dumps(row,ensure_ascii=False,separators=(",",":"))+"\n"); events.flush()
    backend=server=client=None; streams=[]; owned=[]; owned_processes=[]
    result=dict(state="failed",method=method,expected=len(items),
        affinity=sorted(os.sched_getaffinity(0)),memory_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],
        scope="Official Kimina HTTP/SDK replay; same adapted4.27REPL/native closure; CPU-only, root self-review.")
    try:
        if method=="power":
            socket_dir=tempfile.TemporaryDirectory(prefix="kimina-oracle-")
            env["GPU_ARITHMETIC_SUPPORT_SOCKET"]=str(Path(socket_dir.name)/"support.sock")
            errors=(out/"support-stderr.log").open("w"); streams.append(errors)
            command=[str(args.support_python),str(args.build_source/"support-proxy.py"),
                "--backend","highs","--negative-certificates","--socket",env["GPU_ARITHMETIC_SUPPORT_SOCKET"],
                "--log",str(out/"support-calls.jsonl.gz")]
            backend=subprocess.Popen(command,env=env,stdout=subprocess.PIPE,stderr=errors,text=True)
            ready=backend.stdout.readline(); (out/"support-start.json").write_text(ready)
            if not ready or not json.loads(ready).get("ready"): raise RuntimeError("CPU support startup failed")
        logs=(out/"server.log").open("w"); streams.append(logs)
        server=subprocess.Popen([sys.executable,"-m","server"],cwd=args.kimina,env=env,
            stdout=logs,stderr=subprocess.STDOUT,start_new_session=True)
        import httpx
        async with httpx.AsyncClient() as health:
            while True:
                if server.poll() is not None: raise RuntimeError("Kimina exited during startup")
                try:
                    reply=await health.get("http://127.0.0.1:"+str(port)+"/health")
                    if reply.status_code==200: break
                except httpx.ConnectError: pass
                await asyncio.sleep(.1)
        ready_ns=time.monotonic_ns()
        client=AsyncKiminaClient(api_url="http://127.0.0.1:"+str(port))
        async def on_request(request):
            request.extensions["benchmark_start"]=time.monotonic_ns()
            record(dict(event="request",start_ns=request.extensions["benchmark_start"],
                        body=request.content.decode()))
        async def on_response(response):
            await response.aread()
            record(dict(event="response",start_ns=response.request.extensions["benchmark_start"],
                end_ns=time.monotonic_ns(),status=response.status_code,
                request=response.request.content.decode(),body=response.content.decode()))
        client.session.event_hooks={"request":[on_request],"response":[on_response]}
        warm=await client.check([Snippet(id="warm-"+str(i),code=header+"\n#check Nat")for i in range(8)],
            timeout=300,batch_size=1,max_workers=8,reuse=True,show_progress=False)
        if any(x.analyze().status.value!="valid"for x in warm.results): raise RuntimeError("Warm preparation failed")
        verify_start=time.monotonic_ns()
        replies=await client.check(snippets,timeout=300,batch_size=1,max_workers=8,reuse=True,show_progress=False)
        verify_end=time.monotonic_ns()
        rows=[dict(proof_id=x.id,status=x.analyze().status.value,result=x.model_dump(exclude_none=True))for x in replies.results]
        assert len(rows)==len(items)and[x["proof_id"]for x in rows]==[x["proof_id"]for x in items]
        with(out/"results.jsonl").open("w")as f:
            for row in rows: f.write(json.dumps(row,ensure_ascii=False)+"\n")
        result.update(state="complete",returned=len(rows),counts=dict(collections.Counter(x["status"]for x in rows)),
            server_ready_seconds=(ready_ns-start)/1e9,preparation_seconds=(verify_start-start)/1e9,
            warm_verify_seconds=(verify_end-verify_start)/1e9)
    except Exception:
        result["error"]=traceback.format_exc()
    finally:
        if client is not None: await client.close()
        if server is not None:
            try:
                for proc in psutil.Process(server.pid).children(recursive=True):
                    row=dict(pid=proc.pid,birth=proc.create_time(),command=proc.cmdline()[:2])
                    try:
                        row["cpu_affinity"]=proc.cpu_affinity()
                        row["address_limit"]=[s for s in Path("/proc",str(proc.pid),"limits").read_text().splitlines()if s.startswith("Max address space")]
                    except (OSError,psutil.Error): pass
                    owned.append(row); owned_processes.append(proc)
            except psutil.Error: pass
            if server.poll() is None: server.terminate()
            result["server_exit"]=await asyncio.to_thread(server.wait)
            # The application posts asynchronous worker-close tasks. Join their
            # actual processes before the cold lifecycle clock ends.
            # Reuse this capture family's300s finalization allowance.
            gone, pending=await asyncio.to_thread(psutil.wait_procs,owned_processes,timeout=300)
            result["joined_owned_descendants"]=len(gone)
            remaining=[]
            for row in owned:
                try:
                    proc=psutil.Process(row["pid"])
                    if proc.create_time()==row["birth"]and proc.status()!=psutil.STATUS_ZOMBIE:
                        remaining.append(dict(row,status=proc.status()))
                except psutil.Error: pass
            result["owned_descendants_before_shutdown"]=owned
            result["owned_live_descendants_after_shutdown"]=remaining
            if remaining:
                result["state"]="retirement_incomplete"
        if backend is not None:
            if backend.poll() is None: backend.terminate()
            result["backend_exit"]=await asyncio.to_thread(backend.wait)
            backend.stdout.close(); socket_dir.cleanup()
        for stream in streams: stream.close()
        events.close()
        finish=time.monotonic_ns()
        result["whole_lifecycle_seconds"]=(finish-start)/1e9
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        result["waited_child_cpu_seconds"]=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime
        result["cpu_scope"]="Not validated exhaustive descendant CPU; no pure solver attribution."
        result["effective_test_settings"]={k:env[k]for k in["LEAN_SERVER_PROJECT_DIR",
            "LEAN_SERVER_REPL_PATH","LEAN_SERVER_LEAN_VERSION","LEAN_SERVER_MAX_REPL_MEM",
            "LEAN_SERVER_HOST","LEAN_SERVER_PORT","LEAN_SERVER_NATIVE_DYNLIB"]}
        (out/"terminal.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items()if k not in[
        "effective_test_settings","owned_descendants_before_shutdown"]}),flush=True)
    return result

async def main(args):
    build=json.loads((args.build/"build.json").read_text())
    items=[json.loads(s)for s in args.input.open()if s.strip()]
    if args.limit: items=items[:args.limit]
    assert len({x["proof_id"]for x in items})==len(items)
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/"source-ids.json").write_text(json.dumps([x["proof_id"]for x in items])+"\n")
    for rep in range(args.repetitions):
        methods=args.methods[rep%len(args.methods):]+args.methods[:rep%len(args.methods)]
        for method in methods:
            result=await cell(args,method,args.out/("rep"+str(rep+1)+"-"+method),items,build)
            if result["state"]!="complete": return 1
    return 0

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    for name in["kimina","build","build-source","repl","reference","support-python","input","out"]:
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--limit",type=int,default=0)
    parser.add_argument("--repetitions",type=int,default=1)
    parser.add_argument("--methods",nargs="+",choices=["stock","native","power"],default=["stock","native","power"])
    args=parser.parse_args()
    for name in["kimina","build","build_source","repl","reference","support_python","input","out"]:
        setattr(args,name,getattr(args,name).resolve())
    os.sched_setaffinity(0,{20,21,22,23})
    resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    sys.path.insert(0,str(args.kimina)); sys.path.insert(0,str(args.kimina/"client"))
    raise SystemExit(asyncio.run(main(args)))
