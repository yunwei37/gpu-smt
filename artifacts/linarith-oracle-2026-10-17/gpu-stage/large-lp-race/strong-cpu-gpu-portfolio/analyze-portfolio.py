from pathlib import Path
import collections,gzip,json,sys
p=Path(sys.argv[1])
read=lambda q:[json.loads(l)for l in gzip.open(q,'rt')]
races=read(p/'qualification64-gpu/rep1-oracle-gpu/lp-races.jsonl.gz')
calls=read(p/'qualification64-gpu/rep1-oracle-gpu-strong-cpu-backend/support-calls.jsonl.gz')
cpu=read(p/'qualification64-cpu/rep1-oracle-highs/responses.jsonl.gz')
gpu=read(p/'qualification64-gpu/rep1-oracle-gpu/responses.jsonl.gz')
assert len(cpu)==len(gpu)==64
for x,y in zip(cpu,gpu):assert x['proof_id']==y['proof_id']
out={'race_count':len(races),'winners':dict(collections.Counter(x['winner']for x in races)),
'races_missing_strong_cpu_pid':sum(x.get('strong_cpu_pid')is None for x in races),
'strong_cpu_spawn_errors':[x['strong_cpu_spawn_error']for x in races if x.get('strong_cpu_spawn_error')],
'any_wait_or_kill_error':[{k:v for k,v in x.items()if k.endswith('_exit')}for x in races if any(e.get('wait_error')or e.get('kill_error')for e in [x.get('cpu_exit')or{},x.get('gpu_exit')or{},x.get('strong_cpu_exit')or{}])],
'retained_CPU_HiGHS_proxy_connections':len(calls),
'retained_CPU_HiGHS_proxy_parsed':sum(isinstance(x.get('input'),dict)for x in calls),
'full_CPU_GPU_response_difference_proof_ids':[x['proof_id']for x,y in zip(cpu,gpu)if x['response']!=y['response']or x['outcome']!=y['outcome']],
'scope':'Exact repaired certificates/negative evidence selected in native coordinator. CPU-HiGHS and GPU winners are separate. Original sources/outcomes retained. First observed valid certificate does not establish no overhead or causal time saved.'}
(p/'portfolio-engagement-analysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
