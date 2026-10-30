"""Finite typed-deduplicated openai/math original/certificate diagnostic point."""
from pathlib import Path
import json,time,re,os
from run_openai_native import run,ROOT,HERE,persistent_capture_path
LABEL="openai-kernel-seven-v1"
PREP=ROOT/"openai-row-preparation-v3"
def main():
    out=persistent_capture_path(ROOT/LABEL);out.mkdir(exist_ok=False)
    (out/"controller.py").write_bytes(Path(__file__).read_bytes())
    selected=json.loads((PREP/"selected.json").read_text())
    (out/"plan.json").write_text(json.dumps({"selected":selected,"max_group_s":1400,
        "native_self_wall_s":35,"native_jobs":1,"native_memory_MiB":8192,"own_tree_budget_GiB":16,
        "pair_order":"counterbalance original/certificate byrow; plain and recheck separate",
        "timing":"plain=whole-source first checks/imports; observer=extra kernel rechecks of every new theorem+aux, sum separately",
        "scope":"7 integer row types from available typed45; not representative of1354379 annotations"},indent=2))
    began=time.monotonic();count=0
    with (out/"results.jsonl").open("w") as ledger:
      for row in range(7):
       for observer in [False,True]:
        for mode in (["original","certificate"] if row%2==0 else ["certificate","original"]):
         if time.monotonic()-began>1350:raise RuntimeError("group allowance exhausted before next native")
         suffix="-recheck" if observer else ""
         label=f"{LABEL}-row{row}-{mode}"+suffix
         capture,receipt=run(PREP/f"row{row}-{mode}{suffix}.lean",label,35)
         text=(capture/"stdout.txt").read_text();err=(capture/"stderr.txt").read_text()
         ok=receipt["exit"]==0 and "sorryAx" not in text and "error:" not in text
         totals=re.findall(r"M_OPENAI_KERNEL_TOTAL (\d+) (\d+)",text)
         kernels=[{"declaration":n,"ns":int(ns)} for n,ns in re.findall(r"^M_OPENAI_KERNEL ([^ ]+) (\d+)$",text,re.M)]
         rec={"row":row,"mode":mode,"observer":observer,"capture":str(capture),
           "accepted":ok,**receipt,"extra_kernel_declarations":int(totals[-1][0]) if totals else None,
           "extra_kernel_ns":int(totals[-1][1]) if totals else None,"kernel_declarations":kernels}
         ledger.write(json.dumps(rec)+"\n");ledger.flush();count+=1
         if receipt["sampled_budget_violation"]:raise RuntimeError("RSS violation")
      # A bad payload must be rejected by stock kernel.
      source=(PREP/"row0-certificate.lean").read_text().replace(
        "inner (currentRow.2.2[0]!) = (0 : Int)","inner (currentRow.2.2[0]!) = (1 : Int)",1)
      bad=out/"bad-payload.lean";bad.write_text(source)
      capture,receipt=run(bad,LABEL+"-bad-payload",35)
      text=(capture/"stdout.txt").read_text()
      negative={"kind":"mutated-payload","capture":str(capture),**receipt,
                "rejected":receipt["exit"]==1 and "sorryAx" in text}
      ledger.write(json.dumps(negative)+"\n");ledger.flush();count+=1
      if not negative["rejected"]:raise RuntimeError("mutated payload not rejected")
      # Baseline measurement of other compiled/deduplicated target types.
      typedout=out/"typed-baseline.jsonl"
      capture,receipt=run(HERE/"OpenAITypedKernelProbe.lean",LABEL+"-typed45",60,
        extra_env={"M_OPENAI_TYPED_INPUT":str(PREP/"typed45.tsv"),"M_OPENAI_TYPED_OUTPUT":str(typedout)},as_main=True)
      ledger.write(json.dumps({"kind":"typed45","capture":str(capture),**receipt})+"\n");ledger.flush();count+=1
    (out/"terminal.json").write_text(json.dumps({"complete":count==30,"units":count,"wall_s":time.monotonic()-began})+"\n")
if __name__=="__main__":main()
