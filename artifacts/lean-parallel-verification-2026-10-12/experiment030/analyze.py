#!/usr/bin/env python3
"""Recompute complete paired effects, fallback-charged latency and raw fidelity."""
from pathlib import Path
import json,zipfile,statistics,collections
D=Path(__file__).parent;O=D/'full1-proofnet'
def read(label,name):
 p=O/label
 if p.exists():return (p/name).read_bytes()
 with zipfile.ZipFile(O/(label+'.zip')) as z:return z.read(label+'/'+name)
def cell(label):
 terminal=json.loads((O/(label+'.terminal.json')).read_text())
 rows=[json.loads(x) for x in read(label,'results.jsonl').splitlines()]
 primary_events=[json.loads(x) for x in read(label,'primary.events.jsonl').splitlines()]
 initial={e.get('ordinal',e.get('source_index')):e['monotonic_ns'] for e in primary_events if e.get('event')=='admitted'}
 recovery=[]
 for row in rows:
  first=row['admission_monotonic_ns']
  if row['phase']=='native-fallback' and row['ordinal'] in initial:
   first=initial[row['ordinal']]
   recovery.append({'source_index':row['source_index'],'phase_local_seconds':row['elapsed_seconds'],
    'complete_seconds':(row['terminal_observed_monotonic_ns']-first)/1e9})
  row['complete_admission_to_response_seconds']=(row['terminal_observed_monotonic_ns']-first)/1e9
 lat=sorted(x['complete_admission_to_response_seconds'] for x in rows)
 report={'label':label,'terminal':terminal,'returned':len(rows),'basic_counts':dict(collections.Counter(x['basic'] for x in rows)),
  'complete_native_latency_seconds':{'median':statistics.median(lat),'p95':lat[int(.95*(len(lat)-1))],'p99':lat[int(.99*(len(lat)-1))],'max':max(lat)},
  'fallback_latency_reconstruction':recovery,'rows':{x['source_index']:x for x in rows}}
 if terminal['profile']:report['resources']=json.loads(read(label,'resources-summary.json'))
 return report
def main():
 complete={p.name[:-len('.terminal.json')]:cell(p.name[:-len('.terminal.json')]) for p in O.glob('*.terminal.json')}
 pairs=[]
 for rep in range(3):
  a,b=complete.get(f'rep{rep}-warm'),complete.get(f'rep{rep}-gated')
  if not a or not b:continue
  issues=[];artifact_diffs=[];requested_diffs=[]
  if len(a['rows'])!=5952 or len(b['rows'])!=5952:issues.append('population incomplete')
  for index,row in a['rows'].items():
   other=b['rows'].get(index)
   if other is None or row['basic']!=other['basic']:issues.append({'basic_difference':index})
   elif row['native_response']!=other['native_response']:artifact_diffs.append(index)
   if other is not None:
    ar=((row.get('native_response') or {}).get('native') or {}).get('response')
    br=((other.get('native_response') or {}).get('native') or {}).get('response')
    if ar!=br:requested_diffs.append(index)
  aw,bw=a['terminal']['whole_seconds'],b['terminal']['whole_seconds']
  pairs.append({'rep':rep,'warm_seconds':aw,'gated_seconds':bw,'gated_slowdown_percent':(bw/aw-1)*100,
   'relative_wall_reduction_percent':(aw-bw)/aw*100,'basic_issues':issues,
   'raw_native_response_difference_indices':artifact_diffs,'requested_response_difference_indices':requested_diffs,'fallback_count':len(b['terminal']['fallback_indices'])})
 result={'completed_cells':len(complete),'planned_cells':8,'complete':len(complete)==8,'pairs':pairs,
  'cells':{k:{f:v for f,v in c.items() if f!='rows'} for k,c in complete.items()},
  'scope':'complete native warm pool verification with candidate sorry-header gate; native response differences retained, not normalized',
  'latency_note':'fallback rows reconstruct from original gated admission when present; whole clocks already include discarded work and fallback'}
 (D/'matrix-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'complete':result['complete'],'completed_cells':len(complete),'pairs':pairs}))
if __name__=='__main__':main()
