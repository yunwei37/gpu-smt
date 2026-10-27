from pathlib import Path
import sys,json,gzip,collections,math,datetime
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent
load=lambda p:json.loads(gzip.decompress(p.read_bytes())) if p.suffix=='.gz' else json.loads(p.read_text())
original=load(root/'input7808.json.gz')
captures={n:load(root/n/'capture.json.gz') for n in ['native','prepared']}
comp=load(root/'comparison.json'); audit={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cells':{},'scope':'root self-review; no independent audit; single fixed-order own-engine support pair'}
assert len(original['candidates'])==7808
identities=set()
for n,c in captures.items():
 assert c['batch']==original
 rows=c['results']; assert len(rows)==7808
 assert [x['id'] for x in rows]==[x['id'] for x in original['candidates']]
 assert len({x['id'] for x in rows})==7808
 assert all(not x['cached'] and not x['coalesced'] for x in rows)
 consumer=[json.loads(l) for l in gzip.decompress((root/n/'results.jsonl.gz').read_bytes()).splitlines()]
 assert consumer[-1]=={'event':'complete','count':7808}
 assert len(consumer)==7809
 delivered={x['index']:x['verification'] for x in consumer[:-1]}
 assert len(delivered)==7808 and all(delivered[i]==x for i,x in enumerate(rows))
 physical=[json.loads(l) for l in gzip.decompress((root/n/'attempts.jsonl.gz').read_bytes()).splitlines()]
 assert collections.Counter((x['id'],t['exclusive']) for x in rows for t in x['attempts'])==collections.Counter((x['id'],x['exclusive_retry']) for x in physical)
 expected=collections.Counter((x['id'],t['status'],t['exclusive']) for x in rows for t in x['attempts'])
 actual=collections.Counter((x['id'],x['outcome']['status'],x['exclusive_retry']) for x in physical)
 # Wrapper watchdog may override native cancellation/status after the physical journal
 discrepancies=[{'id':k[0],'status':k[1],'exclusive':k[2],'count':v-actual[k]} for k,v in expected.items() if v!=actual[k]]
 attempts=[t for x in rows for t in x['attempts']]
 events=[e for t in attempts for e in t['backend_events']]
 samples=[json.loads(l) for l in gzip.decompress((root/n/'rss-cpu.jsonl.gz').read_bytes()).splitlines()]
 term=load(root/n/'terminal.json')
 assert term['state']=='complete' and not term['interrupted'] and not term['journal_errors']
 births={(b['pid'],b['start_ticks']) for t in attempts for b in t['processes']}
 identities.update(births)
 ready=[json.loads(e['detail']) for e in events if e['stage']=='prepared_ready']
 resource_rows=[{'id':x['id'],'status':x['outcome']['status'],'error':x['outcome']['error'],'attempts':len(x['attempts']),'exclusive_attempts':sum(t['exclusive'] for t in x['attempts'])} for x in rows if x['outcome']['status'] in ['resource_exhausted','backend_error']]
 (root/n/'operational-failures.json.gz').write_bytes(gzip.compress(json.dumps(resource_rows,indent=2).encode(),mtime=0))
 audit['cells'][n]={'statuses':dict(collections.Counter(x['outcome']['status'] for x in rows)),'candidate_count':len(rows),'physical_attempt_rows':len(physical),'attempt_count':len(attempts),'exclusive_attempts':sum(t['exclusive'] for t in attempts),'watchdog_preempted_attempts':sum(t['preemption_rss_bytes'] is not None for t in attempts),'attempt_status_journal_differences':discrepancies,'attempt_status_difference_scope':'native journal precedes engine wrapper watchdog classification; full physical outcomes retained','backend_events':dict(collections.Counter(e['stage'] for e in events)),'parent_preparations':len(ready),'ready_module_counts':sorted({x['prepared_context']['imported_modules'] for x in ready}),'ready_parent_threads':sorted({x['parent_threads'] for x in ready}),'registered_identities':len(births),'cached':0,'coalesced':0,'lifecycle_seconds':c['lifecycle_seconds'],'external_cell_seconds':term['external_cell_seconds'],'terminal_reported_sample_peak_bytes':term['observations']['sampled_peak_rss_bytes'],'retained_sample_peak_bytes':max(x['aggregate_rss_bytes'] for x in samples),'retained_over_budget_samples':sum(x['aggregate_rss_bytes']>c['resources']['memory_bytes'] for x in samples),'retained_samples':len(samples),'retained_max_registered_leaders':max(len(x['registered_leaders']) for x in samples),'resource_failure_errors':dict(collections.Counter(x['outcome']['error'] for x in rows if x['outcome']['status']=='resource_exhausted'))}
left={x['id']:x for x in captures['native']['results']}
right={x['id']:x for x in captures['prepared']['results']}
statusdiff=[i for i in left if left[i]['outcome']['status']!=right[i]['outcome']['status']]
acceptdiff=sorted({i for i,x in left.items() if x['outcome']['status']=='accepted'}^{i for i,x in right.items() if x['outcome']['status']=='accepted'})
omitted=[];other=[];errordiff=[]
for i in left:
 a=left[i]['outcome']['response'];b=right[i]['outcome']['response']
 if a!=b:
  v=dict(a) if isinstance(a,dict) else a
  if isinstance(v,dict) and v.get('ast')==[]:v.pop('ast')
  (omitted if v==b else other).append(i)
 if left[i]['outcome']['error']!=right[i]['outcome']['error']:errordiff.append(i)
assert statusdiff==[] and acceptdiff==[] and other==[]
audit['pair']={'status_changed_ids':statusdiff,'accepted_set_changed_ids':acceptdiff,'omitted_empty_ast_response_ids':omitted,'other_response_changed_ids':other,'operational_error_text_changed_ids':errordiff,'accepted_count':sum(x['outcome']['status']=='accepted' for x in left.values()),'solved_task_count':len({x['task_id'] for x in original['candidates'] if left[x['id']]['outcome']['status']=='accepted'}),'external_native_over_prepared':audit['cells']['native']['external_cell_seconds']/audit['cells']['prepared']['external_cell_seconds'],'elapsed_reduction_percent':100*(1-audit['cells']['prepared']['external_cell_seconds']/audit['cells']['native']['external_cell_seconds']),'lifecycle_ratio':captures['native']['lifecycle_seconds']/captures['prepared']['lifecycle_seconds']}
assert audit['pair']['external_native_over_prepared']==comp['external_native_over_prepared']
live=[]
for pid,birth in identities:
 try:
  parts=Path(f'/proc/{pid}/stat').read_text().split(') ')[1].split()
  if int(parts[19])==birth and parts[0]!='Z':live.append([pid,birth])
 except OSError: pass
assert not live
audit['retirement']={'recorded_pid_birth_pairs':len(identities),'matching_non_zombie_alive':live,'controller_457460_exists':Path('/proc/457460').exists(),'scope':'current recorded-identity check; process absence does not independently authenticate all unregistered descendants'}
old=root.parent/'full7808-20261026T004621Z/native/capture.json.gz'
if old.exists():
 oc=load(old); oldmap={x['id']:x for x in oc['results']}
 audit['historical_native_status_changes']=[{'id':i,'old':oldmap[i]['outcome']['status'],'new':x['outcome']['status']} for i,x in left.items() if oldmap[i]['outcome']['status']!=x['outcome']['status']]
audit['tails']=[{k:v for k,v in t.items() if k not in ['candidate_statuses','ids']} for t in comp['tails']]
(root/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps({'cells':{n:{k:v for k,v in c.items() if k!='attempt_status_journal_differences'} for n,c in audit['cells'].items()},'pair':{k:len(v) if isinstance(v,list) else v for k,v in audit['pair'].items()},'retirement':audit['retirement'],'historical_native_status_changes':audit.get('historical_native_status_changes'),'tails':audit['tails']},indent=2))
