from pathlib import Path
import argparse,json,gzip,collections,datetime,importlib.util,zipfile
D=Path(__file__).parent
ap=argparse.ArgumentParser();ap.add_argument('--cell',default='goedel427-profile-original');args=ap.parse_args()
cell=D/'dynamic-profile-gc-full2'/args.cell
spec=importlib.util.spec_from_file_location('stock_split','/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/server/split.py')
split=importlib.util.module_from_spec(spec);__import__('sys').modules[spec.name]=split;spec.loader.exec_module(split)
source=collections.defaultdict(list);headers=set()
for line in (D/'input.jsonl').read_text().splitlines():
 x=json.loads(line);s=split.split_snippet(x['code']);source[s.body].append(x['proof_id']);headers.add(s.header)
rows=[json.loads(x) for x in (cell/'results.jsonl').read_text().splitlines() if x.strip()]
byid=collections.defaultdict(list)
for row in rows:byid[row['proof_id']].append(row)
totals=collections.Counter();hits=collections.Counter();unmatched=[];deferred=[];header_count=0;matched=[]
files=sorted((cell/'native-profiles').glob('*.json.gz'))
for path in files:
 try:
  p=json.loads(gzip.decompress(path.read_bytes()))
 except (EOFError,OSError,json.JSONDecodeError) as e:
  deferred.append({'file':path.name,'reason':type(e).__name__});continue
 main=next((t for t in p['threads'] if t.get('isMainThread')),None)
 command=main['name'] if main else None
 if command in headers:header_count+=1;continue
 possible=source.get(command,[])
 start_ns=round(p['meta']['startTime']*1000000)
 candidates=[row for id in possible for row in byid[id] if row['admitted_ns']<=start_ns<=row['response_ns']]
 if len(candidates)!=1:
  unmatched.append({'file':path.name,'possible_source_ids':possible,'completed_request_matches':len(candidates)});continue
 row=candidates[0];cost=collections.Counter();negative=0
 for thread in p['threads']:
  stacks=thread['stackTable'];frames=thread['frameTable'];funcs=thread['funcTable'];strings=thread['stringArray']
  for stack,weight in zip(thread['samples']['stack'],thread['samples']['weight']):
   frame=stacks['frame'][stack];function=frames['func'][frame];name=strings[funcs['name'][function]]
   cost[name]+=weight
   if weight<0:negative+=1
 totals.update(cost);hits.update(cost.keys())
 matched.append({'proof_id':row['proof_id'],'source_index':row['source_index'],'basic':row['basic'],'request_seconds':row['elapsed_seconds'],'file':path.name,'negative_slice_count':negative,'traced_leaf_wall_ms':dict(cost)})
rank=[{'class':name,'summed_profile_leaf_wall_ms':value,'source_profiles':hits[name]} for name,value in totals.most_common()]
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cell':args.cell,'completed_request_rows':len(rows),'complete_gzip_profile_files_observed':len(files),'matched_completed_body_profiles':len(matched),'header_profiles':header_count,'unmatched_or_pending_profiles':unmatched,'deferred_partial_profiles':deferred,'ranked_trace_classes':rank,'negative_slice_count':sum(x['negative_slice_count'] for x in matched),'scope':'Partial GC-enabled full-source diagnostic, not wholecorpus or primary performance. Official Firefox synthetic threadCPUDelta and leafweights are wall intervals, not measured CPU. Threshold10ms hides smaller/uninstrumented operations. Different native threads/requests overlap; summed trace work is not makespan/CPU fractions/GPU eligible work. Association uses stock split body bytes and actual native/API monotonic intervals; no ID/response normalization.'}
(D/'gc2-dynamic-profile-partial-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
(D/'gc2-dynamic-profile-per-source.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in matched))
lines=['# Partial native dynamic trace observation','',out['utc'],'',out['scope'],'',f"Completed requests: {len(rows)}; matched completed body profiles: {len(matched)}; header profiles: {header_count}; deferred/unmatched retained in JSON.",'','| Trace class | Summed leaf wall ms | Source profiles |','|---|---:|---:|']
for x in rank[:20]:lines.append(f"|{x['class']}|{x['summed_profile_leaf_wall_ms']:.3f}|{x['source_profiles']}|")
lines+=['','Negative weights are retained and reported, never clipped. This is preliminary operation-selection evidence only. No cost fraction, acceleration ceiling, confidence or native-CPU/GPU gain follows. Full corpus/primary paired results and strongest nativebatch competitor remain open.']
(D/'gc2-dynamic-profile-partial-analysis.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'completed_requests':len(rows),'matched_profiles':len(matched),'header_profiles':header_count,'unmatched_profiles':len(unmatched),'deferred':len(deferred),'negative_weights':out['negative_slice_count'],'top_classes':rank[:12]},indent=2))
