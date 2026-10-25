"""Recompute accepted sets, resource-failure evidence and witness coverage."""
from pathlib import Path
import argparse,collections,csv,gzip,json,math,runpy
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--off',type=Path,required=True);p.add_argument('--on',type=Path,required=True)
 p.add_argument('--analysis',type=Path,required=True);a=p.parse_args()
 d=runpy.run_path(str(Path(__file__).with_name('analyze-screening.py')))
 rows=d['rows'];nt,n,tn=d['read_cell'](a.off);gt,g,tg=d['read_cell'](a.on)
 assert list(n)==list(g) and len(n)==7808
 accepted={k:sorted(i for i,x in data.items()if x['status']=='valid')for k,data in [('native',n),('gpu',g)]}
 accepted['native_only']=sorted(set(accepted['native'])-set(accepted['gpu']))
 accepted['gpu_only']=sorted(set(accepted['gpu'])-set(accepted['native']))
 (a.analysis/'accepted-sets.json').write_text(json.dumps(accepted,indent=2)+'\n')
 failures=[]
 for sid in n:
  if n[sid]['status']!='resource_failure'and g[sid]['status']!='resource_failure':continue
  row=dict(source_id=sid)
  for label,data,times in [('native',n,tn),('gpu',g,tg)]:
   x=data[sid];err=x['result'].get('error','')
   row.update({label+'_status':x['status'],label+'_HTTP_seconds':times[sid],
    label+'_allocation_failure':'std::bad_alloc' in err,
    label+'_error':err,label+'_failed_body_time_available':False})
  row['cause']='Native allocation failure under the configured 24GiB address-space limit; API reports std::bad_alloc.'
  row['exit_PID_source_join']='unknown: retained activity files contain final closed state; no ordering-based PID/source inference'
  failures.append(row)
 with(a.analysis/'resource-failures.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(failures[0]),lineterminator='\n');w.writeheader();w.writerows(failures)
 exit_summary={}
 for label,path,term in [('native',a.off,nt),('gpu',a.on,gt)]:
  exits=list(rows(path/'process-exits.jsonl'))
  exit_summary[label]=dict(records=len(exits),returncodes=dict(collections.Counter(str(x['returncode'])for x in exits)),
   bad_alloc_records=sum('std::bad_alloc'in x.get('stderr','')for x in exits),
   aggregate_watchdog_kills=term['memory_watchdog']['kills'],
   errors=[i for i in n if (n if label=='native'else g)[i]['status']=='resource_failure'])
 witness=sorted({x['source_id']for x in rows(a.on/'goals.jsonl')if x.get('answer',{}).get('exact_counterexample')})
 failed=sorted((i for i in n if n[i]['status']!='valid'),key=lambda i:(-tn[i],i))
 slow=failed[:math.ceil(len(failed)*.1)]
 detail=dict(resource_failure_sources=len(failures),exits=exit_summary,
  resource_failure_cause_limit='API allocation failures and per-process AS limits; not evidence of a global/cgroup OOM. Failed-body time 0 is unavailable timing, not zero work.',
  witness_sources=witness,witness_final_status_counts=dict(collections.Counter(n[i]['status']for i in witness)),
  witness_native_HTTP_sum_seconds=sum(tn[i]for i in witness),
  witness_native_body_sum_seconds=sum(n[i]['result'].get('time',0)or 0 for i in witness),
  witness_gpu_HTTP_sum_seconds=sum(tg[i]for i in witness),
  timeout_sources=[i for i in n if n[i]['status']=='timeout_error'],
  baseline_failed_sources=len(failed),baseline_slowest_10_percent_failed=slow,
  baseline_slowest_10_percent_failed_status_counts=dict(collections.Counter(n[i]['status']for i in slow)),
  native_seconds=nt['whole_lifecycle_seconds'],gpu_seconds=gt['whole_lifecycle_seconds'],
  gpu_extra_elapsed_percent=(gt['whole_lifecycle_seconds']/nt['whole_lifecycle_seconds']-1)*100)
 (a.analysis/'final-evidence.json').write_text(json.dumps(detail,indent=2)+'\n')
 print(json.dumps({k:v for k,v in detail.items()if not isinstance(v,list)and k!='exits'},indent=2))
if __name__=='__main__':main()
