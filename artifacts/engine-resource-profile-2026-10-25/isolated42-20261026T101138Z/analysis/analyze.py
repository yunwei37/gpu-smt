from pathlib import Path
import json,gzip,collections,datetime
r=Path('/workspaces/repository')
p=r/'artifacts/engine-resource-profile-2026-10-25/isolated42-20261026T101138Z'
ctx=json.loads(Path('/tmp/gpu-smt-isolated42-20261026/context.json').read_text())
terminal=json.loads((p/'terminal.json').read_text());assert terminal['exit_code']==0
rows=[v for line in (p/'results.jsonl').read_text().splitlines() for v in json.loads(line)['results']]
assert [x['id'] for x in rows]==ctx['expected_ids']
requests=[json.loads(l) for l in gzip.decompress(Path(ctx['source']).read_bytes()).decode().splitlines()]
assert [b['candidates'][0]['id'] for b in requests]==ctx['expected_ids']
assert all(b['mode']=='all' and len(b['candidates'])==1 and b['candidates'][0]['timeout_ms']==300000 and b['candidates'][0]['reuse'] is False for b in requests)
assert all(not x['cached'] and not x['coalesced'] and len(x['attempts'])==1 and x['attempts'][0]['exclusive'] for x in rows)
events=[json.loads(line) for line in (p/'resource-events.jsonl').read_text().splitlines()]
active=set();maximum=0;registrations=[];releases=[];preemptions=[];samples=[]
for e in events:
 f=e['fields'];message=f.get('message')
 if message=='register active process':
  k=(f['pid'],f['start_ticks']);assert k not in active;active.add(k);maximum=max(maximum,len(active));registrations.append(k)
 elif message=='release active process ownership':
  k=(f['pid'],f['start_ticks']);assert k in active;active.remove(k);releases.append(k)
 elif message=='owned RSS sample':samples.append(f)
 elif message=='preempt owned attempt and requeue exclusively':preemptions.append(f)
assert not active and maximum==1 and len(registrations)==len(releases)==42
budget=48*1024**3
peak=max([e['rss_bytes'] for e in samples+preemptions]+[0])
details=[]
for row,batch in zip(rows,requests):
 a=row['attempts'][0];status=row['outcome']['status']
 assert status in ['resource_exhausted','timeout'] and a['status']==status
 if status=='resource_exhausted':
  matches=[v for v in preemptions if v['origin_id']==row['id']]
  assert len(matches)==1 and a['preemption_rss_bytes']==matches[0]['rss_bytes']>budget
 else:assert a['preemption_rss_bytes'] is None
 details.append({'id':row['id'],'status':status,'error':row['outcome']['error'],
  'attempt_seconds':a['elapsed_seconds'],'consumer_seconds':row['elapsed_seconds'],
  'leader_observed_rss_bytes':a['peak_rss_bytes'],'aggregate_preemption_rss_bytes':a['preemption_rss_bytes'],
  'processes':a['processes'],'exclusive':True,'logical_rejection_established':False})
canonical=json.loads(Path(ctx['previous_manifest']['input']).read_text())
originals={c['id']:c for c in canonical['candidates']}
assert len(originals)==7808
assert all(b['candidates'][0]['code']==originals[b['candidates'][0]['id']]['code'] for b in requests)
unretired=[]
for pid,ticks in registrations:
 f=Path('/proc')/str(pid)/'stat'
 try:
  if int(f.read_text().rsplit(')',1)[1].split()[19])==ticks:unretired.append({'pid':pid,'start_ticks':ticks})
 except FileNotFoundError:pass
assert not unretired
summary={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':len(rows),
 'statuses':dict(collections.Counter(x['outcome']['status'] for x in rows)),'accepted_ids':[],
 'logical_rejections':0,'controller_seconds':terminal['controller_seconds'],
 'sum_attempt_seconds':sum(x['attempts'][0]['elapsed_seconds'] for x in rows),
 'sum_consumer_seconds':sum(x['elapsed_seconds'] for x in rows),
 'resources':{'actual_aggregate_budget_bytes':budget,'cpu_ids':[8,9,10,11],'cores_per_worker':4,
  'maximum_registered_native_leaders':maximum,'fixed_AS_limit':False},
 'watchdog_events':len(preemptions),'retained_RSS_samples':len(samples),
 'sampled_peak_rss_bytes':peak,'sampled_peak_GiB':peak/1024**3,
 'peak_excess_bytes':max(0,peak-budget),'retained_samples_above_budget':sum(x['rss_bytes']>budget for x in samples),
 'all_registered_native_births_retired':True,'original_input_ids_options_match':True,'canonical7808_source_bytes_match':True,
 'scope':'42historicalASfailures rerun solo with larger aggregate headroom;not proof of false goals or universal failure;no cross-resource-point speedup',
 'sampling_limit':'1s watchdog response can overshoot;not hard RSSquota'}
(p/'analysis').mkdir(exist_ok=True)
(p/'analysis/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(p/'analysis/per-candidate.json').write_text(json.dumps(details,indent=2)+'\n')
print(json.dumps(summary,indent=2))
