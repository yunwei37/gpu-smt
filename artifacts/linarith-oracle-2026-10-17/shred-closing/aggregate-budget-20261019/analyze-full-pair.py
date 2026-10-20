"""Complete as-integrated native/SHRED comparison, retaining every failure."""
from pathlib import Path
import collections,csv,gzip,json,math,re,runpy
O=Path(__file__).resolve().parent
H=runpy.run_path(str(O.parent/"analyze-http.py"))
root=O/"full-population/http-full/minif2f"
result=H["analyze"](root)
data={method:{x["proof_id"]:x for x in H["rows"](root/("rep1-"+method)/"results.jsonl")}for method in["native","shred"]}
expected=["minif2f-"+str(i)for i in range(7808)]
assert all(list(rows)==expected for rows in data.values())
terms={m:json.loads((root/("rep1-"+m)/"terminal.json").read_text())for m in data}
latencies={};resources={}
def classification(row):
 if row["status"]=="resource_failure":return"resource_failure"
 if row["status"]=="timeout_error":return"timeout"
 return H["verification_outcome"](row)
def percentile(values,q):
 values=sorted(values);p=(len(values)-1)*q;a=math.floor(p);b=math.ceil(p)
 return values[a]*(1-(p-a))+values[b]*(p-a)
for method in data:
 directory=root/("rep1-"+method);pending={};spans={};statuses=collections.Counter();overlap=0
 with gzip.open(directory/"http.jsonl.gz","rt")as stream:
  for line in stream:
   event=json.loads(line)
   if event["event"]=="request":pending[event["start_ns"]]=event;overlap=max(overlap,len(pending))
   else:
    pending.pop(event["start_ns"]);statuses[event["status"]]+=1
    ident=json.loads(event["request"])["snippets"][0]["id"]
    if ident.startswith("minif2f-"):
     assert ident not in spans
     spans[ident]=(event["end_ns"]-event["start_ns"])/1e9
 assert not pending and set(spans)==set(expected)and overlap==2
 assert statuses=={200:7810}
 latencies[method]=spans
 peak=count=max_native=kills=0;last=None;max_gap=0;limits=set()
 with gzip.open(directory/"memory-rss.jsonl.gz","rt")as stream:
  for line in stream:
   row=json.loads(line);count+=1;peak=max(peak,row["total_rss_bytes"])
   max_native=max(max_native,row["native_repl_count"]);kills+=int("kill"in row)
   assert row["budget_bytes"]==row["effective_threshold_bytes"]==48*1024**3
   if last is not None:max_gap=max(max_gap,(row["time_ns"]-last)/1e9)
   last=row["time_ns"]
   for process in row["processes"]:
    if process["native_repl"]:limits.update(process.get("address_limit",[]))
 assert max_native==2 and peak<48*1024**3 and kills==0
 assert peak==terms[method]["memory_watchdog"]["peak_sampled_owned_rss_bytes"]
 assert limits and all(str(24*1024**3)in line for line in limits)
 resources[method]=dict(peak_sampled_owned_RSS_bytes=peak,samples=count,
  maximum_native_workers=max_native,kills=kills,maximum_sample_gap_seconds=max_gap,
  actual_native_address_limit_lines=sorted(limits))
 result["conditions"][method]["native_outcomes_with_resource_types"]=dict(collections.Counter(classification(x)for x in data[method].values()))
 result["conditions"][method]["HTTP_all_sources_seconds"]={k:percentile(list(spans.values()),q)for k,q in[("p50",.5),("p90",.9),("p99",.99)]}
 result["conditions"][method]["resource_enforcement"]=resources[method]
for method in data:
 directory=root/("rep1-"+method)
 with gzip.open(directory/"process-exits.jsonl.gz","rt")as stream:
  exits=[json.loads(line)for line in stream]
 expected_failures=result["conditions"][method]["native_outcomes_with_resource_types"]["resource_failure"]
 assert len(exits)==expected_failures
 assert all(x["returncode"]==134 and "std::bad_alloc"in x["stderr"]for x in exits)
 result["conditions"][method]["observed_bad_alloc_exits"]=len(exits)
result["whole_native_over_shred"]=terms["native"]["whole_with_input_preparation_seconds"]/terms["shred"]["whole_with_input_preparation_seconds"]
result["shred_more_elapsed_percent"]=(1/result["whole_native_over_shred"]-1)*100
result["warms_native_over_shred"]=terms["native"]["warm_verify_seconds"]/terms["shred"]["warm_verify_seconds"]
result["completed_HTTP_span_scope"]="Per completed HTTPattempt; includes service waiting but excludes SDKpredispatch/global preparation. Concurrent sums overlap, not CPU/removable wall/Amdahl."
native_complete={k for k,x in data["native"].items()if classification(x)=="complete"}
shred_complete={k for k,x in data["shred"].items()if classification(x)=="complete"}
result["lost_genuine_complete_IDs"]=sorted(native_complete-shred_complete)
result["gained_genuine_complete_IDs"]=sorted(shred_complete-native_complete)
result["same_genuine_complete_count"]=len(native_complete&shred_complete)
result["cache_hit_outcomes"]=dict(collections.Counter(classification(x)for x in data["shred"].values()if any("LEAN_PREFIX_CERT event=hit "in m.get("data","")for m in x["result"].get("response",{}).get("messages",[]))))
delta_ids={x["proof_id"]for x in result["native_verification_differences"]}
raw_source_tokens={}
with gzip.open(O.parents[1]/"prefix-opportunity/minif2f-input.jsonl.gz","rt")as stream:
 for line in stream:
  x=json.loads(line);ident="minif2f-"+str(x["index"])
  if ident in delta_ids:raw_source_tokens[ident]=bool(re.search(r"\b(sorry|admit)\b",x["code"]))
result["changed_original_source_has_literal_sorry_or_admit"]=raw_source_tokens
assert len(raw_source_tokens)==len(delta_ids)
with(O/"full-pair-source-latencies.csv").open("w",newline="")as stream:
 writer=csv.writer(stream,lineterminator="\n")
 writer.writerow(["proof_id","native_outcome","shred_outcome","native_status","shred_status","native_HTTP_seconds","shred_HTTP_seconds"])
 for ident in expected:writer.writerow([ident,classification(data["native"][ident]),classification(data["shred"][ident]),data["native"][ident]["status"],data["shred"][ident]["status"],latencies["native"][ident],latencies["shred"][ident]])
ranked=sorted(expected,key=lambda x:(-latencies["native"][x],x))
result["native_ranked_matched_HTTP_tails"]={}
for fraction in[.01,.1]:
 ids=ranked[:math.ceil(len(expected)*fraction)]
 result["native_ranked_matched_HTTP_tails"][str(fraction)]=dict(sources=len(ids),IDs=ids,
  sums_seconds={m:sum(latencies[m][x]for x in ids)for m in data},
  outcomes={m:dict(collections.Counter(classification(data[m][x])for x in ids))for m in data})
result["source_HTTP_regressions"]=sum(latencies["shred"][x]>latencies["native"][x]for x in expected)
result["scope"]="Complete single fixed-order shared-host native/SHRED7808pair with declared Kimina transport/logging/resource patches,2x24GiB within48GiBtotal. As-integrated published executor, not its standalone service or a whole-family negative. No outcome-transparent speedup or GPU bound."
(O/"full-pair-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:result[k]for k in["whole_native_over_shred","shred_more_elapsed_percent","same_genuine_complete_count","lost_genuine_complete_IDs","gained_genuine_complete_IDs","cache_hit_outcomes","source_HTTP_regressions"]}))
print(json.dumps({m:result["conditions"][m]for m in data}))
