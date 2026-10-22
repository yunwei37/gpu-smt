from pathlib import Path
import json,gzip,collections,runpy
O=Path(__file__).resolve().parent;R=O.parents[2]
H=runpy.run_path(str(O.parent/'shred-closing/analyze-http.py'))
def rows(p):
 if not p.exists():p=p.with_name(p.name+'.gz')
 with (gzip.open(p,'rt')if p.suffix=='.gz'else p.open())as z:
  for l in z:
   if l.strip():yield json.loads(l)
def body(s):
 ls=s.splitlines()
 while ls and(not ls[0].strip()or ls[0].startswith('import ')):ls.pop(0)
 return '\n'.join(ls).strip()
items=list(rows(O.parent/'input-top1000.jsonl'));ids={body(x['code']):x['proof_id']for x in items}
def union(intervals):
 end=total=None
 for a,b in sorted(intervals):
  if end is None:total=b-a;end=b
  elif a>=end:total+=b-a;end=b
  elif b>end:total+=b-end;end=b
 return (total or 0)/1e9
out={'scope':'Real qualification and observed diagnostic costs, root self-review. No population/GPU bound or zero-overhead claim.','cells':{}}
all_raw={}
for label in ['frozen','diagnostic-off','diagnostic-on','diagnostic-on-v2','diagnostic-rejected-v2']:
 d=O/label;t=json.loads((d/'terminal.json').read_text());raw=list(rows(d/'results.jsonl'))
 assert len(raw)==t['expected']==t['returned']
 assert t['state']=='complete'and not t['owned_live_descendants_after_shutdown']and not t['memory_watchdog']['error']
 all_raw[label]={x['proof_id']:x for x in raw}
 c=dict(whole_seconds=t['whole_lifecycle_seconds'],warm_seconds=t['warm_verify_seconds'],
       native_outcomes=dict(collections.Counter(H['verification_outcome'](x)for x in raw)),
       resource=t['memory_watchdog'])
 p=d/'native-stages.jsonl.gz'
 if p.exists():
  events=list(rows(p));totals=collections.defaultdict(lambda:[0.,0.]);unknown=[];per_source=collections.defaultdict(list)
  for i,x in enumerate(events):
   source=ids.get(body(x['source']))
   if source is None:unknown.append(i)
   assert x['start_ns']<=x['end_ns']
   for name,begin,end in x['spans']:
    assert x['start_ns']<=begin<=end<=x['end_ns']
    if name in('products','lp'):per_source[source].append((begin,end))
   for name,(cpu,wall)in x['stages'].items():
    totals[name][0]+=cpu/1e9;totals[name][1]+=wall/1e9
  c.update(stage_events=len(events),event_outcomes=dict(collections.Counter(x['outcome']for x in events)),
    profiled_original_sources=len(per_source),unattributed_event_indices=unknown,
    stages_CPU_wall_seconds=dict(totals),
    product_LP_per_source_union_seconds={k:union(v)for k,v in per_source.items()},
    product_LP_global_union_seconds=union([i for v in per_source.values()for i in v]),
    interval_scope='Observed timed-wrapper intervals, not pure LP/product arithmetic or removable critical-path wall. Preprocess total includes legacy manual parse timing absent from spans. Term elaboration, omega, configured/uninstrumented paths and hard-killed finally records are not covered.')
  assert not unknown
 out['cells'][label]=c
ref=all_raw['frozen']
for label in ['diagnostic-off','diagnostic-on','diagnostic-on-v2']:
 assert set(ref)==set(all_raw[label])
 out['cells'][label]['native_outcome_difference_IDs']=[i for i in ref if H['verification_outcome'](ref[i])!=H['verification_outcome'](all_raw[label][i])]
 out['cells'][label]['raw_response_difference_IDs']=[i for i in ref if ref[i]['result'].get('response')!=all_raw[label][i]['result'].get('response')]
 assert not out['cells'][label]['native_outcome_difference_IDs']
# Reuse native outcomes from the complete same-resource original population for eight rejection cases.
with gzip.open(O.parent/'kimina-full29750-budgeted-20261019/full/rep1-native/results.jsonl.gz','rt')as z:
 complete={a['proof_id']:a for a in (json.loads(l)for l in z)}
neg=all_raw['diagnostic-rejected-v2']
out['cells']['diagnostic-rejected-v2']['matched_frozen_population_outcomes']=all(H['verification_outcome'](v)==H['verification_outcome'](complete[k])for k,v in neg.items())
assert out['cells']['diagnostic-rejected-v2']['matched_frozen_population_outcomes']
assert out['cells']['diagnostic-on-v2']['event_outcomes']=={'returned':115}
assert out['cells']['diagnostic-rejected-v2']['event_outcomes'].get('failed',0)>0
(O/'preflight-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{q:v for q,v in c.items()if q not in('resource','product_LP_per_source_union_seconds','interval_scope')}for k,c in out['cells'].items()},indent=2))
