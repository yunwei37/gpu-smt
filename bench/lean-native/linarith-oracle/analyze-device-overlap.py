'''Verify real cross-group device block overlap and allocation retirement.'''
from pathlib import Path
import argparse,collections,gzip,json
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--provider',type=Path,required=True);a=p.parse_args()
 f=gzip.open(a.provider,'rt')if a.provider.suffix=='.gz'else a.provider.open()
 provider=[]
 with f:
  for line in f:
   try:provider.append(json.loads(line))
   except ValueError:pass
 launches=[x for x in provider if x.get('event')=='launch'];retired=[x for x in provider if x.get('event')=='batch_retired']
 keys=[key for x in launches for key in x['keys']]
 assert len(set(keys))==len(keys),'duplicate live launch identity'
 states=[x for x in provider if x.get('device_globaltimer_interval')]
 assert len(set(x['key']for x in states))==len(states)
 pairs=[];events=[]
 for x in states:
  b,e=x['device_globaltimer_interval'];assert 0<b<=e
  events.extend([(b,1,x['batch_id']),(e,-1,x['batch_id'])])
 for i,x in enumerate(states):
  for y in states[i+1:]:
   if x['batch_id']==y['batch_id']:continue
   b=max(x['device_globaltimer_interval'][0],y['device_globaltimer_interval'][0]);e=min(x['device_globaltimer_interval'][1],y['device_globaltimer_interval'][1])
   if e>b:pairs.append({'left':x['key'],'right':y['key'],'left_group':x['batch_id'],'right_group':y['batch_id'],'overlap_globaltimer_ticks':e-b})
 active=peak=peakgroups=0;groups=collections.Counter()
 for tick,delta,group in sorted(events):
  active+=delta;peak=max(peak,active);groups[group]+=delta
  if groups[group]==0:del groups[group]
  peakgroups=max(peakgroups,len(groups))
 assert active==0 and not groups
 raw=json.loads((a.root/'provider-probe.json').read_text());probe=json.loads(raw)if isinstance(raw,str)else raw
 out={'scope':'Root self-review. Device globaltimer sampled inside LP blocks in the actual common CUDA context. Overlapping lifetimes from distinct groups verify independent in-flight progress, not pure ALU work or portable CUDA event timing. Missing model samples stay explicit.',
 'provider_launch_records':len(launches),'actual_kernel_groups':sum(x['batch_size']>0 for x in launches),'actual_models':sum(x['batch_size']for x in launches),
 'actual_group_size_histogram':dict(collections.Counter(x['batch_size']for x in launches if x['batch_size']>0)),
 'zero_model_groups':sum(x['batch_size']==0 for x in launches),
 'all_launch_groups_retired':set(x['batch_id']for x in launches)==set(x['batch_id']for x in retired),
 'model_states_with_device_samples':dict(collections.Counter(x['state']for x in states)),
 'timer_samples':len(states),'models_without_device_sample':sorted(set(keys)-set(x['key']for x in states)),
 'device_maximum_overlapping_LP_block_lifetimes':peak,'device_maximum_overlapping_distinct_groups':peakgroups,
 'cross_group_overlapping_model_pairs':len(pairs),'overlap_pairs':pairs,'provider_retirement_probe':probe}
 (a.root/'device-overlap-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k!='overlap_pairs'},indent=2))
if __name__=='__main__':main()
