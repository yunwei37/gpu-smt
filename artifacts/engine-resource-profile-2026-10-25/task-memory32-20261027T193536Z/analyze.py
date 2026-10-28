from pathlib import Path
import json,gzip,collections,datetime
root=Path(__file__).parent
read=lambda p:json.loads(gzip.decompress(p.read_bytes())) if p.suffix=='.gz' else json.loads(p.read_text())
batch=read(root.parent/'task-memory-preflight-20261027/batch32.json.gz')
result={'collected_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cells':{},'selection':'outcome-informed32development sources,not unbiased final population'}
captures={n:read(root/n/'capture.json.gz') for n in ['fifo','task-memory']}
births=set()
for name,c in captures.items():
 assert c['batch']==batch and c['policy']==name and len(c['results'])==32
 assert [v['id'] for v in c['results']]==[v['id'] for v in batch['candidates']]
 assert len({v['id'] for v in c['results']})==32 and all(not v['cached'] and not v['coalesced'] for v in c['results'])
 rows=c['results'];attempts=[a for v in rows for a in v['attempts']]
 for v in rows:
  for a in v['attempts']:
   for p in a['processes']:births.add((p['pid'],p['start_ticks']))
 launch=read(root/name/'launch.json');births.add((launch['pid'],launch['start_ticks']))
 samples=[]
 for l in gzip.decompress((root/name/'resource-events.jsonl.gz').read_bytes()).splitlines():
  e=json.loads(l);f=e.get('fields',{})
  if f.get('message')=='owned RSS sample':samples.append(f['rss_bytes'])
 t=read(root/name/'terminal.json');ar=read(root/name/'archival.json')
 assert t['exit_code']==0
 result['cells'][name]={'statuses':dict(collections.Counter(v['outcome']['status'] for v in rows)),'external_seconds':t['external_cell_seconds'],'archival_seconds':ar['seconds'],'external_plus_archive':t['external_cell_seconds']+ar['seconds'],'lifecycle_seconds':c['lifecycle_seconds'],'attempts':len(attempts),'retry_attempts':sum(len(v['attempts'])-1 for v in rows),'exclusive_attempts':sum(a['exclusive'] for a in attempts),'watchdog_marked_attempts':sum(a['preemption_rss_bytes'] is not None for a in attempts),'sampled_aggregate_peak_bytes':max(samples),'sampled_aggregate_peak_GiB':max(samples)/2**30,'over_budget_samples':sum(x>c['resources']['memory_bytes'] for x in samples),'resource_failure_errors':dict(collections.Counter(v['outcome']['error'] for v in rows if v['outcome']['status']=='resource_exhausted'))}
assert captures['fifo']['resources']==captures['task-memory']['resources']
assert captures['fifo']['backend']==captures['task-memory']['backend']
assert [v['outcome'] for v in captures['fifo']['results']]==[v['outcome'] for v in captures['task-memory']['results']]
result['all_outcomes_raw_equal']=True
result['external_ratio']=result['cells']['fifo']['external_seconds']/result['cells']['task-memory']['external_seconds']
result['elapsed_reduction_percent']=100*(1-result['cells']['task-memory']['external_seconds']/result['cells']['fifo']['external_seconds'])
changed=[]
for a,b in zip(captures['fifo']['results'],captures['task-memory']['results']):
 if len(a['attempts'])!=len(b['attempts']):changed.append({'id':a['id'],'fifo_attempts':len(a['attempts']),'task_memory_attempts':len(b['attempts']),'final_status':b['outcome']['status']})
result['attempt_count_changed']=changed
live=[]
for pid,birth in births:
 try:
  f=Path(f'/proc/{pid}/stat').read_text().split(') ')[1].split()
  if int(f[19])==birth and f[0]!='Z':live.append([pid,birth])
 except OSError:pass
assert not live
result['retirement']={'fullcell_recorded_native_and_cli_births':len(births),'matching_live_non_zombie':live,'controller_486935_exists':Path('/proc/486935').exists()}
(root/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
