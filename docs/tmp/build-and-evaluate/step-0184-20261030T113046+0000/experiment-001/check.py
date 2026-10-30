from pathlib import Path
import csv,json,collections,os,time,resource,urllib.request,datetime
os.sched_setaffinity(0,{0,1});t0=time.monotonic()
root=Path('/workspaces/repository');raw=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/lean-kernel-verify-static')
meta=json.loads((raw/'metadata.json').read_text());pin='129e65bfd8efbf6c45710732d205c941ef65928c'
assert meta['commit']['sha']==pin and not meta['tree']['truncated']
tree=[x for x in meta['tree']['tree'] if x['type']=='blob']
rows=list(csv.DictReader((root/'workloads/lean-kernel-verify/released-kir-fixtures.csv').open()))
assert len(rows)==90 and len({r['path'] for r in rows})==90
assets=list(csv.DictReader((root/'workloads/lean-kernel-verify/released-json-assets.csv').open()))
assert len(assets)==92 and {r['path'] for r in assets}=={x['path'] for x in tree if x['path'].endswith('.json')}
modes=collections.Counter();input_counts=collections.Counter();wrapper_counts=collections.Counter()
for row in rows:
 p=raw/'source'/row['path'];k=json.loads(p.read_text())
 assert p.stat().st_size==int(row['bytes'])
 for field,key in [('role_definitions','roles'),('parameter_count','params'),('tensor_count','tensors')]:
  assert int(row[field])==len(k.get(key,[])),(row['path'],field)
 assert json.loads(row['grid_json'])==k['grid']
 assert row['native_outcome']=='not_run' and row['native_elapsed_s']=='unknown'
 mode='P1' if 'tmem' in k else 'P0';n=len(k['case']['inputs'])
 modes[mode]+=1;input_counts[mode]+=n;wrapper_counts[mode]+=n*(1 if mode=='P1' else 5)
source_rows=[]
for f in ['README.md','frontend/emit_lean.py','scripts/lkv.py','lean/KV/Check.lean']:
 path=raw/f if f=='README.md' else raw/'source'/f
 local=path.read_bytes();url='https://raw.githubusercontent.com/facebookresearch/lean_kernel_verify/'+pin+'/'+f
 remote=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'gpu-smt-paper-source-audit'}),timeout=30).read()
 assert remote==local
 text=local.decode();tokens={'README.md':['Lean 4.34.0','native_decide'],
 'frontend/emit_lean.py':['native_decide','KV.Holds','SPECS_P1'],
 'scripts/lkv.py':['if errors != len(refuted)','if status != (1 if refuted else 0)','EXIT_STATUS ='],
 'lean/KV/Check.lean':['certain : Bool','def Holds','UNDECIDED']}[f]
 assert all(x in text for x in tokens)
 source_rows.append({'path':f,'url':url,'bytes':len(local),'retained_matches_pinned_primary':True,
 'symbols':{x:[i for i,l in enumerate(text.splitlines(),1) if x in l][:10] for x in tokens}})
d={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pin':pin,
 'native_verifier_invocations':0,'tree_files':len(tree),'Lean_sources':sum(x['path'].endswith('.lean') for x in tree),
 'Lean_source_bytes':sum(x['size'] for x in tree if x['path'].endswith('.lean')),
 'JSON_assets':len(assets),'KIR_fixtures':len(rows),'KIR_bytes':sum(int(r['bytes']) for r in rows),
 'fixture_mode_counts':dict(modes),'concrete_input_counts':dict(input_counts),'static_emitter_wrapper_counts':dict(wrapper_counts),
 'source_checks':source_rows,'root_elapsed_s':time.monotonic()-t0,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
import sys
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
