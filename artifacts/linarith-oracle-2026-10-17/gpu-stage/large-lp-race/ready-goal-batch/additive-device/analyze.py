from pathlib import Path
import json,gzip,collections
A=Path(__file__).resolve().parent
def rows(p):
 with (gzip.open(p,'rt')if p.suffix=='.gz'else p.open()) as f:return [json.loads(l)for l in f]
R=A/'raw';out={}
base={x['proof_id']:x for x in rows(R/'cpu/rep1-fast-hybrid/responses.jsonl.gz')}
for label,method in [('native','fast-hybrid'),('cpu','oracle-highs'),('gpu','oracle-gpu')]:
 d=R/('gpu'if label=='gpu'else'cpu')/('rep1-'+method)
 t=json.loads((d/'terminal.json').read_text());rs={x['proof_id']:x for x in rows(d/'responses.jsonl.gz')}
 assert rs.keys()==base.keys()
 verdict=[k for k in base if(base[k]['outcome']!=rs[k]['outcome'])]
 non=[k for k in base if {a:b for a,b in base[k]['response'].items()if a!='messages'}!={a:b for a,b in rs[k]['response'].items()if a!='messages'}]
 assert not verdict and not non
 out[label]={'whole_seconds':t['whole_ns']/1e9,'counts':t['counts'],'observer_errors':t['sampling_read_errors'],'effective_RLIMIT_AS':t['effective_RLIMIT_AS'],
 'verdict_differences':verdict,'non_message_differences':non,'message_only_difference_IDs':[k for k in base if base[k]['response']!=rs[k]['response']]}
cpu={x['proof_id']:x for x in rows(R/'cpu/rep1-oracle-highs/responses.jsonl.gz')}
gpu={x['proof_id']:x for x in rows(R/'gpu/rep1-oracle-gpu/responses.jsonl.gz')}
out['CPU_GPU_full_JSON_differences']=[k for k in cpu if cpu[k]['response']!=gpu[k]['response']]
races=rows(R/'gpu/rep1-oracle-gpu/lp-races.jsonl.gz')
out['GPU_portfolio']={'races':len(races),'winners':dict(collections.Counter(x['winner']for x in races)),
 'missing_strong_CPU':sum(x.get('strong_cpu_pid')is None for x in races),
 'spawn_errors':[x['strong_cpu_spawn_error']for x in races if x.get('strong_cpu_spawn_error')],
 'retirement_errors':[{k:v for k,v in x.items()if k.endswith('_exit')}for x in races if any(e.get('wait_error')or e.get('kill_error')for e in [x.get('cpu_exit')or{},x.get('gpu_exit')or{},x.get('strong_cpu_exit')or{}])]}
for label in ['cpu','gpu']:
 p=R/label/'goal-batches.jsonl'
 ev=rows(p)if p.exists()else[]
 out[label]['goal_batch_outcomes']=dict(collections.Counter(x['outcome']for x in ev))
 out[label]['checked_problems']=sum(x['checked']for x in ev if x['outcome']=='checked')
 out[label]['native_problem_fallbacks']=sum(x['fallback']for x in ev if x['outcome']=='checked')
out['CPU_vs_native']=out['native']['whole_seconds']/out['cpu']['whole_seconds']
out['GPU_vs_native']=out['native']['whole_seconds']/out['gpu']['whole_seconds']
out['GPU_elapsed_change_vs_CPU']=out['gpu']['whole_seconds']/out['cpu']['whole_seconds']-1
out['scope']='One selected15-source/eightqueue/fourCPU8--11/48GiB warm-pipeline pair; common omega and ready-goal arguments, same private numerical build. Device cold lifecycle separate. Not1000/fullpopulation, confidence, GPU impossibility or novelty. Root self-review.'
(A/'matched-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
