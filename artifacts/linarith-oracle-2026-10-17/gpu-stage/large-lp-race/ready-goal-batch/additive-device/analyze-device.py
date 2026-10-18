from pathlib import Path
import json,gzip,collections
A=Path(__file__).resolve().parent
def rows(p):
 data=gzip.decompress(p.read_bytes())if p.read_bytes().startswith(b'\x1f\x8b')else p.read_bytes()
 out=[]
 for l in data.decode().splitlines():
  try:out.append(json.loads(l))
  except json.JSONDecodeError:pass
 return out
provider=rows(A/'ready-goal-additive15-backend.log.gz')
launch=[x for x in provider if x.get('event')=='launch'];models=[x for x in provider if 'state'in x];retired=[x for x in provider if x.get('event')=='batch_retired']
expected={k for x in launch for k in x['keys']};assert expected=={x['key']for x in models}
assert{v['batch_id']for v in launch}=={x['batch_id']for x in retired}
proxy=rows(A/'raw/gpu/rep1-oracle-gpu-backend/support-calls.jsonl.gz')
strong=rows(A/'raw/gpu/rep1-oracle-gpu-strong-cpu-backend/support-calls.jsonl.gz')
timers=[x for x in models if x.get('device_globaltimer_interval')]
probe=json.loads(json.loads((A/'provider-probe.json').read_text()))
receipt=json.loads((A/'ready-goal-additive15-cleanup.json').read_text())
assert probe['live_allocations']==0 and probe['live_device_bytes']==0
assert receipt['qualifierExit']==receipt['deleteExit']==0 and receipt['labReady']=='True'and receipt['otherWorkspacePhase']=='Running'
out={'launched_groups':len(launch),'group_sizes':[x['batch_size']for x in launch],
 'distinct_candidate_sources_by_group':[x['distinct_sources']for x in launch],
 'models':len(models),'model_states':dict(collections.Counter(x['state']for x in models)),
 'model_iterations':[x['iterations']for x in models],'device_timed_models':len(timers),
 'summed_model_build_seconds_NOT_pure_GPU':sum(x['model_build_ns']for x in launch)/1e9,
 'device_timer_intervals':[x['device_globaltimer_interval']for x in timers],
 'retired_groups':len(retired),'provider_probe':probe,
 'GPU_proxy_connections':len(proxy),'GPU_parsed_models':sum(isinstance(x.get('input'),dict)for x in proxy),
 'strong_CPU_proxy_connections':len(strong),'strong_CPU_parsed_models':sum(isinstance(x.get('input'),dict)for x in strong),
 'GPU_actual_matrix_shapes':[{'rows':x['rows'],'cols':x['cols'],'nnz':x['nnz'],'reply_state':x.get('reply',{}).get('state')}for x in proxy if isinstance(x.get('input'),dict)],
 'restoration':'passed-restored at finite lifecycle boundary; no demonstrated useful GPU acceleration',
 'scope':'Actual device progress and native/HiGHS retention are separate. No selected GPU evidence in this real run. Cancelled calls are not zero CPU work; model build includes allocation/copy/context. Device timer clock is not spliced into host elapsed. Cold lifecycle separately reported.'}
(A/'device-mechanism-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in['GPU_actual_matrix_shapes','device_timer_intervals']},indent=2))
