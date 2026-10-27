"""Existing completed native interval analysis;no execution/control interface."""
from pathlib import Path
import collections,datetime,gzip,json,os
os.sched_setaffinity(0,{11})
root=Path(__file__).resolve().parents[2]/'engine-resource-pair-2026-10-25/full7808-20261027T032050Z'
capture=json.loads(gzip.decompress((root/'native/capture.json.gz').read_bytes()))
proc={}
for row in capture['results']:
 for attempt in row['attempts']:
  assert len(attempt['processes'])==1
  p=attempt['processes'][0];key=(p['pid'],p['start_ticks']);assert key not in proc
  proc[key]={'id':row['id'],'exclusive':attempt['exclusive'],'watchdog':attempt['preemption_rss_bytes'] is not None,'elapsed':attempt['elapsed_seconds'],'status':row['outcome']['status']}
registered={};retired={}
with gzip.open(root/'driver.log.gz','rt')as f:
 for line in f:
  row=json.loads(line);fields=row.get('fields',{});msg=fields.get('message')
  if msg not in ['register active process','release active process ownership']:continue
  key=(fields['pid'],fields['start_ticks'])
  if key not in proc:continue
  target=registered if msg=='register active process' else retired
  assert key not in target
  target[key]=datetime.datetime.fromisoformat(row['timestamp'].replace('Z','+00:00')).timestamp()
assert len(registered)==len(proc)==len(retired)==7852
def union(spans):
 merged=[]
 for lo,hi in sorted(spans):
  assert hi>=lo
  if merged and lo<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],hi)
  else:merged.append([lo,hi])
 return sum(hi-lo for lo,hi in merged)
groups={'all_native':list(proc),'preempted_nonexclusive':[k for k,v in proc.items() if v['watchdog'] and not v['exclusive']],'exclusive_retry':[k for k,v in proc.items() if v['exclusive']],'final_resource_failure':[k for k,v in proc.items() if v['status']=='resource_exhausted'],'preempted_nonexclusive_eventually_resource_failed':[k for k,v in proc.items() if v['watchdog'] and not v['exclusive'] and v['status']=='resource_exhausted']}
den=json.loads((root/'native/terminal.json').read_text())['external_cell_seconds']
summary={'source':str(root.relative_to(Path('/workspaces/repository'))),'reference_whole_cell_seconds':den,'registered_native_span_seconds':max(retired.values())-min(registered.values()),'groups':{},'scope':'UTC registration/retirement occupied-time union;not removable elapsed,Amdahl input,CPU time or counterfactual throughput'}
for name,keys in groups.items():
 spans=[(registered[k],retired[k]) for k in keys];candidates={proc[k]['id']:proc[k]['status'] for k in keys}
 summary['groups'][name]={'attempts':len(keys),'unique_candidates':len(candidates),'interval_union_seconds':union(spans),'overlapping_interval_sum_seconds':sum(hi-lo for lo,hi in spans),'native_monotonic_attempt_sum_seconds':sum(proc[k]['elapsed'] for k in keys),'interval_union_fraction_of_reference_cell':union(spans)/den,'final_statuses_per_attempt':dict(collections.Counter(proc[k]['status'] for k in keys)),'unique_final_statuses':dict(collections.Counter(candidates.values()))}
Path(__file__).with_name('analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
