"""Offline reconstruction of complete E039 source/native phase observations."""
from pathlib import Path
import collections,datetime,gzip,json,os,statistics,sys
R=Path('/workspaces/repository');E=Path(__file__).parent;O=Path(sys.argv[1])
source=R/'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs/proofnet/input.jsonl'
original=[json.loads(x) for x in source.read_text().splitlines()]
def read(p):return [json.loads(x) for x in gzip.open(p,'rt')]
def dist(v):
 v=sorted(v)
 return {'n':len(v),'min':min(v),'median':statistics.median(v),'p95':v[int(.95*(len(v)-1))],'max':max(v)} if v else {'n':0}
def proc_key(p):return str(p['pid'])+'@'+repr(p['created'])
cells=[]
for name in ['rep0','rep1','rep2']:
 p=O/name;t=json.loads((p/'terminal.json').read_text())
 ins=read(p/'input.jsonl.gz');rows=read(p/'http-results.jsonl.gz');events=read(p/'native-phase-events.jsonl.gz')
 assert ins==original and len(rows)==len(original)==t['returned']==t['expected']==5952
 assert sorted((x['ordinal'],x['source_index']) for x in rows)==[(i,x['index']) for i,x in enumerate(original)]
 assert not t['failure'] and t['server_exit']==0
 assert all(t['begin_ns']<=x['admitted_ns']<=x['response_ns']<=t['end_ns'] for x in rows)
 assert t['counts']==dict(collections.Counter(x['basic'] for x in rows))
 observer=[x for x in events if x['event']=='observer_terminal'];assert len(observer)==1
 prep=[x for x in events if x['event']=='preparation_terminal']
 cold=[x for x in prep if not x['reused_started']]
 warm=[x for x in prep if x['reused_started']]
 sends=[x for x in events if x['event']=='native_send_terminal']
 starts=[x for x in events if x['event']=='native_started']
 closes=[x for x in events if x['event']=='native_close_terminal']
 assert len({x['snippet_id'] for x in prep})==len(prep)
 assert {x['snippet_id'] for x in prep}.issubset({'proofnet-'+str(x['index']) for x in original})
 unreached_prep_ids=sorted({'proofnet-'+str(x['index']) for x in original}-{x['snippet_id'] for x in prep})
 snapshots={};final_keys=set();errors=[]
 for event in events:
  for field in ['cpu','cpu_before','cpu_after']:
   sample=event.get(field)
   if not isinstance(sample,dict):continue
   for v in sample.get('processes',[]):
    key=proc_key(v);total=v['user']+v['system']
    old=snapshots.get(key)
    if old is None or total>=old['observed_lifetime_cpu_seconds']:
     snapshots[key]={'pid':v['pid'],'created':v['created'],'observed_lifetime_cpu_seconds':total,'last_event':event['event'],'last_ns':event['ns']}
    if event['event']=='native_close_terminal' and field=='cpu_before':final_keys.add(key)
   errors.extend({'event':event['event'],'ns':event['ns'],'error':e} for e in sample.get('errors',[]))
 for key,v in snapshots.items():v['present_at_before_close']=key in final_keys
 def component(x):
  a={proc_key(v):v['user']+v['system'] for v in x['cpu_before']['processes']}
  b={proc_key(v):v['user']+v['system'] for v in x['cpu_after']['processes']}
  return sum(max(0,value-a.get(key,0)) for key,value in b.items())
 cpu_cold=sum(component(x) for x in cold)
 cpu_import=sum(component(x) for x in cold if x['header'])
 observed_total=sum(x['observed_lifetime_cpu_seconds'] for x in snapshots.values())
 framed=[]
 for f in sorted(p.glob('native-*.stdout.gz')):
  raw=gzip.open(f,'rb').read();good=bad=0;parts=raw.split(b'\n\n')
  for part in parts:
   if not part.strip():continue
   try:json.loads(part);good+=1
   except (ValueError,UnicodeError):bad+=1
  framed.append({'file':f.name,'bytes':len(raw),'parsed_frames':good,'non_json_or_partial_frames':bad})
 headers={}
 for h in sorted({x['header'] for x in prep}):
  q=[x for x in prep if x['header']==h];c=[x for x in q if not x['reused_started']]
  headers[h]={'requests':len(q),'preparations':len(c),'started_reuses':len(q)-len(c),'observed_cold_cpu_seconds':sum(component(x) for x in c),'cold_preparation_response_wall_seconds':dist([x['elapsed_ns']/1e9 for x in c]),'errors':sum(x['error'] is not None for x in c)}
 out={'label':name,'whole_seconds':t['whole_seconds'],'outcomes':t['counts'],'HTTP_status_counts':dict(collections.Counter(str(x['status_code']) for x in rows)),'request_latency_seconds':dist([x['elapsed_seconds'] for x in rows]),'effective_policy':next(x for x in events if x['event']=='observer_start'),'requests_without_preparation_terminal':unreached_prep_ids,'native_worker_starts':len(starts),'native_worker_close_records':len(closes),'native_close_errors':[x for x in closes if x['error']],'all_parent_handles_retired':all(x['exit_code'] is not None for x in observer[0]['workers']),'stock_close_tasks':[x for x in events if x['event']=='stock_close_tasks'],'header_classes':headers,'preparation_observed_native_cpu_seconds':cpu_cold,'nonempty_import_preparation_observed_native_cpu_seconds':cpu_import,'observed_native_lifetime_CPU_seconds':observed_total,'preparation_to_observed_native_CPU_percent':100*cpu_cold/observed_total if observed_total else None,'native_process_lifetimes':list(snapshots.values()),'lifetimes_not_observed_at_close':[v for k,v in snapshots.items() if k not in final_keys],'cpu_snapshot_errors':errors,'native_send_errors':[x for x in sends if x['error']],'header_send_count':sum(x['is_header'] for x in sends),'reported_waited_child_cpu_not_exhaustive':observer[0].get('reported_waited_child_cpu',observer[0].get('waited_native_cpu')),'observer_self_cpu':observer[0]['observer_cpu'],'native_raw_frames':framed,'clock_qualification':'cold preparation wall includes start+header and nested send wall must not be added; overlapping intervals not makespan or removable fraction','CPU_qualification':'observed parent/leaf process cumulative counters at native phases and before stock kill; missing/early exits/counter quantization remain; ratio is scoped observedCPU, not exhaustive nativeCPU/full-wall/GPU bound; collectorCPU/fleetmemory not measured; empty-header managerprep returns before native bootstrap, whose first-command mixed cost is not silently called zero preparation'}
 cells.append(out)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_RQ':'RQ1','sources_per_observation':5952,'complete_whole_observations':len(cells),'total_attempts':len(cells)*5952,'cells':cells,'interpretation_scope':'actual producer-compatible GC49+native arithmetic Kimina request-driven import-prefix characterization; single nonempty import key plus literalNone cases, not17native contexts, completeRQ1, service superiority, causal ideal savings or system/GPU novelty'}
(O/'analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'complete_observations':len(cells),'attempts':len(cells)*5952,'whole_seconds':[x['whole_seconds'] for x in cells],'prep_CPU':[x['preparation_observed_native_cpu_seconds'] for x in cells],'observed_native_CPU':[x['observed_native_lifetime_CPU_seconds'] for x in cells],'scoped_CPU_ratios_percent':[x['preparation_to_observed_native_CPU_percent'] for x in cells]},indent=2))
