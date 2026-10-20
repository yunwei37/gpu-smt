"""Actual source-native capture interrupted by output-ENOSPC, without filling a volume."""
from pathlib import Path
from types import SimpleNamespace
import asyncio,json,os,resource,runpy,sys,time
P=Path(__file__).resolve().parents[3]
R=Path(__file__).resolve().parent
K=Path("/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d")
sys.path[:0]=[str(K),str(K/"client")]
os.sched_setaffinity(0,{8,9,10,11})
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.environ["GPU_SMT_MEMORY_ROOT_PID"]=str(os.getpid())
capture=runpy.run_path(str(P/"bench/lean-native/linarith-oracle/kimina-http.py"))
method=sys.argv[1]
out=Path(sys.argv[2])if len(sys.argv)>2 else R/("real-ENOSPC-"+method)
original_sample=capture["_memory"].MemoryWatchdog.sample
trigger={}
def sample(self,stream):
 original_sample(self,stream)
 http=self.out/"http.jsonl"
 if not trigger and http.exists():
  real=[]
  for line in http.read_text().splitlines():
   row=json.loads(line)
   if row.get("event")=="request":
    payload=json.loads(row.get("body","{}"))
    real.extend(s["id"]for s in payload.get("snippets",[])if not s["id"].startswith("warm-"))
  if real and self.peak_repls:
   trigger.update(source_IDs=real,time_ns=time.monotonic_ns(),actual_live_REPL_peak=self.peak_repls)
   (self.out/"memory-watchdog-error.txt").symlink_to("/dev/full")
   with open("/dev/full","wb")as full:
    full.write(b"actual ENOSPC probe")
    full.flush()
capture["_memory"].MemoryWatchdog.sample=sample
builddir=Path("/tmp/gpu-smt-linarith-oracle-20261017/portable-source-build")
build=json.loads((builddir/"build.json").read_text())
items=[json.loads(s)for s in(P/"artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl").open()][:2]
args=SimpleNamespace(kimina=K,build=builddir,build_source=P/"bench/lean-native/linarith-oracle/reproduction",
 repl=Path("/tmp/gpu-smt-goedel427-20261014/repl-kimina-native-gc-header-repair/.lake/build/bin/repl"),
 reference=P/"artifacts/lean-modern-native-compilation-2026-10-14/farkas-external-support",
 support_python=Path("/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python"),
 native_engine="hybrid",concurrency=2,total_memory_gib=48,per_repl_gib=24,watchdog_test_threshold_bytes=0,skip_warm=False)
async def main():
 try:
  await capture["cell"](args,method,out,items,build)
 except asyncio.CancelledError:
  stopped=time.monotonic_ns()
  terminal=json.loads((out/"terminal.json").read_text())
  assert trigger and terminal["state"]=="monitoring_failed"
  assert "No space left on device"in terminal["memory_watchdog"]["error"]
  assert terminal["memory_watchdog"]["peak_sampled_native_repl_count"]<=2
  import psutil
  remaining=[{"pid":x.pid,"birth":x.create_time(),"name":x.name()}for x in psutil.Process().children(recursive=True)if x.is_running()and x.status()!=psutil.STATUS_ZOMBIE]
  assert not remaining,remaining
  receipt=dict(method=method,trigger=trigger,elapsed_from_injection_to_capture_exit_seconds=(stopped-trigger["time_ns"])/1e9,
   state=terminal["state"],own_live_descendants_after=[],source_membership="Original selected source IDs; no synthetic Lean proof",scope="Real REPL/native body request plus real /dev/full sample/error-record failures. Operational repair qualification only, not completed proof/latency measurement.")
  (out/"fault-result.json").write_text(json.dumps(receipt,indent=2)+"\n")
  print(json.dumps(receipt),flush=True)
 else:raise AssertionError("capture did not abort")
asyncio.run(main())
