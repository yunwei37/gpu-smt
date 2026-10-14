from pathlib import Path
import json,zipfile,collections,statistics,re
D=Path(__file__).parent
STAGES=['frontend_begin','frontend_complete','response_begin','sorries_begin','sorries_complete','response_complete']
def profile(folder,label):
 with zipfile.ZipFile(folder/(label+'.zip')) as z:
  data=z.read(label+'/primary.stderr.bin')
  parent=json.loads(z.read(label+'/primary.command.json'))['pid']
 # Only intact exact JSON records are parsed. Never reconstruct damaged fields.
 pattern=rb'\{"response_profile":true,"index":\d+,"pid":\d+,"stage":"[^"\n]*","wall_ns":\d+,"calling_thread_cpu_ns":\d+\}'
 events=[]
 for m in re.finditer(pattern,data):
  try:events.append(json.loads(m.group()))
  except json.JSONDecodeError:continue
 grouped=collections.defaultdict(list)
 for e in events:
  if e['pid']!=parent:grouped[(e['pid'],e['index'])].append(e)
 complete={};censored=[]
 for key,es in grouped.items():
  if [e['stage'] for e in es]!=STAGES:
   censored.append({'pid':key[0],'index':key[1],'intact_stages':[e['stage'] for e in es]});continue
  if any(a['wall_ns']>b['wall_ns'] or a['calling_thread_cpu_ns']>b['calling_thread_cpu_ns'] for a,b in zip(es,es[1:])):
   censored.append({'pid':key[0],'index':key[1],'reason':'nonmonotone clocks'});continue
  row={}
  for name,a,b in [('frontend',es[0],es[1]),('response_extraction',es[2],es[5]),('sorries',es[3],es[4])]:
   row[name]={'wall_seconds':(b['wall_ns']-a['wall_ns'])/1e9,'calling_thread_cpu_seconds':(b['calling_thread_cpu_ns']-a['calling_thread_cpu_ns'])/1e9}
  assert key[1] not in complete
  complete[key[1]]=row
 regions={}
 for name in ['frontend','response_extraction','sorries']:
  rows=[row[name] for row in complete.values()]
  regions[name]={'samples':len(rows),'summed_worker_wall_seconds':sum(x['wall_seconds'] for x in rows),'summed_calling_thread_cpu_seconds':sum(x['calling_thread_cpu_seconds'] for x in rows),'median_wall_seconds':statistics.median(x['wall_seconds'] for x in rows) if rows else None}
 report={'label':label,'scope':'intact six-stage sequences on calling thread in child workers only; parent seed excluded; frontend background threads excluded from calling-thread CPU. Sum worker wall durations is not whole makespan. Response serialization/witness construction follows final checkpoint. Partial/damaged/panic intervals censored, never reconstructed. Profile-only binaries.', 'raw_markers':data.count(b'response_profile'),'intact_records':len(events),'unparsed_markers':data.count(b'response_profile')-len(events),'complete_sequences':len(complete),'censored_sequences':censored,'regions':regions,'per_source':complete}
 return report
def main():
 folder=D/'full1-proofnet';reports=[]
 for label in ['profile-gated','profile-warm']:
  if (folder/(label+'.zip')).exists():reports.append(profile(folder,label))
 result={'profiles':reports,'matched_source_count':0}
 if len(reports)==2:
  a,b=reports;matched=sorted(set(a['per_source'])&set(b['per_source']))
  result['matched_source_count']=len(matched);result['matched_regions']={}
  for name in ['frontend','response_extraction','sorries']:
   result['matched_regions'][name]={}
   for field in ['wall_seconds','calling_thread_cpu_seconds']:
    av=sum(a['per_source'][i][name][field] for i in matched);bv=sum(b['per_source'][i][name][field] for i in matched)
    result['matched_regions'][name][field]={'gated':av,'warm':bv,'difference_warm_minus_gated':bv-av}
 (D/'response-cost-profile.json').write_text(json.dumps(result,indent=2)+'\n')
 small={'matched_source_count':result['matched_source_count'],'profiles':[{k:v for k,v in p.items() if k not in ['per_source','censored_sequences']} for p in reports]}
 if 'matched_regions' in result:small['matched_regions']=result['matched_regions']
 print(json.dumps(small))
if __name__=='__main__':main()
