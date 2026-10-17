from pathlib import Path
import collections,gzip,json,shutil,statistics
r=Path('/workspaces/repository');s=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000'
base=Path('/tmp/gpu-smt-e038-full-native-batch-20261016T150428Z');src=base/'rep1-stock'
out=s/'completed-native-and-profile-20261017T001153+0000';dst=out/'native-rep1-stock';dst.mkdir(exist_ok=True)
terminal=json.loads((src/'terminal.json').read_text())
assert terminal['state']=='complete' and terminal['expected']==terminal['attempts']==29750
assert all(p.is_file() for p in src.iterdir())
for p in src.iterdir():shutil.copyfile(p,dst/p.name)
shutil.copyfile(base/'launch.json',out/'native-original-launch.json')
inputs=[json.loads(x) for x in (r/'artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl').open()]
with gzip.open(dst/'responses.jsonl.gz','rt') as f:rows=[json.loads(x) for x in f]
assert len(rows)==29750 and [x['index'] for x in rows]==list(range(29750))
assert all(a['proof_id']==b['proof_id'] for a,b in zip(inputs,rows))
counts=dict(collections.Counter(x['outcome'] for x in rows));assert counts==terminal['counts']
event_counts=collections.Counter();errors=collections.Counter();batches=[];workers=[]
with gzip.open(dst/'events.jsonl.gz','rt') as f:
 for line in f:
  x=json.loads(line);event_counts[x['event']]+=1
  if x['event']=='batch_operational':errors[x['error']]+=1
  if x['event']=='batch_terminal':batches.append(x)
  if x['event']=='worker_terminal':workers.append(x)
bad=[x for x in batches if x['operational']]
assert len(batches)==1240 and len(bad)==40 and sum(x['count'] for x in bad)==counts['operational']==960
assert len(workers)==41 and workers[-1]['exit_code']==0 and workers[-1]['normal_eof']
sample_n=sample_bad=peak_pss=peak_rss=0
with gzip.open(dst/'resources.jsonl.gz','rt') as f:
 for line in f:
  x=json.loads(line);sample_n+=1;sample_bad+=bool(x['errors']);peak_pss=max(peak_pss,x['pss']);peak_rss=max(peak_rss,x['rss'])
assert peak_pss==terminal['sampled_peak_fleet_pss_with_collector'] and peak_rss==terminal['sampled_peak_fleet_rss_with_collector']
report={'scope':'One complete stock offline-batch cell of the ongoing nine-cell frozen-v1 matrix, no method comparison or new speedup. Public CLI did not execute this capture.','rows':len(rows),'counts':counts,'whole_seconds':terminal['whole_ns']/1e9,'events':dict(event_counts),'batch_operational_errors':dict(errors),'timeout_affected_rows':960,'timeout_batches_seconds_sum':sum(x['elapsed_ns'] for x in bad)/1e9,'all_batches_seconds_sum':sum(x['elapsed_ns'] for x in batches)/1e9,'sample_count':sample_n,'incomplete_samples':sample_bad,'worker_exit_counts':dict(collections.Counter(str(x['exit_code']) for x in workers)),'peak_fleet_pss_bytes_including_collector':peak_pss,'peak_fleet_rss_bytes_including_collector':peak_rss,'cpu':terminal['cpu'],'cpu_scope':'Collector self plus waited-child rusage, not an exhaustive CPU sum of killed/orphaned descendants. Sampling non-atomic; no uninstrumented/native-only cost inferred.','input_id_order_checked':True,'all_static_completed_cell_files_preserved':True,'source_versions':'eager-on-read v1, not the later first-write implementation'}
(dst/'reconstruction.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
