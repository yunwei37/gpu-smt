"""Observe the four remaining limits with a qualified nonallocating C profile hook."""
from pathlib import Path
import os,time,json,select,re,collections
import run_finite
from run_candidate_recovery import classify
ROOT=run_finite.CAPTURE_ROOT.parent
HERE=Path(__file__).resolve().parent
def main():
    # Confirm the known live owner, then wait on that exact process exit event.
    pid=59080;birth="743007837"
    stat=Path(f"/proc/{pid}/stat")
    if stat.exists():
        assert stat.read_text().split()[21]==birth
        fd=os.pidfd_open(pid)
        while not select.select([fd],[],[],30)[0]:pass
        os.close(fd)
    first=ROOT/"power-family32-pair-v1"
    assert json.loads((first/"terminal.json").read_text())["complete"]
    out=ROOT/"remaining-four-c-diagnostic-v1";out.mkdir(exist_ok=False)
    (out/"controller.py").write_bytes(Path(__file__).read_bytes())
    native=ROOT/"generated/remaining-wrapped-cli-v1/lean"
    lib=ROOT/"generated/candidate-certificate-v12"
    pos=HERE/"CandidateCertificatePositive.lean"
    code=run_finite.run(pos,"remaining-c-positive-v1",25,native_executable=native,embedded_probe=True,module_path=lib)
    cap=run_finite.CAPTURE_ROOT/"remaining-c-positive-v1"
    events=list(map(json.loads,(cap/"tactics.jsonl").read_text().splitlines()))
    assert code==0 and any(x["event"]=="enter" for x in events),"C callback qualification failed"
    reference=(run_finite.CAPTURE_ROOT/"candidate-certificate-positive-v12/stdout.txt").read_text()
    normal=lambda s:re.sub(r"[^\s:]+\.lean:", "SOURCE.lean:",s)
    assert normal(reference)==normal((cap/"stdout.txt").read_text()),"positive diagnostics differ"
    rows=[]
    for id in ["3683","3698","3703","3710"]:
        original=run_finite.CAPTURE_ROOT/f"candidate-recovery49-pair-v3-minif2f-{id}-certificate"
        code=run_finite.run(original/"source.lean","remaining-four-c-v1-"+id,16,
           native_executable=native,embedded_probe=True,module_path=lib)
        c=run_finite.CAPTURE_ROOT/("remaining-four-c-v1-"+id)
        text=(c/"stdout.txt").read_text();err=(c/"stderr.txt").read_text()
        receipt=json.loads((c/"receipt.json").read_text())
        oldreceipt=json.loads((original/"receipt.json").read_text())
        status=classify(code,text,err)
        oldstatus=classify(oldreceipt["exit"],(original/"stdout.txt").read_text(),(original/"stderr.txt").read_text())
        events=list(map(json.loads,(c/"tactics.jsonl").read_text().splitlines()))
        entries={x["id"]:x for x in events if x["event"]=="enter"}
        finished={x["id"]:x for x in events if x["event"]=="exit"}
        complete=[{**x,"wall_s":(finished[i]["wall_ns"]-x["wall_ns"])/1e9,
                    "cpu_s":(finished[i]["cpu_ns"]-x["cpu_ns"])/1e9}
                   for i,x in entries.items() if i in finished]
        openframes=[x for i,x in entries.items() if i not in finished]
        rows.append({"id":"minif2f-"+id,"status":status,"prior_status":oldstatus,
          "receipt":receipt,"capture":str(c),"complete_frames":complete,"open_frames":openframes,
          "trace_records":len(events),"diagnostic_text_equal":normal(text)==normal((original/"stdout.txt").read_text())})
        (out/"results.json").write_text(json.dumps(rows,indent=2)+"\n")
        if status!=oldstatus:raise RuntimeError("observer changes operational category")
    (out/"terminal.json").write_text(json.dumps({"complete":len(rows)==4,"units":len(rows)})+"\n")
if __name__=="__main__":main()
