from pathlib import Path
import json,gzip,collections,runpy,sys,math,csv
O=Path(__file__).resolve().parent
F=runpy.run_path(str(O.parents[1]/'kimina-full29750-budgeted-20261019/analyze.py'))
def rows(path):
 if path.suffix=='.gz' and path.exists():
  with gzip.open(path,'rt')as stream:
   for line in stream:
    if line.strip():yield json.loads(line)
 else:yield from F['rows'](path)
phase='gpu-phase'in sys.argv
full=phase or 'full'in sys.argv
items=list(rows(O.parents[1]/'input-top1000.jsonl'));items=items if full else items[:24];ids=[x['proof_id']for x in items]
prefix='full1000-'if full else'qualification24-'
ready='ready'in sys.argv

def nonmessage(v):
 if isinstance(v,dict):return {k:nonmessage(x)for k,x in v.items()if k!='messages'}
 if isinstance(v,list):return [nonmessage(x)for x in v]
 return v
cells={};data={};lat={};memory={}
def body(s):
 a=s.splitlines()
 while a and(not a[0].strip()or a[0].startswith('import ')):a.pop(0)
 return '\n'.join(a).strip()
bybody={body(x['code']):x['proof_id']for x in items}
for method in(['gpu']if phase else['native','power','gpu']):
 label=prefix+method+('-ready'if ready and method=='gpu'else'')
 p=O/label/'terminal.json'
 if not p.exists()or json.loads(p.read_text())['state']!='complete':raise SystemExit('Three matched cells must be closed complete')
 cells[method],data[method],lat[method]=F['closed_cell'](O/label,ids)
 identities=set();peer_samples=0;peak_peer=0
 for x in rows(O/label/'memory-rss.jsonl'):
  remote=x.get('external_owned_provider');extra=0
  if remote:
   extra=remote['rss_bytes'];assert extra==sum(p['rss_bytes']for p in remote['processes'])
   assert remote['affinity']==[8,9,10,11]
   identities.add((remote['root_pid'],remote['root_start_ticks']));peer_samples+=1;peak_peer=max(peak_peer,extra)
  assert x['total_rss_bytes']==sum(p['rss']for p in x['processes'])+extra
 if method=='gpu':assert peer_samples==cells[method]['terminal']['memory_watchdog']['samples']and len(identities)==1
 memory[method]=dict(provider_sample_count=peer_samples,provider_identities=list(identities),peak_provider_RSS_bytes=peak_peer,
  arithmetic_checked='Every total equals local own RSS plus exact-owned provider tree RSS; no GPU-Pod host memory exclusion.')
assert len(bybody)==len(items), 'Ambiguous source bodies require explicit attribution'
native=data.get('native');changes={}
for method in([]if phase else['power','gpu']):
 changes[method]=dict(native_verdict_difference_IDs=[i for i in ids if F['native_outcome'](native[i])!=F['native_outcome'](data[method][i])],
  native_nonmessage_difference_IDs=[i for i in ids if nonmessage(native[i]['result'].get('response'))!=nonmessage(data[method][i]['result'].get('response'))],
  raw_response_difference_IDs=[i for i in ids if native[i]['result'].get('response')!=data[method][i]['result'].get('response')])
gpu_races=list(rows(O/(prefix+'gpu'+('-ready'if ready else''))/'lp-races.jsonl'))
race_sources=[];unknown=[];errors=[]
for x in gpu_races:
 i=bybody.get(body(x['source']))
 if i is None:unknown.append(x['call_id'])
 else:race_sources.append(i)
 if x.get('strong_cpu_spawn_error')or not x.get('strong_cpu_pid'):errors.append(x)
 if x.get('second_child_role')=='cpu-highs':
  assert x['gpu_exit']['pid']==x['strong_cpu_pid']
 for k in['cpu_exit','gpu_exit','strong_cpu_exit']:
  v=x.get(k)
  if v and(v.get('kill_error')or v.get('wait_error')):errors.append(x)
tail={}
for f in([]if phase else[.01,.1]):
 selected=sorted(ids,key=lambda i:lat['native'][i],reverse=True)[:math.ceil(len(ids)*f)]
 tail[str(f)]=dict(IDs=selected,overlapping_HTTP_seconds={m:sum(lat[m][i]for i in selected)for m in lat})
lifecycle=O/('gpu-full-lifecycle.json'if full else'gpu-lifecycle.json')
life=json.loads(lifecycle.read_text())if lifecycle.exists()else None
probe=json.loads(life['providerProbe'])if life and life.get('providerProbe')else None
provider_path=O/('gpu-full-provider.log.gz'if full else'gpu-provider.log.gz')
provider_events=[]
if provider_path.exists():
 for line in gzip.decompress(provider_path.read_bytes()).decode().splitlines():
  if line.startswith('{'):provider_events.append(json.loads(line))
launches=[x for x in provider_events if x.get('event')=='launch']
retired={x['batch_id']for x in provider_events if x.get('event')=='batch_retired'}
proxy_calls=list(rows(O/(prefix+'gpu'+('-ready'if ready else''))/'support-calls.jsonl.gz'))
call_sources=collections.defaultdict(set)
for x in proxy_calls:
 if x.get('input'):call_sources[x['input']['call_id']].add(x['input']['source'])
unknown_launches=[]
for x in launches:
 if any(len(call_sources[c])!=1 for c in x['call_ids']):unknown_launches.append(x['batch_id']);continue
 assert len({next(iter(call_sources[c]))for c in x['call_ids']})==x['distinct_sources']
device=dict(launch_events=len(launches),launches=sum(x['batch_size']>0 for x in launches),empty_cancelled_groups=sum(x['batch_size']==0 for x in launches),models=sum(x['batch_size']for x in launches),
 batch_sizes=dict(collections.Counter(str(x['batch_size'])for x in launches)),model_states=dict(collections.Counter(x['state']for x in provider_events if 'state'in x)),
 verified_cross_source_multi_model_launches=sum(x['distinct_sources']>1 and x['batch_id']not in unknown_launches for x in launches),
 unknown_source_call_launch_IDs=unknown_launches,
 unretired_launch_IDs=[x['batch_id']for x in launches if x['batch_id']not in retired])
# Inspect observed submissions and retirement; do not assume synchronous admission.
# Count only decoded, source-owned arrivals; malformed/cancelled inputs stay unknown.
batch_events=list(rows(O/(prefix+'gpu'+('-ready'if ready else''))/'support-calls.jsonl.gz.batches'))
submits={x['batch_id']:x for x in batch_events if x.get('event')=='device_submit'}
group_retire={x['batch_id']:x for x in batch_events if x.get('event')=='device_batch_retired'}
by_request={x['id']:x for x in proxy_calls if x.get('input')}
arrivals=[];submitted_spans=[]
for group,b in submits.items():
 if group not in group_retire:continue
 end=group_retire[group]['monotonic_ns'];submitted_spans.append((b['monotonic_ns'],end))
 sources={by_request[int(k.split(':')[-1])]['input']['source']for k in b['keys']}
 for x in proxy_calls:
  q=x.get('input')
  if q and q['source']not in sources and b['monotonic_ns']<=x['start_ns']<end:
   arrivals.append(dict(call_id=q['call_id'],source_ID=bybody.get(body(q['source'])),prior_group=group,
    finished_before_prior_retirement=x['end_ns']<=end,
    arrival_to_prior_retirement_ns=end-x['start_ns'],proxy_ns=x['end_ns']-x['start_ns']))
ordered=sorted(submitted_spans)
dispatch=dict(proxy_records=len(proxy_calls),decoded_proxy_records=len(by_request),
 undecoded_proxy_records=sum(not x.get('input')for x in proxy_calls),
 undecoded_errors=dict(collections.Counter(str(x.get('reply',{}).get('error'))for x in proxy_calls if not x.get('input'))),
 submitted_groups=len(submits),missing_retire_group_IDs=sorted(set(submits)-set(group_retire)),
 overlapping_submitted_group_pairs=sum(a[0]<b[1]and b[0]<a[1]for i,a in enumerate(ordered)for b in ordered[i+1:]),
 source_owned_arrivals_during_prior_group_retirement=arrivals,
 limitations='Only decoded inputs are source-attributed; queued-before-submission/undecoded work is not reconstructed. Fixed-trace overlaps are not counterfactual speedup or strict Amdahl.')
model_sources={}
for x in launches:
 for key,call in zip(x['keys'],x['call_ids']):
  texts=call_sources[call]
  model_sources[key]=bybody.get(body(next(iter(texts))))if len(texts)==1 else None
ticks=[];unknown_ticks=[]
for x in provider_events:
 v=x.get('device_globaltimer_interval')
 if v and len(v)==2 and v[0]>0 and v[1]>=v[0]:
  source=model_sources.get(x.get('key'))
  if not source:unknown_ticks.append(x.get('key'));continue
  ticks.append(dict(key=x['key'],source_ID=source,start=v[0],end=v[1],
   iterations=x.get('iterations'),state=x.get('state')))
cross=[]
for i,a in enumerate(ticks):
 for b in ticks[i+1:]:
  if a['source_ID']!=b['source_ID']and a['start']<b['end']and b['start']<a['end']:
   cross.append(dict(first=a,second=b,overlap_ns=min(a['end'],b['end'])-max(a['start'],b['start'])))
device['hardware_interval_models']=len(ticks)
device['unknown_hardware_interval_keys']=unknown_ticks
device['cross_source_hardware_interval_pairs']=cross
device['cross_source_non_cancelled_positive_iteration_pairs']=sum(
 all(x[k].get('iterations',0)>0 and x[k].get('state')!='cancelled'for k in ['first','second'])for x in cross)
device['interval_scope']='Per-model device-globaltimer spans; cancelled/zero-iteration work is explicitly retained and is not useful solve throughput.'
gpu_winning_sources=collections.defaultdict(set)
for x in gpu_races:
 i=bybody.get(body(x['source']))
 if x['winner']in['gpu','external-infeasible']and i:gpu_winning_sources[x['winner']].add(i)
out=dict(scope=('Closed GPU cell only; CPU/native controls still pending, no paired speedup.'if phase else('Complete matched current-resource original candidate service observation, root self-review; preflight is not full result.'if not full else'Complete matched original1000 same-resource observation, root self-review.')),
 conditions=cells,response_changes=changes,CPU_GPU_fullresponse_difference_IDs=None if phase else[i for i in ids if data['power'][i]['result'].get('response')!=data['gpu'][i]['result'].get('response')],
 aggregate_provider_memory=memory,GPU_races=len(gpu_races),actual_race_source_count=len(set(race_sources)),unknown_race_source_calls=unknown,
 retained_CPU_or_retirement_errors=errors,GPU_race_winners=dict(collections.Counter(x['winner']for x in gpu_races)),GPU_winning_source_IDs={k:sorted(v)for k,v in gpu_winning_sources.items()},
 actual_GPU_child_races=sum(x.get('gpu_pid')is not None for x in gpu_races),
 small_LP_retained_CPU_only_races=sum(x.get('second_child_role')=='cpu-highs'for x in gpu_races),
 lifecycle=life,provider_retirement_probe=probe,device_engagement=device,dispatch_serialization=dispatch,native_ranked_tails=tail,
 GPU_over_CPU_whole=None if phase else cells['gpu']['terminal']['whole_lifecycle_seconds']/cells['power']['terminal']['whole_lifecycle_seconds'],
 limitations=['Fresh one fixed-order/shared-host observation, not confidence or global optimum.',
 'Original source outcomes/native JSON govern; CPU/GPU contention and startup can lose.',
 'GPUzeroallocations means no CUDAmodels engaged, not fast device solving.',
 'Tail HTTP sums overlap and are not isolated tail lifecycles; cold provider lifecycle is separate.',
 'No strict GPU bound, broad route closure, independent audit or OSDI contribution acceptance.'])
if full and not phase:
 native_whole=cells['native']['terminal']['whole_lifecycle_seconds']
 cpu_whole=cells['power']['terminal']['whole_lifecycle_seconds']
 gpu_whole=cells['gpu']['terminal']['whole_lifecycle_seconds']
 out['paired_summary']=dict(native_over_CPU=native_whole/cpu_whole,native_over_GPU_cell=native_whole/gpu_whole,
  GPU_cell_elapsed_reduction_vs_CPU=1-gpu_whole/cpu_whole,
  GPU_cold_over_CPU=life['completeColdLifecycleSeconds']/cpu_whole,
  native_over_GPU_cold=native_whole/life['completeColdLifecycleSeconds'],
  comparisons='Whole completed original1000 matched resource point; one fixed-order shared-host observation, not uncertainty estimate.')
 per_source=[]
 for i in ids:
  per_source.append(dict(proof_id=i,native_outcome=F['native_outcome'](native[i]),
   native_HTTP_seconds=lat['native'][i],CPU_HTTP_seconds=lat['power'][i],GPU_HTTP_seconds=lat['gpu'][i],
   GPU_minus_CPU_HTTP_seconds=lat['gpu'][i]-lat['power'][i]))
 with (O/'paired-source-latencies.csv').open('w',newline='')as stream:
  writer=csv.DictWriter(stream,fieldnames=list(per_source[0]),lineterminator='\n');writer.writeheader();writer.writerows(per_source)
 out['GPU_CPU_source_HTTP_comparison']=dict(GPU_shorter=sum(lat['gpu'][i]<lat['power'][i]for i in ids),
  GPU_longer=sum(lat['gpu'][i]>lat['power'][i]for i in ids),
  largest_GPU_regressions=sorted(per_source,key=lambda x:x['GPU_minus_CPU_HTTP_seconds'],reverse=True)[:10],
  largest_GPU_improvements=sorted(per_source,key=lambda x:x['GPU_minus_CPU_HTTP_seconds'])[:10],
  interpretation='Per-source envelopes overlap, include queue/contention and fixed-order host drift; not isolated latency trials or device causation.')
(O/('gpu-phase-analysis.json'if phase else('full-analysis.json'if full else'preflight-analysis.json'))).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in['conditions','native_ranked_tails','lifecycle','limitations']},indent=2))
