"""One finite serial PC-sampling qualification after the active C matrix retires."""
import json, os, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
EXT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30")

def alive(receipt):
    p=Path("/proc")/str(receipt["pid"])/"stat"
    try:return p.read_text().split()[21]==receipt["start_ticks"]
    except OSError:return False

def main():
    terminal=EXT/"native-cohort-matrix/terminal.json"
    if not terminal.exists():raise SystemExit("Current C cohort not terminal; no second Lean process started")
    matrix=json.loads(terminal.read_text())
    for c in matrix["cells"]:
        receipt=json.loads((Path(c["raw_capture"])/"receipt.json").read_text())
        if alive(receipt):raise SystemExit("Previous native process still alive")
    out=EXT/"pc-qualification";out.mkdir(exist_ok=False)
    env=dict(os.environ,M_OWNERSHIP_ROOT_PID=str(os.getpid()),
             M_OWNERSHIP_ROOT_BIRTH=Path(f"/proc/{os.getpid()}/stat").read_text().split()[21])
    base=EXT/"generated/software-probe-timing/software-probe.so"
    sampler=EXT/"generated/late-pc-sampler-v2/pc-sampler.so"
    records=[]
    for mode in ["stock","library-off","sampler-on"]:
        label="pc-native-qualification-"+mode
        capture=EXT/"captures"/label
        native_env=env.copy();native_env.pop("M_LATE_PC_FILE",None)
        libs=str(base)
        if mode!="stock":libs+=":"+str(sampler)
        if mode=="sampler-on":native_env["M_LATE_PC_FILE"]=str(capture/"samples.bin")
        args=["taskset","-c","12,13","python3","-u",str(HERE/"run_finite.py"),
              str(HERE/"PCMeasureControls.lean"),label,"--wall-seconds","60",
              "--library",libs,"--input",str(HERE/"cold-timing-control.json")]
        with (out/(mode+".stdout")).open("x") as stdout,(out/(mode+".stderr")).open("x") as stderr:
            result=subprocess.run(args,env=native_env,stdout=stdout,stderr=stderr)
        receipt=json.loads((capture/"receipt.json").read_text())
        if alive(receipt):raise RuntimeError("Native process survived")
        record={"mode":mode,"client_exit":result.returncode,"receipt":receipt}
        records.append(record)
        (out/"cells.json").write_text(json.dumps(records,indent=2)+chr(10))
        if result.returncode:raise SystemExit("Preserve failed qualifier; do not continue sampling")
    from analyze_c_timing import read_rows
    from analyze_pc_samples import analyze
    rows={r["mode"]:read_rows(EXT/"captures"/("pc-native-qualification-"+r["mode"])/"stdout.txt")
          for r in records}
    for mode,r in rows.items():
        if len(r)!=4:raise ValueError("Wrong qualifier return count")
    differences=[]
    for comparator in ["library-off","sampler-on"]:
        for a,b in zip(rows["stock"],rows[comparator]):
            if a["id"]!=b["id"]:raise ValueError("Source mismatch")
            fields=[k for k in ["hasErrors","errors","infos","allocatedHeartbeatDelta"] if a[k]!=b[k]]
            if fields:differences.append({"id":a["id"],"mode":comparator,"fields":fields})
    pc=analyze(EXT/"captures/pc-native-qualification-sampler-on/samples.bin")
    summary={"sources":4,"returns":12,"differences":differences,
             "sampler_engaged":pc["samples_retained"]>0,"raw":str(out),
             "all_native_retired":True,"native_controls_qualified":not differences and pc["samples_retained"]>0,
             "limits":"Small diagnostic controls only; not full7808 acceptance or measured speedup.",
             "software_samples":pc}
    (out/"terminal.json").write_text(json.dumps(summary,indent=2)+chr(10))
    (HERE/"pc-native-qualification.json").write_text(json.dumps(summary,indent=2)+chr(10))
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
