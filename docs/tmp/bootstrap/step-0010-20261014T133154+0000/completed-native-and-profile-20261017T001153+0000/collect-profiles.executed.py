from pathlib import Path
import collections,gzip,json,shutil,zipfile,statistics
r=Path('/workspaces/repository');s=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000'
out=s/'completed-native-and-profile-20261017T001153+0000';out.mkdir(exist_ok=True)
source=r/'artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl'
original=source.read_bytes();inputs=[json.loads(x) for x in original.splitlines()]
assert len(inputs)==29750 and len({x['proof_id'] for x in inputs})==29750
profiles=[]
for directory,label,tag in [('full-gc2','goedel427-profile-original','gc-original'),('farkas-fast427-full1','goedel427-profile-fast-hybrid','fast-hybrid')]:
 base=source.parent/directory;archive=base/(label+'.zip')
 terminal=json.loads((base/(label+'.terminal.json')).read_text())
 assert terminal['failure'] is None and terminal['returned']==terminal['expected']==29750
 dst=out/tag;dst.mkdir(exist_ok=True)
 with archive.open('rb') as src:
  parts=[];index=0
  while data:=src.read(32*1024*1024):
   target=dst/(archive.name+'.part-%03d'%index);target.write_bytes(data)
   assert target.read_bytes()==data;parts.append({'name':target.name,'bytes':len(data)});index+=1
  assert sum(x['bytes'] for x in parts)==archive.stat().st_size
 with zipfile.ZipFile(archive) as z:
  assert z.read(label+'/input.jsonl')==original
  rows=[json.loads(x) for x in z.read(label+'/results.jsonl').splitlines()]
  assert len(rows)==29750 and {x['source_index'] for x in rows}==set(range(29750))
  assert all(x['proof_id']==inputs[x['source_index']]['proof_id'] for x in rows)
  assert dict(collections.Counter(x['basic'] for x in rows))==terminal['counts']
  for row in rows:assert label+'/'+row['raw_response'] in z.namelist()
  summary=json.loads(z.read(label+'/resources-summary.json'))
  n=bad=peak=priv=0;previous=None;intervals=[]
  with gzip.GzipFile(fileobj=z.open(label+'/resources.jsonl.gz')) as raw:
   for line in raw:
    row=json.loads(line);n+=1;bad+=bool(row['errors'])
    peak=max(peak,row['total_kib'].get('Pss',0))
    priv=max(priv,row['total_kib'].get('Private_Clean',0)+row['total_kib'].get('Private_Dirty',0))
    if previous is not None:intervals.append((row['monotonic_ns']-previous)/1e9)
    previous=row['monotonic_ns']
  assert (n,bad,peak,priv)==(summary['samples'],summary['incomplete_samples'],summary['sampled_peak_total_pss_kib'],summary['sampled_peak_total_private_kib'])
  for f in ['command.json','resources-summary.json']: (dst/f).write_bytes(z.read(label+'/'+f))
 shutil.copyfile(base/(label+'.terminal.json'),dst/'terminal.json')
 info={'label':label,'zip_bytes':archive.stat().st_size,'parts':parts,'input_bytes_equal':True,'all_input_id_and_recorded_outcome_counts_reconciled':True,'all_raw_response_members_present':True,'resources_recomputed':True,'actual_sample_gap_median_seconds':statistics.median(intervals),'scope':'One separately profiled observation; no replicated resource advantage or exhaustive descendant CPU qualification.'}
 (dst/'publication.json').write_text(json.dumps(info,indent=2)+'\n')
 profiles.append({'label':label,'terminal':terminal,'resources':summary,'publication':info})
print(json.dumps(profiles,indent=2))
(out/'profile-reconstruction.json').write_text(json.dumps(profiles,indent=2)+'\n')
