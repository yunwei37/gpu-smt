"""Finite matched official-service arithmetic capture at the user resource point."""
from pathlib import Path
import argparse,asyncio,collections,datetime,gzip,json,os,resource,runpy,shutil,time
from types import SimpleNamespace
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17"
O=Path(__file__).resolve().parent
K=Path("/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d")
parser=argparse.ArgumentParser()
parser.add_argument("--stage",choices=["preflight","full"],required=True)
stage=parser.parse_args().stage
os.sched_setaffinity(0,{8,9,10,11})
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.environ["GPU_SMT_MEMORY_ROOT_PID"]=str(os.getpid())
import sys
sys.path[:0]=[str(K),str(K/"client")]
capture=runpy.run_path(str(R/"bench/lean-native/linarith-oracle/kimina-http.py"))
def event(**values):
 print(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**values)),flush=True)
def archive_closed(directory):
 receipt=[]
 for source in list(directory.iterdir()):
  if not source.is_file()or source.suffix not in[".jsonl",".log"]:continue
  target=source.with_name(source.name+".gz")
  assert not target.exists()
  with source.open("rb")as inp,gzip.open(target,"wb",compresslevel=1)as out:shutil.copyfileobj(inp,out)
  with source.open("rb")as inp,gzip.open(target,"rb")as out:
   while True:
    chunk=inp.read(1024*1024)
    assert chunk==out.read(1024*1024)
    if not chunk:break
  receipt.append(dict(source=source.name,archive=target.name,raw_bytes=source.stat().st_size,
   archive_bytes=target.stat().st_size,byte_equal_roundtrip=True))
  source.unlink()
 (directory/"raw-archive.json").write_text(json.dumps(dict(scope="Closed lifecycle only; byte-equal lossless archival outside method clocks.",files=receipt),indent=2)+"\n")
input_start=time.monotonic_ns()
source=R/"artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl"
items=[json.loads(line)for line in source.open()]
assert len(items)==29750 and len({x["proof_id"]for x in items})==29750
if stage=="preflight":
 byid={x["proof_id"]:x for x in items}
 selected=[json.loads(x)for x in(A/"input-top1000.jsonl").open()][:24]
 assert len(selected)==24 and all(x["code"]==byid[x["proof_id"]]["code"]for x in selected)
 items=selected
builddir=Path("/tmp/gpu-smt-linarith-oracle-20261017/portable-source-build")
build=json.loads((builddir/"build.json").read_text())
out=O/stage;out.mkdir(exist_ok=False)
(out/"input-materialization.json").write_text(json.dumps(dict(
 elapsed_seconds=(time.monotonic_ns()-input_start)/1e9,original_source_bytes=source.stat().st_size,
 selected_sources=len(items),scope="Shared read of released replay data and build metadata, outside individual method lifecycle. Snippet construction/imports and all method-specific preparation are inside each capture clock."),indent=2)+"\n")
(out/"source-ids.json").write_text(json.dumps([x["proof_id"]for x in items])+"\n")
with gzip.open(out/"original-input.jsonl.gz","wt",compresslevel=1)as stream:
 for x in items:stream.write(json.dumps(x,ensure_ascii=False)+"\n")
args=SimpleNamespace(kimina=K,build=builddir,build_source=R/"bench/lean-native/linarith-oracle/reproduction",
 repl=Path("/tmp/gpu-smt-goedel427-20261014/repl-kimina-native-gc-header-repair/.lake/build/bin/repl"),
 reference=R/"artifacts/lean-modern-native-compilation-2026-10-14/farkas-external-support",
 support_python=Path("/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python"),
 native_engine="hybrid",concurrency=2,total_memory_gib=48,per_repl_gib=24,
 watchdog_test_threshold_bytes=0,skip_warm=False)
async def main():
 results=[]
 for rep in range(1 if stage=="preflight" else 3):
  for method in(["native","power"]if rep%2==0 else["power","native"]):
   directory=out/("rep"+str(rep+1)+"-"+method)
   event(event="cell_start",stage=stage,method=method,rep=rep+1,sources=len(items),
    free_bytes=shutil.disk_usage(R).free)
   terminal=await capture["cell"](args,method,directory,items,build)
   results.append(terminal)
   assert terminal["state"]=="complete" and terminal["returned"]==len(items),terminal
   assert not terminal["owned_live_descendants_after_shutdown"],terminal
   guard=terminal["memory_watchdog"]
   assert guard["error"]is None and guard["peak_sampled_native_repl_count"]<=2
   assert guard["budget_bytes"]==48*1024**3 and guard["effective_threshold_bytes"]==48*1024**3
   event(event="cell_complete",stage=stage,method=method,rep=rep+1,
    whole_lifecycle_seconds=terminal["whole_lifecycle_seconds"],counts=terminal["counts"],
    memory_watchdog=guard)
   archive_closed(directory)
 event(event="stage_complete",stage=stage,cells=len(results))
asyncio.run(main())
