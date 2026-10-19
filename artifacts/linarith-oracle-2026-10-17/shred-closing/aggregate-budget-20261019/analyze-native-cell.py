"""Stream the closed complete native7808 cell; never treat it as a paired result."""
from pathlib import Path
import collections,csv,gzip,json,math,runpy
O=Path(__file__).resolve().parent
D=O/"full-population/http-full/minif2f/rep1-native"
outcome=runpy.run_path(str(O.parent/"analyze-http.py"))["verification_outcome"]
def lines(name):
 path=D/name
 if not path.exists():path=path.with_name(path.name+".gz")
 with(gzip.open(path,"rt")if path.suffix==".gz"else path.open())as stream:
  for line in stream:yield json.loads(line)
def quantile(values,q):
 values=sorted(values);n=(len(values)-1)*q
 return values[math.floor(n)]*(1-(n-math.floor(n)))+values[math.ceil(n)]*(n-math.floor(n))
term=json.loads((D/"terminal.json").read_text())
assert term["state"]=="complete"and term["returned"]==term["expected"]==7808
assert not term["owned_live_descendants_after_shutdown"]
assert term["source_concurrency"]==term["maximum_live_native_repls"]==2
assert term["aggregate_memory_budget_bytes"]==48*1024**3
assert term["per_native_repl_address_limit_bytes"]==24*1024**3
pending={};http={};http_status=collections.Counter();maximum_overlap=0;attempts=collections.Counter()
for event in lines("http.jsonl"):
 if event["event"]=="request":
  pending[event["start_ns"]]=event
  maximum_overlap=max(maximum_overlap,len(pending))
 else:
  request=pending.pop(event["start_ns"])
  snippets=json.loads(event["request"])["snippets"]
  assert len(snippets)==1
  ident=snippets[0]["id"];attempts[ident]+=1;http_status[event["status"]]+=1
  if ident.startswith("minif2f-"):
   http[ident]=dict(seconds=(event["end_ns"]-event["start_ns"])/1e9,status=event["status"])
assert not pending
assert set(http)=={"minif2f-"+str(i)for i in range(7808)}
assert maximum_overlap==2
counts=collections.Counter();sdk=collections.Counter();sources=[];resource=[];timeouts=[]
for index,row in enumerate(lines("results.jsonl")):
 ident=row["proof_id"];assert ident=="minif2f-"+str(index)
 classification="resource_failure"if row["status"]=="resource_failure"else outcome(row)
 if row["status"]=="timeout_error":classification="timeout"
 counts[classification]+=1;sdk[row["status"]]+=1
 if row["status"]=="resource_failure":
  error=row["result"].get("error","")
  assert "std::bad_alloc"in error
  resource.append(ident)
 if row["status"]=="timeout_error":timeouts.append(ident)
 sources.append(dict(proof_id=ident,status=row["status"],native_outcome=classification,
  completed_HTTP_attempt_seconds=http[ident]["seconds"],HTTP_status=http[ident]["status"],
  HTTP_attempts=attempts[ident],native_reported_body_seconds=row["result"].get("time")))
assert len(sources)==7808 and dict(sdk)==term["counts"]
sample_count=peak_rss=peak_repls=kills=0;max_gap=0;previous=None;actual_limits=set()
for sample in lines("memory-rss.jsonl"):
 sample_count+=1;peak_rss=max(peak_rss,sample["total_rss_bytes"])
 peak_repls=max(peak_repls,sample["native_repl_count"]);kills+=int("kill"in sample)
 assert sample["budget_bytes"]==sample["effective_threshold_bytes"]==48*1024**3
 if previous is not None:max_gap=max(max_gap,(sample["time_ns"]-previous)/1e9)
 previous=sample["time_ns"]
 for proc in sample["processes"]:
  if proc["native_repl"]:actual_limits.update(proc.get("address_limit",[]))
assert peak_rss==term["memory_watchdog"]["peak_sampled_owned_rss_bytes"]<48*1024**3
assert peak_repls==2 and sample_count==term["memory_watchdog"]["samples"]and kills==0
assert actual_limits and all(str(24*1024**3)in x for x in actual_limits)
exits=list(lines("process-exits.jsonl"))
assert len(exits)==len(resource)==47
assert all(x["returncode"]==134 and "std::bad_alloc"in x["stderr"]for x in exits)
with(O/"native-full-source-latencies.csv").open("w",newline="")as stream:
 writer=csv.DictWriter(stream,fieldnames=list(sources[0]),lineterminator="\n");writer.writeheader();writer.writerows(sources)
values=[x["completed_HTTP_attempt_seconds"]for x in sources]
ranked=sorted(sources,key=lambda x:(-x["completed_HTTP_attempt_seconds"],x["proof_id"]))
tails={}
for fraction in[0.01,0.1]:
 n=math.ceil(len(sources)*fraction);chosen=ranked[:n]
 tails[str(fraction)]=dict(sources=n,HTTP_elapsed_sum_seconds=sum(x["completed_HTTP_attempt_seconds"]for x in chosen),
  counts=dict(collections.Counter(x["native_outcome"]for x in chosen)),IDs=[x["proof_id"]for x in chosen])
result=dict(scope="Complete single native7808-source cell at aggregate48GiB/two24GiB workers. SHRED paired acquisition is incomplete; no speedup or cross-resource inference.",
 source_count=len(sources),native_outcome_counts=dict(counts),SDK_counts=dict(sdk),
 whole_with_input_preparation_seconds=term["whole_with_input_preparation_seconds"],
 warm_verify_seconds=term["warm_verify_seconds"],resources=term["memory_watchdog"],
 maximum_RSS_sample_gap_seconds=max_gap,actual_native_address_limit_lines=sorted(actual_limits),
 HTTP=dict(response_status_counts=dict(http_status),maximum_completed_attempt_overlap=maximum_overlap,
  unanswered_attempts=len(pending),source_attempt_counts=dict(collections.Counter(attempts[x["proof_id"]]for x in sources)),
  all_source_completed_attempt_seconds={name:quantile(values,q)for name,q in[("p50",.5),("p90",.9),("p99",.99)]},
  scope="One completed HTTP attempt per source; excludes SDK predispatch waiting and global preparation. Concurrent sums overlap; not solver CPU or removable whole wall."),
 cumulative_completed_HTTP_span_seconds=sum(values),
 cumulative_completed_HTTP_span_by_outcome={key:sum(x["completed_HTTP_attempt_seconds"]for x in sources if x["native_outcome"]==key)for key in counts},
 native_ranked_tails=tails,resource_failure_IDs=resource,timeout_IDs=timeouts,
 native_allocation_exit_count=len(exits),native_allocation_returncodes=dict(collections.Counter(x["returncode"]for x in exits)),
 lifecycle=dict(joined_owned_descendants=term["joined_owned_descendants"],live_after=term["owned_live_descendants_after_shutdown"]),
 note="Native-reported body time is zero for some top-level failures; use charged HTTP attempts for all-source latency. Waited-child CPU is not exhaustive phase attribution.")
(O/"native-full-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(dict(counts=result["native_outcome_counts"],whole=result["whole_with_input_preparation_seconds"],
 peak_RSS_GiB=peak_rss/1024**3,samples=sample_count,max_gap=max_gap,
 HTTP=result["HTTP"],tails={k:{key:value for key,value in v.items()if key!="IDs"}for k,v in tails.items()})))
