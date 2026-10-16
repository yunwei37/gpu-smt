from pathlib import Path
import json,zipfile,collections,datetime,copy,argparse
D=Path(__file__).parent;B=D/'highs-native-cpu-full1'
parser=argparse.ArgumentParser();parser.add_argument('--rep',type=int,default=0)
rep=parser.parse_args().rep
v=json.loads((D/'highs-native-cpu-complete-cells-analysis.json').read_text())
source=(D/'input.jsonl').read_bytes();inputs=[json.loads(l) for l in source.splitlines()]
cells={}
for method in ['tiered','hybrid','highs']:
 label=f'goedel427-rep{rep}-'+method
 with zipfile.ZipFile(B/(label+'.zip')) as z:
  assert z.read(label+'/input.jsonl')==source
  rows=[json.loads(x) for x in z.read(label+'/results.jsonl').splitlines()]
  assert len(rows)==len(inputs)==29750
  byid={r['source_index']:r for r in rows}
  assert len(byid)==29750
  assert all(r['source_index']==inputs[r['ordinal']]['index'] for r in rows)
  command=json.loads(z.read(label+'/command.json'))
  payload={i:json.loads(z.read(label+'/'+row['raw_response'])) for i,row in byid.items()}
  cells[method]={'rows':byid,'payload':payload,'affinity':command['affinity']}
assert cells['tiered']['affinity']==cells['hybrid']['affinity']==cells['highs']['affinity']==[4,5,6,7]
def messages(body):
 return [m for f in body.get('results',[]) if isinstance(f,dict) for m in ((f.get('response') or {}).get('messages') or [])] if isinstance(body,dict) else []
def stripped(body,remove_messages=False):
 b=copy.deepcopy(body)
 if isinstance(b,dict):
  for f in b.get('results',[]):
   r=f.get('response') if isinstance(f,dict) else None
   if isinstance(r,dict):
    r.pop('time',None)
    if remove_messages:r.pop('messages',None)
 return b
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rep':rep,'scope':f'All three complete block{rep} original29750source cells; byte/order/affinity checks and every native/outcome difference retained. Removing messages is used only to classify differences, never to claim normalized parity. No partial clocks or whole-matrix conclusion.','comparisons':[]}
for c in v['complete_primary_trio_comparisons']:
 if c['rep']!=rep:continue
 method=c['method'];a=cells['tiered'];b=cells[method];classes=collections.Counter();basic=[];details=[]
 for i in c['native_payload_differences_excluding_adapter_time']:
  ra,rb=a['rows'][i],b['rows'][i];pa,pb=a['payload'][i],b['payload'][i]
  if ra['basic']!=rb['basic']:category='basic outcome change'
  elif stripped(pa,True)==stripped(pb,True):
   category='message differences containing native errors' if any(x.get('severity')=='error' for x in messages(pa)+messages(pb)) else 'warning/info-message-only differences'
  else:category='other native field differences'
  classes[category]+=1
  detail={'source_index':i,'category':category,'reference_basic':ra['basic'],'candidate_basic':rb['basic'],'reference_response':f"goedel427-rep{rep}-tiered.zip:goedel427-rep{rep}-tiered/{ra['raw_response']}",'candidate_response':f"goedel427-rep{rep}-{method}.zip:goedel427-rep{rep}-{method}/{rb['raw_response']}"}
  details.append(detail)
  if category=='basic outcome change':
   item=dict(detail)
   for name,payload in [('reference',pa),('candidate',pb)]:
    item[name+'_errors']=[x.get('data','')[:1600] for x in messages(payload) if x.get('severity')=='error']
    item[name+'_operational']=payload.get('detail') if isinstance(payload,dict) else None
   basic.append(item)
 out['comparisons'].append({'method':method,'whole_change_percent':c['whole_change_percent'],'difference_classes':dict(classes),'basic_changes':basic,'all_differences':details})
(D/('highs-native-cpu-first-trio-difference-review.json' if rep==0 else f'highs-native-cpu-rep{rep}-trio-difference-review.json')).write_text(json.dumps(out,indent=2)+'\n')
for c in out['comparisons']:
 print(json.dumps({k:v for k,v in c.items() if k!='all_differences'},ensure_ascii=False))
