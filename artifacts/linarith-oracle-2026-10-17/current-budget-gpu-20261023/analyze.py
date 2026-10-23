from pathlib import Path
import json,gzip,collections,runpy,sys,math
O=Path(__file__).resolve().parent
F=runpy.run_path(str(O.parent/'kimina-full29750-budgeted-20261019/analyze.py'))
rows=F['rows']
full='full'in sys.argv
items=list(rows(O.parent/'input-top1000.jsonl'));items=items if full else items[:24];ids=[x['proof_id']for x in items]
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
for method in['native','power','gpu']:
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
native=data['native'];changes={}
for method in['power','gpu']:
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
 for k in['cpu_exit','gpu_exit','strong_cpu_exit']:
  v=x.get(k)
  if v and(v.get('kill_error')or v.get('wait_error')):errors.append(x)
tail={}
for f in[.01,.1]:
 selected=sorted(ids,key=lambda i:lat['native'][i],reverse=True)[:math.ceil(len(ids)*f)]
 tail[str(f)]=dict(IDs=selected,overlapping_HTTP_seconds={m:sum(lat[m][i]for i in selected)for m in lat})
lifecycle=O/('gpu-full-lifecycle.json'if full else'gpu-lifecycle.json')
life=json.loads(lifecycle.read_text())if lifecycle.exists()else None
probe=json.loads(life['providerProbe'])if life and life.get('providerProbe')else None
out=dict(scope='Complete matched current-resource original candidate service observation, root self-review; preflight is not full result.'if not full else'Complete matched original1000 same-resource observation, root self-review.',
 conditions=cells,response_changes=changes,CPU_GPU_fullresponse_difference_IDs=[i for i in ids if data['power'][i]['result'].get('response')!=data['gpu'][i]['result'].get('response')],
 aggregate_provider_memory=memory,GPU_races=len(gpu_races),actual_race_source_count=len(set(race_sources)),unknown_race_source_calls=unknown,
 retained_CPU_or_retirement_errors=errors,GPU_race_winners=dict(collections.Counter(x['winner']for x in gpu_races)),
 actual_GPU_child_races=sum(x.get('gpu_pid')is not None for x in gpu_races),
 small_LP_retained_CPU_only_races=sum(x.get('second_child_role')=='cpu-highs'for x in gpu_races),
 lifecycle=life,provider_retirement_probe=probe,native_ranked_tails=tail,
 GPU_over_CPU_whole=cells['gpu']['terminal']['whole_lifecycle_seconds']/cells['power']['terminal']['whole_lifecycle_seconds'],
 limitations=['Fresh one fixed-order/shared-host observation, not confidence or global optimum.',
 'Original source outcomes/native JSON govern; CPU/GPU contention and startup can lose.',
 'GPUzeroallocations means no CUDAmodels engaged, not fast device solving.',
 'Tail HTTP sums overlap and are not isolated tail lifecycles; cold provider lifecycle is separate.',
 'No strict GPU bound, broad route closure, independent audit or OSDI contribution acceptance.'])
(O/('full-analysis.json'if full else'preflight-analysis.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in['conditions','native_ranked_tails','lifecycle','limitations']},indent=2))
