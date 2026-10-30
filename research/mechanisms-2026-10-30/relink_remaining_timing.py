"""Relink the matching prebuilt Lean SDK; no Lean/Mathlib source build."""
from pathlib import Path
import subprocess,os,time,json,resource
HERE=Path(__file__).resolve().parent
SDK=Path("/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux")
OUT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/generated/remaining-wrapped-cli-v1")
SOURCE=Path("/workspaces/.agent-state/gpu-smt-deps/lean49-owned-runtime/lean4-be6c4894e0a6/src/shell/lean.cpp")
def owned_rss():
    table={}
    for d in Path("/proc").iterdir():
        if not d.name.isdigit():continue
        try:
            text=(d/"stat").read_text();fields=text[text.rfind(")")+2:].split()
            parent=int(fields[1]);birth=fields[19]
            rss=int(next(x.split()[1] for x in (d/"status").read_text().splitlines() if x.startswith("VmRSS:")))*1024
            table[int(d.name)]=(parent,birth,rss)
        except (OSError,ValueError,StopIteration):continue
    ids={os.getpid()}
    while True:
        more={i for i,(parent,_,_) in table.items() if parent in ids}
        if more<=ids:break
        ids|=more
    return [{"pid":i,"start_ticks":table[i][1],"rss_bytes":table[i][2]} for i in ids if i in table]
def main():
    OUT.mkdir(parents=True,exist_ok=False)
    commands=[
      [str(SDK/"bin/leanc"),"-c",str(SOURCE),"-o",str(OUT/"main.o")],
      ["gcc","-std=c11","-fPIC","-I"+str(SDK/"include"),"-c",str(HERE/"software_probe.c"),"-O2","-o",str(OUT/"probe.o")],
      ["gcc","-std=c11","-fPIC","-I"+str(SDK/"include"),"-c",str(HERE/"remaining_timing.c"),"-O2","-DM_PROFILE_STATIC_WRAP","-o",str(OUT/"timing.o")],
      [str(SDK/"bin/leanc"),str(OUT/"main.o"),str(OUT/"probe.o"),str(OUT/"timing.o"),
       "-Wl,--whole-archive","-lLean","-lInit","-lleancpp","-lleanrt","-Wl,--no-whole-archive",
       "-Wl,--wrap=lean_profileit","-Wl,--export-dynamic","-o",str(OUT/"lean")]]
    receipts=[]
    with (OUT/"memory.jsonl").open("w") as mem:
      for i,command in enumerate(commands):
        started=time.monotonic();peak=0;usage0=resource.getrusage(resource.RUSAGE_CHILDREN)
        with (OUT/f"step-{i}.log").open("w") as log:
          child=subprocess.Popen(["taskset","-c","8,9"]+command,stdout=log,stderr=subprocess.STDOUT)
          while child.poll() is None:
            ps=owned_rss();rss=sum(p["rss_bytes"] for p in ps);peak=max(peak,rss)
            mem.write(json.dumps({"step":i,"elapsed_s":time.monotonic()-started,"owned_rss_bytes":rss,"processes":ps})+"\n");mem.flush()
            try:child.wait(timeout=1)
            except subprocess.TimeoutExpired:pass
          status=child.wait()
        usage=resource.getrusage(resource.RUSAGE_CHILDREN)
        result={"argv":command,"exit_code":status,"wall_s":time.monotonic()-started,
          "sampled_peak_owned_RSS_bytes":peak,"cumulative_kernel_child_peak_bytes":usage.ru_maxrss*1024,
          "CPU_seconds":usage.ru_utime+usage.ru_stime-usage0.ru_utime-usage0.ru_stime}
        receipts.append(result);print(json.dumps(result),flush=True)
        (OUT/"receipt.json").write_text(json.dumps(receipts,indent=2))
        if status:
            print((OUT/f"step-{i}.log").read_text()[-6000:],flush=True);return status
    return 0
if __name__=="__main__":raise SystemExit(main())
