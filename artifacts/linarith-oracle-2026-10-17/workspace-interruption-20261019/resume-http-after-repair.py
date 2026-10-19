from pathlib import Path
import os,sys,resource,runpy,json,asyncio
from types import SimpleNamespace
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17/kimina-http"
old=json.loads((A/"full1000-launch.json").read_text())["command"][3:]
opts={old[i][2:].replace("-","_"):old[i+1]for i in range(0,len(old),2)}
for k in["kimina","build","build_source","repl","reference","support_python","input","out"]:opts[k]=Path(opts[k]).absolute()
opts.update(native_engine="hybrid",affinity=[20,21,22,23])
args=SimpleNamespace(**opts)
os.sched_setaffinity(0,set(args.affinity))
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
sys.path[:0]=[str(args.kimina),str(args.kimina/"client")]
mod=runpy.run_path(str(R/"bench/lean-native/linarith-oracle/kimina-http.py"))
build=json.loads((args.build/"build.json").read_text())
items=[json.loads(s)for s in args.input.open()if s.strip()]
assert len(items)==1000
out=A/"full1000-recovery2-20261019";out.mkdir(exist_ok=False)
async def main():
 for method in["stock","native"]:
  result=await mod["cell"](args,method,out/("rep3-"+method),items,build)
  if result["state"]!="complete" or result.get("counts",{}).get("valid",0)==0:return 1
 return 0
raise SystemExit(asyncio.run(main()))
