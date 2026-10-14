from pathlib import Path
import json,re,collections,zipfile,io
d=Path(__file__).parent
totals=collections.defaultdict(collections.Counter);paired=set();missing=[];bad=[]
with zipfile.ZipFile(d/'full-proofnet.zip') as z:
 for member in z.namelist():
  if not member.endswith('/stderr.bin'):continue
  pending={};current=None
  def finish(g):
   if g is None:return
   key=(member,g['pid'],g['index'])
   if g['stage']=='frontend_begin':pending[key]=g
   elif g['stage']=='frontend_complete':
    before=pending.pop(key,None)
    if before is None:missing.append({'index':g['index'],'reason':'no begin','member':member});return
    if key in paired:bad.append({'index':g['index'],'reason':'duplicate'});return
    for bucket in before['rows'].keys()|g['rows'].keys():
     delta={k:g['rows'].get(bucket,{}).get(k,0)-before['rows'].get(bucket,{}).get(k,0) for k in ['count','wall_ns','inclusive_thread_cpu_ns','exclusive_thread_cpu_ns']}
     if min(delta.values())<0:bad.append({'index':g['index'],'reason':'nonmonotonic'});continue
     totals[bucket].update(delta)
    paired.add(key)
  with io.TextIOWrapper(z.open(member),errors='replace') as stream:
   for line in stream:
    if line.startswith('meta_whnf_snapshot '):
     finish(current);v=dict(re.findall(r'(\w+)=([^ ]+)',line))
     current={'pid':int(v['pid']),'index':int(v['checkpoint']),'stage':v['stage'],'rows':{}}
    elif line.startswith('meta_whnf_named ') and current is not None:
     v=dict(re.findall(r'(\w+)=([^ ]+)',line));key=(int(v['group']),int(v['contextual']),int(v['success']))
     current['rows'][key]={k:int(v[k]) for k in ['count','wall_ns','inclusive_thread_cpu_ns','exclusive_thread_cpu_ns']}
  finish(current)
  for key in pending:missing.append({'index':key[2],'reason':'no complete','member':member})
labels=['other','outParam','Ring.toSemiring','CommRing.toRing','Semiring.toNonUnitalSemiring','NonUnitalSemiring.toNonUnitalNonAssocSemiring','OfNat.ofNat','AddCommMonoid.toAddMonoid','projection_expr']
by=collections.defaultdict(collections.Counter)
for (g,c,o),values in totals.items():by[labels[g]].update(values)
out={'pairs':len(paired),'missing_pairs':missing,'bad_pairs':bad,'buckets':[{'group':labels[g],'contextual':c,'success':o,**dict(v)} for (g,c,o),v in totals.items()],'by_group':{k:dict(v) for k,v in by.items()}}
(d/'archive-recomputed-named-cost.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:round(v['exclusive_thread_cpu_ns']/1e9,6) for k,v in by.items()})
