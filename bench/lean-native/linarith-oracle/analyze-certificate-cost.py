"""Join original certificate features to same-call Lean checking costs; observational only."""
from pathlib import Path
import argparse,collections,gzip,json,math,statistics

def records(path):
 with gzip.open(path,'rt')as h:
  for line in h:yield json.loads(line)
def spread(xs):
 xs=sorted(xs)
 return {'count':len(xs),'sum':sum(xs),'median':statistics.median(xs)if xs else None,
 'p90':xs[min(len(xs)-1,math.ceil(.9*len(xs))-1)]if xs else None,'max':max(xs,default=None)}
def union(spans):
 total=0;right=None
 for l,r in sorted(spans):
  if right is None or l>right:total+=r-l;right=r
  elif r>right:total+=r-right;right=r
 return total/1e9
def ranks(xs):
 order=sorted(range(len(xs)),key=xs.__getitem__);out=[0.]*len(xs);i=0
 while i<len(xs):
  j=i+1
  while j<len(xs)and xs[order[j]]==xs[order[i]]:j+=1
  for k in order[i:j]:out[k]=(i+j-1)/2
  i=j
 return out
def spearman(xs,ys):
 a,b=ranks(xs),ranks(ys);ma,mb=statistics.mean(a),statistics.mean(b)
 den=math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
 return sum((x-ma)*(y-mb)for x,y in zip(a,b))/den if den else None
def features(cert):
 def nodes(origin):
  if not isinstance(origin,list)or not origin:return 0
  return 1+sum(nodes(x)for x in origin[1:]if isinstance(x,list))
 bits=[int(x['coeff']).bit_length()for x in cert]
 return {'terms':len(cert),'product_terms':sum(x.get('origin',[None])[0]=='mul'for x in cert),
 'provenance_nodes':sum(nodes(x.get('origin'))for x in cert),
 'coefficient_bits_sum':sum(bits),'coefficient_bits_max':max(bits,default=0)}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('cell',type=Path);a=p.parse_args()
 answers={};checks=[]
 for x in records(a.cell/'oracle.jsonl.gz'):
  if x.get('ty')=='cost-direct-roundtrip':
   key=(x['source'],x['call_id'])
   if key in answers:raise ValueError('duplicate same-call roundtrip')
   answers[key]=x
  elif x.get('ty')=='cost-direct-check':checks.append(x)
 matched=[];missing=0;unreturned=0
 for x in checks:
  y=answers.get((x['source'],x['call_id']))
  if y is None:missing+=1;continue
  cert=y.get('answer',{}).get('cert')
  if not isinstance(cert,list):unreturned+=1;continue
  matched.append({'source':x['source'],'call_id':x['call_id'],'accepted':x['accepted'],
   'cpu_seconds':x['cpu_ns']/1e9,'wall_seconds':(x['end_ns']-x['start_ns'])/1e9,
   'start_ns':x['start_ns'],'end_ns':x['end_ns'],**features(cert)})
 accepted=[x for x in matched if x['accepted']]
 names=['terms','product_terms','provenance_nodes','coefficient_bits_sum','coefficient_bits_max']
 out={'scope':'Original complete corrected-family CPU-oracle diagnostic, not the later HiGHS/two-sided implementation. Same-call/source joins. Thread CPU is not total service CPU; overlapping wall is not removable critical-path time. Feature correlation is observational, not proof that a different certificate reduces end-to-end time.',
 'roundtrips':len(answers),'check_records':len(checks),'missing_roundtrip':missing,
 'checks_without_returned_certificate':unreturned,'matched_returned_certificates':len(matched),
 'accepted':len(accepted),'rejected_returned_certificates':len(matched)-len(accepted),
 'all_checks_CPU_seconds':sum(x['cpu_ns']for x in checks)/1e9,
 'accepted_CPU_seconds':sum(x['cpu_seconds']for x in accepted),
 'accepted_check_wall_sum':sum(x['wall_seconds']for x in accepted),
 'accepted_check_occupied_union_seconds':union((x['start_ns'],x['end_ns'])for x in accepted),
 'features':{n:spread([x[n]for x in accepted])for n in names},
 'spearman_accepted_CPU':{n:spearman([x[n]for x in accepted],[x['cpu_seconds']for x in accepted])for n in names},
 'accepted_check_CPU_distribution':spread([x['cpu_seconds']for x in accepted]),
 'largest_check_CPU':sorted([{k:v for k,v in x.items()if k!='source'}for x in accepted],key=lambda x:x['cpu_seconds'],reverse=True)[:20]}
 (a.cell/'certificate-cost-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
