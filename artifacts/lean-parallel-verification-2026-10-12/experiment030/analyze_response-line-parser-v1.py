from pathlib import Path
import json,zipfile,collections,statistics
D=Path(__file__).parent
def profile(folder,label):
 with zipfile.ZipFile(folder/(label+'.zip')) as z:
  events=[]
  for line in z.read(label+'/primary.stderr.bin').splitlines():
   try: e=json.loads(line)
   except (ValueError,UnicodeDecodeError):continue
   if e.get('response_profile'):events.append(e)
  parent=json.loads(z.read(label+'/primary.command.json'))['pid']
 clocks={};durations=collections.defaultdict(list);unfinished=[];count=collections.Counter()
 for e in events:
  if e['pid']==parent:continue
  key=(e['pid'],e['index']);stage=e['stage'];clocks.setdefault(key,{})[stage]=e
  if stage=='response_complete':
   c=clocks.pop(key)
   for name,start,end in [('frontend','frontend_begin','frontend_complete'),('response_extraction','response_begin','response_complete'),('sorries','sorries_begin','sorries_complete')]:
    if start not in c or end not in c:unfinished.append({'key':key,'missing':name});continue
    a,b=c[start],c[end];durations[name].append({'wall_seconds':(b['wall_ns']-a['wall_ns'])/1e9,'calling_thread_cpu_seconds':(b['calling_thread_cpu_ns']-a['calling_thread_cpu_ns'])/1e9})
 for key,c in clocks.items():unfinished.append({'key':key,'open_stages':list(c)})
 report={'label':label,'scope':'native checkpoints on calling thread in child workers only; parent seed excluded; frontend background threads excluded from calling-thread CPU. Sum worker wall durations is not whole makespan; response serialization/witness construction occurs after final checkpoint. Panic/open work remains censored. Profile-only binaries.', 'completed_sequences':len(durations['frontend']),'unfinished_sequences':unfinished,'regions':{}}
 for name,rows in durations.items():
  report['regions'][name]={'samples':len(rows),'summed_worker_wall_seconds':sum(x['wall_seconds'] for x in rows),'summed_calling_thread_cpu_seconds':sum(x['calling_thread_cpu_seconds'] for x in rows),'median_wall_seconds':statistics.median(x['wall_seconds'] for x in rows)}
 return report
def main():
 folder=D/'full1-proofnet';out=[]
 for label in ['profile-gated','profile-warm']:
  if (folder/(label+'.zip')).exists():out.append(profile(folder,label))
 (D/'response-cost-profile.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out))
if __name__=='__main__':main()
