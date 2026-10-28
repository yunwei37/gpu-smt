from pathlib import Path
import collections,datetime,gzip,json,os,shutil,subprocess
os.sched_setaffinity(0,{11})
r=Path('/workspaces/repository')
src=Path('/tmp/gpu-smt-prepared-policy7808-20261028T034248Z')
q=Path(Path('/tmp/gpu-smt-active-warm-resource-qualification.txt').read_text().strip())
s=Path(Path('/tmp/gpu-smt-step0093-path.txt').read_text().strip())
out=r/'artifacts/engine-resource-profile-2026-10-25/policy7808-20261028T034248Z'
out.mkdir(exist_ok=False)
begin=datetime.datetime.now(datetime.timezone.utc).isoformat()
copies=[]
def copy(source,dest):
    shutil.copy2(source,dest)
    with source.open('rb')as a,dest.open('rb')as b:
        while True:
            x=a.read(1024*1024);y=b.read(1024*1024)
            assert x==y
            if not x:break
    copies.append({'source':str(source),'destination':str(dest),'bytes':dest.stat().st_size,'full_byte_comparison':True})
def pack(source,dest):
    with source.open('rb')as a,gzip.open(dest,'wb')as b:
        shutil.copyfileobj(a,b,1024*1024)
    with source.open('rb')as a,gzip.open(dest,'rb')as b:
        while True:
            x=a.read(1024*1024);y=b.read(1024*1024)
            assert x==y
            if not x:break
    copies.append({'source':str(source),'destination':str(dest),'bytes':dest.stat().st_size,'full_decompressed_byte_comparison':True})
for name in ['manifest.json','qualification-comparison.json','qualification-compare.stderr']:
    if(src/name).exists():copy(src/name,out/name)
for name in ['original7808.json','qualification24.json']:pack(src/name,out/(name+'.gz'))
driver=Path('/tmp/gpu-smt-prepared-policy7808-driver-20261028.py')
copy(driver,out/'original-serial-driver-source.py')
cells=['qualification-fifo','qualification-task-memory','block1-fifo']
for name in cells:
    dest=out/name;dest.mkdir()
    for f in sorted((src/name).iterdir()):
        if f.is_file()and(f.suffix=='.gz'or f.suffix=='.json'):
            copy(f,dest/f.name)
copy(q/'retained-fifo-terminal.json',out/'block1-fifo/terminal-observation.json')
with gzip.open(out/'block1-fifo/capture.json.gz','rt')as f:cap=json.load(f)
with gzip.open(out/'original7808.json.gz','rt')as f:expected=json.load(f)
assert cap['batch']==expected and len(cap['results'])==7808
inputs={v['id']:v for v in expected['candidates']}
rows={v['id']:v for v in cap['results']}
assert len(inputs)==len(rows)==7808 and inputs.keys()==rows.keys()
assert cap['batch']['mode']=='all'
assert all(not v['cached']and not v['coalesced']for v in rows.values())
assert all(v['timeout_ms']==300000 and v['reuse']is False for v in inputs.values())
terminal=json.loads((out/'block1-fifo/terminal-observation.json').read_text())
assert int(terminal['kernel_wait_status'])==0 and terminal['returned']==7808
assert terminal['lifecycle_seconds']==cap['lifecycle_seconds']
parent_ids=set()
attempts=[a for v in rows.values()for a in v['attempts']]
events=[e for a in attempts for e in a.get('backend_events',[])]
for e in events:
    if e['stage']=='prepared_ready':
        d=json.loads(e['detail']);parent_ids.add(d['parent_pid'])
active=set();registered={};released=[];samples=0;peak=0;above=0;watchdog=[]
max_registered=max_known_candidate_children=0
with gzip.open(out/'block1-fifo/resource-events.jsonl.gz','rt')as f:
    for line in f:
        d=json.loads(line);v=d['fields'];msg=v.get('message')
        if msg=='register active process':
            key=(v['pid'],v['start_ticks']);assert key not in active
            active.add(key);registered[key]=v['origin_id']
            max_registered=max(max_registered,len(active))
            max_known_candidate_children=max(max_known_candidate_children,sum(k[0]not in parent_ids for k in active))
        elif msg=='release active process ownership':
            key=(v['pid'],v['start_ticks']);assert key in active
            active.remove(key);released.append(key)
        elif msg=='owned RSS sample':
            samples+=1;peak=max(peak,v['rss_bytes'])
            above+=v['rss_bytes']>cap['resources']['memory_bytes']
        elif msg=='preempt owned attempt and requeue exclusively':
            watchdog.append(v);peak=max(peak,v['rss_bytes'])
assert not active and len(registered)==len(released)
native_survivors=[];native_zombies=[]
for (pid,birth),origin in registered.items():
    p=Path('/proc')/str(pid)/'stat'
    try:
        v=p.read_text().rsplit(')',1)[1].split()
        if int(v[19])==birth:
            (native_zombies if v[0]=='Z'else native_survivors).append({'pid':pid,'start_ticks':birth,'origin_id':origin})
    except FileNotFoundError:pass
assert not native_survivors
previous=r/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z'
with gzip.open(previous/'prepared/capture.json.gz','rt')as f:prior=json.load(f)
with gzip.open(previous/'input7808.json.gz','rt')as f:canonical=json.load(f)
canonical_inputs={v['id']:v for v in canonical['candidates']}
source_differences={key:[i for i in inputs if inputs[i].get(key)!=canonical_inputs[i].get(key)]
                    for key in ['code','timeout_ms','reuse','task_id']}
assert inputs.keys()==canonical_inputs.keys()and not any(source_differences.values())
prior_rows={v['id']:v for v in prior['results']}
assert rows.keys()==prior_rows.keys()
prior_status_changes=[{'id':i,'previous':prior_rows[i]['outcome']['status'],'current':rows[i]['outcome']['status']}
                      for i in rows if rows[i]['outcome']['status']!=prior_rows[i]['outcome']['status']]
payload_changes=[i for i in rows if rows[i]['outcome']['response']!=prior_rows[i]['outcome']['response']]
aliases={'valid':'accepted','lean_error':'rejected','sorry':'incomplete','timeout_error':'timeout',
         'resource_failure':'resource_exhausted','server_error':'backend_error','repl_error':'backend_error'}
with gzip.open(r/'artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-20261024T0913/off/results.jsonl.gz','rt')as f:
    warm={v['proof_id']:v for v in map(json.loads,f)}
assert rows.keys()==warm.keys()
warm_changes=[{'id':i,'historical_warm':aliases[warm[i]['status']],'current':rows[i]['outcome']['status']}
              for i in rows if aliases[warm[i]['status']]!=rows[i]['outcome']['status']]
accepted=lambda d:{i for i,v in d.items()if v['outcome']['status']=='accepted'}
accepted_current=accepted(rows);accepted_prior=accepted(prior_rows)
accepted_warm={i for i,v in warm.items()if v['status']=='valid'}
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'returned':len(rows),'statuses':dict(collections.Counter(v['outcome']['status']for v in rows.values())),
 'accepted_ids':sorted(accepted_current),'attempts':len(attempts),
 'attempt_statuses':dict(collections.Counter(a['status']for a in attempts)),
 'exclusive_attempts':sum(a['exclusive']for a in attempts),
 'fresh_fallback_reasons':dict(collections.Counter(e['detail']for e in events if e['stage']=='fresh_fallback')),
 'prepared_ready_event_rows':sum(e['stage']=='prepared_ready'for e in events),
 'unique_ready_import_parent_pids':len(parent_ids),
 'resources':cap['resources'],'RSS_samples':samples,'sampled_peak_aggregate_RSS_bytes':peak,
 'sampled_peak_aggregate_GiB':peak/1024**3,'samples_above_budget':above,
 'watchdog_event_rows':len(watchdog),'registered_native_births':len(registered),
 'maximum_registered_active_processes':max_registered,
 'maximum_active_processes_excluding_known_ready_parents':max_known_candidate_children,
 'live_registered_native_survivors':native_survivors,'unreaped_registered_native_zombies':native_zombies,
 'original_input_and_canonical_fields_match':True,'source_option_differences_from_canonical':source_differences,
 'internal_lifecycle_seconds':cap['lifecycle_seconds'],'original_external_controller_seconds':None,
 'kernel_wait_status':0,'collector_source_claim':'8045cca frozen release;not9d/cf/library-repaired run',
 'previous_prepared_status_changes':prior_status_changes,'raw_native_payload_changes_from_previous_prepared':payload_changes,
 'accepted_only_previous_prepared':sorted(accepted_prior-accepted_current),
 'accepted_only_current_vs_previous_prepared':sorted(accepted_current-accepted_prior),
 'historical_warm_status_changes':warm_changes,
 'accepted_only_historical_warm':sorted(accepted_warm-accepted_current),
 'accepted_only_current_vs_historical_warm':sorted(accepted_current-accepted_warm),
 'deferred_unexecuted_policy_cells':['block1-task-memory','block2-task-memory','block2-fifo'],
 'native_library_scope':'This frozenFIFO/oldstockREPL does not restore the historicalwarm explicitcompiledMathlib dependency. Corrected4warm/engine is a separate pendingpoint.',
 'timing_scope':'Internalmainentry through execution/shutdown only;pausedoriginalwrapper loses completeexternalclock. Do not reconstruct from calendar/pidfdwaitchunks or pool nativecode/AS/concurrency/runorder points.',
 'resource_scope':'RSS is sampled and can overshoot;active registration omits backend-owned idleparent. No hardquota/no-globalOOM claim.',
 'interpretation':'Complete historicalFIFOdata,not correctedwarmparity,policygain,novelty or fullpaperacceptance.'}
(out/'analysis').mkdir()
(out/'analysis/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(out/'analysis/watchdog-events.json').write_text(json.dumps(watchdog,indent=2)+'\n')
copies_record={'begin_utc':begin,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'copies':copies,'actual_executed_cells':cells,'deferred_policy_queue_resumed':False,
 'native_candidate_executions_by_ingestion':0,'original_runtime_binaries_preserved_privately':True,
 'private_core_archive_receipt':str(q/'retained-private-core-archives.json'),
 'warm_launch_present_at_analysis_end':(q/'warm-launch.json').exists(),
 'support_CPU_affinity':[11],'clock_scope':'ingestion is supportingwork,not the oldbenchmarkclock'}
(out/'ingestion.json').write_text(json.dumps(copies_record,indent=2)+'\n')
(s/'experiment-001/artifact-path.txt').write_text(str(out)+'\n')
(s/'experiment-001/analysis-source.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({k:v for k,v in summary.items()if k not in ['accepted_ids','raw_native_payload_changes_from_previous_prepared']},indent=2))
print('PAYLOAD_CHANGED_COUNT',len(payload_changes),'ARTIFACT',out)
