'''Analyze remaining race costs on one completed current CPU-oracle clock.

Race labels "gpu" in a CPU-oracle run mean external CPU HiGHS, not CUDA.
Fixed-duration stage deletion is sensitivity only, not a strict Amdahl theorem.
'''
from pathlib import Path
import argparse,collections,importlib.util,json
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--input',type=Path,required=True);a=p.parse_args()
 spec=importlib.util.spec_from_file_location('batch_analysis',Path(__file__).with_name('analyze-batch.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 inputs=m.rows(a.input);ref=m.cell(a.root,'fast-hybrid',inputs);cell=m.cell(a.root,'oracle-highs',inputs)
 assert not cell['missing_candidate_spans']and not cell['unmatched_candidate_spans']
 races=m.rows(m.retained_file(a.root/'rep1-oracle-highs','lp-races.jsonl'))
 assert len(set((x['source'],x['call_id'])for x in races))==len(races)
 ids={x['source']:i for i,x in cell['byidx'].items()};byidx=collections.Counter();bywinner=collections.defaultdict(collections.Counter)
 unmatched=[]
 for x in races:
  key=x['source']
  if key not in ids:unmatched.append(x['call_id']);continue
  byidx[ids[key]]+=x['whole_ns']/1e9
  z=bywinner[x['winner']];z['count']+=1;z['decision_seconds']+=x['decision_ns']/1e9;z['whole_seconds']+=x['whole_ns']/1e9;z['retirement_seconds']+=x['retirement_ns']/1e9
 assert not unmatched
 calls=[x for x in cell['calls']if isinstance(x.get('input'),dict)]
 unparsed=len(cell['calls'])-len(calls)
 numeric=collections.Counter();callids=set()
 for x in calls:
  q=x['input'];reply=x['reply'];callids.add((q['source'],q['call_id']))
  for k in ['solver_seconds','build_ns','call_ns']:
   v=reply.get(k)
   if isinstance(v,(int,float)):numeric[k]+=v
  numeric['thread_cpu_ns']+=x['thread_cpu_ns']
 float_by_lane=collections.Counter()
 for x in calls:
  source=x['input']['source']
  assert source in ids
  float_by_lane[ids[source]//(len(inputs)//cell['terminal']['width'])]+=x['reply'].get('solver_seconds',0)
 intervals=[(x['start_ns'],x['end_ns'])for x in calls]
 whole=cell['terminal']['whole_ns']/1e9;native=ref['terminal']['whole_ns']/1e9
 n=len(inputs);width=cell['terminal']['width'];q,r=divmod(n,width);assert r==0,'equal-lane cohort required';origin=min(x['start_ns']for x in cell['byidx'].values());finish=max(x['end_ns']for x in cell['byidx'].values())
 durations={i:(x['end_ns']-x['start_ns'])/1e9 for i,x in cell['byidx'].items()}
 excess=[{'index':i,'race_seconds':v,'candidate_seconds':durations[i]}for i,v in byidx.items()if v>durations[i]+1e-6]
 lanes=[];start=0
 for lane in range(width):
  end=start+q+(lane<r);ix=list(range(start,end));xs=[cell['byidx'][i]for i in ix]
  assert all(xs[j]['start_ns']>=xs[j-1]['end_ns']for j in range(1,len(xs)))
  last=(xs[-1]['end_ns']-origin)/1e9;budget=sum(byidx[i]for i in ix)
  lanes.append({'lane':lane,'observed_last_end_seconds':last,'race_whole_sum_seconds':budget,'modeled_last_end_after_zero_races_seconds':last-budget,'external_HiGHS_solver_wall_sum_seconds':float_by_lane[lane],'modeled_last_end_after_zero_HiGHS_search_seconds':last-float_by_lane[lane]})
  start=end
 window=(finish-origin)/1e9
 model_whole=whole-window+max(x['modeled_last_end_after_zero_races_seconds']for x in lanes)
 out={'scope':'CURRENT completed full1000 third CPU-oracle, original sources/four CPUs/eight fixed native lanes/48GiB. No counters transferred from the older stacked-header or hybrid diagnostic acquisitions. CPU external solver labels are legacy names, not CUDA.',
 'threshold_1_5_candidate_whole_seconds':native/1.5,'current_third_pair_shortfall_seconds':whole-native/1.5,
 'count':n,'native_whole_seconds':native,'CPU_oracle_whole_seconds':whole,'actual_native_over_CPU_oracle':native/whole,
 'race_calls':len(races),'race_keys_unique':True,'race_calls_per_winner':dict(bywinner),
 'race_whole_sum_seconds':sum(byidx.values()),'race_sum_divided_by_whole':sum(byidx.values())/whole,
 'race_scope':'Full speculative numeric stage: worker launch, CPU hybrid versus CPU HiGHS, exact positive/negative repair/check, cancellation and wait. Not pure LP work and not a disjoint whole-pipeline wall share. Small ineligible LPs and product expansion have no complete current-phase attribution here.',
 'parsed_external_HiGHS_calls':len(calls),'unparsed_or_aborted_connections':unparsed,
 'external_HiGHS_observed_totals':dict(numeric),
 'external_HiGHS_connection_interval_union_seconds':m.intervals_union(intervals),
 'external_HiGHS_interval_union_divided_by_whole':m.intervals_union(intervals)/whole,
 'external_scope':'solver_seconds is per-call solver WALL, summed across calls; not CPU work or removable end-to-end time. Parsed calls omit workers cancelled before full JSON reception, retained as unparsed/aborted connections, not invented LP outcomes. Connection union includes receiving/build/serialization; it is not GPU-replaceable wall.',
 'source_race_budget_exceeds_candidate_span':excess,
 'zero_race_fixed_lane_model':{'lanes':lanes,'modeled_whole_seconds':model_whole,
 'modeled_native_over_oracle':native/model_whole,
 'modeled_oracle_acceleration':whole/model_whole,
 'zero_external_HiGHS_search_only_modeled_whole_seconds':whole-window+max(x['modeled_last_end_after_zero_HiGHS_search_seconds']for x in lanes),
 'zero_external_HiGHS_search_only_modeled_native_ratio':native/(whole-window+max(x['modeled_last_end_after_zero_HiGHS_search_seconds']for x in lanes)),
 'assumptions':'Delete ENTIRE recorded race stage, including non-GPU repair/launch/retirement; preserve observed lane assignments, all outside-race durations and gaps. Contention/durations can change. Source keys join exactly but no absolute race-start/end interval trace exists. Not measured performance, scheduler-independent bound, or a proof allowing GPU route closure. Missing product/small-LP phase attribution prevents exhaustive replacement coverage.'}}
 (a.root/'current-race-budget.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
