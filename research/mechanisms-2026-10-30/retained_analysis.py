"""Retained-data mechanism opportunity census and peak-reservation sensitivity model.
This does not infer a dependency DAG from syntax or replay native outcomes under a new RSS budget.
"""
from pathlib import Path
import collections,gzip,json,heapq,random
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PAIR=ROOT/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
def gz(p):
 with gzip.open(p,'rt') as f:return json.load(f)
def model(rows,budget,mode):
 waiting=list(rows);active=[];now=0.;seq=0;done=[];killed=[];overshoot=0;peak=0
 while waiting or active:
  if mode=='admission':
   i=0
   while len(active)<4 and i<len(waiting):
    row=waiting[i]
    if sum(x[2]['peak'] for x in active)+row['peak']<=budget:
     waiting.pop(i);seq+=1;heapq.heappush(active,(now+row['cost'],seq,row,now))
    else:i+=1
  else:
   while waiting and len(active)<4:
    row=waiting.pop(0);seq+=1;heapq.heappush(active,(now+row['cost'],seq,row,now))
  used=sum(x[2]['peak'] for x in active);peak=max(peak,used)
  if mode=='kill' and used>budget:
   # Memory trajectory is unavailable: an instantaneous-peak stress model.
   victim=max(active,key=lambda x:x[2]['peak'])
   active.remove(victim);heapq.heapify(active);killed.append(victim[2]);continue
  if not active:
   assert not waiting, 'All modeled jobs must individually fit the selected point'
   break
  end,_,row,start=heapq.heappop(active)
  if used>budget:overshoot+=end-now
  now=end;done.append(row)
 return {'mode':mode,'makespan_proxy_s':now,'frozen_label_survivors':len(done),
  'frozen_terminal_goodput_proxy_per_s':len(done)/now if now else None,'modeled_operational_kills':len(killed),
  'modeled_accepted_suppressed':sum(x['accepted'] for x in killed),
  'accepted_surviving':sum(x['accepted'] for x in done),'over_budget_proxy_s':overshoot,
  'peak_sum_reserved_bytes':peak,'never_over_reserved_budget_in_model':peak<=budget}
def main():
 data=gz(PAIR/'engine.stdout.gz');inputs={x['id']:x for x in gz(PAIR/'input7808.json.gz')['candidates']}
 rows=[]
 for x in data['results']:
  assert x['attempts']
  peaks=[a['peak_rss_bytes'] for a in x['attempts']]
  rows.append({'id':x['id'],'task':inputs[x['id']]['task_id'],'status':x['outcome']['status'],
   'accepted':x['outcome']['status']=='accepted','cost':sum(a['elapsed_seconds'] for a in x['attempts']),
   'peak':max(peaks),'attempts':len(x['attempts']),
   'censored':x['outcome']['status'] in ['resource_exhausted','timeout']})
 assert len(rows)==7808 and len({x['id'] for x in rows})==7808
 profile=json.loads((ROOT/'artifacts/lean-failure-profile-2026-10-25/full480-analysis/per-source.json').read_text())
 prof={x['source_id']:x for x in profile}
 with gzip.open(ROOT/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/native-units.jsonl.gz','rt') as f:
  syntax={x['proposalId']:x for l in f if (x:=json.loads(l))['proposalId'] in inputs}
 strata={'accepted':50,'rejected':60,'timeout':50,'resource_exhausted':40}
 selected=[]
 for status,count in strata.items():
  group=sorted([x for x in rows if x['status']==status],key=lambda x:(x['cost'],x['id']))
  assert len(group)>=count
  selected += [group[(i*len(group))//count] for i in range(count)]
 census=[];tot=collections.Counter()
 for x in selected:
  u=syntax.get(x['id']);units=(u or {}).get('units',[])
  count=collections.Counter()
  for unit in units:
   k=unit['syntaxKind'];text=unit['text'].strip()
   if 'tacticHave' in k:count['have_units']+=1
   if k.endswith('.case') or k.endswith('.caseTag'):count['case_units']+=1
   if '<;>' in text:count['and_then_containing_units']+=1
   if 'all_goals' in text:count['all_goals_containing_units']+=1
   if text.startswith('first'):count['first_units']+=1
  p=prof.get(x['id'])
  d={**x,'native_syntax_available':u is not None,'native_top_level_units':len(units),
    'source_structure_counts':dict(count),'prior_profile_available':p is not None,
    'prior_measured_profile_exclusive_CPU_s':p['measured_exclusive_cpu_seconds'] if p else None,
    'prior_profile_body_s':p.get('profile_body_seconds') if p else None,
    'work_DAG_s':None,'critical_path_DAG_s':None,'average_available_parallelism':None,
    'shared_metavariable_edges':None,'reason':'Prior exported Syntax/aggregated profile does not retain per-call mctx dependency DAG or per-node aligned durations.'}
  census.append(d);tot.update(count)
 out=HERE/'retained-analysis';out.mkdir(exist_ok=True)
 (out/'stratified200.json').write_text(json.dumps({'strata':strata,'selected':census,'total_source_structure_counts':dict(tot),
   'profiled_selected':sum(x['prior_profile_available'] for x in census),'fresh_Lean_executions':0,
   'conclusion':'The requested DAG parallelism remains unknown; syntactic have/case/<;>/first counts are not independent tasks or proof of A>=1.3.'},indent=2)+'\n')
 matrix=[]
 for percore in [2,4,8,12]:
  budget=4*percore*1024**3
  fit=[x for x in rows if 0<x['peak']<=budget];excluded=[x for x in rows if x not in fit]
  matrix.append({'per_core_GiB':percore,'cores':4,'aggregate_budget_bytes':budget,
    'coverage_fit_sources':len(fit),'excluded_observed_peak_above_budget_or_missing':len(excluded),
    'excluded_original_accepted':sum(x['accepted'] for x in excluded),
    'censored_sources_in_fit':sum(x['censored'] for x in fit),
    'subset_original_accepted':sum(x['accepted'] for x in fit),
    'policies':[model(fit,budget,k) for k in ['fixed','kill','admission']]})
 result={'source_point':str(PAIR.relative_to(ROOT)),'sources':len(rows),'matrix':matrix,
  'scope':['Frozen sum of physical attempt times; consumer queue latency is excluded.',
    'Observed peak reservation is hindsight, not an online predictor. Memory demand is flat at observed peak; no memory trajectory is invented.',
    'Kill model detects pressure immediately at dispatch and has optimistic zero kill/cleanup overhead; native labels for killed work are unavailable, never logical rejection.',
    'Admission charges each full recorded peak, including any parent contribution. No unmeasured COW memory discount is introduced; actual sharing advantage is unidentified.',
    'Every policy compares the SAME budget-fit subset at each point. Excluded original accepted/censored jobs remain visible; this is not full7808 throughput.',
    'Timeout/resource peaks are censored. New host load can change operational outcomes; true same-budget native verdict parity requires a real paired run.',
    'Model goodput counts surviving original terminal outcomes, so dropping difficult jobs is not reported as verification acceleration.']}
 (out/'memory-matrix.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'stratified_sources':len(census),'profiled_selected':sum(x['prior_profile_available'] for x in census),'structure':dict(tot),
  'memory_rows':[{k:v for k,v in x.items() if k!='policies'} for x in matrix]},indent=2))
 for m in matrix:print(m['per_core_GiB'],json.dumps(m['policies']))
if __name__=='__main__':main()
