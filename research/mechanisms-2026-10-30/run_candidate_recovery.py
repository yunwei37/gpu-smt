"""Finite original-candidate recovery census; preserve all non-compute commands."""
from pathlib import Path
import csv, gzip, json, os, re, sys, time
import run_finite
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PAIR=ROOT/"artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z"
LIB=run_finite.BUILD_ROOT/"candidate-certificate-v5"
def mask_comments(text):
    chars=list(text);depth=0;i=0;string=False
    while i<len(text):
        if depth:
            if text.startswith("/-",i):depth+=1;chars[i:i+2]=[" "," "];i+=2;continue
            if text.startswith("-/",i):depth-=1;chars[i:i+2]=[" "," "];i+=2;continue
            if chars[i]!="\n":chars[i]=" "
            i+=1;continue
        if string:
            if chars[i]!="\n":chars[i]=" "
            if text[i]=="\\" and i+1<len(text):
                chars[i+1]=" ";i+=2;continue
            if text[i]=='"':string=False
            i+=1;continue
        if text.startswith("/-",i):depth=1;chars[i:i+2]=[" "," "];i+=2;continue
        if text.startswith("--",i):
            end=text.find("\n",i)
            if end<0:end=len(text)
            chars[i:end]=[" "]*(end-i);i=end;continue
        if text[i]=='"':string=True;chars[i]=" "
        i+=1
    return "".join(chars)
def rewrite(source,family):
    masked=mask_comments(source);edits=[]
    if family=="digits":
        for m in re.finditer(r"(?m)^(\s*)rfl\b(?=\s*(?:<;>|$))",masked):
            start=m.start()+len(m.group(1));edits.append((start,start+3,"m_digits_rfl"))
    else:
        for m in re.finditer(r"\binterval_cases\s+([A-Za-z_][A-Za-z_0-9']*)",masked):
            edits.append((m.start(),m.start()+len("interval_cases"),"m_interval_cases"))
    spans=[{"line":source.count("\n",0,a)+1,"original":source[a:b],"replacement":c} for a,b,c in edits]
    for a,b,c in reversed(edits):source=source[:a]+c+source[b:]
    # Finite diagnostic point: never silently retain maxHeartbeats0.
    source,n=re.subn(r"(set_option\s+maxHeartbeats\s+)\d+",r"\g<1>200000",source)
    if n==0:source="set_option maxHeartbeats 200000\n"+source
    return "import CertificateMethods\n"+source,spans
def classify(code,stdout,stderr):
    text=stdout+"\n"+stderr
    if "INTERNAL PANIC" in text or "PANIC at" in text:return "native_process_failure"
    if any(s in text.lower() for s in ["out of memory","memory limit","bad_alloc","failed to allocate"]):return "resource_exhausted"
    if code in [124,-14] or "maximum number of heartbeats" in text or "maximum recursion depth" in text:return "budget_exceeded"
    if code==0 and "error:" not in text and "sorryAx" not in text:return "accepted"
    if code in [0,1]:return "lean_error"
    return "native_process_failure"
def main():
    out=run_finite.persistent_capture_path(run_finite.CAPTURE_ROOT.parent/"candidate-recovery49-v2")
    out.mkdir(exist_ok=False)
    (out/"collector.py").write_bytes(Path(__file__).read_bytes())
    inputs={x["id"]:x for x in json.load(gzip.open(PAIR/"input7808.json.gz","rt"))["candidates"]}
    original={x["id"]:x for x in json.load(gzip.open(PAIR/"engine.stdout.gz","rt"))["results"]}
    selected=[x for x in csv.DictReader((HERE/"coverage/minif2f126.csv").open()) if x["category"]=="checked_family"]
    assert len(selected)==49
    (out/"plan.json").write_text(json.dumps({"ids":[x["id"] for x in selected],
      "source_budget":200000,"native_memory_MiB":8192,"native_jobs":1,"cpus":"8,9,10,11",
      "per_case_wall_s":28,"group_max_s":1750,"library":str(LIB),
      "comparison":"historical original outcomes matched by id; new hardware/cap means no timing speedup ratio",
      "method":"replace standalone closing rfl or interval_cases token only; retain prefix/suffix/error behavior; immutable compiled certificate module"},indent=2)+"\n")
    began=time.monotonic();completed=0
    with (out/"results.jsonl").open("w") as ledger:
      for row in selected:
        if time.monotonic()-began>1710 or (out/"STOP").exists():break
        x=inputs[row["id"]];family="digits" if "digits" in row["computation"] else "grid"
        source,spans=rewrite(x["code"],family)
        source += "\n#print axioms "+x["task_id"]+"\n"
        f=out/(x["id"]+".lean");f.write_text(source)
        label="candidate-recovery49-v2-"+x["id"]
        code=run_finite.run(f,label,wall_seconds=28,module_path=LIB)
        c=run_finite.CAPTURE_ROOT/label
        stdout=(c/"stdout.txt").read_text();stderr=(c/"stderr.txt").read_text();receipt=json.loads((c/"receipt.json").read_text())
        status=classify(code,stdout,stderr)
        errors=[{"line":int(a),"message":msg} for a,msg in re.findall(r":(\d+):\d+: error: ([^\n]+)",stdout)]
        first_hook=min((s["line"]+1 for s in spans),default=10**9)
        old=original[x["id"]]
        record={"id":x["id"],"task":x["task_id"],"family":family,"status":status,
          "wall_s":receipt["wall_s"],"sampled_peak_owned_rss_bytes":receipt["sampled_peak_owned_rss_bytes"],
          "hits":stdout.count("M_CERT_HIT"),"fallbacks":stdout.count("M_CERT_FALLBACK"),
          "unsupported":stdout.count("M_CERT_UNSUPPORTED"),"edits":spans,"errors":errors,
          "prefix_error_observed":any(e["line"]<first_hook for e in errors),
          "axioms_with_sorry":"sorryAx" in stdout,
          "original_status":old["outcome"]["status"],
          "original_physical_attempt_wall_s":sum(a["elapsed_seconds"] for a in old["attempts"]),
          "original_attempts":len(old["attempts"]),"capture":str(c)}
        ledger.write(json.dumps(record)+"\n");ledger.flush();completed+=1
        print("M_RECOVERY",x["id"],status,record["hits"],record["wall_s"],flush=True)
        if status=="native_process_failure":break
    (out/"terminal.json").write_text(json.dumps({"completed":completed,"planned":49,"group_wall_s":time.monotonic()-began,"complete":completed==49})+"\n")
if __name__=="__main__":main()
