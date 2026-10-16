from pathlib import Path
import json,zipfile,gzip,base64,collections,datetime,importlib.util,time,resource,subprocess
R=Path('/workspaces/repository');A=R/'artifacts/lean-modern-native-compilation-2026-10-14'
S=R/'docs/tmp/bootstrap/step-0010-20261014T133154+0000';O=Path(__file__).parent
start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic_ns();cpu=resource.getrusage(resource.RUSAGE_SELF)
spec=importlib.util.spec_from_file_location('native_loader',A/'analyze-native-oracle.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
old=json.loads((S/'completed-cpu-cells-20261016/published-completed-cells.json').read_text())
groups={}
for c in old['cells']:groups.setdefault(c['group'],R/Path(c['original_archive']).parent)
known={(c['group'],c['label']) for c in old['cells']};new=[]
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def load(group,label):
 b=groups[group];t=json.loads((b/(label+'.terminal.json')).read_text());v=m.load_cell(b,t)
 assert v['valid_complete'],(label,v['source_issues'])
 with zipfile.ZipFile(b/(label+'.zip')) as z:v['command']=json.loads(z.read(label+'/command.json'))
 return v
def pair(group,reference,candidate):
 a,b=[load(group,n) for n in [reference,candidate]]
 for k in ['command','cwd','backend','affinity','stock_defaults','api']:assert a['command'][k]==b['command'][k],k
 diff=[]
 for i,x in a['native_rows'].items():
  if x!=b['native_rows'].get(i):diff.append({'source_index':i,'reference_basic':a['basic_rows'][i],'candidate_basic':b['basic_rows'].get(i),'reference_native':x,'candidate_native':b['native_rows'].get(i)})
 result={'reference':reference,'candidate':candidate,'reference_whole_seconds':a['whole_seconds'],'candidate_whole_seconds':b['whole_seconds'],'wall_reduction_percent':100*(1-b['whole_seconds']/a['whole_seconds']),'reference_counts':a['counts'],'candidate_counts':b['counts'],'reference_request_latency_seconds':a['request_latency_seconds'],'candidate_request_latency_seconds':b['request_latency_seconds'],'basic_transitions':dict(collections.Counter(x['reference_basic']+'->'+x['candidate_basic'] for x in diff if x['reference_basic']!=x['candidate_basic'])),'native_difference_count':len(diff),'native_differences':diff,'reference_command':a['command'],'candidate_command':b['command']}
 return result
# Publish only finalized new cells. Preserve HTTP response bytes, not just normalized fields.
for group,b in groups.items():
 with zipfile.ZipFile(R/next(c['original_archive'] for c in old['cells'] if c['group']==group)) as z:
  oldlabel=next(c['label'] for c in old['cells'] if c['group']==group);original=z.read(oldlabel+'/input.jsonl')
 for tpath in sorted(b.glob('*.terminal.json')):
  t=json.loads(tpath.read_text());label=t['label'];archive=b/(label+'.zip')
  if (group,label) in known or t.get('failure') or t.get('returned')!=t.get('expected') or not archive.exists():continue
  dest=O/'published-cells'/group;dest.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(archive) as z:
   assert z.read(label+'/input.jsonl')==original,(group,label,'source bytes changed')
   inputs=[json.loads(s) for s in original.splitlines()];rows=sorted([json.loads(s) for s in z.read(label+'/results.jsonl').splitlines()],key=lambda v:v['ordinal'])
   assert len(rows)==len(inputs)==t['expected']
   assert [(v['ordinal'],v['source_index']) for v in rows]==[(i,v['index']) for i,v in enumerate(inputs)]
   assert dict(collections.Counter(v['basic'] for v in rows))==t['counts']
   with gzip.open(dest/(label+'.results.jsonl.gz'),'wb',compresslevel=6) as f:f.write(z.read(label+'/results.jsonl'))
   with gzip.open(dest/(label+'.raw-responses.jsonl.gz'),'wt',compresslevel=6) as f:
    for row in rows:
     body=z.read(label+'/'+row['raw_response'])
     f.write(json.dumps({'ordinal':row['ordinal'],'source_index':row['source_index'],'member':row['raw_response'],'status_code':row['status_code'],'body_base64':base64.b64encode(body).decode()},separators=(',',':'))+'\n')
   command=json.loads(z.read(label+'/command.json'));write(dest/(label+'.command.json'),command);write(dest/(label+'.terminal.json'),t)
   resource_members=[n for n in ['resources-summary.json','resources.jsonl.gz'] if label+'/'+n in z.namelist()]
   for name in resource_members:
    (dest/(label+'.'+name)).write_bytes(z.read(label+'/'+name))
   new.append({'group':group,'label':label,'attempts':len(rows),'counts':t['counts'],'whole_seconds':t['whole_seconds'],'original_archive':str(archive.relative_to(R)),'archive_bytes':archive.stat().st_size,'published_rows':str((dest/(label+'.results.jsonl.gz')).relative_to(R)),'published_raw_responses':str((dest/(label+'.raw-responses.jsonl.gz')).relative_to(R)),'resource_members':resource_members})
write(O/'new-terminal-cells.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'delta against the earlier52cell source-attempt publication; finalized only; complete raw HTTP response bytes are base64 encoded losslessly; no original archive deleted/moved','cells':new})
print('PUBLISHED_NEW_CELLS',len(new),sum(c['attempts'] for c in new),flush=True)
# New GC third pair; older two primary pairs are valid existing evidence, not new runs.
gc=pair('full-gc2','goedel427-rep2-original','goedel427-rep2-compiled')
write(O/'gc-third-primary-pair.json',gc)
# Complete separate profiles, not extra primary repetitions or a new timing denominator.
profiles={}
for group,methods in [('highs-native-cpu-full1',['tiered','hybrid','highs']),('stock-products-full1',['stock','products'])]:
 values={}
 for method in methods:
  v=load(group,'goedel427-profile-'+method)
  values[method]={k:x for k,x in v.items() if k not in ['basic_rows','native_rows','legacy_rows']}
 comparisons=[pair(group,'goedel427-profile-'+methods[0],'goedel427-profile-'+method) for method in methods[1:]]
 profiles[group]={'cells':values,'native_comparisons':comparisons}
write(O/'complete-profile-analysis.json',profiles)
previous_gc=json.loads((A/'gc2-complete-cells-analysis.json').read_text());previous_stock=json.loads((A/'stock-products-complete-cells-analysis.json').read_text());previous_highs=json.loads((A/'highs-native-cpu-complete-cells-analysis.json').read_text())
reused={'gc_prior_primary_pairs':previous_gc['primary_pairs'],'stock_products_primary_pairs':previous_stock['pairs'],'highs_primary_comparisons':previous_highs['complete_primary_trio_comparisons']}
write(O/'reused-primary-evidence.json',reused)
counts=collections.Counter(c['group'] for c in old['cells']+new)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'new_completed_cells':len(new),'new_attempts':sum(c['attempts'] for c in new),'source_attempt_publication_cells':len(old['cells'])+len(new),'source_attempt_publication_attempts':sum(c['attempts'] for c in old['cells']+new),'source_attempt_publication_group_counts':dict(counts),'gc_primary_reductions_percent':[p['wall_reduction_percent'] for p in previous_gc['primary_pairs']]+[gc['wall_reduction_percent']],'gc_third_native_differences':gc['native_difference_count'],'gc_third_basic_transitions':gc['basic_transitions'],'matrix_status':{'highs-native-cpu-full1':'12/12 complete including three separate profiles; result review pending','stock-products-full1':'8/8 complete including two separate profiles; result review pending','full-gc2':'three primary pairs complete; two resource profiles incomplete','farkas-fast427-full1':'incomplete; finalized delta persisted only'},'qualification':'Do not sum overlapping request durations or infer IID confidence, cross-affinity ranking, exact/exhaustive CPU/peak memory, CPU/GPU superiority or novel contribution. Primary timings reused from their own blocks; profiles remain separate.'}
write(O/'analysis.json',out)
after=resource.getrusage(resource.RUSAGE_SELF)
write(O/'execution.json',{'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':(time.monotonic_ns()-clock)/1e9,'analysis_cpu_seconds':after.ru_utime+after.ru_stime-cpu.ru_utime-cpu.ru_stime,'role':'offline complete-terminal result reuse/publication, not another native acquisition; competing shared-CPU/I/O load during existing captures; no collector or candidate image modified'})
print(json.dumps(out,indent=2),flush=True)
