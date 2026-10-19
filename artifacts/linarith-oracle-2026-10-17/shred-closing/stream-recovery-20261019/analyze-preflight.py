"""Recompute the closed real54-source qualification; no full-corpus claim."""
from pathlib import Path
import runpy,json,collections,gzip
O=Path(__file__).resolve().parent
D=runpy.run_path(str(O.parent/"analyze-http.py"))
Q=O/"real-preflight"
result=D["analyze"](Q)
engagement={}
for method in["native","shred"]:
 directory=Q/("rep1-"+method)
 data=D["rows"](directory/"results.jsonl")
 http=D["rows"](directory/"http.jsonl")
 finals=[x for x in http if x["event"]=="response"]
 points=[];failures=collections.defaultdict(list);sizes=[]
 for event in finals:
  points.extend([(event["start_ns"],1),(event["end_ns"],-1)])
  ids=[x["id"]for x in json.loads(event["request"])["snippets"]]
  if event["status"]!=200:
   for ident in ids:failures[ident].append(event["status"])
  sizes.append(len(event["body"].encode()))
 active=peak=0
 for stamp,delta in sorted(points):active+=delta;peak=max(peak,active)
 operational=[x["proof_id"]for x in data if D["verification_outcome"](x)=="operational"]
 log=gzip.decompress((directory/"server.log.gz").read_bytes()).decode(errors="replace")
 engagement[method]=dict(operational_IDs=operational,failed_HTTP_attempts=dict(failures),
  HTTP_response_count=len(finals),HTTP_request_count=sum(x["event"]=="request"for x in http),
  maximum_completed_attempt_overlap=peak,maximum_HTTP_response_body_bytes=max(sizes),
  actual_LimitOverrunError_occurrences=log.count("LimitOverrunError"),
  source_concurrency=json.loads((directory/"terminal.json").read_text())["source_concurrency"])
 assert peak==2 and len(http)==2*len(finals)
 assert operational==["minif2f-579","minif2f-663","minif2f-664"]
 assert set(failures)==set(operational)and all(v==[500]*3 for v in failures.values())
 assert not log.count("LimitOverrunError")
assert not result["native_verification_differences"]and not result["status_differences"]
result["real_HTTP_engagement"]=engagement
result["scope"]="Closed selected54-source real service repair qualification only. Full7808-source native/SHRED pair remains separate, incomplete. Application patched equally; no selected-cohort speedup or whole-RQ conclusion. Root self-review."
(O/"real-preflight-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(dict(sources=result["source_count"],status_differences=len(result["status_differences"]),native_outcome_differences=len(result["native_verification_differences"]),HTTP=engagement)))
