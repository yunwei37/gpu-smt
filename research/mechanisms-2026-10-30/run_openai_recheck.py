"""Correct raw kernel heartbeat units; preserve v1 incomplete rechecks."""
from pathlib import Path
import json,time
from run_openai_native import run,ROOT,HERE,persistent_capture_path
def main():
    first=ROOT/"openai-kernel-seven-v1"
    assert json.loads((first/"terminal.json").read_text())["complete"]
    out=persistent_capture_path(ROOT/"openai-recheck-v2");out.mkdir(exist_ok=False)
    (out/"controller.py").write_bytes(Path(__file__).read_bytes())
    (out/"plan.json").write_text(json.dumps({"reason":"raw kernel1million means1000 user heartbeats; three v1 cert observers censored by artificial kernel bound",
       "kernel_maxHeartbeats":"Core.getMaxHeartbeats current source options =200000*1000 raw",
       "source_maxHeartbeats":200000,"maxRecDepth":10000,"same_proofs_as_v1":True,
       "modes":"all14 observers matched budget, plus typed45 baseline; no plain proof rerun",
       "self_wall":35,"max_group_s":900},indent=2))
    started=time.monotonic();count=0
    with (out/"results.jsonl").open("w") as ledger:
      for row in range(7):
       for mode in (["original","certificate"] if row%2==0 else ["certificate","original"]):
        s=(ROOT/"openai-row-preparation-v3"/f"row{row}-{mode}-recheck.lean").read_text()
        s=s.replace("env.addDeclCore 1000000 1000000",
          "env.addDeclCore (Core.getMaxHeartbeats (← getOptions)).toUSize (maxRecDepth.get (← getOptions)).toUSize")
        s=s.replace('| .error e => throwError "original kernel recheck failed"',
          '| .error e => throwError m!"kernel recheck {name}: {e.toMessageData (← getOptions)}"')
        f=out/f"row{row}-{mode}.lean";f.write_text(s)
        capture,receipt=run(f,f"openai-recheck-v2-row{row}-{mode}",35)
        text=(capture/"stdout.txt").read_text()
        ok=receipt["exit"]==0 and "sorryAx" not in text and "error:" not in text
        import re
        totals=re.findall(r"M_OPENAI_KERNEL_TOTAL (\d+) (\d+)",text)
        kernels=[{"declaration":n,"ns":int(ns)} for n,ns in re.findall(r"^M_OPENAI_KERNEL ([^ ]+) (\d+)$",text,re.M)]
        rec={"row":row,"mode":mode,"observer":True,"capture":str(capture),"accepted":ok,**receipt,
          "extra_kernel_declarations":int(totals[-1][0]) if totals else None,
          "extra_kernel_ns":int(totals[-1][1]) if totals else None,"kernel_declarations":kernels}
        ledger.write(json.dumps(rec)+"\n");ledger.flush();count+=1
        if not ok:raise RuntimeError("matched-budget recheck failed; preserve before diagnosis")
        if time.monotonic()-started>800:raise RuntimeError("group boundary")
      f=out/"typed.lean"
      f.write_text((HERE/"OpenAITypedKernelProbe.lean").read_text().replace("env.addDeclCore 1000000 1000000","env.addDeclCore 200000000 10000"))
      typedout=out/"typed-baseline.jsonl"
      capture,receipt=run(f,"openai-recheck-v2-typed45",60,extra_env={
        "M_OPENAI_TYPED_INPUT":str(ROOT/"openai-row-preparation/typed45.tsv"),"M_OPENAI_TYPED_OUTPUT":str(typedout)},as_main=True)
      ledger.write(json.dumps({"kind":"typed45","capture":str(capture),**receipt})+"\n");ledger.flush();count+=1
    (out/"terminal.json").write_text(json.dumps({"complete":count==15,"units":count,"wall_s":time.monotonic()-started})+"\n")
if __name__=="__main__":main()
