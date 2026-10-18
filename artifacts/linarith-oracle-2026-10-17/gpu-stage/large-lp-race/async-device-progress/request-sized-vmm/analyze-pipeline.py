"""Join retained proxy/device/race records; host occupancy is not GPU kernel time."""
from pathlib import Path
import argparse,collections,gzip,json,math,statistics

def rows(path):
 with(gzip.open(path,'rt')if path.suffix=='.gz'else path.open())as h:
  return[json.loads(l)for l in h if l.startswith('{')]
def spread(xs):
 xs=sorted(xs)
 return {'count':len(xs),'sum':sum(xs),'min':xs[0]if xs else None,
 'median':statistics.median(xs)if xs else None,
 'p90':xs[min(len(xs)-1,math.ceil(.9*len(xs))-1)]if xs else None,
 'max':xs[-1]if xs else None}
def key(x):
 q=x.get('input')
 if not isinstance(q,dict):return None
 return json.dumps({k:v for k,v in q.items()if k not in['source','call_id','request_id']},sort_keys=True,separators=(',',':'))+'\u0001'+q.get('source','')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--provider',required=True,type=Path);a=p.parse_args()
 cpu=rows(Path('/workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/candidate-capacity32/qualification64-cpu/rep1-oracle-highs-backend/support-calls.jsonl.gz'))
 gpu=rows(a.root/'qualification64-gpu/rep1-oracle-gpu-backend/support-calls.jsonl.gz')
 races=rows(a.root/'qualification64-gpu/rep1-oracle-gpu/lp-races.jsonl.gz')
 events=rows(a.root/'qualification64-gpu/rep1-oracle-gpu-backend/support-calls.jsonl.batches.gz')
 provider=rows(a.provider)
 submitted={key:x for x in events if x.get('event')=='device_submit'for key in x['keys']}
 launched={key:x for x in provider if x.get('event')=='launch'for key in x['keys']}
 states={x['key']:x for x in provider if 'key'in x and x.get('state')}
 retired={x['batch_id']:x for x in provider if x.get('event')=='batch_retired'}
 cancellations={key:x for x in events if x.get('event')=='model_cancel'for key in x['keys']}
 bycall={x.get('input',{}).get('call_id'):x for x in gpu if isinstance(x.get('input'),dict)}
 racebycall={x['call_id']:x for x in races}
 model=[];unjoined=[]
 for k,st in states.items():
  launch=launched[k];ci=launch['call_ids'][launch['keys'].index(k)]
  call=bycall.get(ci)
  if call is None:unjoined.append(k);continue
  assert call['input']['request_id']==int(k.rsplit(':',1)[1])
  assert launch['batch_id']==st['batch_id']
  beg,end=call['start_ns'],call['end_ns']
  sb,lb,sr=submitted[k]['monotonic_ns'],launch['batch_id'],st['monotonic_ns']
  assert beg<=sb<=lb<=sr, (k,beg,sb,lb,sr)
  model.append({'key':k,'call_id':ci,'rows':call['rows'],'cols':call['cols'],'nnz':call['nnz'],
    'state':st['state'],'iterations':st['iterations'],'race_winner':racebycall.get(ci,{}).get('winner'),
    'proxy_arrival_to_submit_seconds':(sb-beg)/1e9,
    'submit_to_provider_group_begin_seconds':(lb-sb)/1e9,
    'provider_group_begin_to_result_seconds':(sr-lb)/1e9,
    'model_build_seconds':st['build_ns']/1e9,
    'proxy_call_seconds':(end-beg)/1e9,
    'cancel_rpc_ack_to_model_result_signed_seconds':(sr-cancellations[k]['monotonic_ns'])/1e9 if k in cancellations else None})
 cpukeys=collections.defaultdict(list)
 for x in cpu:
  k=key(x)
  if k is not None:cpukeys[k].append(x)
 matched=[]
 for x in gpu:
  k=key(x)
  if k is not None and k in cpukeys:
   ys=cpukeys[k]
   matched.append({'gpu_connection_id':x['id'],'cpu_same_payload_observations':len(ys),
    'rows':x['rows'],'cols':x['cols'],'nnz':x['nnz'],'gpu_state':x['reply'].get('state'),
    'gpu_proxy_call_seconds':(x['end_ns']-x['start_ns'])/1e9,
    'cpu_proxy_call_seconds':[(y['end_ns']-y['start_ns'])/1e9 for y in ys],
    'cpu_LP_solver_seconds':[y['reply'].get('solver_seconds')for y in ys]})
 out={'scope':'Root self-review. Retained same-node monotonic host records, joined by exact call_id/request key. Provider group begin includes model allocation/copy/context startup; all intervals include host observation. This host join does not use device globaltimer samples; see device-overlap-analysis.json. Current Lean certificate-stage attribution is unavailable. Signed cancellation intervals start at RPC acknowledgement, not send, and can be negative in an acknowledgement/result race.',
  'connections':{'cpu':len(cpu),'gpu':len(gpu)},
  'parsed':{'cpu':sum(isinstance(x.get('input'),dict)for x in cpu),'gpu':sum(isinstance(x.get('input'),dict)for x in gpu)},
  'cpu_states':dict(collections.Counter(x.get('reply',{}).get('state')for x in cpu)),
  'gpu_states':dict(collections.Counter(x.get('reply',{}).get('state')for x in gpu)),
  'gpu_models':len(model),'unjoined_models':unjoined,
  'GPU_race_winners':dict(collections.Counter(x['winner']for x in races)),
  'host_model_statistics':{field:spread([m[field]for m in model if m[field]is not None])for field in[
    'proxy_arrival_to_submit_seconds','submit_to_provider_group_begin_seconds',
    'provider_group_begin_to_result_seconds','model_build_seconds','proxy_call_seconds','cancel_rpc_ack_to_model_result_signed_seconds']},
  'summed_CPU_HiGHS_solver_seconds':sum(x['reply'].get('solver_seconds')or 0 for x in cpu),
  'matched_exact_payload_calls':len(matched),'matched_payload_call_records':matched,
  'models':model}
 (a.root/'device-pipeline-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k not in['matched_payload_call_records','models']},indent=2))
if __name__=='__main__':main()
