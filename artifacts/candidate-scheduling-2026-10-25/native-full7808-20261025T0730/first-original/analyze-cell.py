"""Audit this completed first-original cell only; live first-short remains untouched."""
from pathlib import Path
import collections,gzip,json
A=Path(__file__).resolve().parent;R=A.parents[3]
def rows(path):
 path=path if path.exists()else path.with_suffix(path.suffix+'.gz')
 with(gzip.open(path,'rt')if path.suffix=='.gz'else path.open())as stream:
  yield from map(json.loads,stream)
terminal=json.loads((A/'terminal.json').read_text())
assert terminal['state']=='complete'and terminal['returned']==7808
assert terminal['owned_live_descendants_after_shutdown']==[]
actual=list(rows(A/'consumer-results.jsonl.gz'));by={x['proof_id']:x for x in actual}
assert len(by)==len(actual)==7808
native={sid:row for sid,row in by.items()if row['native_response_returned']}
cancelled={sid:row for sid,row in by.items()if not row['native_response_returned']}
assert len(native)==3631 and len(cancelled)==4177
for sid,row in cancelled.items():
 assert row['status']=='cancelled_after_success'and row['result']['time']is None
 winner=row['winner'];assert by[winner]['status']=='valid'
 assert int(sid.split('-')[1])//32==int(winner.split('-')[1])//32
inputs=json.loads(gzip.decompress((R/'artifacts/engine-resource-profile-2026-10-25/population-inputs/all.json.gz').read_bytes()))
codes={x['id']:x['code']for x in inputs['candidates']}
assert set(codes)==set(by)
history={x['proof_id']:x for x in rows(A.parent/'all/consumer-results.jsonl.gz')}
valid={sid for sid,row in by.items()if row['status']=='valid'}
oldvalid={sid for sid,row in history.items()if row['status']=='valid'}
resource=[]
for sid,row in native.items():
 if row['status']!='resource_failure':continue
 error=row['result'].get('error','')
 assert 'std::bad_alloc'in error
 resource.append(dict(source_id=sid,reason='native std::bad_alloc under24GiBAS',
  previous_status=history[sid]['status'],
  supplied_body_clock=row['result'].get('time'),interpreted_body_clock=None))
changes=[dict(source_id=sid,previous=history[sid]['status'],current=row['status'])
 for sid,row in native.items()if history[sid]['status']!=row['status']]
seen=collections.Counter()
for event in rows(A/'http.jsonl.gz'):
 if event.get('event')!='request':continue
 body=json.loads(event['body'])
 for snippet in body.get('snippets',[]):
  sid=snippet.get('id')
  if sid not in codes:continue
  assert snippet['code']==codes[sid]
  seen[sid]+=1
assert set(seen)==set(native) and all(n==1 for n in seen.values())
peak=0;maximum_repls=0;samples=0
for sample in rows(A/'memory-rss.jsonl.gz'):
 samples+=1;peak=max(peak,sample['total_rss_bytes'])
 maximum_repls=max(maximum_repls,sample['native_repl_count'])
assert peak==terminal['memory_watchdog']['peak_sampled_owned_rss_bytes']
assert samples==terminal['memory_watchdog']['samples']
assert peak<=48*1024**3 and maximum_repls<=2
result=dict(returned=7808,counts=dict(collections.Counter(x['status']for x in actual)),
 original_source_bytes_match=True,requests_per_source=dict(collections.Counter(seen.values())),
 solved_task_ids=sorted({int(x.split('-')[1])//32 for x in valid}),
 all_solved_task_ids=sorted({int(x.split('-')[1])//32 for x in oldvalid}),
 accepted_winner_count=len(valid),actual_native_responses=len(native),cancelled_before_start=len(cancelled),
 status_changes=changes,resource_failures=resource,
 body_clock_scope='Resource body zeros from transport are unknown; raw values preserved,not zero cost.',
 consumer_complete_lifecycle_seconds=terminal['consumer_complete_lifecycle_seconds'],
 native_complete_lifecycle_seconds=terminal['whole_lifecycle_seconds'],
 sampled_owned_peak_rss_bytes=peak,memory_samples=samples,maximum_repls=maximum_repls,
 watchdog_kills=terminal['memory_watchdog']['kills'],watchdog_error=terminal['memory_watchdog']['error'],
 old_resource_point=dict(per_process_AS_bytes=24*1024**3,workers=2,aggregate_sampled_RSS_bytes=48*1024**3,cpus=[8,9,10,11]),
 comparison_state='all and first-original complete;first-short remains live;group incomplete',
 scope='Completed first-original cell with source/task/cancellation audit against the paired all cell. Shared host and own development controls overlap retained;not new4worker resource point or RL-per-candidate reward equivalence.')
(A/'cell-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='resource_failures'}))
