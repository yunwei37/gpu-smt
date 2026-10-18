"""Measure fixed native-lane imbalance; FIFO model is not a performance result."""
from pathlib import Path
import argparse,collections,heapq,importlib.util,json

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('root',type=Path);p.add_argument('--input',type=Path,required=True)
 p.add_argument('--method',default='fast-hybrid');a=p.parse_args()
 spec=importlib.util.spec_from_file_location('native_analysis',Path(__file__).with_name('analyze-batch.py'))
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 inputs=m.rows(a.input);cell=m.cell(a.root,a.method,inputs);terminal=cell['terminal']
 if cell['missing_candidate_spans']or cell['unmatched_candidate_spans']:raise ValueError('complete exact source timing required')
 width=terminal['width'];n=len(inputs);q,r=divmod(n,width);start=0;lanes=[]
 spans=cell['byidx'];origin=min(x['start_ns']for x in spans.values())
 finish=max(x['end_ns']for x in spans.values());window=(finish-origin)/1e9
 durations=[(spans[i]['end_ns']-spans[i]['start_ns'])/1e9 for i in range(n)]
 for lane in range(width):
  stop=start+q+(lane<r);ids=list(range(start,stop));xs=[spans[i]for i in ids]
  overlaps=[ids[k]for k in range(1,len(xs))if xs[k]['start_ns']<xs[k-1]['end_ns']]
  lanes.append({'lane':lane,'first_index':start,'past_last_index':stop,
   'candidate_count':len(ids),'task_span_sum_seconds':sum(durations[i]for i in ids),
   'first_start_seconds':(xs[0]['start_ns']-origin)/1e9,
   'last_end_seconds':(xs[-1]['end_ns']-origin)/1e9,
   'same_lane_overlaps':overlaps})
  start=stop
 events=[]
 for x in spans.values():events.extend([(x['start_ns'],1),(x['end_ns'],-1)])
 histogram=collections.Counter();active=0;prior=origin;peak=0
 for tick,delta in sorted(events):
  histogram[active]+=(tick-prior)/1e9;active+=delta;prior=tick;peak=max(peak,active)
 assert active==0 and start==n
 fifo=[(0.,i)for i in range(width)];heapq.heapify(fifo)
 for duration in durations:
  when,lane=heapq.heappop(fifo);heapq.heappush(fifo,(when+duration,lane))
 modeled=max(x[0]for x in fifo)
 whole=terminal['whole_ns']/1e9
 cpu=sum(x['user']+x['system']for x in terminal['cpu'].values())
 out={'scope':'Complete native candidate intervals, actual fixed contiguous upstream lanes. FIFO model preserves input order, width and each observed task duration. Durations depend on contention; modeled wall is illustrative, NOT measured speedup, causal savings, an Amdahl bound or an admission to change a running capture.',
  'count':n,'width':width,'method':a.method,'whole_seconds':whole,
  'observed_candidate_window_seconds':window,'maximum_observed_active_candidates':peak,
  'active_candidate_occupied_seconds':dict(sorted(histogram.items())),
  'slot_occupancy_fraction_in_window':sum(durations)/(width*window),
  'reported_process_CPU_seconds':cpu,
  'reported_CPU_divided_by_four_core_whole':cpu/(4*whole),
  'CPU_scope':'Reported collector+waited-children accounting, not proven exhaustive descendant or physical idle-time measurement. Four CPUs are the declared cohort condition, not a hardware utilization counter.',
  'lane_summaries':lanes,
  'FIFO_fixed_duration_model_window_seconds':modeled,
  'FIFO_fixed_duration_model_whole_seconds':whole-window+modeled,
  'FIFO_fixed_duration_model_window_ratio':window/modeled}
 target=a.root/('lane-balance-'+a.method+'.json')
 target.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
