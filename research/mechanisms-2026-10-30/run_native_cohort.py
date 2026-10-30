"""Finite serial native/linked-off/linked-on cohort matrix; no daemon or retries."""
from pathlib import Path
import subprocess,os,json,time
HERE=Path(__file__).resolve().parent
ROOT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30")
MATRIX=ROOT/"native-cohort-matrix"
EXE=ROOT/"generated/wrapped-cli-v5/lean"
LIB=ROOT/"generated/software-probe-timing/software-probe.so"
def identity_alive(receipt):
    f=Path("/proc")/str(receipt["pid"])/"stat"
    try:return f.read_text().split()[21]==receipt["start_ticks"]
    except OSError:return False
def native_seconds_left(started, now=None):
    """Honor the user's30minute whole-collection bound across finite cells."""
    remaining=int(1800-((time.monotonic() if now is None else now)-started))-1
    return max(0,min(1500,remaining))

def main():
    import argparse
    global MATRIX
    parser=argparse.ArgumentParser();parser.add_argument("--accepted-original",action="store_true")
    cli=parser.parse_args()
    if cli.accepted_original:MATRIX=ROOT/"accepted-original-matrix"
    shards=[0] if cli.accepted_original else [0,1]
    expected=50 if cli.accepted_original else 100
    prefix="accepted-original" if cli.accepted_original else "native-cohort"
    per_native=300 if cli.accepted_original else 1500
    MATRIX.mkdir(parents=True,exist_ok=True)
    os.environ["M_OWNERSHIP_ROOT_PID"]=str(os.getpid())
    os.environ["M_OWNERSHIP_ROOT_BIRTH"]=Path(f"/proc/{os.getpid()}/stat").read_text().split()[21]
    records=[];started=time.monotonic()
    def finish(state):
        (MATRIX/"terminal.json").write_text(json.dumps({
          "state":state,"elapsed_s":time.monotonic()-started,"whole_group_limit_s":1800,
          "finished_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
          "cells":records},indent=2))
    for shard in shards:
        cells=["stock","linked-off","linked-on"]
        if shard==1:cells.reverse()
        for cell in cells:
            label=f"{prefix}-s{shard}-{cell}"
            out=ROOT/"captures"/label
            if out.exists():
                raise RuntimeError(f"Preserve existing capture instead of rerunning {label}")
            seconds=min(per_native,native_seconds_left(started))
            if not seconds:
                finish("group_deadline_partial");return 124
            mode="observe" if cell=="linked-on" else "control"
            args=["taskset","-c","12,13","python3","-u",str(HERE/"run_finite.py"),
              str(HERE/"CMeasureCohort.lean"),label,"--wall-seconds",str(seconds),
              "--input",str(MATRIX/f"shard-{shard}-{mode}.json")]
            if cell=="stock":args+=["--library",str(LIB)]
            else:args+=["--native-executable",str(EXE),"--embedded-probe"]
            print("START",label,time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),flush=True)
            with (MATRIX/(label+".client-stdout")).open("x") as stdout,(MATRIX/(label+".client-stderr")).open("x") as stderr:
                result=subprocess.run(args,stdout=stdout,stderr=stderr)
            receipt=json.loads((out/"receipt.json").read_text())
            assert not identity_alive(receipt),"Do not overlap a surviving native process"
            rows=sum(line.startswith("M_DAG ") for line in (out/"stdout.txt").open())
            record={"shard":shard,"cell":cell,"label":label,"client_exit":result.returncode,
              "native_exit":receipt["exit"],"rows":rows,"expected":expected,"native_retired":True,
              "wall_s":receipt["wall_s"],"raw_capture":str(out)}
            records.append(record)
            (MATRIX/"cell-results.json").write_text(json.dumps(records,indent=2))
            print("END",json.dumps(record),flush=True)
            if result.returncode!=0 or receipt["exit"]!=0 or rows!=expected:
                finish("native_failure_or_deadline_partial");return 1
    finish("complete")
    return 0
if __name__=="__main__":raise SystemExit(main())
