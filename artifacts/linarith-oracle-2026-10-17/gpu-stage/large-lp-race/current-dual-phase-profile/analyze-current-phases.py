"""Current-build phase attribution; no clock, outcome or scheduler substitution."""
from pathlib import Path
import argparse,json,gzip,collections,math,os,resource,io
R=Path('/workspaces/repository')
HEADER="import Mathlib\nimport Aesop\n"
class Parts(io.RawIOBase):
 def __init__(self,paths):
  super().__init__();self.paths=iter(paths);self.current=None
 def readable(self):return True
 def readinto(self,b):
  while True:
   if self.current is None:
    try:self.current=open(next(self.paths),'rb')
    except StopIteration:return 0
   n=self.current.readinto(b)
   if n:return n
   self.current.close();self.current=None
 def close(self):
  if self.current:self.current.close()
  super().close()
def rows(p):
 parts=sorted(p.parent.glob(p.name+'.part*'))
 if p.exists():f=gzip.open(p,'rt')if str(p).endswith('.gz')else open(p)
 else:
  assert parts,p
  f=io.TextIOWrapper(gzip.GzipFile(fileobj=io.BufferedReader(Parts(parts)),mode='rb'))
 with f:
  for l in f:yield json.loads(l)
def merged(xs):
 out=[]
 for a,b in sorted(xs):
  assert b>=a
  if out and a<=out[-1][1]:out[-1]=(out[-1][0],max(b,out[-1][1]))
  else:out.append((a,b))
 return out
def duration(xs):return sum(b-a for a,b in merged(xs))
def clipped(xs,a,b):return[(max(a,l),min(b,r))for l,r in xs if l<b and r>a]
def quant(xs):
 if not xs:return None
 xs=sorted(xs);n=len(xs)
 return dict(count=n,min=xs[0],p50=xs[(n-1)//2],p90=xs[int(.9*(n-1))],p99=xs[int(.99*(n-1))],max=xs[-1])
def overlap(requests):
 ev=sorted([(x['start_ns'],1,x['source'])for x in requests]+[(x['end_ns'],-1,x['source'])for x in requests])
 active=collections.Counter();hist=collections.Counter();last=None;peak=0;cross=0
 for t,sign,s in ev:
  if last is not None:
   hist[sum(active.values())]+=t-last
   if len(active)>1:cross+=t-last
  active[s]+=sign
  if not active[s]:del active[s]
  peak=max(peak,len(active));last=t
 return dict(peak_distinct_candidates=peak,cross_candidate_request_overlap_seconds=cross/1e9,
  wall_seconds_by_outstanding_requests={str(k):v/1e9 for k,v in sorted(hist.items())},
  scope='Exported request lifetimes include IPC/lock/wait; not instantaneous GPU-ready LPs or batch speedup.')
def analyze(d,inputs):
 t=json.loads((d/'terminal.json').read_text());assert t['state']=='complete'
 inp=list(rows(inputs));bodies={}
 for i,x in enumerate(inp):
  assert x['code'].startswith(HEADER)
  b="\n\n"+x['code'][len(HEADER):];assert b not in bodies;bodies[b]=(i,x['proof_id'])
 spans={x['source']:x for x in rows(d/'candidate-times.jsonl')}
 assert set(spans)==set(bodies)
 responses=list(rows(d/'responses.jsonl.gz'));assert len(responses)==len(inp)
 timed=collections.defaultdict(list);phase=collections.defaultdict(list);requests=[];checks={}
 sizes=collections.defaultdict(list);outcomes=collections.Counter();totals=collections.defaultdict(collections.Counter)
 defects=collections.Counter();aux=collections.Counter();envelope=[];by_source=collections.defaultdict(list)
 per_numeric=collections.defaultdict(collections.Counter)
 for x in rows(d/'lean-costs.jsonl.gz'):
  ty=x['ty'];src=x.get('source')
  if src is None:aux[ty]+=1;continue
  assert src in spans
  if ty in ['cost-stage','cost-direct-check']:
   st=x['stage']if ty=='cost-stage'else'direct_certificate_check'
   a,b=x['start_ns'],x['end_ns'];assert spans[src]['start_ns']<=a<=b<=spans[src]['end_ns']
   phase[st].append((a,b));timed[src].append((st,a,b,x['cpu_ns']))
   if st in ['products','lp']:envelope.append((a,b));by_source[src].append((a,b))
   if ty=='cost-direct-check':checks[(src,x['call_id'])]=bool(x['accepted'])
  if ty not in ['cost-native-roundtrip','cost-direct-roundtrip']:continue
  req=x['request'];ans=x['answer'];a,b=x['start_ns'],x['end_ns']
  assert req['source']==src and req['call_id']==x['call_id']
  assert spans[src]['start_ns']<=a<=b<=spans[src]['end_ns']
  kind='direct'if ty=='cost-direct-roundtrip'else'native'
  state='certificate'if ans.get('cert')is not None else'no_certificate_or_error'
  outcomes[kind+'_'+state]+=1;requests.append({'source':src,'call_id':x['call_id'],'start_ns':a,'end_ns':b,'kind':kind,'state':state})
  phase[kind+'_roundtrip'].append((a,b));envelope.append((a,b));by_source[src].append((a,b))
  totals[kind][state+'_roundtrip_ns']+=b-a
  per_numeric[src][kind+'_'+state+'_roundtrip_ns']+=b-a
  if kind=='direct':
   for k in ['linear_ns','products_ns','lp_ns']:
    if k in ans:
     totals[kind][state+'_'+k]+=ans[k];per_numeric[src][kind+'_'+state+'_'+k]+=ans[k]
   shape=ans.get('exact_certificate_shape')
   if shape is None:defects['direct_missing_shape']+=1
   else:
    for k in ['rows','cols','nnz']:sizes[kind+'_'+k].append(shape[k])
    assert len(ans['product_columns'])==shape['cols']
    sizes[kind+'_generated_products'].append(ans['generated_products'])
    sizes[kind+'_product_columns'].append(sum(ans['product_columns']))
  else:
   hs=req['hyps'];flags=req['product_columns'];assert len(hs)==len(flags)
   sizes['native_rows'].append(req['maxVar']+2);sizes['native_cols'].append(len(hs))
   sizes['native_nnz'].append(sum(sum(int(c)!=0 for _,c in h[1])+int(h[0]=='lt')for h in hs))
   sizes['native_product_columns'].append(sum(flags))
 cpu=collections.Counter();per_cpu={}
 for src,events in timed.items():
  # Nested calling-thread CPU; remove only immediate contained timer children.
  parent={}
  for i,(st,a,b,c)in enumerate(events):
   candidates=[(j,v)for j,v in enumerate(events)if j!=i and v[1]<=a and b<=v[2]and(v[1]<a or b<v[2])]
   if candidates:parent[i]=min(candidates,key=lambda z:z[1][2]-z[1][1])[0]
  ex=[e[3]for e in events]
  for child,p in parent.items():ex[p]-=events[child][3]
  if any(v<0 for v in ex):defects['negative_exclusive_Lean_CPU']+=sum(v<0 for v in ex)
  c=collections.Counter()
  for e,v in zip(events,ex):c[e[0]]+=v
  cpu.update(c);per_cpu[src]=c
 keys=[(x['source'],x['call_id'])for x in requests];assert len(keys)==len(set(keys))
 assert set(checks)=={(x['source'],x['call_id'])for x in requests if x['kind']=='direct'}
 for x in requests:
  if x['kind']=='direct':outcomes['direct_Lean_accepted'if checks[(x['source'],x['call_id'])]else'direct_Lean_fallback']+=1
 width=t['width'];base,rem=divmod(len(inp),width);lanes=[];start=0
 for i in range(width):
  count=base+(i<rem);items=[]
  for index in range(start,start+count):
   src="\n\n"+inp[index]['code'][len(HEADER):];sp=spans[src]
   items.append((index,src,sp['start_ns'],sp['end_ns']))
  assert all(x[3]<=y[2]for x,y in zip(items,items[1:])),'lane/source mapping not supported'
  lanes.append(items);start+=count
 origin=min(x['start_ns']for x in spans.values());last=max(x['end_ns']for x in spans.values())
 modeled=[];critical=max(range(width),key=lambda i:lanes[i][-1][3])
 for lane in lanes:
  removed=sum(duration(clipped(by_source[src],a,b))for _,src,a,b in lane)
  modeled.append({'indices':[x[0]for x in lane],'observed_end_from_origin_seconds':(lane[-1][3]-origin)/1e9,
   'optimistically_deleted_envelope_seconds':removed/1e9,'modeled_end_from_origin_seconds':(lane[-1][3]-origin-removed)/1e9})
 overhead=t['whole_ns']-(last-origin)
 modeled_whole=(overhead/1e9)+max(x['modeled_end_from_origin_seconds']for x in modeled)
 tails={}
 ranked=sorted(spans,key=lambda s:spans[s]['end_ns']-spans[s]['start_ns'],reverse=True)
 for frac in [.01,.1]:
  chosen=ranked[:math.ceil(len(ranked)*frac)];c=collections.Counter();ns=collections.Counter()
  for src in chosen:
   c.update(per_cpu.get(src,{}));ns.update(per_numeric.get(src,{}))
  tails[str(frac)]={'proof_ids':[bodies[s][1]for s in chosen],
   'summed_candidate_service_seconds':sum(spans[s]['end_ns']-spans[s]['start_ns']for s in chosen)/1e9,
   'Lean_exclusive_calling_thread_CPU_seconds':{k:v/1e9 for k,v in c.items()},
   'numeric_reply_elapsed_sums_seconds_NOT_CPU':{k:v/1e9 for k,v in ns.items()},
   'summed_envelope_seconds':sum(duration(by_source[s])for s in chosen)/1e9,
   'overlapping_request_count':sum(x['source']in chosen for x in requests)}
 return {'per_candidate':[{'proof_id':bodies[src][1],'input_order':bodies[src][0],'service_seconds':(spans[src]['end_ns']-spans[src]['start_ns'])/1e9,'Lean_exclusive_calling_thread_CPU_seconds':{k:v/1e9 for k,v in per_cpu.get(src,{}).items()},'numeric_reply_elapsed_sums_seconds_NOT_CPU':{k:v/1e9 for k,v in per_numeric.get(src,{}).items()}}for src in ranked],
 'terminal':t,'complete_source_spans':len(spans),'request_outcomes':dict(outcomes),'data_quality_defects':dict(defects),
 'source_less_auxiliary_rows':dict(aux),'coefficient_space_sizes':{k:quant(v)for k,v in sizes.items()},
 'Lean_exclusive_calling_thread_CPU_seconds':{k:v/1e9 for k,v in cpu.items()},
 'phase_elapsed_occupied_seconds_NOT_additive':{k:duration(v)/1e9 for k,v in phase.items()},
 'numeric_reply_elapsed_sums_seconds_NOT_CPU':{k:{n:v/1e9 for n,v in ns.items()}for k,ns in totals.items()},
 'request_availability':overlap(requests),'own_ranked_tail':tails,
 'optimistic_fixed_path_envelope':{'occupied_union_seconds':duration(envelope)/1e9,'whole_seconds':t['whole_ns']/1e9,
  'occupied_union_fraction':duration(envelope)/t['whole_ns'],'fixed_lane_model_whole_seconds':modeled_whole,
  'critical_lane':critical,'lanes':modeled,
  'scope':'Deletes all Lean products/LP stages and complete numerical roundtrips, including non-GPU IPC/repair/queue/retirement. Fixed source path, candidate durations outside these windows, inter-command gaps and static lane assignments. Not a scheduler-independent or support-changing GPU upper bound.'},
 'limitations':['reply lp_ns includes complete numeric search/race, not pure floating solve','cancelled child internal CPU unknown',
  'exact coefficient-space shapes are not scaled floating solver shapes','calling-thread CPU excludes worker child CPU; cannot add to roundtrip as exclusive whole cost',
  'diagnostic scan/logging/gzip charged; not a new primary performance result']}
def main():
 p=argparse.ArgumentParser();p.add_argument('--cell',type=Path,required=True);p.add_argument('--input',type=Path,default=R/'artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 os.sched_setaffinity(0,{12,13,14,15});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
 result=analyze(a.cell,a.input);a.out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in ['optimistic_fixed_path_envelope','own_ranked_tail','per_candidate']},indent=2))
 print('MODEL',json.dumps({k:v for k,v in result['optimistic_fixed_path_envelope'].items()if k!='lanes'}))
if __name__=='__main__':main()
