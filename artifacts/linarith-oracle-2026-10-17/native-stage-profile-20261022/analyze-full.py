"""Analyze only the complete original1000 diagnostic pair; no cross-run phase rescaling."""
from pathlib import Path
import json,gzip,runpy,collections,math,csv,sys
O=Path(__file__).resolve().parent;R=O.parents[2]
F=runpy.run_path(str(O.parent/'kimina-full29750-budgeted-20261019/analyze.py'))
H=F['H']
def rows(p):return F['rows'](p)
def body(s):
 a=s.splitlines()
 while a and(not a[0].strip()or a[0].startswith('import ')):a.pop(0)
 return '\n'.join(a).strip()
def union(xs):
 end=None;total=0
 for a,b in sorted(xs):
  if end is None:total=b-a;end=b
  elif a>=end:total+=b-a;end=b
  elif b>end:total+=b-end;end=b
 return total/1e9
items=list(rows(O.parent/'input-top1000.jsonl'));expected=[a['proof_id']for a in items]
assert len(expected)==len(set(expected))==1000
bybody=collections.defaultdict(list)
for a in items:bybody[body(a['code'])].append(a['proof_id'])
def ident(source):
 matches=bybody.get(body(source),[])
 return matches[0]if len(matches)==1 else None
profile_label=sys.argv[1]if len(sys.argv)>1 else 'full-profile-v2'
assert profile_label in('full-profile-v2','reference-full1000')
labels=['full-frozen',profile_label]
for label in labels:
 p=O/label/'terminal.json'
 if not p.exists()or json.loads(p.read_text())['state']!='complete':
  raise SystemExit('Both original1000cells must be terminal complete; no live file or partial prefix is analyzed.')
cells={};data={};lat={}
for label in labels:cells[label],data[label],lat[label]=F['closed_cell'](O/label,expected)
profile=O/profile_label;terminal=cells[profile_label]['terminal']
intervals=collections.defaultdict(list);stages=collections.defaultdict(lambda:[0.,0.]);source_events=collections.Counter()
source_stages=collections.defaultdict(lambda:collections.defaultdict(lambda:[0.,0.]));outcomes=collections.Counter();unknown=[]
http={};pending={}
for e in rows(profile/'http.jsonl'):
 if e['event']=='request':
  i=json.loads(e['body'])['snippets'][0]['id'];pending[e['start_ns']]=i
  if i in expected:http[i]=[e['start_ns'],None]
 else:
  i=pending.pop(e['start_ns'])
  if i in http:http[i][1]=e['end_ns']
assert not pending
outside=[];event_count=0
for x in rows(profile/'native-stages.jsonl'):
 event_count+=1;i=ident(x['source']);outcomes[x['outcome']]+=1
 if i is None:unknown.append(event_count);continue
 source_events[i]+=1
 for name,(cpu,wall)in x['stages'].items():
  stages[name][0]+=cpu/1e9;stages[name][1]+=wall/1e9
  source_stages[i][name][0]+=cpu/1e9;source_stages[i][name][1]+=wall/1e9
 for name,a,b in x['spans']:
  assert x['start_ns']<=a<=b<=x['end_ns']
  if not(http[i][0]<=a<=b<=http[i][1]):outside.append({'id':i,'stage':name,'start_ns':a,'end_ns':b})
  if name in('products','lp'):intervals[i].append((a,b))
omega=collections.Counter();unknown_omega=[]
for x in rows(profile/'omega-control.jsonl'):
 i=ident(x['source'])
 if i is None:unknown_omega.append(x)
 else:omega[i]+=1
whole=terminal['whole_lifecycle_seconds']
intervalsum=sum(union(v)for v in intervals.values())
globalunion=union([span for values in intervals.values()for span in values])
diff=[i for i in expected if F['native_outcome'](data[labels[0]][i])!=F['native_outcome'](data[labels[1]][i])]
rawdiff=[i for i in expected if data[labels[0]][i]['result'].get('response')!=data[labels[1]][i]['result'].get('response')]
tails={}
for fraction in (.01,.1):
 ids=sorted(expected,key=lambda i:lat[labels[0]][i],reverse=True)[:math.ceil(len(expected)*fraction)]
 total=collections.defaultdict(lambda:[0.,0.])
 for i in ids:
  for k,v in source_stages[i].items():
   total[k][0]+=v[0];total[k][1]+=v[1]
 tails[str(fraction)]=dict(IDs=ids,profile_stages_CPU_wall_seconds=dict(total),
  native_outcomes=dict(collections.Counter(F['native_outcome'](data[labels[0]][i])for i in ids)),
  profile_outcomes=dict(collections.Counter(F['native_outcome'](data[labels[1]][i])for i in ids)),
  native_overlapping_HTTP_seconds=sum(lat[labels[0]][i]for i in ids),
  profile_overlapping_HTTP_seconds=sum(lat[labels[1]][i]for i in ids))
out=dict(scope='Complete original1000 native-algorithm diagnostic. Root self-review; wrapper timings are not pure solver work or a strict GPU ceiling.',
 conditions=cells,native_outcome_difference_IDs=diff,raw_response_difference_IDs=rawdiff,
 profile_events=event_count,pipeline_outcomes=dict(outcomes),unknown_profile_events=unknown,
 stage_CPU_wall_seconds=dict(stages),profiled_sources=len(source_events),omega_sources=len(omega),
 source_IDs_without_profile_or_omega=[i for i in expected if i not in source_events and i not in omega],
 unknown_omega_events=unknown_omega,profile_intervals_outside_own_HTTP=outside,
 own_profile_whole_seconds=whole,product_LP_per_source_interval_union_sum_seconds=intervalsum,
 product_LP_global_interval_union_seconds=globalunion,
 product_LP_observed_global_occupancy=globalunion/whole,
 sum_deleted_envelope_sensitivity=whole/(whole-intervalsum)if intervalsum<whole else None,
 sensitivity_scope='Fixed-observed-envelope optimistic deletion only. Overlapping/request-wait wrappers are not additive removable critical path; null means sum>=whole, not zero speedup. Never a strict GPU impossibility bound.',
 instrumentation_ratio_profile_over_frozen=whole/cells['full-frozen']['terminal']['whole_lifecycle_seconds'],
 native_ranked_matched_tails=tails,
 limitations=['Own instrumented denominator only; no2234.69/810.71/full29750rescaling.',
 'LPwrapper includes packing, IPC and repair; products include native proof generation.',
 'Preprocess legacy manual parse timing has no interval.',
 'Term elaboration, omega, configured or indirect stock calls and finally lost to hard death are not exhaustively covered.',
 'Concurrent phase/HTTP sums are not isolated CPU or removable wall.',
 'Single fixed-order/shared-host pair does not establish zero overhead or GPU acceleration.'])
(O/('full-analysis.json'if profile_label=='full-profile-v2'else 'reference-stage-analysis.json')).write_text(json.dumps(out,indent=2)+'\n')
with(O/('full-source-costs.csv'if profile_label=='full-profile-v2'else 'reference-stage-source-costs.csv')).open('w',newline='')as z:
 w=csv.writer(z);w.writerow(['proof_id','frozen_outcome','profile_outcome','frozen_HTTP_seconds','profile_HTTP_seconds','profile_events','omega_events','product_LP_interval_union_seconds','profile_stage_CPU_wall_seconds'])
 for i in expected:w.writerow([i,F['native_outcome'](data[labels[0]][i]),F['native_outcome'](data[labels[1]][i]),lat[labels[0]][i],lat[labels[1]][i],source_events[i],omega[i],union(intervals[i])if i in source_events else None,json.dumps(dict(source_stages[i]))])
print(json.dumps({k:v for k,v in out.items()if k not in('conditions','native_ranked_matched_tails','limitations','sensitivity_scope')},indent=2))
