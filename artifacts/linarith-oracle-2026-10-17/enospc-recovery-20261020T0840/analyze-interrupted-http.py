"""Recover observed HTTP outcomes without scoring an interrupted full acquisition."""
from pathlib import Path
import sys,gzip,json,csv,collections,runpy
P=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path[:0]=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/client"]
from kimina_client import CheckResponse
H=runpy.run_path(str(P/"artifacts/linarith-oracle-2026-10-17/shred-closing/analyze-http.py"))
F=P/"artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/full.partial-enospc-20261020T0840"
ids=json.loads((F/"source-ids.json").read_text());assert len(ids)==29750 and len(set(ids))==29750
requests=collections.Counter();status=collections.Counter();seen={};bad=0
with gzip.open(F/"rep1-native/http.jsonl.gz","rt")as stream:
 for line in stream:
  try:e=json.loads(line)
  except ValueError:bad+=1;continue
  if e["event"]=="request":
   for s in json.loads(e["body"])["snippets"]:requests[s["id"]]+=1
  else:
   status[str(e["status"])]+=1
   if e["status"]!=200:continue
   for x in CheckResponse.model_validate_json(e["body"]).results:
    if x.id.startswith("warm-"):continue
    assert x.id in ids
    sdk=x.analyze().status.value
    row=dict(proof_id=x.id,status="resource_failure"if(x.error or"").startswith("resource_failure:")else sdk,sdk_status=sdk,result=x.model_dump(exclude_none=True))
    if row["status"]=="resource_failure":native="resource_failure"
    elif row["status"]=="timeout_error":native="timeout"
    else:native=H["verification_outcome"](row)
    seen[x.id]=dict(row,native_outcome=native)
with(R/"partial-source-outcomes.csv").open("w",newline="")as stream:
 w=csv.writer(stream,lineterminator="\n")
 w.writerow(["proof_id","observation","recorded_HTTP_attempts","SDK_status","native_outcome"])
 for ident in ids:
  x=seen.get(ident)
  w.writerow([ident,"recorded_response"if x else"censored_no_response"if ident in requests else"not_observed_before_stop",requests[ident],x["sdk_status"]if x else"",x["native_outcome"]if x else""])
out=dict(original_source_count=len(ids),recorded_original_response_IDs=len(seen),
 recorded_native_outcomes=dict(collections.Counter(x["native_outcome"]for x in seen.values())),
 recorded_SDK_statuses=dict(collections.Counter(x["sdk_status"]for x in seen.values())),
 request_only_original_IDs=[i for i in ids if i in requests and i not in seen],
 not_observed_original_IDs=sum(i not in requests for i in ids),
 HTTP_status_records=dict(status),truncated_JSONL_lines=bad,
 scope="Incomplete native first cell only. Every original ID retained; no verdict for censored/unseen sources, no complete clock or matched ratio. SDK/native classifier reuse is root self-review, not independent audit.")
(R/"partial-outcome-analysis.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
