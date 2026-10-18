"""Describe fixed baseline LP cost concentration; no speedup or policy tuning."""
from pathlib import Path
import argparse,collections,gzip,json,math
def records(p):
 with(gzip.open(p,'rt')if p.suffix=='.gz'else p.open())as f:
  for l in f:yield json.loads(l)
p=argparse.ArgumentParser(description=__doc__);p.add_argument('numeric',type=Path);p.add_argument('analysis',type=Path);p.add_argument('out',type=Path);a=p.parse_args()
calls=[]
for x in records(a.numeric):
 if x.get('kind')not in ['direct','fallback']or x.get('request',{}).get('hello'):continue
 shapes=[e for e in x['events']if e.get('stage')=='shape']
 phase=collections.Counter()
 for e in x['events']:
  if'cpu_ns'in e:phase[e['stage']]+=e['cpu_ns']/1e9
 calls.append({'start_ns':x['start_ns'],'pid':x['pid'],'call_id':x.get('request',{}).get('call_id'),'shape':shapes[-1]if shapes else None,'LP_CPU_seconds':phase['fp_solve']+phase['exact_lp'],'exact_CPU_seconds':phase['exact_lp'],'certificate':x.get('answer',{}).get('cert')is not None})
whole=sum(x['LP_CPU_seconds']for x in calls)
with(gzip.open(a.analysis,'rt')if a.analysis.suffix=='.gz'else a.analysis.open())as f:d=json.load(f)
def describe(xs):
 return {'calls':len(xs),'LP_CPU_seconds':sum(x['LP_CPU_seconds']for x in xs),'LP_CPU_fraction':sum(x['LP_CPU_seconds']for x in xs)/whole,'certificates':sum(x['certificate']for x in xs)}
out={'count':len(calls),'LP_CPU_seconds':whole,'shape_quartiles':{},'LP_call_tail':{},'candidate_LP_CPU_tail':{},'scope':'Calling-thread CPU cost concentration on a closed native baseline capture. Shape quartiles have equal call counts, not equal CPU. Candidate LP-CPU ranking is not end-to-end wall tail ranking. Four unknown source IDs remain explicit.'}
for metric in ['rows','cols','nnz']:
 ranked=sorted([x for x in calls if x['shape']],key=lambda x:x['shape'][metric]);n=len(ranked);bins=[]
 for q in range(4):
  xs=ranked[q*n//4:(q+1)*n//4];r=describe(xs);r.update({'quartile':q+1,'shape_min':min(x['shape'][metric]for x in xs),'shape_max':max(x['shape'][metric]for x in xs)});bins.append(r)
 out['shape_quartiles'][metric]=bins
ranked=sorted(calls,key=lambda x:x['LP_CPU_seconds'],reverse=True)
for fraction in [.01,.1]:
 n=math.ceil(len(calls)*fraction);xs=ranked[:n];out['LP_call_tail'][str(fraction)]=dict(describe(xs),most_expensive=xs[:10])
lookup={(x['kind'],x['start_ns']):x.get('index')for x in d['calls']}
by_source=collections.Counter();unknown=0.
for x in calls:
 i=lookup.get(('fallback',x['start_ns']))
 if i is None:unknown+=x['LP_CPU_seconds']
 else:by_source[i]+=x['LP_CPU_seconds']
out['unknown_source_LP_CPU_seconds']=unknown
for fraction in [.01,.1]:
 n=math.ceil(d['terminal']['expected']*fraction);xs=by_source.most_common(n)
 out['candidate_LP_CPU_tail'][str(fraction)]={'candidate_count':len(xs),'indices':[x[0]for x in xs],'LP_CPU_seconds':sum(x[1]for x in xs),'LP_CPU_fraction':sum(x[1]for x in xs)/whole,'selection':'LP calling-thread CPU only; not full candidate latency'}
a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['shape_quartiles','LP_call_tail']},indent=2))
