from pathlib import Path
import zipfile,gzip,json,collections,datetime,importlib.util,sys
D=Path(__file__).parent;B=D/'fast-native-stage2'
spec=importlib.util.spec_from_file_location('fastStageSplit','/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/server/split.py')
split=importlib.util.module_from_spec(spec);sys.modules[spec.name]=split;spec.loader.exec_module(split)
selected=[json.loads(x) for x in (D/'highs-preflight-input.jsonl').read_text().splitlines()]
bybody={split.split_snippet(x['code']).body:x['proof_id'] for x in selected}
def clean(v):
 v=json.loads(json.dumps(v))
 for f in v.get('results',[]):
  if isinstance(f.get('response'),dict):f['response'].pop('time',None)
 return v
results={};payload={}
for method in ['tiered','hybrid','highs']:
 t=B/(method+'.terminal.json')
 if not t.exists():continue
 terminal=json.loads(t.read_text());path=B/(method+'.zip')
 if terminal['failure'] or terminal['returned']!=4 or not path.exists():continue
 with zipfile.ZipFile(path) as z:
  rows=[json.loads(x) for x in z.read(method+'/results.jsonl').splitlines()]
  parsed={};payload[method]={}
  for name in z.namelist():
   if '/native-profiles/' not in name or not name.endswith('.json.gz'):continue
   profile=json.loads(gzip.decompress(z.read(name)))
   main=next((t for t in profile['threads'] if t.get('isMainThread')),None)
   pid=bybody.get(main['name']) if main else None
   if pid is None:continue
   row=next(x for x in rows if x['proof_id']==pid)
   start_ns=round(profile['meta']['startTime']*1e6)
   assert row['admitted_ns']<=start_ns<=row['response_ns']
   cost=collections.Counter();negative=0
   for thread in profile['threads']:
    for stack,weight in zip(thread['samples']['stack'],thread['samples']['weight']):
     frame=thread['stackTable']['frame'][stack];fn=thread['frameTable']['func'][frame]
     name=thread['stringArray'][thread['funcTable']['name'][fn]]
     cost[name]+=weight;negative+=weight<0
   groups={}
   for stage,key in [('oracle','Invoking oracle'),('final_expression','Building final expression'),('linear_forms','linearFormsAndMaxVar'),('kernel','Kernel:')]:
    found=[v for k,v in cost.items() if key in k]
    groups[stage]=sum(found) if found else None
   # An absent pretty trace label is unobserved (possibly below threshold), not zero cost.
   parsed[pid]={'stages_leaf_wall_ms':groups,'negative_slice_count':negative,
    'top_trace_leaf_names':[{'name':k,'wall_ms':v} for k,v in cost.most_common(18)]}
  for row in rows:
   pid=row['proof_id'];body=json.loads(z.read(method+'/'+row['raw_response']))
   payload[method][pid]=clean(body)
   parsed.setdefault(pid,{}).update(basic=row['basic'],request_seconds=row['elapsed_seconds'])
 results[method]={'whole_diagnostic_seconds':terminal['whole_seconds'],'per_source':parsed}
diff={}
if 'tiered' in payload:
 for method in ['hybrid','highs']:
  if method in payload:diff[method]=[pid for pid in payload['tiered'] if payload['tiered'][pid]!=payload[method].get(pid)]
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'methods':results,'native_response_differences_excluding_adapter_time':diff,
 'scope':'Selected4source residual-cost discriminator with officialPP/nativeAOT/nativeoracle/nativeGC; oneorder/CPU16-19/width4/8006. Observer costs included, not representative/repeated whole-performance. Native fields retained except actual backwardadapter response.time. Profile wall slices overlap across threads/requests, default10ms hides small/uninstrumented work; not measured CPU, disjoint fractions, a wholeGPU ceiling or eligibility. Primary/full29k matrices unaffected.'}
(D/'fast-native-stage2-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'completed_methods':list(results),'response_differences':diff,'per_source':{method:{pid:{k:v for k,v in row.items() if k!='top_trace_leaf_names'} for pid,row in result['per_source'].items()} for method,result in results.items()}},indent=2))
