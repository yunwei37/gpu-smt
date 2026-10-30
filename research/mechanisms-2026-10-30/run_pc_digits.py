"""Finite stock/off/on sampling of the existing ordinary-kernel declaration recheck."""
import os,json,re,subprocess
from pathlib import Path
from run_finite import persistent_capture_path
from run_pc_qualification import EXT,HERE,alive
from analyze_pc_samples import analyze

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--point",choices=["pc-digits","pc-digits-pure-timing"],default="pc-digits")
    point=parser.parse_args().point
    if not json.loads((EXT/"pc-qualification/terminal.json").read_text())["native_controls_qualified"]:
        raise SystemExit("Short native sampler control did not qualify")
    previous=json.loads((EXT/"pc-representatives/cells.json").read_text())
    if any(alive(c["receipt"]) for c in previous):
        raise SystemExit("Previous representative native still active")
    out=persistent_capture_path(EXT/point);out.mkdir(exist_ok=False)
    env=dict(os.environ,M_OWNERSHIP_ROOT_PID=str(os.getpid()),
             M_OWNERSHIP_ROOT_BIRTH=Path(f"/proc/{os.getpid()}/stat").read_text().split()[21])
    base=EXT/"generated/software-probe-timing/software-probe.so"
    sampler=EXT/"generated/late-pc-sampler-v2/pc-sampler.so"
    records=[];canonical=[]
    for mode in ["stock","library-off","sampler-on"]:
        label=point+"-"+mode;capture=EXT/"captures"/label
        native_env=env.copy();native_env.pop("M_LATE_PC_FILE",None)
        libs=str(base)
        if mode!="stock":libs+=":"+str(sampler)
        if mode=="sampler-on":native_env["M_LATE_PC_FILE"]=str(capture/"samples.bin")
        args=["taskset","-c","12,13","python3","-u",str(HERE/"run_finite.py"),
              str(HERE/"PCDigitsCertificate.lean"),label,"--wall-seconds","180","--library",libs]
        with (out/(mode+".stdout")).open("x") as stdout,(out/(mode+".stderr")).open("x") as stderr:
            result=subprocess.run(args,env=native_env,stdout=stdout,stderr=stderr)
        receipt=json.loads((capture/"receipt.json").read_text())
        if alive(receipt):raise RuntimeError("Native process survived")
        text=(capture/"stdout.txt").read_text()
        hbs=re.findall(r"M_KERNEL_RECHECK_HB=([0-9]+)",text)
        ns=re.findall(r"M_KERNEL_RECHECK_NS=([0-9]+)",text)
        canon=[line for line in text.splitlines() if not line.startswith(("M_KERNEL_RECHECK_NS=","M_KERNEL_RECHECK_HB="))]
        record={"mode":mode,"client_exit":result.returncode,"receipt":receipt,
                "recheck_raw_HB":int(hbs[0]) if len(hbs)==1 else None,
                "recheck_wall_ns":int(ns[0]) if len(ns)==1 else None,
                "canonical_stdout":canon}
        records.append(record);canonical.append(canon)
        (out/"cells.json").write_text(json.dumps(records,indent=2)+chr(10))
        if result.returncode or len(hbs)!=1 or len(ns)!=1:
            raise SystemExit("Preserve failed closed-computation control")
    if any("sorryAx" in "\n".join(c) for c in canonical):raise ValueError("Sorry axiom found")
    summary={"cells":records,"same_non_timing_stdout":all(c==canonical[0] for c in canonical),
             "same_recheck_raw_HB":len({r["recheck_raw_HB"]for r in records})==1,
             "all_native_retired":True,"software_samples":analyze(EXT/"captures"/(point+"-sampler-on")/"samples.bin"),
             "limits":["Actual computed_count ordinary-kernel recheck,not a generic extraction engine.",
                       "C/libc samples and out-of-line categories are not PMU cycle or complete allocation fractions.",
                       "New software-sampled runs have their own timing denominators; previous certificate run remains intact."]}
    (out/"terminal.json").write_text(json.dumps(summary,indent=2)+chr(10))
    (HERE/(point+"-result.json")).write_text(json.dumps(summary,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in summary.items() if k!="software_samples"},indent=2))
if __name__=="__main__":main()
