"""Read the closed full profiler ZIP; no verifier execution or SHA gate."""
from pathlib import Path
import json,gzip,zipfile,collections,datetime,importlib.util,sys
D=Path(__file__).parent;B=D/'dynamic-profile-gc-full2';label='goedel427-profile-original'
t=json.loads((B/(label+'.terminal.json')).read_text())
if t['failure']or t['returned']!=t['expected']:raise RuntimeError('capture is incomplete; retain original output')
if (B/label).exists():raise RuntimeError('original collector may still archive this directory; wait for its terminal process')
spec=importlib.util.spec_from_file_location('profile_stock_split','/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/server/split.py')
split=importlib.util.module_from_spec(spec);sys.modules[spec.name]=split;spec.loader.exec_module(split)
original=(D/'input.jsonl').read_bytes();inputs=[json.loads(l)for l in original.splitlines()]
bodies=collections.defaultdict(list);headers=set()
for x in inputs:
 s=split.split_snippet(x['code']);bodies[s.body].append(x['index']);headers.add(s.header)
with zipfile.ZipFile(B/(label+'.zip'))as z:
 read=lambda rel:z.read(label+'/'+rel)
 assert read('input.jsonl')==original
 rows=sorted([json.loads(l)for l in read('results.jsonl').splitlines()],key=lambda r:r['ordinal'])
 assert len(rows)==len(inputs)==t['expected']
 for ordinal,row in enumerate(rows):
  assert row['ordinal']==ordinal and row['source_index']==inputs[ordinal]['index']
 byindex={r['source_index']:r for r in rows};assert len(byindex)==len(inputs)
 files=sorted(n for n in z.namelist()if n.startswith(label+'/native-profiles/')and n.endswith('.json.gz'))
 totals=collections.Counter();hits=collections.Counter();matched=[];header_count=0;unmatched=[];partial=[]
 for i,name in enumerate(files):
  try:p=json.loads(gzip.decompress(z.read(name)))
  except (OSError,EOFError,json.JSONDecodeError)as e:
   partial.append({'file':name,'error':type(e).__name__});continue
  main=next((th for th in p['threads']if th.get('isMainThread')),None)
  command=main['name']if main else None
  if command in headers:header_count+=1;continue
  possible=bodies.get(command,[]);start=round(p['meta']['startTime']*1000000)
  candidates=[byindex[idx]for idx in possible if byindex[idx]['admitted_ns']<=start<=byindex[idx]['response_ns']]
  if len(candidates)!=1:
   unmatched.append({'file':name,'possible_source_indices':possible,'interval_matches':len(candidates)});continue
  row=candidates[0];cost=collections.Counter();negative=0;unattributed=0;unpaired=0
  for th in p['threads']:
   stacks=th['stackTable'];frames=th['frameTable'];funcs=th['funcTable'];strings=th['stringArray']
   samples=th['samples'];unpaired+=abs(len(samples['stack'])-len(samples['weight']))
   for stack,weight in zip(samples['stack'],samples['weight']):
    if stack is None:unattributed+=1;continue
    frame=stacks['frame'][stack];fun=frames['func'][frame];cls=strings[funcs['name'][fun]]
    cost[cls]+=weight
    if weight<0:negative+=1
  totals.update(cost);hits.update(cost.keys())
  matched.append({'source_index':row['source_index'],'proof_id':row['proof_id'],'basic':row['basic'],
   'request_seconds':row['elapsed_seconds'],'file':name,'negative_slice_count':negative,
   'unattributed_samples':unattributed,'unpaired_sample_values':unpaired,'traced_leaf_wall_ms':dict(cost)})
  if (i+1)%5000==0:print('profiles_read',i+1,flush=True)
seen=collections.Counter(x['source_index']for x in matched)
missing=[{'source_index':r['source_index'],'proof_id':r['proof_id'],'basic':r['basic']}for r in rows if r['source_index']not in seen]
rank=[{'class':k,'summed_profile_leaf_wall_ms':v,'body_profiles':hits[k]}for k,v in totals.most_common()]
scope='Complete original-source diagnostic acquisition; body-profile coverage is separately reported. Native Firefox synthetic threadCPUDelta and leaf weights are wall intervals, not measured CPU. Threshold10ms and uninstrumented regions hide work. Threads/requests overlap; sums are not makespan/CPU fractions or GPU eligible coverage. Missing/partial/unmatched profiles are retained, never assigned zero cost.'
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'terminal':t,'source_rows':len(rows),
 'request_outcomes':dict(collections.Counter(r['basic']for r in rows)),'native_profile_members':len(files),
 'matched_body_profiles':len(matched),'sources_with_body_profiles':len(seen),'header_profiles':header_count,
 'unmatched_profiles':unmatched,'partial_profiles':partial,'sources_without_body_profiles':missing,
 'multiple_profiles_per_source':{str(k):v for k,v in seen.items()if v>1},
 'negative_slice_count':sum(x['negative_slice_count']for x in matched),
 'unattributed_samples':sum(x['unattributed_samples']for x in matched),
 'unpaired_sample_values':sum(x['unpaired_sample_values']for x in matched),'ranked_trace_classes':rank,'scope':scope}
(D/'gc2-dynamic-profile-complete-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
with gzip.open(D/'gc2-dynamic-profile-complete-per-source.jsonl.gz','wt')as f:
 for x in matched:f.write(json.dumps(x,ensure_ascii=False)+'\n')
lines=['# Complete source-native diagnostic capture','',out['utc'],'',scope,'',
 f"Original sources returned: {len(rows)}. Matched body profiles: {len(matched)} over{len(seen)}sources. Header profiles:{header_count}. Sources without body profiles:{len(missing)}. Partial:{len(partial)}; unmatched:{len(unmatched)}.",
 '','| Recorded trace class | Summed leaf wall ms | Body profiles |','|---|---:|---:|']
for x in rank[:20]:lines.append(f"|{x['class']}|{x['summed_profile_leaf_wall_ms']:.3f}|{x['body_profiles']}|")
lines+=['','The whole capture clock includes profiler/observer costs and is not a primary speed comparison. These observations support operation selection only; they do not answer a complete RQ, establish GPU cost coverage or identify a fastest CPU route. Repetitions/resources of the already running performance comparisons remain required.']
(D/'gc2-dynamic-profile-complete-analysis.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'source_rows':len(rows),'body_profiles':len(matched),'sources_with_profiles':len(seen),
 'missing':len(missing),'headers':header_count,'partial':len(partial),'unmatched':len(unmatched),
 'negative':out['negative_slice_count'],'unattributed':out['unattributed_samples'],
 'unpaired':out['unpaired_sample_values'],'top_classes':rank[:10]},indent=2))
