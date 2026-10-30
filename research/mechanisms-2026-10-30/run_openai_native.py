"""Bounded Lean4.34.1 native point; no legacy ABI preload or external signal."""
from pathlib import Path
import os,subprocess,json,time,signal,resource,argparse
from run_finite import persistent_capture_path,owned_tree
HERE=Path(__file__).resolve().parent
ROOT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30")
SDK=Path("/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux")
def run(source,label,seconds=35,jobs=1,extra_env=None,as_main=False):
    out=persistent_capture_path(ROOT/"openai-native"/label);out.mkdir(parents=True,exist_ok=False)
    (out/"source.lean").write_bytes(source.read_bytes())
    (out/"runner.py").write_bytes(Path(__file__).read_bytes())
    paths=Path("/workspaces/.agent-state/gpu-smt-captures/workloads/mathlib4341-setup/LEAN_PATH.txt").read_text().strip()
    oai="/workspaces/.agent-state/gpu-smt-workloads/openai4341-oleans"
    env=os.environ.copy();env.pop("LD_PRELOAD",None)
    env.update(LEAN_SYSROOT=str(SDK),LEAN_PATH=oai+":"+paths,LEAN_NUM_THREADS=str(jobs))
    env.update(extra_env or {})
    args=["taskset","-c","8,9,10,11,12,13,14,15",str(SDK/"bin/lean"),f"-j{jobs}","-M8192"]
    if as_main:args+=["--run"]
    args += [str(out/"source.lean")]
    def own_alarm():
        signal.signal(signal.SIGALRM,signal.SIG_DFL)
        signal.setitimer(signal.ITIMER_REAL,seconds)
    start=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN)
    with (out/"stdout.txt").open("w") as so,(out/"stderr.txt").open("w") as se:
        q=subprocess.Popen(args,env=env,stdout=so,stderr=se,preexec_fn=own_alarm)
        birth=Path(f"/proc/{q.pid}/stat").read_text().split()[21]
        launch={"pid":q.pid,"birth":birth,"argv":args,"self_wall_s":seconds,"external_signals":0,
                "memory_native_MiB":8192,"M_own_tree_budget_GiB":16,"jobs":jobs,"point":"phobos-vt Lean4.34.1 locked openai/math",
                "boot_id":Path("/proc/sys/kernel/random/boot_id").read_text().strip()}
        (out/"launch.json").write_text(json.dumps(launch,indent=2)+"\n")
        peak=0;over=False
        with (out/"memory.jsonl").open("w") as mem:
            while True:
                tree=owned_tree();rss=sum(x["rss_bytes"] for x in tree);peak=max(peak,rss);over|=rss>16*1024**3
                mem.write(json.dumps({"s":time.monotonic()-start,"rss_bytes":rss,"owned":tree})+"\n");mem.flush()
                try:code=q.wait(timeout=1);break
                except subprocess.TimeoutExpired:pass
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    receipt={"exit":code,"wall_s":time.monotonic()-start,
        "cpu_s":after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
        "sampled_peak_owned_tree_RSS_bytes":peak,"sampled_budget_violation":over,
        "retired":not Path(f"/proc/{q.pid}").exists(),"self_wall_s":seconds,"jobs":jobs,
        "limits":"single finite SDK process; native -M is cooperative, parent sampling not hard RSS enforcement; self alarm no external signals"}
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("M_OPENAI_RUN",label,json.dumps(receipt),flush=True)
    return out,receipt
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("label");p.add_argument("--seconds",type=int,default=35)
    a=p.parse_args();run(a.source,a.label,a.seconds)
