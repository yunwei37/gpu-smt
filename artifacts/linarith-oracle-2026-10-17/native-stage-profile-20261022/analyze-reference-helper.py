"""Closed-only helper attribution, nested intervals excluded; root self-review."""
from pathlib import Path
import collections,csv,gzip,json,runpy,sys,math
O=Path(__file__).resolve().parent
F=runpy.run_path(str(O.parent/'kimina-full29750-budgeted-20261019/analyze.py'))
def rows(p):return F['rows'](p)
def body(s):
 a=s.splitlines()
 while a and(not a[0].strip()or a[0].startswith('import ')):a.pop(0)
 return '\n'.join(a).strip()
items=list(rows(O.parent/'input-top1000.jsonl'));ids=[x['proof_id']for x in items]
bybody=collections.defaultdict(list)
for x in items:bybody[body(x['code'])].append(x['proof_id'])
def ident(s):
 a=bybody[body(s)]if isinstance(s,str)else []
 return a[0]if len(a)==1 else None
def union(xs):
 total=0;end=None
 for a,b in sorted(xs):
  if end is None or a>=end:total+=b-a;end=b
  elif b>end:total+=b-end;end=b
 return total/1e9
full='full'in sys.argv[1:]
labels=['reference-full1000']if full else ['reference-frozen24','reference-off24','reference-on24','reference-rejected8']
reject={'Proof_00710','Proof_12175','Proof_15022','Proof_15224','Proof_16530','Proof_17093','Proof_20359','Proof_25649'}
expected={label:(ids if full else [i for i in ids if i in reject]if label.endswith('rejected8')else ids[:24])for label in labels}
cells={};data={};lat={}
for label in labels:
 p=O/label/'terminal.json'
 if not p.exists()or json.loads(p.read_text())['state']!='complete':raise SystemExit('Required cells are not all terminal complete')
 cells[label],data[label],lat[label]=F['closed_cell'](O/label,expected[label])
reference_label='full-frozen'if full else 'reference-frozen24'
reference_ids=ids if full else ids[:24]
ref_t,ref_data,ref_lat=F['closed_cell'](O/reference_label,reference_ids)
_,negative_data,_=F['closed_cell'](O/'full-frozen',ids)
out={'scope':'Own-clock native reference helper diagnostic; root self-review; no GPU execution or strict upper bound.','conditions':cells,'comparisons':{},'profiles':{}}
for label in labels:
 ref=negative_data if label.endswith('rejected8')else ref_data
 out['comparisons'][label]={
  'native_outcome_difference_IDs':[i for i in expected[label]if F['native_outcome'](data[label][i])!=F['native_outcome'](ref[i])],
  'raw_response_difference_IDs':[i for i in expected[label]if data[label][i]['result'].get('response')!=ref[i]['result'].get('response')]}
 if not cells[label]['terminal'].get('reference_phases'):continue
 spans=[];pending={};invalid=[];source_map={};pairs=collections.defaultdict(list)
 for x in rows(O/label/'native-helper-phases.jsonl'):
  key=(x['pid'],x['tid'],x['id'])
  if x['event']=='begin':
   if key in pending:raise AssertionError('duplicate begin')
   pending[key]=x
   if x['stage']=='native_reference_request':
    ck=(x['pid'],x['call_id']);i=ident(x.get('source'));source_map[ck]=i
  else:
   a=pending.pop(key,None)
   if a is None:invalid.append(x);continue
   assert a['stage']==x['stage']and a['call_id']==x['call_id']
   assert x['wall_ns']>=a['wall_ns']and x['thread_cpu_ns']>=a['thread_cpu_ns']
   spans.append(dict(stage=x['stage'],source_key=(x['pid'],x['call_id']),a=a['wall_ns'],b=x['wall_ns'],cpu=(x['thread_cpu_ns']-a['thread_cpu_ns'])/1e9))
 totals=collections.defaultdict(lambda:[0.,0.,0]);sourcecost=collections.defaultdict(lambda:collections.defaultdict(lambda:[0.,0.,0]))
 unknown=[];requests={};outside=[]
 for v in spans:
  totals[v['stage']][0]+=v['cpu'];totals[v['stage']][1]+=(v['b']-v['a'])/1e9;totals[v['stage']][2]+=1
  i=source_map.get(v['source_key'])
  if i is None:unknown.append(v);continue
  q=sourcecost[i][v['stage']];q[0]+=v['cpu'];q[1]+=(v['b']-v['a'])/1e9;q[2]+=1
  pairs[v['source_key']].append(v)
  if v['stage']=='native_reference_request':requests[v['source_key']]=v
 residual=0;pure_cpu=0;pure_wall=0;repair_exclusive=0
 for key,vs in pairs.items():
  rq=requests.get(key)
  if rq is None:outside.extend(vs);continue
  nested=[v for v in vs if v['stage']!='native_reference_request']
  for v in nested:
   if not(rq['a']<=v['a']<=v['b']<=rq['b']):outside.append(v)
  residual+=(rq['b']-rq['a'])/1e9-union([(v['a'],v['b'])for v in nested])
  lp=[v for v in nested if v['stage']in('lp_float_solve','lp_exact_solve')]
  pure_wall+=union([(v['a'],v['b'])for v in lp]);pure_cpu+=sum(v['cpu']for v in lp)
  for v in nested:
   if v['stage']=='exact_repair':
    checks=[z for z in nested if z['stage']=='exact_certificate_verify'and v['a']<=z['a']<=z['b']<=v['b']]
    repair_exclusive+=(v['b']-v['a'])/1e9-union([(z['a'],z['b'])for z in checks])
 whole=cells[label]['terminal']['whole_lifecycle_seconds']
 out['profiles'][label]=dict(stage_CPU_wall_count=dict(totals),pending_begin_events=list(pending.values()),unmatched_end_events=invalid,
  source_owned_requests=len(requests),profiled_sources=len(sourcecost),unknown_phase_records=len(unknown),phase_records_outside_own_request=len(outside),
  FP_solver_plus_exact_fallback_envelope_CPU_seconds=pure_cpu,FP_solver_plus_exact_fallback_envelope_accumulated_wall_seconds=pure_wall,
  exact_repair_wall_excluding_nested_verify_seconds=repair_exclusive,
  request_wall_outside_recorded_inner_stage_union_seconds=residual,own_whole_seconds=whole,
  per_source_stages={i:dict(v)for i,v in sourcecost.items()},
  limitations=['Nested stage sums overlap; exact repair exclusive subtracts nested verification only.',
   'Whole/request wall includes preparation, packing, communication, logging, cancellation and cleanup; no historical rescaling.',
   'Request guard starts after initial context JSON parse and ends before stdout flush; residual is not all IPC.',
   'Non-helper/stock calls, omega and hard-death missing events are not silently pure LP or zero.',
   'Exact fallback includes matrix construction, coefficient conversion and rational cleanup, not only pivot loops.',
   'No LP shapes are emitted here; no GPU batches or theorem-level speedups are inferred.'])
name='reference-full-analysis.json'if full else 'reference-preflight-analysis.json'
(O/name).write_text(json.dumps(out,indent=2)+'\n')
compact={k:v for k,v in out.items()if k!='conditions'}
for v in compact['profiles'].values():v.pop('per_source_stages',None)
print(json.dumps(compact,indent=2))
