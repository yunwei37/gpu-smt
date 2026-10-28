
import pathlib,json,gzip,datetime,collections,shutil
r=pathlib.Path('/workspaces/repository');s=r/pathlib.Path('/tmp/gpu-smt-step0095-path.txt').read_text().strip()
q=pathlib.Path(pathlib.Path('/tmp/gpu-smt-active-warm-resource-qualification.txt').read_text().strip())
out=r/'artifacts/engine-resource-profile-2026-10-25/warm-resource-qualification-20261028T044624Z'
out.mkdir(exist_ok=False)
exit=json.loads((q/'warm-exit.json').read_text());terminal=json.loads((q/'warm/terminal.json').read_text())
assert exit['exit']==0 and terminal['state']=='complete' and terminal['native_survivors']==[]
batch=json.loads((q/'input24.json').read_text())
rows=json.loads((q/'warm/results.json').read_text())
expected=batch['candidates'] if isinstance(batch,dict)else batch
assert rows['original_candidates']==expected
assert len(rows['results'])==24 and {x['id']for x in rows['results']}=={x['id']for x in expected}
assert collections.Counter(x['status']for x in rows['results'])==terminal['counts']
readiness=json.loads((q/'warm/native-library-readiness.json').read_text())
assert len(readiness)==4 and all(x['mapped']and x['native_library']==terminal['native_library']for x in readiness)
receipts=[]
for p in sorted((q/'warm').rglob('*')):
 if not p.is_file():continue
 rel=pathlib.Path('warm')/p.relative_to(q/'warm');dest=out/rel
 dest.parent.mkdir(parents=True,exist_ok=True)
 raw=p.read_bytes()
 # Raw formatting remains byte-for-byte in gzip; no trimming or normalization.
 if p.stat().st_size>20000 or p.suffix in ['.jsonl','.log']:
  dest=dest.with_name(dest.name+'.gz');dest.write_bytes(gzip.compress(raw,mtime=0))
  assert gzip.decompress(dest.read_bytes())==raw
 else:dest.write_bytes(raw);assert dest.read_bytes()==raw
 receipts.append({'source':str(p),'artifact':str(dest.relative_to(out)),'bytes':len(raw),'full_byte_comparison':True})
for name in ['manifest.json','input24.json','warm-launch.json','warm-exit.json','warm-run.py','warm.stdout','warm.stderr']:
 p=q/name;raw=p.read_bytes();dest=out/name
 if name.endswith(('.stdout','.stderr')):dest=dest.with_name(dest.name+'.gz');dest.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(dest.read_bytes())==raw
 else:dest.write_bytes(raw);assert dest.read_bytes()==raw
 receipts.append({'source':str(p),'artifact':str(dest.relative_to(out)),'bytes':len(raw),'full_byte_comparison':True})
table=[]
for row in rows['results']:
 table.append({'id':row['id'],'status':row['status'],'exclusive':row['exclusive'],'wall_seconds':row['wall_seconds'],
               'attempts':[{'exclusive':a['exclusive'],'status':a['status'],'wall_seconds':a['wall_seconds']}for a in rows['attempts'][row['id']]]})
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'warm-side-complete-engine-side-pending',
 'returned':24,'counts':terminal['counts'],'accepted_ids':[x['id']for x in rows['results']if x['status']=='valid'],
 'internal_seconds':terminal['whole_seconds'],'external_seconds':exit['external_seconds'],'preparation_seconds':terminal['preparation_seconds'],
 'physical_attempts':terminal['physical_attempts'],'memory':terminal['memory'],'resources':terminal['resources'],
 'native_survivors':terminal['native_survivors'],'four_warm_workers_mapped_library':True,'source_fields_equal_frozen_input':True,
 'per_id':table,'engine_side_pending':True,'new_db8ecbf_retry_order_applied':False,
 'performance_scope':'selected development24 qualification,with disclosed root CPU10-11 support overlap;not fullthroughput or a pairedgain',
 'review':'root self-review only'}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(out/'ingestion.json').write_text(json.dumps({'utc':summary['utc'],'receipts':receipts,'raw_warm_retained':True,
 'engine_directory_not_touched':True,'native_candidate_executions':0},indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k not in ['accepted_ids','memory','per_id']},indent=2))
print('TARGETS',json.dumps([x for x in table if int(x['id'].split('-')[-1])>=16],indent=2))
