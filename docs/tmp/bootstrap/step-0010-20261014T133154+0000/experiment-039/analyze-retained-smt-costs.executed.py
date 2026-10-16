"""Reuse complete retained SMT parent-phase events; no new solver execution."""
from pathlib import Path
import collections,datetime,gzip,json,statistics,time
R=Path('/workspaces/repository')
E=Path(__file__).parent
B=R/'artifacts/autoverus-native-2026-10-09/experiment025/full-registry-repaired1'
D=E/'retained-smt-prefix-costs';D.mkdir(exist_ok=True)
def dist(v):
 v=sorted(v)
 return {'n':len(v),'min':min(v),'median':statistics.median(v),'max':max(v),'sum':sum(v)} if v else {'n':0}
rows=[]
for block in ['rep0','rep1','rep2','profile']:
 for method in ['branch','logical']:
  p=B/(block+'-'+method)/'service/service.jsonl'
  raw=p.read_bytes();events=[json.loads(x) for x in raw.splitlines()]
  prep=[(i,x) for i,x in enumerate(events) if x.get('kind')=='parent-preparation']
  closes=[x for x in events if x.get('kind') in ['parent-eviction','parent-terminal']]
  lookups=[x for x in events if x.get('kind')=='online-lookup']
  matches=[x for x in lookups if x.get('route')=='retained-native-branch']
  kindcounts=dict(collections.Counter(x.get('kind') for x in events))
  assert kindcounts.get('service-start')==kindcounts.get('service-terminal')==1
  assert len(prep)==473 and len(closes)==473
  assert len({x['pid'] for _,x in prep})==len(prep)
  assert {x['pid'] for _,x in prep}=={x['pid'] for x in closes}
  dest=D/(block+'-'+method+'.service.jsonl.gz')
  with gzip.open(dest,'wb',compresslevel=6) as out:out.write(raw)
  assert gzip.open(dest,'rb').read()==raw
  rows.append({'block':block,'method':method,'role':'separate resource profile' if block=='profile' else 'primary whole observation','original_events':str(p.relative_to(R)),'published_raw':str(dest.relative_to(R)),'event_counts':kindcounts,'parent_preparations':len(prep),'supported_preparations':sum(x['supported'] for _,x in prep),'distinct_prefix_identity_count':len({x['prefix_sha256'] for _,x in prep}),'native_parent_CPU_to_readiness_seconds':dist([x['native_cpu_s'] for _,x in prep]),'native_prepare_wall_seconds':dist([x['native_wall_s'] for _,x in prep]),'launch_to_ready_wall_seconds':dist([x['launch_ready_wall_s'] for _,x in prep]),'started_reuse_selections':sum(x.get('parent_miss') is False for x in matches),'new_parent_selections':sum(x.get('parent_miss') is True for x in matches),'parent_lifetime_close_records':len(closes),'nonzero_parent_close_codes':[x for x in closes if x.get('returncode',x.get('terminal_returncode')) not in (None,0)],'original_plan_scope':'complete original3566source Verus cohort, native outputs/failures and logical annotations unchanged; no new execution or exclusive resources','CPU_meaning':'native parent getrusage SELF cumulative from process birth at first ready; includes init before serve and excludes future child suffix CPU, launcher/transport/Verus/observer; never wholeCPU fraction or hypothetical saved work','wall_meaning':'native prepare steady_clock interval inside serve; launch-ready includes parent startup; nested and possibly overlapping intervals, do not sum as makespan or add CPU+wall','preparation_records':[{'line_index0':i,**x} for i,x in prep]})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_RQ':'RQ1','scope':'reuse already-completed repaired-registry SMT phase evidence; no new matrix, fork/solver variant, CPU share, counterfactual savings, verification-equivalence or novel system claim','counter_source':'logical-hit-refusal-diagnosis-20261015/native_parent.registry-repaired.cpp serve getrusage(RUSAGE_SELF) before first ready; native_service.py Parent emits once per native process','cells':rows}
(D/'analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{k:v[k] for k in ['block','method','parent_preparations','started_reuse_selections','native_parent_CPU_to_readiness_seconds','launch_to_ready_wall_seconds']} for v in rows],indent=2))
